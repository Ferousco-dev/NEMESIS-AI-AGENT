"""
Base agent — all NEMESIS agents inherit from this.
Handles Gemini API calls with Groq fallback on rate limits.
Includes intelligent caching to reduce API calls.
"""

from __future__ import annotations
import os
import json
import time
from typing import Union, Optional
import google.generativeai as genai
from groq import Groq
from utils.logger import logger
from utils.cache import APICache


class BaseAgent:
    DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
    DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"

    def __init__(self, memory, system_instruction: str):
        self.memory = memory
        self.system_instruction = system_instruction
        self.gemini_model_name = os.getenv("GEMINI_MODEL", self.DEFAULT_GEMINI_MODEL)
        self.groq_model_name = os.getenv("GROQ_MODEL", self.DEFAULT_GROQ_MODEL)
        
        # Track which provider to use
        self.provider = os.getenv("LLM_PROVIDER", "gemini").lower()  # "gemini", "groq", or "auto"
        self.use_gemini = True  # For auto mode, start with Gemini
        
        self._configure()

    def _configure(self):
        """Configure both Gemini and Groq clients."""
        # Configure Gemini
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key:
            genai.configure(api_key=gemini_key)
            self.gemini_model = genai.GenerativeModel(
                model_name=self.gemini_model_name,
                system_instruction=self.system_instruction,
                generation_config=genai.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=4096,
                )
            )
        else:
            self.gemini_model = None
            logger.warning("GEMINI_API_KEY not set.")
        
        # Configure Groq
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            self.groq_client = Groq(api_key=groq_key)
        else:
            self.groq_client = None
            logger.warning("GROQ_API_KEY not set.")
        
        # Validate at least one provider is configured
        if not self.gemini_model and not self.groq_client:
            raise EnvironmentError(
                "Neither GEMINI_API_KEY nor GROQ_API_KEY is set."
            )

    def _call(self, prompt: str, expect_json: bool = False, cache_key: str = None) -> Union[str, dict]:
        """
        Call LLM with automatic fallback from Gemini to Groq on rate limit.
        Includes caching to reduce API calls.
        
        Args:
            prompt: The prompt to send
            expect_json: Whether to parse response as JSON
            cache_key: Optional cache key (if provided, checks cache first)
        
        Returns:
            LLM response (string or dict if JSON)
        """
        # Check cache if key provided
        if cache_key:
            cached = APICache.get(cache_key)
            if cached:
                logger.info(f"Using cached response for key: {cache_key}")
                if expect_json and isinstance(cached, str):
                    return self._parse_json(cached)
                return cached
        
        if self.provider == "gemini":
            result = self._call_gemini(prompt, expect_json)
        elif self.provider == "groq":
            result = self._call_groq(prompt, expect_json)
        else:  # "auto" - try Gemini first, fall back to Groq
            result = self._call_with_fallback(prompt, expect_json)
        
        # Cache the result if key provided
        if cache_key:
            APICache.set(cache_key, result)
            logger.info(f"Cached response with key: {cache_key}")
        
        return result

    def _call_gemini(self, prompt: str, expect_json: bool = False) -> Union[str, dict]:
        """Call Gemini API with retry logic."""
        if not self.gemini_model:
            raise EnvironmentError("Gemini model not configured.")
        
        for attempt in range(3):
            try:
                response = self.gemini_model.generate_content(prompt)
                text = response.text.strip()

                if expect_json:
                    return self._parse_json(text)
                return text

            except Exception as e:
                error_msg = str(e)
                
                # Check for rate limit errors - don't log these, fail fast
                if "429" in error_msg or "rate" in error_msg.lower() or "quota" in error_msg.lower():
                    raise
                
                # Log other errors for debugging
                logger.warning(f"Gemini attempt {attempt+1} failed: {e}")
                
                if attempt < 2:
                    time.sleep(2 ** attempt)
                else:
                    raise

    def _call_groq(self, prompt: str, expect_json: bool = False) -> Union[str, dict]:
        """Call Groq API with retry logic."""
        if not self.groq_client:
            raise EnvironmentError("Groq client not configured.")
        
        for attempt in range(3):
            try:
                response = self.groq_client.chat.completions.create(
                    model=self.groq_model_name,
                    messages=[
                        {"role": "system", "content": self.system_instruction},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=4096,
                )
                text = response.choices[0].message.content.strip()

                if expect_json:
                    return self._parse_json(text)
                return text

            except Exception as e:
                error_msg = str(e)
                
                # Check for rate limit errors - don't log these, fail fast
                if "429" in error_msg or "rate" in error_msg.lower() or "quota" in error_msg.lower() or "exhausted" in error_msg.lower():
                    raise
                
                # Log other errors for debugging
                logger.warning(f"Groq attempt {attempt+1} failed: {e}")
                
                if attempt < 2:
                    time.sleep(2 ** attempt)
                else:
                    raise

    def _parse_json(self, text: str) -> dict:
        """Extract JSON from response even if wrapped in markdown."""
        clean = text
        if "```json" in clean:
            clean = clean.split("```json")[1].split("```")[0]
        elif "```" in clean:
            clean = clean.split("```")[1].split("```")[0]
        try:
            return json.loads(clean.strip())
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON: {clean[:200]}")
            return {"raw": text}

    def _call_with_history(self, history: list, new_message: str) -> str:
        """Multi-turn conversation with history."""
        if self.provider == "groq":
            return self._call_with_history_groq(history, new_message)
        else:  # Gemini or auto
            try:
                return self._call_with_history_gemini(history, new_message)
            except Exception as e:
                if "429" in str(e) or "rate" in str(e).lower() or "quota" in str(e).lower():
                    logger.warning(f"Gemini rate limit, falling back to Groq: {e}")
                    return self._call_with_history_groq(history, new_message)
                raise

    def _call_with_history_gemini(self, history: list, new_message: str) -> str:
        """Multi-turn conversation with Gemini."""
        if not self.gemini_model:
            raise EnvironmentError("Gemini model not configured.")
        
        chat = self.gemini_model.start_chat(history=[
            {"role": t["role"], "parts": [t["content"]]}
            for t in history
        ])
        response = chat.send_message(new_message)
        return response.text.strip()

    def _call_with_history_groq(self, history: list, new_message: str) -> str:
        """Multi-turn conversation with Groq."""
        if not self.groq_client:
            raise EnvironmentError("Groq client not configured.")
        
        messages = [{"role": t["role"], "content": t["content"]} for t in history]
        messages.append({"role": "user", "content": new_message})
        
        response = self.groq_client.chat.completions.create(
            model=self.groq_model_name,
            messages=messages,
            temperature=0.7,
            max_tokens=4096,
        )
        return response.choices[0].message.content.strip()
