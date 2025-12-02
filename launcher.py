# Citation: I used claudeAI to learn the subprocess and shutil imports,
# custom error handling, aichat, and general debugging.

# Launcher.py is responsible for launching the external chat tool (Claude, Gemini, GPT-4, or Codex)
# with the user's optimized prompt after PromptPrompt finished processing

import subprocess       # Built-in python module for running external programs
import shutil           # Built-in python module for shell utilities (check if aichat is installed)

# Try to import the custom LauncherError from the exceptions.py file
try:
    from exceptions import LauncherError
except ImportError:
    # Fallback if exceptions.py doesn't exist yet
    class LauncherError(Exception):
        pass

class ChatLauncher:
    # Map of model names to their CLI commands
    TOOL_COMMANDS = {
        "claude": ["claude"],  # Assumes 'claude' CLI is installed
        "gemini": ["gcloud", "ai", "models", "predict", "--model=gemini-pro"],
        "gpt-4": ["openai", "api", "chat.completions.create", "-m", "gpt-4", "-g", "user"],
        "codex": ["openai", "api", "completions.create", "-m", "code-davinci-002"],
    }

    # Launches external chat tool (aichat) with optimized prompt
    def __init__(self, default_model="claude"):
        # Initialize with chat tool name (default: claude)
        self.default_model = default_model
        self.chat_tool = self._get_tool_for_model(default_model)

    def _get_tool_for_model(self, model):
        """Get the base CLI tool for a given model"""
        if model == "claude":
            return "claude"
        elif model == "gemini":
            return "gcloud"
        elif model in ["gpt-4", "codex"]:
            return "openai"
        else:
            raise LauncherError(f"Unknown model: {model}")

    def check_installed(self):
        # Check if the chat tool is installed and available in PATH
        # shutil.which() searches for a program in your system's PATH.
        # Returns the full path if found, None if not found
        return shutil.which(self.chat_tool) is not None

    def launch(self, optimized_prompt, model=None):
        # Launch the appropriate chat tool with the optimized prompt
        use_model = model if model else self.default_model

        # Check if tool is installed
        tool = self._get_tool_for_model(use_model)
        if not shutil.which(tool):
            raise LauncherError(
                f"{tool} is not installed. "
                f"Install instructions: {self._get_install_instructions(tool)}"
            )

        # Get the command for this model
        if use_model not in self.TOOL_COMMANDS:
            raise LauncherError(f"Model '{use_model}' not supported")

        # Build the full command
        command = self.TOOL_COMMANDS[use_model].copy()

        # Add the prompt based on the tool
        if use_model == "claude":
            command.append(optimized_prompt)
        elif use_model == "gemini":
            command.append(f'--prompt={optimized_prompt}')
        elif use_model in ["gpt-4", "codex"]:
            command.append(optimized_prompt)

        # Run the command
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            raise LauncherError(f"Failed to launch {use_model}: {e}")

    def _get_install_instructions(self, tool):
        # Get installation instructions for each tool
        instructions = {
            "claude": "Visit https://claude.ai/download for CLI installation",
            "gcloud": "Install gcloud: https://cloud.google.com/sdk/docs/install",
            "openai": "Install with: pip install openai",
        }
        return instructions.get(tool, "Check the tool's documentation")

# Test if tools is installed
if __name__ == "__main__":
    launcher = ChatLauncher()

    # Test if the tool is installed
    if launcher.check_installed():
        print(f"{launcher.chat_tool} is installed!")
    else:
        print(f"{launcher.chat_tool} is not installed")
        print(launcher._get_install_instructions(launcher.chat_tool))
