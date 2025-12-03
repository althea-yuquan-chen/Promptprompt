import sys
import os
from getpass import getpass
from dotenv import load_dotenv

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
    gemini_key = os.getenv("GEMINI_API_KEY")

    # If keys already exist, skip the setup process
    if groq_key or gemini_key:
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

    # 2. Get Gemini Key (Optional)
    # print("\nPlease enter your Google Gemini API Key (Optional):")
    # print("Get key here: https://aistudio.google.com/app/apikey")
    # new_gemini = getpass("Gemini Key (Press Enter to skip): ").strip()

    # if new_gemini:
    #     with open(ENV_PATH, "a") as f:
    #         f.write(f"\nGEMINI_API_KEY={new_gemini}")
    #     print("✓ Gemini Key saved.")

    # print("\n[Setup Complete] Starting system...\n")
    
    # Reload again to ensure the program reads the newly written keys immediately
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

    # # --- STEP 2: User Authentication ---
    # auth = UserAuth()
    # current_user = None
    
    # while not current_user:
    #     print("\n--- Authentication Required ---")
    #     print("1. Login")
    #     print("2. Register")
    #     print("3. Exit")
    #     choice = input("Select an option (1-3): ").strip()
        
    #     if choice == '1':
    #         user = input("Username: ")
    #         pwd = getpass("Password: ") 
    #         if auth.login_user(user, pwd):
    #             current_user = user
    #     elif choice == '2':
    #         user = input("New Username: ")
    #         pwd = getpass("New Password: ")
    #         if auth.register_user(user, pwd):
    #             print("Registration successful! Please login.")
    #     elif choice == '3':
    #         print("Exiting system. Goodbye!")
    #         sys.exit(0)
    #     else:
    #         print("Invalid choice, please try again.")

    # print(f"\n[System] Welcome, {current_user}!")

    # --- STEP 3: Initialize Business Logic (Optimizer) ---
    print("[System] Loading Optimizer Logic...")
    try:
        # Pass the initialized API client to the optimizer
        optimizer = PromptOptimizer(api_client=api)
        storage = Storage()
        # launcher = ChatLauncher()
        launcher = weblauncher.WebLauncher()
    except Exception as e:
        print(f"[Error] Failed to initialize optimizer: {e}")
        # print("Hint: Ensure you have a 'prompts' folder with .txt files.")
        sys.exit(1)

    # --- STEP 4: Launch the CLI (View) ---
    print("[System] Launching User Interface...\n")
    try:
        # Pass the optimizer to the CLI
        cli_app = CLI(optimizer=optimizer, storage=storage, launcher=launcher)
        cli_app.run()
    except KeyboardInterrupt:
        print("\n[System] Program interrupted by user.")
    except Exception as e:
        print(f"\n[Error] An unexpected error occurred in the CLI: {e}")

if __name__ == "__main__":
    main()