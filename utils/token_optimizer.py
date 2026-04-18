"""
Token Optimization System for NEMESIS
Helps reduce Groq API consumption by using compact prompts.
"""

import os


class TokenOptimizer:
    """Reduce token consumption while maintaining quality."""
    
    # Mode: "full" (verbose, high quality) or "lite" (compact, token-efficient)
    MODE = os.getenv("NEMESIS_MODE", "lite").lower()
    
    VERBOSE = MODE == "full"
    
    @staticmethod
    def get_mode() -> str:
        """Get current optimization mode."""
        return TokenOptimizer.MODE
    
    @staticmethod
    def is_verbose() -> bool:
        """Check if in verbose mode (uses more tokens)."""
        return TokenOptimizer.VERBOSE
    
    @staticmethod
    def shadow_system_prompt() -> str:
        """Get Shadow agent system prompt (optimized)."""
        if TokenOptimizer.VERBOSE:
            return """You are THE SHADOW — behavioral intelligence.
Extract: recurring behaviors, avoidance patterns, emotional triggers, 
self-deception markers, time patterns, relationship patterns, decision signatures.
Output: structured summary in third person. No fluff."""
        else:
            return """Extract behavioral signals: patterns, triggers, avoidance, time behavior.
Third person summary only. No fluff."""
    
    @staticmethod
    def profiler_system_prompt() -> str:
        """Get Profiler agent system prompt (optimized)."""
        if TokenOptimizer.VERBOSE:
            return """You are THE PROFILER — psychological architect.
Build a model of the person's mind using behavioral signals.
Output: personality traits, core wounds, defense mechanisms, blind spots, strengths.
Be specific. Cite evidence."""
        else:
            return """Build psychological model: traits, wounds, mechanisms, blind spots, strengths.
Cite evidence. Be specific."""
    
    @staticmethod
    def oracle_system_prompt() -> str:
        """Get Oracle agent system prompt (optimized)."""
        if TokenOptimizer.VERBOSE:
            return """You are THE ORACLE — prediction engine.
Based on the psychological profile, simulate the next 30 days.
Predict: high-risk situations, what happens if they do nothing, outcomes of action.
Output: structured prediction with scenarios."""
        else:
            return """Predict next 30 days: risk situations, outcomes of inaction vs. action.
Structured scenarios only."""
    
    @staticmethod
    def voice_system_prompt() -> str:
        """Get Voice agent system prompt (optimized)."""
        if TokenOptimizer.VERBOSE:
            return """You are THE VOICE — intervention specialist.
Using the full profile, deliver direct interventions. No comfort, just truth.
Reference evidence. Name patterns. Show two futures. Give one specific action."""
        else:
            return """Direct intervention: name pattern, show two futures, one specific action.
Evidence-based only. No comfort."""
    
    @staticmethod
    def summarize_data(raw_data: str, max_chars: int = 1000) -> str:
        """
        Summarize raw data to reduce token usage.
        In lite mode, only use first N characters.
        """
        if TokenOptimizer.VERBOSE:
            return raw_data
        
        if len(raw_data) > max_chars:
            return raw_data[:max_chars] + "\n[... data truncated for token efficiency ...]"
        return raw_data
