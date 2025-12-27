"""
Yonca Chatbot Engine
Azerbaijani language intent-based chatbot for agricultural advice
"""

import json
import re
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from difflib import SequenceMatcher


@dataclass
class ChatResponse:
    """Chatbot response structure"""
    intent: str
    confidence: float
    response: str
    action: Optional[str] = None
    quick_replies: Optional[List[str]] = None
    context_update: Optional[Dict[str, Any]] = None


class YoncaChatbot:
    """
    Intent-based chatbot for Azerbaijani agricultural advice
    """
    
    def __init__(self, intents_path: Optional[Path] = None):
        if intents_path is None:
            intents_path = Path(__file__).parent / "intents.json"
        
        with open(intents_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.intents = self.data['intents']
        self.entities = self.data.get('entities', {})
        self.quick_replies = self.data.get('quick_replies', {})
        
        # Build pattern index for faster matching
        self._build_pattern_index()
        
        # Conversation context
        self.context: Dict[str, Any] = {}
    
    def _build_pattern_index(self):
        """Pre-process patterns for efficient matching"""
        self.pattern_index: List[Tuple[str, str, List[str]]] = []
        
        for intent_data in self.intents:
            intent_name = intent_data['intent']
            patterns = intent_data.get('patterns', [])
            
            # Normalize patterns
            normalized_patterns = [self._normalize(p) for p in patterns]
            
            if normalized_patterns:
                self.pattern_index.append((intent_name, intent_data, normalized_patterns))
    
    def _normalize(self, text: str) -> str:
        """Normalize text for matching"""
        text = text.lower().strip()
        # Remove punctuation
        text = re.sub(r'[^\w\s]', '', text)
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        return text
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        return SequenceMatcher(None, text1, text2).ratio()
    
    def _fuzzy_match(self, user_input: str, pattern: str) -> float:
        """Fuzzy match user input against a pattern"""
        # Exact match
        if user_input == pattern:
            return 1.0
        
        # Contains match
        if pattern in user_input:
            return 0.9
        
        # Word overlap
        user_words = set(user_input.split())
        pattern_words = set(pattern.split())
        
        if pattern_words and user_words:
            overlap = len(user_words & pattern_words)
            max_len = max(len(user_words), len(pattern_words))
            if overlap > 0:
                return 0.5 + (0.4 * overlap / max_len)
        
        # Sequence similarity
        similarity = self._calculate_similarity(user_input, pattern)
        if similarity > 0.7:
            return similarity * 0.8
        
        return 0.0
    
    def _find_best_intent(self, user_input: str) -> Tuple[str, float, Dict]:
        """Find the best matching intent for user input"""
        normalized_input = self._normalize(user_input)
        
        best_intent = 'unknown'
        best_confidence = 0.0
        best_intent_data = None
        
        for intent_name, intent_data, patterns in self.pattern_index:
            if intent_name == 'unknown':
                continue
            
            for pattern in patterns:
                confidence = self._fuzzy_match(normalized_input, pattern)
                
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_intent = intent_name
                    best_intent_data = intent_data
        
        # If no good match found, use unknown
        if best_confidence < 0.3:
            for intent_data in self.intents:
                if intent_data['intent'] == 'unknown':
                    return 'unknown', 0.0, intent_data
        
        return best_intent, best_confidence, best_intent_data
    
    def _extract_entities(self, user_input: str) -> Dict[str, str]:
        """Extract entities from user input"""
        extracted = {}
        normalized = self._normalize(user_input)
        
        for entity_type, entity_map in self.entities.items():
            for az_term, en_term in entity_map.items():
                if az_term in normalized:
                    extracted[entity_type] = en_term
                    break
        
        return extracted
    
    def _get_response(self, intent_data: Dict) -> str:
        """Get a random response for the intent"""
        responses = intent_data.get('responses', ['Bağışlayın, cavab tapa bilmədim.'])
        return random.choice(responses)
    
    def _get_quick_replies(self, intent: str, action: Optional[str]) -> Optional[List[str]]:
        """Get quick reply suggestions based on intent and action"""
        if action == 'ask_irrigation_details':
            return self.quick_replies.get('crop_selection')
        elif action == 'ask_fertilization_details':
            return self.quick_replies.get('crop_selection')
        elif action == 'ask_pest_details':
            return self.quick_replies.get('problem_type')
        elif action == 'ask_livestock_details':
            return self.quick_replies.get('animal_selection')
        return None
    
    def _update_context(self, intent: str, entities: Dict[str, str]):
        """Update conversation context"""
        self.context['last_intent'] = intent
        self.context['entities'] = {**self.context.get('entities', {}), **entities}
    
    def chat(self, user_input: str) -> ChatResponse:
        """
        Process user input and return response
        
        Args:
            user_input: User's message in Azerbaijani
            
        Returns:
            ChatResponse with intent, response, and optional actions
        """
        # Find best matching intent
        intent, confidence, intent_data = self._find_best_intent(user_input)
        
        # Extract entities
        entities = self._extract_entities(user_input)
        
        # Get response
        response = self._get_response(intent_data)
        
        # Get action if any
        action = intent_data.get('action')
        
        # Get quick replies
        quick_replies = self._get_quick_replies(intent, action)
        
        # Update context
        self._update_context(intent, entities)
        
        return ChatResponse(
            intent=intent,
            confidence=confidence,
            response=response,
            action=action,
            quick_replies=quick_replies,
            context_update={'entities': entities} if entities else None
        )
    
    def get_context(self) -> Dict[str, Any]:
        """Get current conversation context"""
        return self.context.copy()
    
    def reset_context(self):
        """Reset conversation context"""
        self.context = {}
    
    def get_intent_list(self) -> List[str]:
        """Get list of all available intents"""
        return [intent['intent'] for intent in self.intents]


# Singleton instance
_chatbot_instance: Optional[YoncaChatbot] = None


def get_chatbot() -> YoncaChatbot:
    """Get or create chatbot instance"""
    global _chatbot_instance
    if _chatbot_instance is None:
        _chatbot_instance = YoncaChatbot()
    return _chatbot_instance
