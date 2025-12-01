import sys
import os
from getpass import getpass

from api_client import ModelConnector
from user_auth import UserAuth
# Ensure you have installed 'rich': pip install rich
from cli import CLI
from optimizer import PromptOptimizer


# Just a framework of Main
def main():
    print("\n" + "="*50)
    print("   PROMPT PROMPT SYSTEM STARTUP   ")
    print("="*50 + "\n")
    
    # --- STEP 1: Initialize API Connection ---
    print("[System] Initializing AI Models...")
    try:
        api = ModelConnector()
        # Verify if at least one model is available
        if not api.groq_client and not api.gemini_available:
            print("[Error] No API keys found. Please check your .env file.")
            sys.exit(1)
        print("[System] AI Models Connected.")
    except Exception as e:
        print(f"[Critical Error] Failed to connect to AI models: {e}")
        sys.exit(1)

    # --- STEP 2: User Authentication ---
    auth = UserAuth()
    current_user = None
    
    while not current_user:
        print("\n--- Authentication Required ---")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Select an option (1-3): ").strip()
        
        if choice == '1':
            user = input("Username: ")
            pwd = getpass("Password: ") # getpass hides the input
            if auth.login_user(user, pwd):
                current_user = user
        elif choice == '2':
            user = input("New Username: ")
            pwd = getpass("New Password: ")
            if auth.register_user(user, pwd):
                print("Registration successful! Please login.")
        elif choice == '3':
            print("Exiting system. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice, please try again.")

    print(f"\n[System] Welcome, {current_user}!")

    # --- STEP 3: Initialize Business Logic (Optimizer) ---
    # pass the 'api' object into the 'PromptOptimizer'
    print("[System] Loading Optimizer Logic...")
    try:
        optimizer = PromptOptimizer(api_client=api)
    except Exception as e:
        print(f"[Error] Failed to initialize optimizer: {e}")
        print("Hint: Ensure you have a 'prompts' folder with .txt files (system.txt, etc.)")
        sys.exit(1)

    # --- STEP 4: Launch the CLI (View) ---
    # pass the 'optimizer' object into the 'CLI'
    print("[System] Launching User Interface...\n")
    try:
        cli_app = CLI(optimizer=optimizer)
        cli_app.run()
    except KeyboardInterrupt:
        print("\n[System] Program interrupted by user.")
    except Exception as e:
        print(f"\n[Error] An unexpected error occurred in the CLI: {e}")

if __name__ == "__main__":
    main()