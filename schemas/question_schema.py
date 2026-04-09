from pydantic import BaseModel
from typing import Optional, List

class QuestionSchema(BaseModel):
    id: int
    lesson_id: int
    question: str
    code: Optional[str] = None
    options: Optional[List[str]] = []
    correct_answer: Optional[int] = 0
    order: Optional[int] = 0

class QuestionIdSchema(BaseModel):
    id: int

class QuestionCreateSchema(BaseModel):
    lesson_id: int
    question: str
    code: Optional[str] = None
    options: Optional[List[str]] = []
    correct_answer: Optional[int] = 0
    order: Optional[int] = 0

class QuestionUpdateSchema(BaseModel):
    question: Optional[str] = None
    code: Optional[str] = None
    options: Optional[List[str]] = None
    correct_answer: Optional[int] = None
    order: Optional[int] = None