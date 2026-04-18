"""
Agent 2: THE PROFILER
======================
Role: Psychological model builder.
Takes The Shadow's raw signals and constructs a deep psychological profile.
Returns structured JSON — the user's behavioral fingerprint.
"""

from agents.base import BaseAgent
from utils.cache import CacheKeys, hash_data


PROFILER_SYSTEM_PROMPT = """Build psychological model: traits, wounds, mechanisms, blind spots, strengths.
Cite evidence. Be specific. Return JSON only."""


class ProfilerAgent(BaseAgent):
    def __init__(self, memory):
        super().__init__(memory, PROFILER_SYSTEM_PROMPT)

    async def analyze(self) -> dict:
        shadow_summary = self.memory.data.get("shadow_summary", "")
        raw_text = self.memory.get_all_raw_text()

        if not shadow_summary and not raw_text:
            return {"error": "No data available. Run ingestion first."}

        # Create cache key
        data_hash = hash_data(shadow_summary + raw_text)
        cache_key = f"profiler_{data_hash}"

        prompt = f"""Analyze this behavioral data and return psychological profile as JSON.

=== SIGNALS ===
{shadow_summary}

=== DATA ===
{raw_text[:5000]}

Return JSON: {{"traits": [...], "wounds": [...], "mechanisms": [...], "blind_spots": [...], "strengths": [...]}}"""
        
        profile = self._call(prompt, expect_json=True, cache_key=cache_key)
        self.memory.set_profile(profile)

        # Extract patterns list for Oracle
        patterns = []
        if isinstance(profile, dict):
            patterns += profile.get("blind_spots", [])
            patterns += profile.get("mechanisms", [])
            patterns += profile.get("decision_flaws", [])
        self.memory.set_patterns(patterns)

        return profile
