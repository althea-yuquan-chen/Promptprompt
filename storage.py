# still need to check，not final version
import os
from datetime import datetime
from pathlib import Path

class StorageError(Exception):
    pass


class PromptStorage:
    """
    Storage component for PromptPrompt.
    Saves ONE .txt file per session inside ~/.promptprompt/prompts/
    """

    def __init__(self, base_dir=None):
        # Directory: ~/.promptprompt/prompts/
        self.base_dir = Path(base_dir) if base_dir else Path.home() / ".promptprompt" / "prompts"

        try:
            self.base_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise StorageError(f"Failed to create storage directory: {e}")

    def save_prompts(self, prompt_pair: dict) -> Path:
        """
        Saves a session file:
            YYYY-MM-DD-HHMMSS-session.txt
        Returns a Path object.
        """

        # Validate input
        required_keys = {"original", "optimized", "timestamp"}
        if not required_keys.issubset(prompt_pair.keys()):
            raise StorageError("prompt_pair missing required fields")

        # Extract fields
        original = prompt_pair["original"]
        optimized = prompt_pair["optimized"]
        timestamp_str = prompt_pair["timestamp"]

        # Parse timestamp or fallback
        try:
            dt = datetime.fromisoformat(timestamp_str)
        except:
            dt = datetime.now()

        # File name format: 2025-11-28-143022-session.txt
        filename = dt.strftime("%Y-%m-%d-%H%M%S-session.txt")
        file_path = self.base_dir / filename

        # Build text content
        content = (
            "========================================\n"
            "PromptPrompt Session\n"
            f"Date: {dt.strftime('%Y-%m-%d %H:%M:%S')}\n"
            "========================================\n\n"
            "ORIGINAL PROMPT:\n"
            f"{original}\n\n"
            "OPTIMIZED PROMPT:\n"
            f"{optimized}\n"
            "========================================\n"
        )

        try:
            file_path.write_text(content, encoding="utf-8")
        except Exception as e:
            raise StorageError(f"Failed to write file: {e}")

        return file_path


# Manual test
if __name__ == "__main__":
    storage = PromptStorage()
    test_data = {
        "original": "write a blog post",
        "optimized": "Write a 500-word blog post about AI tools...",
        "timestamp": "2025-11-28T14:30:22"
    }
    path = storage.save_prompts(test_data)
    print("Saved to:", path)
