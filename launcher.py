# Citation: I used claudeAI to learn the subprocess and shutil imports,
# custom error handling, aichat, and general debugging.

# Launcher.py is responsible for launching the external chat tool (aichat) with the
# user's optimized prompt after PromptPrompt finished processing

import subprocess       # Built-in python module for running external programs
import shutil           # Built-in python module for shell utilities (check if aichat is installed)

# Try to import the custom LauncherError from the exceptions.py file
try:
    from promptprompt.exceptions import LauncherError
except ImportError:
    # Fallback if exceptions.py doesn't exist yet
    class LauncherError(Exception):
        pass

class ChatLauncher:
    # Launches external chat tool (aichat) with optimized prompt
    def __init__(self, chat_tool="aichat"):
        # Initialize with chat tool name (default: aichat)
        self.chat_tool = chat_tool

    def check_installed(self):
        # Check if the chat tool is installed and available in PATH
        # shutil.which() searches for a program in your system's PATH.
        # Returns the full path if found, None if not found
        return shutil.which(self.chat_tool) is not None

    def launch(self, optimized_prompt):
        # Launch the chat tool with the optimized prompt
        # Need to check if installed first
        if not self.check_installed():
            raise LauncherError(f"{self.chat_tool} is not installed. Install it first.")

        # Build the command
        # Like typing in terminal: "aichat -m claude "your prompt"
        command = [
            self.chat_tool,         # "aichat"
            "-m", "claude",         # Use Claude model
            optimized_prompt        # The prompt to send
        ]

        # Run the command
        subprocess.run(command)

# Test if it finds aichat
if __name__ == "__main__":
    launcher = ChatLauncher()

    # Test if aichat is installed
    if launcher.check_installed():
        print("aichat is installed!")
    else:
        print("aichat is not installed")
        print("Install it with: brew install aichat")

