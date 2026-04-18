"""
Agent 4: THE VOICE
===================
Role: The only agent the user talks to directly.
Armed with the full psychological profile, patterns, and predictions,
The Voice delivers real-time interventions.

It does NOT comfort. It does NOT validate.
It tells the truth — backed by evidence from the user's own data.
"""

from agents.base import BaseAgent
from utils.cache import CacheKeys, hash_data


VOICE_SYSTEM_PROMPT = """You are NEMESIS intervention voice. Mirror user's patterns. Show two futures.
One specific action, 24h. Be direct, cite evidence, no softening."""


class VoiceAgent(BaseAgent):
    def __init__(self, memory):
        super().__init__(memory, VOICE_SYSTEM_PROMPT)

    def _build_context_block(self) -> str:
        profile = self.memory.get_profile_summary()
        patterns = self.memory.get_patterns_summary()
        predictions = self.memory.get_predictions_summary()

        return f"""
PROFILE: {profile}
PATTERNS: {patterns}
PREDICTIONS: {predictions}
"""

    async def intervene(self, user_message: str) -> str:
        history = self.memory.get_conversation_history()
        context = self._build_context_block()

        # Create cache key based on user message and profile
        data_hash = hash_data(user_message + context)
        cache_key = f"voice_{data_hash}"

        # First turn: inject context + user message
        if not history:
            prompt = f"""{context}

User said: "{user_message}"

Deliver intervention. Format: [PATTERN DETECTED] [THE TRUTH] [TWO FUTURES] [YOUR MOVE]"""
            
            return self._call(prompt, cache_key=cache_key)

        # Subsequent turns: use conversation history
        enriched_history = [
            {"role": "user", "content": context + "\n\nBegin the conversation."},
            {"role": "model", "content": "NEMESIS is active. Tell me what's happening."},
        ] + history

        return self._call_with_history(enriched_history, user_message)
