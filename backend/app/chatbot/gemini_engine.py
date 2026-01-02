"""
AgriAdvisor Chatbot Engine - Gemini AI Integration
Azerbaijani agricultural chatbot powered by Google Gemini
"""

import os
import google.generativeai as genai
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
project_root = Path(__file__).parent.parent.parent.parent
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)


@dataclass
class ChatResponse:
    """Chatbot response structure"""
    response: str
    quick_replies: Optional[List[str]] = None


class AgriAdvisorGeminiChatbot:
    """
    Gemini AI-powered chatbot for Azerbaijani agricultural advice
    """

    # System prompt to guide Gemini's behavior
    SYSTEM_PROMPT = """Sən AgriAdvisor adlı kənd təsərrüfatı məsləhətçisisən. Azərbaycan fermerlərinin kənd təsərrüfatı ilə bağlı suallarına Azərbaycan dilində cavab verirsən.

Sənin biliklərin:
- Suvarma: vaxt, miqdar, üsullar (damcı, şırım, yağmurlama)
- Gübrələmə: NPK, üzvi gübrələr, normalar, vaxtlar
- Xəstəliklər və zərərvericilər: diaqnoz, müalicə, profilaktika
- Hava şəraiti: isti, soyuq, yağış zamanı tədbirlər
- Heyvandarlıq: yemləmə, sağlamlıq, peyvənd
- Yığım: vaxtlar, üsullar

Azərbaycan iqlimi və kənd təsərrüfatı şəraitini nəzərə al.

QAYDALAR:
✅ Həmişə Azərbaycan dilində cavab ver
✅ Praktik, konkret məsləhətlər ver - QISA və AYDIN
✅ Rəqəmlər və normalar göstər (məs: "Pomidora gündə 5-10 L su")
✅ Emoji istifadə et (🌾 🍅 💧 ✅)
✅ Hava şəraiti və regionu nəzərə al
✅ Əgər dəqiq cavab bilmirsənsə, ümumi məlumat ver

⚠️ ÇOX VACIB FORMATLAŞDIRMA QAYDALARI:
❌ HEÇ VAXT cədvəl (table) istifadə etmə!
❌ HEÇ VAXT | simvolu ilə cədvəl yaratma!
✅ Yalnız bullet point siyahılardan istifadə et
✅ Qısa, aydın, oxunaqlı format
✅ Maksimum 5-6 bullet point

CAVAB FORMATI (QISA):
1. Başlıq (emoji + maksimum 5 söz)
2. Qısa giriş (1 cümlə)
3. Əsas məlumat (3-5 bullet point, CƏDVƏL YOX!)
4. Konkret rəqəmlər (2-3 nümunə, bullet point ilə)
5. 1-2 praktik tövsiyə
6. 1 vacib xəbərdarlıq (⚠️)

NÜMUNƏ DÜZGÜN FORMAT:
🌿 NPK Gübrələmə mərhələləri:
- **Vegetativ böyümə**: Yüksək Azot (N) - NPK 20-10-10
- **Çiçəkləmə**: Yüksək Fosfor (P) - NPK 10-52-10
- **Meyvə böyüməsi**: Yüksək Kalium (K) - NPK 15-5-30

Uzun cavabdan çəkin! Qısa, dəqiq, faydalı ol!

Fermerə dost, peşəkar və faydalı ol!"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini chatbot

        Args:
            api_key: Gemini API key (if not provided, loads from GEMINI_API_KEY env var)
        """
        # Get API key from parameter or environment
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. Please set it in .env file or pass as parameter."
            )

        # Configure Gemini
        genai.configure(api_key=self.api_key)

        # Initialize model (gemini-flash-latest - free, fast, and always up-to-date)
        self.model = genai.GenerativeModel(
            model_name='gemini-flash-latest',
            generation_config={
                'temperature': 0.7,
                'top_p': 0.95,
                'top_k': 40,
                'max_output_tokens': 1500,  # Balanced: detailed but complete responses
            }
        )

        # Chat history storage (session_id -> chat_session)
        self.sessions: Dict[str, any] = {}

    def _get_or_create_session(self, session_id: Optional[str] = None):
        """Get existing chat session or create new one"""
        if session_id and session_id in self.sessions:
            return self.sessions[session_id]

        # Create new chat session with system prompt
        chat = self.model.start_chat(history=[
            {
                'role': 'user',
                'parts': [self.SYSTEM_PROMPT]
            },
            {
                'role': 'model',
                'parts': ['Başa düşdüm! Mən AgriAdvisor - Azərbaycan fermerlərinin kənd təsərrüfatı məsləhətçisiyəm. Sizə praktik, konkret məsləhətlər verəcəyəm. Sualınızı gözləyirəm! 🌾']
            }
        ])

        if session_id:
            self.sessions[session_id] = chat

        return chat

    def _generate_quick_replies(self, user_message: str, response: str) -> List[str]:
        """Generate contextual quick reply suggestions"""
        # Basic keyword-based quick replies
        message_lower = user_message.lower()

        if any(word in message_lower for word in ['suvar', 'su', 'nəmlik']):
            return ["💧 Nə qədər su?", "⏰ Nə vaxt suvarım?", "🌊 Hansı üsul?"]

        elif any(word in message_lower for word in ['gübrə', 'npk', 'azot']):
            return ["🌿 Hansı gübrə?", "⚖️ Nə qədər?", "📅 Nə vaxt?"]

        elif any(word in message_lower for word in ['xəstə', 'zərər', 'böcək', 'saral']):
            return ["🐛 Nə xəstəlikdir?", "💊 Müalicə?", "🛡️ Qoruma?"]

        elif any(word in message_lower for word in ['hava', 'isti', 'soyuq', 'yağış']):
            return ["🌡️ İsti hava", "❄️ Soyuq hava", "🌧️ Yağış"]

        elif any(word in message_lower for word in ['heyvan', 'inək', 'qoyun', 'yem']):
            return ["🐄 Yemləmə", "💉 Peyvənd", "🩺 Sağlamlıq"]

        else:
            return ["📋 Tövsiyə al", "❓ Kömək", "🌾 Başqa sual"]

    def chat(self, user_message: str, session_id: Optional[str] = None) -> ChatResponse:
        """
        Process user message and return AI response

        Args:
            user_message: User's message in Azerbaijani
            session_id: Optional session ID for conversation history

        Returns:
            ChatResponse with AI-generated response and quick replies
        """
        try:
            # Get or create chat session
            chat_session = self._get_or_create_session(session_id)

            # Send message and get response
            response = chat_session.send_message(user_message)
            response_text = response.text

            # Generate quick replies based on context
            quick_replies = self._generate_quick_replies(user_message, response_text)

            return ChatResponse(
                response=response_text,
                quick_replies=quick_replies
            )

        except Exception as e:
            # Fallback response on error
            return ChatResponse(
                response=f"Bağışlayın, texniki xəta baş verdi. Zəhmət olmasa bir az sonra yenidən cəhd edin.\n\nXəta: {str(e)}",
                quick_replies=["🔄 Yenidən cəhd et", "🏠 Ana səhifə"]
            )

    def reset_session(self, session_id: str):
        """Reset a chat session"""
        if session_id in self.sessions:
            del self.sessions[session_id]

    def get_session_count(self) -> int:
        """Get number of active sessions"""
        return len(self.sessions)


# Singleton instance
_chatbot_instance: Optional[AgriAdvisorGeminiChatbot] = None


def get_chatbot() -> AgriAdvisorGeminiChatbot:
    """Get or create chatbot instance"""
    global _chatbot_instance
    if _chatbot_instance is None:
        _chatbot_instance = AgriAdvisorGeminiChatbot()
    return _chatbot_instance
