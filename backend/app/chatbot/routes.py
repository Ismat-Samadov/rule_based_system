"""
Chatbot API Routes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.chatbot.engine import get_chatbot


router = APIRouter(prefix="/chat", tags=["Chatbot"])


class ChatMessage(BaseModel):
    """User chat message"""
    message: str
    session_id: Optional[str] = None


class ChatResponseModel(BaseModel):
    """Chatbot response"""
    intent: str
    confidence: float
    response: str
    action: Optional[str] = None
    quick_replies: Optional[List[str]] = None
    entities: Optional[Dict[str, Any]] = None


class ConversationContext(BaseModel):
    """Conversation context"""
    session_id: str
    context: Dict[str, Any]


# Session storage (in production, use Redis or database)
_sessions: Dict[str, Dict[str, Any]] = {}


@router.post("/message", response_model=ChatResponseModel)
async def send_message(chat: ChatMessage):
    """
    Send a message to the chatbot and get a response
    
    Chatbot-a mesaj göndərin və cavab alın.
    """
    chatbot = get_chatbot()
    
    # Get or create session context
    if chat.session_id and chat.session_id in _sessions:
        chatbot.context = _sessions[chat.session_id]
    
    # Process message
    result = chatbot.chat(chat.message)
    
    # Save session context
    if chat.session_id:
        _sessions[chat.session_id] = chatbot.get_context()
    
    return ChatResponseModel(
        intent=result.intent,
        confidence=result.confidence,
        response=result.response,
        action=result.action,
        quick_replies=result.quick_replies,
        entities=result.context_update.get('entities') if result.context_update else None
    )


@router.get("/intents")
async def list_intents():
    """
    Get list of all available intents
    
    Bütün mövcud intent-lərin siyahısı.
    """
    chatbot = get_chatbot()
    return {
        "intents": chatbot.get_intent_list(),
        "count": len(chatbot.get_intent_list())
    }


@router.post("/reset")
async def reset_session(session_id: str):
    """
    Reset a chat session
    
    Söhbət sessiyasını sıfırlayın.
    """
    if session_id in _sessions:
        del _sessions[session_id]
    
    return {"status": "ok", "message": "Session reset"}


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


@router.get("/quick-replies")
async def get_quick_replies():
    """
    Get quick reply options
    
    Sürətli cavab variantları.
    """
    chatbot = get_chatbot()
    return chatbot.quick_replies
