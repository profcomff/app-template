from my_app_api.utils.check_permission import check_permission
from sqlalchemy.dialects.postgresql import array
from fastapi import HTTPException
from sqlalchemy import delete, or_, select

from my_app_api.models.models_db import PostOrm
from my_app_api.shemas.posts import SPost, SPostAdd, SPostGetAll, SPostPatch
from my_app_api.orm.database import new_session
from my_app_api.utils.date_refactor import date_refactor


class PostRepository:
    @staticmethod
    def get_one_post(post_id: int, auth) -> SPost:
        with new_session() as session:
            query = (
                select(PostOrm)
                .filter(PostOrm.post_id == post_id)
            )
            result = session.execute(query)
            result = result.scalars().first()
            if not result:
                raise HTTPException(
                    status_code=404, detail='Мероприятие не найдено')

            banner = SPost.model_validate(
                result, from_attributes=True)

            return banner

    @staticmethod
    def add_post(data: SPostAdd, picture: str, auth) -> int:
        check_permission(auth)

        # refactor date
        try:
            data.event_date = date_refactor(data.event_date)
        except:
            raise HTTPException(
                status_code=422, detail='Неверный формат даты')

        with new_session() as session:
            query = (
                select(PostOrm)
                .where(PostOrm.title == data.title)
                .where(PostOrm.event_date == data.event_date)
            )
            result = session.execute(query)
            if result.scalars().all():
                raise HTTPException(
                    status_code=400, detail='Похожее мероприятие уже есть')

            # Upload picture
            if picture:
                picture = picture
            else:
                picture = "url://no_pic.png"

            post_dict = data.model_dump()
            post_dict.update({'picture': picture})

            post = PostOrm(**post_dict)
            session.add(post)
            session.flush()
            post_id = post.post_id
            session.commit()
            return post_id

    @staticmethod
    def get_posts(params: SPostGetAll, auth) -> list[SPost]:
        with new_session() as session:
            query = select(PostOrm)

            if params.offset is not None:
                query = query.offset(params.offset)
            if params.limit is not None:
                query = query.limit(params.limit)

            result = session.execute(query)
            post_models = result.scalars().all()

            post_schemas = [SPost.model_validate(
                post_orm, from_attributes=True) for post_orm in post_models]

            return post_schemas

    @staticmethod
    def delete_post(post_id: int, auth):
        check_permission(auth)
        with new_session() as session:
            # Verify if banner is not exist
            post = session.get(PostOrm, (post_id, ))
            if not post:
                raise HTTPException(
                    status_code=404, detail='Мероприятие не найдено')

            stmt = delete(PostOrm).filter(PostOrm.post_id == post_id)
            session.execute(stmt)
            session.commit()

    @staticmethod
    def patch_post(post_id: int, patch_post: SPostPatch, auth):
        check_permission(auth)
        with new_session() as session:
            post = session.get(PostOrm, post_id)

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
            result = session.execute(query)
            if result.scalars().all():
                raise HTTPException(
                    status_code=400, detail='Похожее мероприятие уже есть')

            session.flush()
            session.commit()
