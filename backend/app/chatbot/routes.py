"""
Chatbot API Routes - Gemini AI Integration
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from app.chatbot.gemini_engine import get_chatbot


router = APIRouter(prefix="/chat", tags=["Chatbot"])


class ChatMessage(BaseModel):
    """User chat message"""
    message: str
    session_id: Optional[str] = None


class ChatResponseModel(BaseModel):
    """Chatbot response"""
    response: str
    quick_replies: Optional[List[str]] = None


@router.post("/message", response_model=ChatResponseModel)
async def send_message(chat: ChatMessage):
    """
    Send a message to the Gemini AI chatbot and get a response

    Chatbot-a mesaj göndərin və AI-powered cavab alın.
    """
    try:
        chatbot = get_chatbot()

        # Process message with Gemini
        result = chatbot.chat(chat.message, session_id=chat.session_id)

        return ChatResponseModel(
            response=result.response,
            quick_replies=result.quick_replies
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chatbot error: {str(e)}"
        )


@router.post("/reset")
async def reset_session(session_id: str):
    """
    Reset a chat session

    Söhbət sessiyasını sıfırlayın.
    """
    chatbot = get_chatbot()
    chatbot.reset_session(session_id)

    return {"status": "ok", "message": "Session reset"}


@router.get("/stats")
async def get_stats():
    """
    Get chatbot statistics

    Chatbot statistikası.
    """
    chatbot = get_chatbot()

    return {
        "active_sessions": chatbot.get_session_count(),
        "model": "Gemini Pro",
        "status": "operational"
    }


@router.get("/examples")
async def get_examples():
    """
    Get example questions to ask the chatbot

    Chatbot-a verilə biləcək nümunə suallar.
    """
    return {
        "examples": [
            {
                "category": "Suvarma",
                "questions": [
                    "Pomidoru nə vaxt suvarmalıyam?",
                    "Nə qədər su vermək lazımdır?",
                    "Damcı suvarma nədir?"
                ]
            },
            {
                "category": "Gübrələmə",
                "questions": [
                    "Buğdaya hansı gübrə lazımdır?",
                    "NPK nədir?",
                    "Nə vaxt gübrələmək lazımdır?"
                ]
            },
            {
                "category": "Xəstəlik/Zərərverici",
                "questions": [
                    "Yarpaqlar niyə saraldı?",
                    "Fitoftora nədir?",
                    "Mənənə ilə necə mübarizə aparım?"
                ]
            },
            {
                "category": "Heyvandarlıq",
                "questions": [
                    "İnəyi necə yemləmək lazımdır?",
                    "Peyvənd vaxtları nədir?",
                    "Süd azalıbsa nə edim?"
                ]
            },
            {
                "category": "Hava",
                "questions": [
                    "Hava çox istidir, nə edim?",
                    "Şaxta olacaqsa nə edim?",
                    "Yağış gözlənilir, nə edim?"
                ]
            }
        ]
    }
