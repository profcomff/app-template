from sqlalchemy.dialects.postgresql import array
from fastapi import HTTPException
from sqlalchemy import delete, or_, select

from my_app_api.models.models_db import PostOrm
from my_app_api.shemas.posts import SPost
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
