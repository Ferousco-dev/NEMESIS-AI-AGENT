"""
Memory — NEMESIS persistent state store
Holds everything the agents know about the user across sessions.
"""

import json
import os
from datetime import datetime
from pathlib import Path


MEMORY_FILE = Path("data/nemesis_memory.json")


class Memory:
    def __init__(self):
        self.data = {
            "raw_entries": [],
            "behavioral_patterns": [],
            "psychological_profile": {},
            "predictions": [],
            "interventions": [],
            "conversation_history": [],
            "last_updated": None,
        }
        self._load()

    def _load(self):
        if MEMORY_FILE.exists() and MEMORY_FILE.stat().st_size > 0:
            try:
                with open(MEMORY_FILE, "r") as f:
                    loaded = json.load(f)
                    if loaded:  # Ensure loaded data is not empty
                        self.data = loaded
            except (json.JSONDecodeError, IOError):
                # File corrupted or empty - use default data
                pass

    def save(self):
        MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        self.data["last_updated"] = datetime.now().isoformat()
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.data, f, indent=2)

    def add_raw_entry(self, entry: str, source: str = "manual"):
        self.data["raw_entries"].append({
            "text": entry,
            "source": source,
            "timestamp": datetime.now().isoformat()
        })
        self.save()

    def set_profile(self, profile: dict):
        self.data["psychological_profile"] = profile
        self.save()

    def set_patterns(self, patterns: list):
        self.data["behavioral_patterns"] = patterns
        self.save()

    def add_prediction(self, prediction: dict):
        self.data["predictions"].append({
            **prediction,
            "timestamp": datetime.now().isoformat()
        })
        self.save()

    def add_intervention(self, situation: str, response: str):
        self.data["interventions"].append({
            "situation": situation,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
        self.save()

    def add_conversation_turn(self, role: str, content: str):
        self.data["conversation_history"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self.save()

    def get_all_raw_text(self) -> str:
        return "\n\n---\n\n".join(
            f"[{e['source']} | {e['timestamp'][:10]}]\n{e['text']}"
            for e in self.data["raw_entries"]
        )

    def get_profile_summary(self) -> str:
        p = self.data["psychological_profile"]
        if not p:
            return "No profile built yet. Run: python main.py analyze"
        return json.dumps(p, indent=2)

    def get_patterns_summary(self) -> str:
        patterns = self.data["behavioral_patterns"]
        if not patterns:
            return "No patterns detected yet."
        return "\n".join(f"- {p}" for p in patterns)

    def get_predictions_summary(self) -> str:
        preds = self.data["predictions"]
        if not preds:
            return "No predictions generated yet."
        return json.dumps(preds[-1], indent=2) if preds else ""

    def get_conversation_history(self) -> list:
        return [
            {"role": t["role"], "content": t["content"]}
            for t in self.data["conversation_history"]
        ]

    def has_data(self) -> bool:
        return len(self.data["raw_entries"]) > 0

    def has_profile(self) -> bool:
        return bool(self.data["psychological_profile"])
