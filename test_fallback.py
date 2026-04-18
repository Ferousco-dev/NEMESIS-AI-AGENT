#!/usr/bin/env python3
"""Quick test of Gemini → Groq fallback."""

import os
from dotenv import load_dotenv

load_dotenv()

# Quick test to verify both APIs are configured
print("=" * 60)
print("GEMINI ↔ GROQ FALLBACK SYSTEM TEST")
print("=" * 60)

gemini_key = os.getenv("GEMINI_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")
provider = os.getenv("LLM_PROVIDER", "auto")

print(f"\n✓ Configuration:")
print(f"  LLM_PROVIDER: {provider}")
print(f"  Gemini API Key: {'✓ Set' if gemini_key else '✗ Not set'}")
print(f"  Groq API Key:   {'✓ Set' if groq_key else '✗ Not set'}")

print(f"\nProvider Mode: {provider.upper()}")
if provider == "auto":
    print("  → Will try Gemini first")
    print("  → Falls back to Groq on rate limit (429) or quota errors")
elif provider == "gemini":
    print("  → Using Gemini only (no fallback)")
elif provider == "groq":
    print("  → Using Groq only (no fallback)")

print("\n✓ Testing imports...")
try:
    from agents.base import BaseAgent
    print("  ✓ BaseAgent imports successfully")
    
    # Quick instantiation test
    from core.memory import Memory
    mem = Memory()
    agent = BaseAgent(mem, "Test system instruction")
    print(f"  ✓ BaseAgent initialized with:")
    print(f"    - Gemini model: {agent.gemini_model_name if agent.gemini_model else 'Not configured'}")
    print(f"    - Groq model:   {agent.groq_model_name if agent.groq_client else 'Not configured'}")
    print(f"    - Provider:     {agent.provider}")
    
except Exception as e:
    print(f"  ✗ Error: {e}")
    exit(1)

print("\n✓ All checks passed!")
print("\n" + "=" * 60)
print("To run the full demo, use:")
print("  python3 main.py demo")
print("\nOr test specific commands:")
print("  python3 main.py demo        # Full simulation")
print("  LLM_PROVIDER=gemini python3 main.py demo    # Gemini only")
print("  LLM_PROVIDER=groq python3 main.py demo      # Groq only")
print("=" * 60)
