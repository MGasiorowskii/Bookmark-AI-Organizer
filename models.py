from enum import Enum

from pydantic import BaseModel, Field


class Seniority(str, Enum):
    junior = "junior"
    mid = "mid"
    senior = "senior"


class Bookmark(BaseModel):
    title: str = Field(..., description="The title of the bookmark")
    url: str = Field(..., description="The URL of the bookmark")
    description: str = Field(..., description="A short description of the bookmark")
    seniority: list[Seniority] = Field(
        ..., description="The list of seniority levels the content is suitable for"
    )
    tags: list[str] = Field(..., description="A list of tags describing the topic")


class BookmarkSummaries(BaseModel):
    bookmarks: list[Bookmark]
