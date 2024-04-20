import logging

from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Annotated

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/example", tags=["Example"])



class Post(BaseModel):
    post_id: int | None = None
    title: str | None = None
    description: str | None = None
    picture_id: int | None = None
    create_date: str | None = None
    event_date: str | None = None


@router.post("/posts")
def create_post(post: Annotated[], auth=Depends(UnionAuth(allow_none=False))):
    pass


@router.delete("/posts/{post_id}/{user_id}")
def delete_post(post: Annotated[DeletePost, Depends(DeletePost)], auth=Depends(UnionAuth(allow_none=False))):
    pass


@router.get("/posts")
def get_posts(auth=Depends(UnionAuth(allow_none=False))):
    pass


@router.get("/posts/{post_id}")
def get_post(post: Annotated[GetPost, Depends(GetPost)], auth=Depends(UnionAuth(allow_none=False))):
    pass


@router.get("/posts/reaction")
def get_reaction(auth=Depends(UnionAuth(allow_none=False))):
    pass


@router.delete("/posts/reaction/{reaction_id}")
def delete_reaction(reaction: Annotated[DeleteReaction, Depends(DeleteReaction)],
                    auth=Depends(UnionAuth(allow_none=False))):
    pass
