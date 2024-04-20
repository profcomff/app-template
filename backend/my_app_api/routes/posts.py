import logging

from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends
from typing import Annotated

from my_app_api.shemas.posts import SPostAdd, SPostGetAll, SPost
from my_app_api.orm.repository import PostRepository

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/{post_id}")
def get_one_post(
    post_id: int,
    auth=Depends(UnionAuth(allow_none=False))
) -> SPost:
    post = PostRepository.get_one_post(post_id, auth)
    return post


@router.post("/")
def create_post(
    post: Annotated[SPostAdd, Depends(SPostAdd)],
    auth=Depends(UnionAuth(allow_none=False))
) -> dict:
    post_id = PostRepository.add_post(post, auth)
    return {'post_id': post_id}


@router.get("/")
def get_posts(
        params: Annotated[SPostGetAll, Depends(SPostGetAll)],
        auth=Depends(UnionAuth(allow_none=False))
) -> list[SPost]:
    posts = PostRepository.get_posts(params, auth)
    return posts


@router.delete('/{post_id}')
def delete_post(post_id: int, auth=Depends(UnionAuth(allow_none=False))) -> dict:
    pass
