import webbrowser
import time
import platform
import sys

# Try to import required libraries
try:
    import pyperclip
    import pyautogui
except ImportError:
    print("[Error] Missing libraries. Please run: pip install pyperclip pyautogui")
    sys.exit(1)

class WebLauncher:
    """
    Handles opening the web browser and automating the prompt insertion.
    """
    def __init__(self):
        # You can change this to "https://gemini.google.com/app" if you prefer
        self.target_url = "https://chatgpt.com/"

    def launch(self, prompt):
        """
        Opens the default web browser to the AI page, copies the prompt 
        to the clipboard, and attempts to paste it automatically.

        Args:
            prompt (str): The optimized prompt text to send.
        """
        print(f"\n[Launcher] Preparing to launch web session...")

        # 1. Copy prompt to clipboard
        # This is the fail-safe. If automation fails, user can just press Ctrl+V manually.
        try:
            pyperclip.copy(prompt)
            print("[Launcher] Prompt copied to system clipboard.")
        except Exception as e:
            print(f"[Launcher] Warning: Could not copy to clipboard: {e}")

        # 2. Open the Web Browser
        print(f"[Launcher] Opening {self.target_url} in Default Browser...")
        webbrowser.open(self.target_url)

        # 3. Wait for the browser to load
        # We need to give the browser enough time to open and render the text box.
        # 5 seconds is usually safe.
        print("[Launcher] Waiting for page to load...")
        time.sleep(2)

        # 4. Simulate Keyboard Input (Auto-Paste)
        print("[Launcher] Automating input...")

        try:
            # Determine the control key based on OS (Command for Mac, Ctrl for Windows)
            ctrl_key = 'command' if platform.system() == 'Darwin' else 'ctrl'

            # Simulate pressing Ctrl+V (or Cmd+V)
            pyautogui.hotkey(ctrl_key, 'v')
            
            # Wait a split second
            time.sleep(1)
            
            # Pressing Enter to send 
            pyautogui.press('enter')
            
            print("[Launcher] Prompt pasted successfully!")
            
        except Exception as e:
            print(f"[Launcher] Automation error: {e}")
            print("[Launcher] Please paste the prompt manually (Ctrl+V).")

# --- Test Code ---
if __name__ == "__main__":
    launcher = WebLauncher()
    test_prompt = "Hello AI, this is a test prompt from Python."
    launcher.launch(test_prompt)