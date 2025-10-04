"""
Caching layer for the Figma SDK.

Provides file-based caching with TTL support and cache management.
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, Optional
from .exceptions import FigmaCacheError
from .types import FigmaFile


class CacheEntry:
    """Single cache entry with TTL support."""

    def __init__(self, data: Any, ttl: int = 300):
        self.data = data
        self.timestamp = time.time()
        self.ttl = ttl

    def is_expired(self) -> bool:
        """Check if cache entry has expired."""
        return time.time() - self.timestamp > self.ttl

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "data": self.data,
            "timestamp": self.timestamp,
            "ttl": self.ttl
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CacheEntry":
        """Create from dictionary."""
        entry = cls(data["data"], data["ttl"])
        entry.timestamp = data["timestamp"]
        return entry


class FigmaCache:
    """File-based cache for Figma API responses."""

    def __init__(self, cache_dir: str = "figma_cache"):
        """Initialize cache with directory."""
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self, key: str) -> Path:
        """Get cache file path for a key."""
        # Ensure key is filesystem-safe
        safe_key = "".join(c if c.isalnum() else "_" for c in key)
        return self.cache_dir / f"{safe_key}.json"

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        cache_path = self._get_cache_path(key)

        if not cache_path.exists():
            return None

        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                entry_data = json.load(f)

            entry = CacheEntry.from_dict(entry_data)

            if entry.is_expired():
                self.delete(key)
                return None

            return entry.data

        except (json.JSONDecodeError, IOError, KeyError) as e:
            raise FigmaCacheError(f"Failed to read cache entry {key}: {e}")

    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        """Set value in cache with TTL."""
        cache_path = self._get_cache_path(key)
        entry = CacheEntry(value, ttl)

        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(entry.to_dict(), f, indent=2)
        except IOError as e:
            raise FigmaCacheError(f"Failed to write cache entry {key}: {e}")

    def delete(self, key: str) -> bool:
        """Delete cache entry."""
        cache_path = self._get_cache_path(key)

        if cache_path.exists():
            try:
                cache_path.unlink()
                return True
            except IOError:
                return False

        return False

    def clear(self) -> None:
        """Clear all cache entries."""
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                cache_file.unlink()
            except IOError:
                pass

    def cleanup_expired(self) -> int:
        """Remove expired cache entries and return count of removed items."""
        removed_count = 0

        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    entry_data = json.load(f)

                entry = CacheEntry.from_dict(entry_data)

                if entry.is_expired():
                    cache_file.unlink()
                    removed_count += 1

            except (json.JSONDecodeError, IOError, KeyError):
                # Remove corrupted cache files
                try:
                    cache_file.unlink()
                    removed_count += 1
                except IOError:
                    pass

        return removed_count

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_entries = 0
        expired_entries = 0
        total_size = 0

        for cache_file in self.cache_dir.glob("*.json"):
            total_entries += 1

            try:
                total_size += cache_file.stat().st_size

                with open(cache_file, 'r', encoding='utf-8') as f:
                    entry_data = json.load(f)

                entry = CacheEntry.from_dict(entry_data)

                if entry.is_expired():
                    expired_entries += 1

            except (json.JSONDecodeError, IOError, KeyError):
                # Count corrupted files as expired
                expired_entries += 1

        return {
            "total_entries": total_entries,
            "expired_entries": expired_entries,
            "valid_entries": total_entries - expired_entries,
            "total_size_bytes": total_size
        }