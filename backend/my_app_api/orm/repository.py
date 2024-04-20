from sqlalchemy.dialects.postgresql import array
from fastapi import HTTPException
from sqlalchemy import delete, or_, select

from my_app_api.models.models_db import PostOrm
from my_app_api.shemas.posts import SPost, SPostAdd, SPostGetAll
from my_app_api.orm.database import new_session


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
    def add_post(data: SPostAdd, auth):
        with new_session() as session:
            query = (
                select(PostOrm)
                .where(PostOrm.title == data.title)
                .where(PostOrm.is_active)
            )
            result = session.execute(query)
            if result.scalars().all():
                raise HTTPException(
                    status_code=400, detail='Похожее мероприятие уже есть')

            post_dict = data.model_dump()
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
