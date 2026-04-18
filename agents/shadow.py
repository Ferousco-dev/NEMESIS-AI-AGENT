"""
Agent 1: THE SHADOW
====================
Role: Silent watcher. Ingests raw user data and extracts behavioral signals.
Never speaks to the user directly.
Feeds structured observations to The Profiler.
"""

from agents.base import BaseAgent
from utils.cache import CacheKeys, hash_data


SHADOW_SYSTEM_PROMPT = """Extract behavioral signals: patterns, triggers, avoidance, time behavior.
Third person summary only. No fluff."""


class ShadowAgent(BaseAgent):
    def __init__(self, memory):
        super().__init__(memory, SHADOW_SYSTEM_PROMPT)

    async def process(self, raw_data: str) -> str:
        if not raw_data.strip():
            return "No data to process."

        # Create cache key based on data hash
        data_hash = hash_data(raw_data)
        cache_key = f"shadow_{data_hash}"

        prompt = f"""Process data. Extract ALL behavioral signals.
Be exhaustive. Miss nothing.

=== RAW DATA ===
{raw_data}
=== END DATA ===

Return structured behavioral signal report."""
        
        result = self._call(prompt, cache_key=cache_key)

        # Store the shadow summary in memory
        self.memory.data["shadow_summary"] = result
        self.memory.save()

        return "Behavioral signals extracted and stored. The Profiler is ready."
