
from pathlib import Path
from datetime import datetime

try:
    from promptprompt.exceptions import StorageError
except ImportError:

    class StorageError(Exception):
        """Fallback StorageError used when promptprompt.exceptions is unavailable."""
        pass


class Storage:
    """
    Storage component for PromptPrompt.
    Saves ONE .txt file per session inside ~/.promptprompt/prompts/
    """

    def __init__(self, base_dir: Path | None = None):
        """
        Initialize storage directory.

        Args:
            base_dir: Optional base directory override, mainly for testing.
                      Defaults to ~/.promptprompt/prompts/
        """
        if base_dir is None:
            # base_dir = Path.home() / ".promptprompt" / "prompts"
            base_dir = Path(__file__).parent / "prompts" / "optimized prompts"

        self.base_dir = Path(base_dir)

        try:
            # Create directory if it doesn't exist
            self.base_dir.mkdir(parents=True, exist_ok=True)
        except Exception as exc:
            raise StorageError(f"Failed to create storage directory: {exc}") from exc

    def save_prompts(self, prompt_pair: dict) -> Path:
        """
        Saves a session file:
            YYYY-MM-DD-HHMMSS-session.txt

        File contents format:

        ========================================
        PromptPrompt Session
        Date: YYYY-MM-DD HH:MM:SS
        ========================================

        ORIGINAL PROMPT:
        ...

        OPTIMIZED PROMPT:
        ...
        ========================================

        Args:
            prompt_pair: dict with keys:
                - "original": original prompt (str-like)
                - "optimized": optimized prompt (str-like)
                - "timestamp": ISO-8601 timestamp string

        Returns:
            Path: path to the saved file.
        """

        required_keys = {"original", "optimized", "timestamp"}
        if not required_keys.issubset(prompt_pair):
            missing = required_keys - set(prompt_pair)
            raise StorageError(
                f"prompt_pair missing required fields: {', '.join(sorted(missing))}"
            )

        original = str(prompt_pair["original"])
        optimized = str(prompt_pair["optimized"])
        timestamp_str = str(prompt_pair["timestamp"])

        try:
            dt = datetime.fromisoformat(timestamp_str)
        except Exception:
            dt = datetime.now()

        # File name format: 2025-11-28-143022-session.txt
        filename = dt.strftime("%Y-%m-%d-%H%M%S-session.txt")
        file_path = self.base_dir / filename

        content_lines = [
            "========================================",
            "PromptPrompt Session",
            f"Date: {dt.strftime('%Y-%m-%d %H:%M:%S')}",
            "========================================",
            "",
            "ORIGINAL PROMPT:",
            original,
            "",
            "OPTIMIZED PROMPT:",
            optimized,
            "========================================",
            "",
        ]
        content = "\n".join(content_lines)

        # Write to file
        try:
            file_path.write_text(content, encoding="utf-8")
        except Exception as exc:
            raise StorageError(f"Failed to write file: {exc}") from exc

        return file_path


# manual test
if __name__ == "__main__":
    storage = Storage()
    test_data = {
        "original": "write a blog post",
        "optimized": "Write a 500-word blog post about AI tools...",
        "timestamp": "2025-11-28T14:30:22",
    }
    path = storage.save_prompts(test_data)
    print("Saved to:", path)
