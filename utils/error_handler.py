"""
Error Handler & Graceful Fallback System
Catches rate limit errors and provides helpful user feedback.
"""

from utils.ui import NemesisUI
from utils.cache import APICache
import asyncio


class RateLimitHandler:
    """Handle rate limit errors gracefully."""
    
    @staticmethod
    def is_rate_limit_error(error: Exception) -> bool:
        """Check if error is a rate limit error."""
        error_msg = str(error).lower()
        return any(phrase in error_msg for phrase in [
            'rate limit',
            '429',
            'quota',
            'exceeded',
            'tokens per day'
        ])
    
    @staticmethod
    def handle_rate_limit(error: Exception, stage: str = "API"):
        """
        Handle rate limit error gracefully.
        
        Args:
            error: The exception
            stage: What stage failed (Shadow, Profiler, etc)
        """
        error_msg = str(error)
        
        # Extract retry time if available
        retry_time = None
        if "Please try again in" in error_msg:
            try:
                import re
                match = re.search(r'Please try again in (.+?)\. Need', error_msg)
                if match:
                    retry_time = match.group(1)
            except:
                pass
        
        # Show user-friendly message
        NemesisUI.panel_error(
            "Rate Limit Reached",
            f"[yellow]The LLM provider has exhausted daily token limits.[/yellow]\n\n"
            f"[cyan]What happened:[/cyan] {stage} stage tried to call the API\n"
            f"[cyan]Status:[/cyan] Daily token quota exceeded (100k tokens/day)\n\n"
            f"[cyan]Options:[/cyan]\n"
            f"  1. [green]Use cached demo:[/green] python3 cached_demo.py\n"
            f"  2. [green]Wait until tomorrow:[/green] Rate limits reset at midnight UTC\n"
            f"  3. [green]Upgrade Groq tier:[/green] https://console.groq.com/settings/billing\n"
            f"  4. [green]Use different API:[/green] Set OPENAI_API_KEY or other provider\n\n"
            + (f"[dim]Retry available in: {retry_time}[/dim]" if retry_time else "")
        )
    
    @staticmethod
    async def use_cached_mode():
        """Fall back to cached demo mode."""
        NemesisUI.panel_warning(
            "Falling back to Cached Demo",
            "Using pre-computed results to show functionality without API calls.\n"
            "All features work the same - this is cached data from previous runs."
        )
        await asyncio.sleep(1)
        
        # Import and run cached demo
        from cached_demo import run_cached_demo
        await run_cached_demo()
        return True


class APIErrorHandler:
    """Handle all API-related errors."""
    
    @staticmethod
    def handle(error: Exception, context: str = "") -> tuple[bool, str]:
        """
        Handle API error and return recovery info.
        
        Args:
            error: The exception
            context: Context where error occurred
            
        Returns:
            Tuple of (is_rate_limit, message)
        """
        error_str = str(error)
        
        if RateLimitHandler.is_rate_limit_error(error):
            return (True, "Rate limit exceeded. Use cached demo or wait until tomorrow.")
        
        if "invalid_request_error" in error_str:
            if "model" in error_str and "decommissioned" in error_str:
                return (False, "Model is deprecated. Update GROQ_MODEL in .env")
            return (False, "Invalid request format.")
        
        if "not found" in error_str.lower() or "404" in error_str:
            return (False, "API key or model not found. Check .env configuration.")
        
        if "authentication" in error_str.lower() or "unauthorized" in error_str.lower():
            return (False, "Authentication failed. Check your API keys.")
        
        return (False, f"API error: {error_str[:100]}")


def show_cached_option():
    """Show user the cached demo option."""
    NemesisUI.panel_info(
        "API Rate Limited",
        "[yellow]⚠️ Daily API quota reached for all providers[/yellow]\n\n"
        "[cyan]Alternative: Use Cached Demo[/cyan]\n"
        "  [green]python3 cached_demo.py[/green]\n\n"
        "[dim]Cached demo shows exactly what the system does - with no API costs![/dim]"
    )
