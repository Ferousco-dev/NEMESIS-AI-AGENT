"""
Agent 3: THE ORACLE
====================
Role: Future simulator.
Takes the psychological profile and simulates the most likely scenarios
the person will face in the next 30 days — and where they will fail.
"""

from agents.base import BaseAgent
from utils.cache import CacheKeys, hash_data


ORACLE_SYSTEM_PROMPT = """Simulate 30-day behavior scenarios. Specific triggers, probabilities, outcomes.
Risk level: GREEN/AMBER/RED. Return JSON only."""


class OracleAgent(BaseAgent):
    def __init__(self, memory):
        super().__init__(memory, ORACLE_SYSTEM_PROMPT)

    async def simulate(self) -> dict:
        profile = self.memory.get_profile_summary()
        patterns = self.memory.get_patterns_summary()
        raw = self.memory.get_all_raw_text()

        # Create cache key
        data_hash = hash_data(profile + patterns + raw)
        cache_key = f"oracle_{data_hash}"

        prompt = f"""Predict 30-day scenarios for this person. Return JSON.

=== PROFILE ===
{profile}

=== PATTERNS ===
{patterns}

=== DATA ===
{raw[:5000]}

Return JSON: {{"overall_risk": "GREEN|AMBER|RED", "scenarios": [...], "verdict": "string"}}"""
        
        prediction = self._call(prompt, expect_json=True, cache_key=cache_key)
        self.memory.add_prediction(prediction if isinstance(prediction, dict) else {"raw": str(prediction)})
        return prediction
