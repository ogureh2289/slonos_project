from fastapi import APIRouter, HTTPException
import traceback

from .models import Question, Answer
from .llm_service import TinyLlamaService

router = APIRouter()
llm_service = TinyLlamaService()


@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Python Tutor 🐍"}


@router.post("/ask", response_model=Answer)
async def ask_question(question: Question):
    try:
        response = llm_service.generate_answer(question.question)
        return Answer(**response)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))