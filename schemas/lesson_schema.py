from pydantic import BaseModel
from typing import Optional

class LessonSchema(BaseModel):
    id: int
    course_id: int
    title: str
    description: Optional[str] = ""
    order: Optional[int] = 0

class LessonCreateSchema(BaseModel):
    course_id: int
    title: str
    description: Optional[str] = ""
    order: Optional[int] = 0

class LessonUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None