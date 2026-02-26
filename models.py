from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

# Задание 1.4
class User(BaseModel):
    name: str
    id: int

# Задание 1.5
class UserWithAge(BaseModel):
    name: str
    age: int

# Задание 2.1
class Feedback(BaseModel):
    name: str
    message: str

# Задание 2.2
class FeedbackValidated(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Имя от 2 до 50 символов")
    message: str = Field(..., min_length=10, max_length=500, description="Сообщение от 10 до 500 символов")
    
    @field_validator('message')
    @classmethod
    def validate_message(cls, v: str) -> str:
        forbidden_words = ['крингк', 'рофл', 'вайб']
        v_lower = v.lower()
        for word in forbidden_words:
            pattern = r'\b' + re.escape(word) + r'\b'
            if re.search(pattern, v_lower):
                raise ValueError('Использование недопустимых слов')
        return v