# still need to check，not final version
import os
import json
from datetime import datetime

class StorageError(Exception):
    """Custom error for storage failures."""
    pass


class PromptStorage:
    """
    Handles saving optimized + original prompts into the user's local machine.
    Directory: ~/.promptprompt/prompts/
    """

    def __init__(self, base_dir=None):
        # Default directory: ~/.promptprompt/prompts/
        self.base_dir = base_dir or os.path.expanduser("~/.promptprompt/prompts/")
        try:
            os.makedirs(self.base_dir, exist_ok=True)
        except Exception as e:
            raise StorageError(f"Failed to create storage directory: {e}")

    def save_prompts(self, prompt_pair):
        """
        Save the prompts to a timestamped JSON file.

        prompt_pair = {
            "original": "...",
            "optimized": "...",
            "timestamp": "2025-01-01T12:00:00"
        }
        """

        if not isinstance(prompt_pair, dict):
            raise StorageError("Invalid prompt data. Expected dict.")

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"prompt_{timestamp}.json"
        file_path = os.path.join(self.base_dir, filename)

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(prompt_pair, f, ensure_ascii=False, indent=4)
        except Exception as e:
            raise StorageError(f"Failed to write prompt file: {e}")

        return file_path


# Manual test
if __name__ == "__main__":
    storage = PromptStorage()
    test_data = {
        "original": "Write a poem about AI.",
        "optimized": "Write a detailed poem about AI in a humorous tone.",
        "timestamp": datetime.now().isoformat()
    }
    path = storage.save_prompts(test_data)
    print("Saved to:", path)
