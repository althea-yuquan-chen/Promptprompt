import sys
import os
from getpass import getpass
from dotenv import load_dotenv
import shutil

# Import your modules
from api_client import ModelConnector
# from user_auth import UserAuth
from cli import CLI
from optimizer import PromptOptimizer
# from launcher import ChatLauncher
from storage import Storage
import weblauncher

# Path to the environment configuration file
ENV_PATH = ".env"

def setup_api_keys():
    """
    Check if API keys exist in the environment variables.
    If not, prompt the user to input them and save to the .env file.
    """
    # Force reload environment variables (in case they were just updated)
    load_dotenv(ENV_PATH, override=True)

    # Check if core keys exist (Using Groq as the example since it's mandatory/default)
    groq_key = os.getenv("GROQ_API_KEY")

    if groq_key :
        return

    print("\n" + "="*60)
    print("   First Time Setup   ")
    print("   No API keys detected. Please configure them now.")
    print("   (Keys will be securely saved to the local .env file)")
    print("="*60 + "\n")

    # 1. Get Groq Key (Mandatory)
    print("Please enter your Groq API Key (Recommended, Fast & Free):")
    print("Get key here: https://console.groq.com/keys")
    new_groq = getpass("Groq Key (Input hidden): ").strip()
    
    if new_groq:
        # Append to .env file
        with open(ENV_PATH, "a") as f:
            f.write(f"\nGROQ_API_KEY={new_groq}")
        print("✓ Groq Key saved.")
    load_dotenv(ENV_PATH, override=True)

def main():
    print("\n" + "*"*50)
    print("   PROMPT PROMPT SYSTEM STARTUP   ")
    print("*"*50 + "\n")
    
    # --- STEP 0: Check & Ask for API Keys ---
    setup_api_keys()

    # --- STEP 1: Initialize API Connection ---
    print("[System] Initializing AI Models...")
    try:
        # This re-reads the environment variables
        api = ModelConnector()
        
        # Verify connection success
        if not api.groq_client and not api.gemini_available:
            print("[Error] No valid API keys found.")
            print("Please check the .env file or delete it to re-run setup.")
            sys.exit(1)
            
        print("[System] AI Models Connected.")
    except Exception as e:
        print(f"[Critical Error] Failed to connect to AI models: {e}")
        sys.exit(1)

    # --- STEP 2: Initialize Business Logic (Optimizer) ---
    print("[System] Loading Optimizer Logic...")
    try:
        # Pass the initialized API client to the optimizer
        optimizer = PromptOptimizer(api_client=api)
        storage = Storage()
        # launcher = ChatLauncher()
        launcher = weblauncher.WebLauncher(use_claude_code=True)
    except Exception as e:
        print(f"[Error] Failed to initialize optimizer: {e}")
        # print("Hint: Ensure you have a 'prompts' folder with .txt files.")
        sys.exit(1)

    # --- STEP 3: Get Claude Code path ---
    claude_code_path = None
    if launcher.use_claude_code:
        # Load config to check for saved path
        config = storage.load_config()
        claude_code_path = config.get("claude_code_path")

        # If not in config, check if it's in PATH
        if not claude_code_path:
            if shutil.which("claude"):
                claude_code_path = "claude"
                # Save to config for future use
                config["claude_code_path"] = claude_code_path
                storage.save_config(config)
            # If not in PATH either, CLI will prompt user later

    # --- STEP 4: Launch the CLI (View) ---/
    print("[System] Launching User Interface...\n")
    try:
        # Pass the optimizer to the CLI
        cli_app = CLI(optimizer=optimizer, storage=storage, launcher=launcher)

        # If Claude Code enabled but no path found, prompt user
        if launcher.use_claude_code and not claude_code_path:
            claude_code_path = cli_app.get_claude_code_path()
            if claude_code_path:
                # Save to config
                config = storage.load_config()
                config["claude_code_path"] = claude_code_path
                storage.save_config(config)

        cli_app.run(claude_code_path=claude_code_path)
    except KeyboardInterrupt:
        print("\n[System] Program interrupted by user.")
    except Exception as e:
        print(f"\n[Error] An unexpe1cted error occurred in the CLI: {e}")

if __name__ == "__main__":
    main()