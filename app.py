from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from pydantic import ValidationError
import uvicorn
from typing import List

from models import User, UserWithAge, Feedback, FeedbackValidated
from feedback_storage import feedbacks
app = FastAPI()

# Задание 1.1
@app.get("/")
async def root():
    return {"message": "Добро пожаловать в моё приложение FastAPI!"}

# Задание 1.2
@app.get("/html")
async def get_html():
    return FileResponse("index.html")

# Задание 1.3
@app.post("/calculate")
async def calculate(num1: float, num2: float):
    result = num1 + num2
    return {"result": result}

# Задание 1.4
user = User(name="Зубенко Михаил Петрович", id=1)  # Замените на свое имя

@app.get("/users")
async def get_user():
    return user

# Задание 1.5
@app.post("/user")
async def check_adult(user_data: UserWithAge):
    is_adult = user_data.age >= 18
    return {
        "name": user_data.name,
        "age": user_data.age,
        "is_adult": is_adult
    }

# Задание 2.1

@app.post("/feedback")
async def create_feedback(feedback: Feedback):
    feedbacks.append(feedback.dict())
    return {"message": f"Feedback received. Thank you, {feedback.name}."}

@app.get("/feedbacks", response_model=List[Feedback])
async def get_all_feedbacks():
    return feedbacks

# Задание 2.2
@app.post("/feedback/v2")
async def create_feedback_validated(feedback: FeedbackValidated):
    try:
        feedbacks.append(feedback.dict())
        return {"message": f"Спасибо, {feedback.name}! Ваш отзыв сохранён."}
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)