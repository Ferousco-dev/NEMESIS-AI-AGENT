"""
Intelligent Cache System for NEMESIS
Stores all API responses to avoid redundant calls and reduce token consumption.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Union, Dict, List


class APICache:
    """Cache system for API responses to minimize token usage."""
    
    CACHE_DIR = Path("./cache")
    CACHE_DIR.mkdir(exist_ok=True)
    
    # Cache expiry: 24 hours
    CACHE_EXPIRY = timedelta(hours=24)
    
    @staticmethod
    def _get_cache_file(key: str) -> Path:
        """Get cache file path for a key."""
        return APICache.CACHE_DIR / f"{key}.json"
    
    @staticmethod
    def _is_expired(timestamp: float) -> bool:
        """Check if cache entry is expired."""
        created = datetime.fromtimestamp(timestamp)
        return datetime.now() - created > APICache.CACHE_EXPIRY
    
    @staticmethod
    def get(key: str) -> Optional[Dict]:
        """
        Get cached value if it exists and is not expired.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value dict or None if not found/expired
        """
        cache_file = APICache._get_cache_file(key)
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r') as f:
                data = json.load(f)
            
            # Check expiry
            if APICache._is_expired(data.get('timestamp', 0)):
                cache_file.unlink()  # Delete expired cache
                return None
            
            return data.get('value')
        except Exception as e:
            print(f"Cache read error: {e}")
            return None
    
    @staticmethod
    def set(key: str, value: Union[Dict, str, List]) -> bool:
        """
        Store value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            
        Returns:
            True if successful
        """
        cache_file = APICache._get_cache_file(key)
        
        try:
            data = {
                'timestamp': datetime.now().timestamp(),
                'value': value
            }
            with open(cache_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Cache write error: {e}")
            return False
    
    @staticmethod
    def clear_all():
        """Clear all cache files."""
        try:
            for f in APICache.CACHE_DIR.glob("*.json"):
                f.unlink()
            return True
        except Exception as e:
            print(f"Cache clear error: {e}")
            return False
    
    @staticmethod
    def get_cache_stats() -> dict:
        """Get cache statistics."""
        cache_files = list(APICache.CACHE_DIR.glob("*.json"))
        return {
            'cached_items': len(cache_files),
            'cache_dir': str(APICache.CACHE_DIR),
            'items': [f.stem for f in cache_files]
        }


# Cache keys for each agent
class CacheKeys:
    """Predefined cache keys."""
    
    SHADOW_SUMMARY = "shadow_summary"
    PROFILER_PROFILE = "profiler_profile"
    ORACLE_PREDICTION = "oracle_prediction"
    VOICE_HISTORY_PREFIX = "voice_history_"
    
    @staticmethod
    def voice_history(turn: int) -> str:
        """Get cache key for voice interaction turn."""
        return f"{CacheKeys.VOICE_HISTORY_PREFIX}{turn}"


def create_cache_key(agent: str, data_hash: str) -> str:
    """Create cache key from agent name and data hash."""
    return f"{agent}_{data_hash}"


def hash_data(data: str) -> str:
    """Create simple hash of data (first 20 chars clean)."""
    import hashlib
    return hashlib.md5(data.encode()).hexdigest()[:16]
