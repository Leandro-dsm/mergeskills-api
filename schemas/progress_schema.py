from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

class SubmitAnswerSchema(BaseModel):
    user_id: int
    question_id: int
    selected_option: int

class AnswerResultSchema(BaseModel):
    is_correct: bool
    correct_answer: int
    message: str

class ResetProgressSchema(BaseModel):
    user_id: int

class AttemptSchema(BaseModel):
    id: int
    user_id: int
    question_id: int
    selected_option: int
    is_correct: bool
    timestamp: Optional[str] = None

class LessonProgressSchema(BaseModel):
    id: int
    user_id: int
    lesson_id: int
    is_completed: bool
    completed_at: Optional[str] = None

class UserHistorySchema(BaseModel):
    user_id: int
    completed_lessons: List[Any]
    recent_attempts: List[Any]
    total_score: int

class ProgressResponseSchema(BaseModel):
    user_id: int
    lesson_id: int
    is_completed: bool
    completed_at: Optional[str] = None