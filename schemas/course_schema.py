from pydantic import BaseModel
from typing import Optional

class CourseSchema(BaseModel):
    id: int
    title: str
    description: Optional[str] = ""
    icon: Optional[str] = ""
    color: Optional[str] = "#000000"
    total_lessons: Optional[int] = 0

class CourseCreateSchema(BaseModel):
    title: str
    description: Optional[str] = ""
    icon: Optional[str] = ""
    color: Optional[str] = "#000000"
    total_lessons: Optional[int] = 0

class CourseUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    total_lessons: Optional[int] = None