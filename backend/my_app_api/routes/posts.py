import logging

from auth_lib.fastapi import UnionAuth
from my_app_api.orm.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, File, UploadFile
from typing import Annotated, Optional
from fastapi.responses import JSONResponse

from my_app_api.shemas.posts import SPostAdd, SPostGetAll, SPost, SPostPatch
from my_app_api.orm.repository import PostRepository

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/{post_id}")
async def get_one_post(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    post_id: int,
    auth=Depends(UnionAuth(allow_none=False))
) -> SPost:
    post = await PostRepository.get_one_post(session, post_id, auth)
    return post


@router.post("/")
async def create_post(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    post: Annotated[SPostAdd, Depends(SPostAdd)],
    picture: Optional[UploadFile] = File(None),
    auth=Depends(UnionAuth(allow_none=False))
) -> dict:
    post_id = await PostRepository.add_post(session, post, picture, auth)
    return JSONResponse(
        status_code=201,
        content={'post_id': post_id}
    )


@router.get("/")
async def get_posts(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    params: Annotated[SPostGetAll, Depends(SPostGetAll)],
    auth=Depends(UnionAuth(allow_none=False))
) -> list[SPost]:
    posts = await PostRepository.get_posts(session, params, auth)
    return posts


@router.delete('/{post_id}')
async def delete_post(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    post_id: int,
    auth=Depends(UnionAuth(allow_none=False))
):
    await PostRepository.delete_post(session, post_id, auth)


@router.patch('/{post_id}')
async def patch_post(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    post_id: int,
    post: Annotated[SPostPatch, Depends(SPostPatch)],
    auth=Depends(UnionAuth(allow_none=False))
) -> dict:
    await PostRepository.patch_post(session, post_id, post, auth)
    return JSONResponse(
        status_code=201,
        content={'detail': 'ok'}
    )
