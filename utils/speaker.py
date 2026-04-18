"""
AI Voice Speaker using OpenAI TTS API
Streams and plays audio without saving files.
"""

import os
import io
from typing import Optional
from openai import OpenAI
import threading
from utils.ui import NemesisUI, console


class AIVoiceSpeaker:
    """Generates and plays AI voice using OpenAI TTS."""
    
    # Voice options: alloy, echo, fable, onyx, nova, shimmer
    AVAILABLE_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    TTS_MODEL = "tts-1"  # or "tts-1-hd" for higher quality (slower, more expensive)
    
    def __init__(self, voice: str = "nova", enable_audio: bool = True):
        """
        Initialize the AI voice speaker.
        
        Args:
            voice: OpenAI voice name (default: nova - sounds natural)
            enable_audio: Whether to actually play audio (can be disabled for testing)
        """
        self.voice = voice if voice in self.AVAILABLE_VOICES else "nova"
        self.enable_audio = enable_audio
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self._audio_thread = None
    
    def _validate_api_key(self) -> bool:
        """Check if OpenAI API key is configured."""
        if not os.getenv("OPENAI_API_KEY"):
            NemesisUI.warning("OpenAI API key not configured. Audio disabled.")
            return False
        return True
    
    def _play_audio(self, audio_data: bytes):
        """Play audio using pygame (fallback: silent mode)."""
        if not self.enable_audio:
            return
        
        try:
            import pygame
            
            # Initialize pygame mixer
            pygame.mixer.init()
            
            # Load audio from bytes
            audio_stream = io.BytesIO(audio_data)
            sound = pygame.mixer.Sound(audio_stream)
            
            # Play sound
            sound.play()
            
            # Wait for playback to finish
            while pygame.mixer.get_busy():
                pass
                
        except ImportError:
            console.print("[dim]pygame not available for audio playback[/dim]")
        except Exception as e:
            console.print(f"[dim]Audio playback error: {e}[/dim]")
    
    def speak(self, text: str, async_play: bool = True):
        """
        Generate and play AI voice for the given text.
        
        Args:
            text: Text to speak
            async_play: If True, play audio in background thread (non-blocking)
        """
        if not self.enable_audio:
            return
        
        if not self._validate_api_key():
            return
        
        try:
            # Clean text
            clean_text = self._clean_text_for_speech(text)
            
            # Generate speech using OpenAI TTS
            response = self.client.audio.speech.create(
                model=self.TTS_MODEL,
                voice=self.voice,
                input=clean_text,
                speed=1.0,  # 0.25 to 4.0
            )
            
            # Get audio bytes from response
            audio_data = response.content
            
            # Play audio
            if async_play:
                # Play in background thread so it doesn't block
                self._audio_thread = threading.Thread(
                    target=self._play_audio,
                    args=(audio_data,),
                    daemon=True
                )
                self._audio_thread.start()
            else:
                # Block until audio finishes
                self._play_audio(audio_data)
        
        except Exception as e:
            # Fail gracefully - voice is optional
            console.print(f"[dim]Voice generation failed: {e}[/dim]")
    
    def speak_and_display(self, text: str, title: str = "The Voice"):
        """
        Speak the text while displaying it in a rich panel.
        
        Args:
            text: Text to speak and display
            title: Panel title
        """
        # Display in panel
        NemesisUI.agent_speaking(title, text)
        
        # Speak in background
        self.speak(text, async_play=True)
    
    @staticmethod
    def _clean_text_for_speech(text: str) -> str:
        """
        Clean text for better speech output by removing markdown and special chars.
        """
        # Remove markdown formatting
        clean = text.replace("**", "").replace("*", "").replace("__", "").replace("_", "")
        
        # Remove markdown headers
        lines = clean.split("\n")
        lines = [line.lstrip("#").strip() for line in lines]
        clean = "\n".join(lines)
        
        # Remove code blocks
        clean = clean.replace("```", "").replace("`", "")
        
        # Remove excess whitespace
        clean = " ".join(clean.split())
        
        # Remove special characters that sound weird
        chars_to_remove = ["[", "]", "{", "}", "→", "←", "↑", "↓", "─", "═", "╔", "╗", "╚", "╝"]
        for char in chars_to_remove:
            clean = clean.replace(char, "")
        
        # Limit to 4096 chars (OpenAI TTS limit)
        if len(clean) > 4096:
            clean = clean[:4096] + "..."
        
        return clean
    
    def get_voice_name(self) -> str:
        """Get the current voice name."""
        return self.voice
    
    def set_voice(self, voice: str):
        """
        Switch to a different voice.
        
        Args:
            voice: Voice name from AVAILABLE_VOICES
        """
        if voice in self.AVAILABLE_VOICES:
            self.voice = voice
            NemesisUI.success(f"Voice changed to: {voice}")
        else:
            NemesisUI.error(f"Voice '{voice}' not available. Use one of: {', '.join(self.AVAILABLE_VOICES)}")


class SilentFallback:
    """Fallback speaker when voice is disabled or API fails."""
    
    def __init__(self):
        pass
    
    def speak(self, text: str, async_play: bool = True):
        """Silent mode - do nothing."""
        pass
    
    def speak_and_display(self, text: str, title: str = "The Voice"):
        """Display text without audio."""
        NemesisUI.agent_speaking(title, text)


def get_speaker(enable_voice: bool = True) -> AIVoiceSpeaker:
    """
    Factory function to get a configured speaker.
    
    Args:
        enable_voice: Whether to enable AI voice (or use silent mode)
    
    Returns:
        AIVoiceSpeaker or SilentFallback instance
    """
    if enable_voice and os.getenv("OPENAI_API_KEY"):
        return AIVoiceSpeaker(voice="nova", enable_audio=True)
    elif enable_voice:
        # OpenAI key not set - fall back to silent
        console.print("[yellow]OpenAI API key not set - voice disabled. Set OPENAI_API_KEY to enable.[/yellow]")
        return SilentFallback()
    else:
        return SilentFallback()
