from my_app_api.utils.file_handle import safe_file
from my_app_api.utils.check_permission import check_permission
from sqlalchemy.dialects.postgresql import array
from fastapi import HTTPException, UploadFile
from sqlalchemy import delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession


from my_app_api.models.models_db import PostOrm
from my_app_api.shemas.posts import SPost, SPostAdd, SPostGetAll, SPostPatch
from my_app_api.orm.database import new_session
from my_app_api.utils.date_refactor import date_refactor


class PostRepository:
    @staticmethod
    async def get_one_post(session: AsyncSession, post_id: int, auth) -> SPost:
        query = (
            select(PostOrm)
            .filter(PostOrm.post_id == post_id)
        )
        result = await session.execute(query)
        result = result.scalars().first()
        if not result:
            raise HTTPException(
                status_code=404, detail='Мероприятие не найдено')

        banner = SPost.model_validate(
            result, from_attributes=True)

        return banner

    @staticmethod
    async def add_post(session: AsyncSession, data: SPostAdd, picture, auth) -> int:
        check_permission(auth)

        # refactor date
        try:
            data.event_date = date_refactor(data.event_date)
        except:
            raise HTTPException(
                status_code=422, detail='Неверный формат даты')

        query = (
            select(PostOrm)
            .where(PostOrm.title == data.title)
            .where(PostOrm.event_date == data.event_date)
        )
        result = await session.execute(query)
        if result.scalars().all():
            raise HTTPException(
                status_code=400, detail='Похожее мероприятие уже есть')

        # Upload picture
        picture_url = await safe_file(picture)

        post_dict = data.model_dump()
        post_dict.update({'picture_url': picture_url})

        post = PostOrm(**post_dict)
        session.add(post)
        await session.flush()
        post_id = post.post_id
        await session.commit()
        return post_id

    @staticmethod
    async def get_posts(session: AsyncSession, params: SPostGetAll, auth) -> list[SPost]:

        query = select(PostOrm)

        if params.offset is not None:
            query = query.offset(params.offset)
        if params.limit is not None:
            query = query.limit(params.limit)

        result = await session.execute(query)
        post_models = result.scalars().all()

        post_schemas = [SPost.model_validate(
            post_orm, from_attributes=True) for post_orm in post_models]

        return post_schemas

    @staticmethod
    async def delete_post(session: AsyncSession, post_id: int, auth):
        check_permission(auth)

        # Verify if banner is not exist
        post = await session.get(PostOrm, (post_id, ))
        if not post:
            raise HTTPException(
                status_code=404, detail='Мероприятие не найдено')

        stmt = delete(PostOrm).filter(PostOrm.post_id == post_id)
        await session.execute(stmt)
        await session.commit()

    @staticmethod
    async def patch_post(session: AsyncSession, post_id: int, patch_post: SPostPatch, auth):
        check_permission(auth)

        post = await session.get(PostOrm, post_id)

        # Verify 1 If banner by id exists
        if post:
            if patch_post.description is not None:
                post.description = patch_post.description
            if patch_post.title is not None:
                post.title = patch_post.title
            if patch_post.event_date is not None:
                try:
                    post.event_date = date_refactor(patch_post.event_date)
                except:
                    raise HTTPException(
                        status_code=422, detail='Неверный формат даты')
            if patch_post.is_active is not None:
                post.is_active = patch_post.is_active
        else:
            raise HTTPException(status_code=404, detail='Баннер не найден')

        # Verify 2 If banner with same options exists
        query = (
            select(PostOrm)
            .where(PostOrm.post_id != post.post_id)
            .where(PostOrm.title == post.title)
            .where(PostOrm.event_date == post.event_date)
        )
        result = await session.execute(query)
        if result.scalars().all():
            raise HTTPException(
                status_code=400, detail='Похожее мероприятие уже есть')

        await session.flush()
        await session.commit()
