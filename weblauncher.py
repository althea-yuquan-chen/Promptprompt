import webbrowser
import time
import platform
import sys
import subprocess

# Claude AI was used to fic bug in launching claude code and the web browser as well as comments
try:
    import pyperclip
except ImportError:
    print("[Error] Missing libraries. Please run: pip install pyperclip")
    sys.exit(1)

class WebLauncher:
    """
    Handles launching external tools: Claude Code or web browser.
    Simple executor - no config management, no user prompts.
    """

    def __init__(self, use_claude_code=False):
        self.target_url = "https://chatgpt.com/"
        self.use_claude_code = use_claude_code

    def launch(self, prompt, claude_code_path=None):
        """
        Launches either Claude Code in terminal or opens web browser,
        depending on use_claude_code setting.

        Args:
            prompt (str): The optimized prompt text to send.
            claude_code_path (str): Path to Claude Code executable (required if use_claude_code=True).
        """
        if self.use_claude_code:
            if not claude_code_path:
                print("[Launcher] Error: Claude Code path not provided. Falling back to web.")
                self.launch_web(prompt)
            else:
                self.launch_claude_code(prompt, claude_code_path)
        else:
            self.launch_web(prompt)

    def launch_claude_code(self, prompt, claude_code_path):
        """
        Launches Claude Code in the terminal with the optimized prompt.

        Args:
            prompt (str): The optimized prompt text to send.
            claude_code_path (str): Path to Claude Code executable.
        """
        print(f"\n[Launcher] Preparing to launch Claude Code...")

        # Copy prompt to clipboard as backup
        try:
            pyperclip.copy(prompt)
            print("[Launcher] Prompt copied to clipboard as backup.")
        except Exception as e:
            print(f"[Launcher] Warning: Could not copy to clipboard: {e}")

        # Launch Claude Code with the prompt
        try:
            print("[Launcher] Starting Claude Code in terminal...")
            print("[Launcher] Launching: " + " ".join([claude_code_path, "--", prompt[:50] + "..."]))

            # prevents special characters in the prompt from being interpreted as options
            result = subprocess.run([claude_code_path, "--", prompt], check=False)

            if result.returncode == 0:
                print("[Launcher] ✓ Claude Code session completed!")
            else:
                print(f"[Launcher] Claude Code exited with code {result.returncode}")

        except FileNotFoundError as e:
            print(f"[Launcher] ✗ Claude Code not found at: {claude_code_path}")
            print(f"[Launcher] Please update the path in launcher_config.json")
            print("[Launcher] Falling back to web launcher...")
            self.launch_web(prompt)
        except Exception as e:
            print(f"[Launcher] ✗ Error launching Claude Code: {e}")
            print("[Launcher] Falling back to web launcher...")
            self.launch_web(prompt)

    def launch_web(self, prompt):
        """
        Opens the default web browser to the AI page.
        Simple, bulletproof approach: copy to clipboard + print to terminal.

        Args:
            prompt (str): The optimized prompt text to send.
        """
        print(f"\n[Launcher] Preparing to launch web session...")

        # Determine paste shortcut based on OS
        paste_key = 'Cmd+V' if platform.system() == 'Darwin' else 'Ctrl+V'

        # 1. Try to copy to clipboard (best effort)
        clipboard_success = False
        try:
            pyperclip.copy(prompt)
            clipboard_success = True
            print(f"[Launcher] ✓ Prompt copied to clipboard!")
        except Exception as e:
            print(f"[Launcher] ✗ Could not copy to clipboard: {e}")

        # 2. Print prompt to terminal in a nice box
        print("\n" + "="*70)
        print(" "*20 + "YOUR OPTIMIZED PROMPT")
        print("="*70)
        print(prompt)
        print("="*70)

        # 3. Show clear instructions
        print("\n📋 INSTRUCTIONS:")
        if clipboard_success:
            print(f"  1. Your prompt is copied to clipboard")
            print(f"  2. Browser is opening to {self.target_url}")
            print(f"  3. Press {paste_key} to paste your prompt")
        else:
            print(f"  1. Select and copy the prompt above (from the terminal)")
            print(f"  2. Browser is opening to {self.target_url}")
            print(f"  3. Paste it into the chat box")

        # 4. Open the browser
        print(f"\n[Launcher] Opening browser...")
        webbrowser.open(self.target_url)
        print(f"[Launcher] ✓ Browser opened!")

        print("\n" + "="*70)

# --- Test Code ---
if __name__ == "__main__":
    launcher = WebLauncher()
    test_prompt = "Hello AI, this is a test prompt from Python."
    launcher.launch(test_prompt)
