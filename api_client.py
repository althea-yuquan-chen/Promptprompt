# prevent freezing on Windows
import mimetypes
# Forcefully patch to bypass Windows registry initialization issue causing hangs
mimetypes.MimeTypes.read_windows_registry = lambda self, strict=True: None

import os
from dotenv import load_dotenv
# from openai import OpenAI
# from anthropic import Anthropic
import google.generativeai as genai
from groq import Groq

# Load environment variables from the .env file
# Gemini and Groq are free with no bug, while OpenAI and Claude haven't been tested
load_dotenv()

class ModelConnector:
    def __init__(self):
        """
        Initialize the connector and load API keys from environment variables.
        """
        # # Initialize OpenAI client
        # self.openai_api_key = os.getenv("OPENAI_API_KEY")
        # if self.openai_api_key:
        #     self.openai_client = OpenAI(api_key=self.openai_api_key)
        # else:
        #     print("Warning: OPENAI_API_KEY not found in environment.")
        #     self.openai_client = None

        # # Initialize Claude (Anthropic) client
        # self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        # if self.anthropic_api_key:
        #     self.anthropic_client = Anthropic(api_key=self.anthropic_api_key)
        # else:
        #     print("Warning: ANTHROPIC_API_KEY not found in environment.")
        #     self.anthropic_client = None

        # Initialize Gemini
        # self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        # if self.gemini_api_key:
        #     genai.configure(api_key=self.gemini_api_key)
        #     self.gemini_available = True
        # else:
        #     print("Warning: GEMINI_API_KEY not found. Free tier unavailable.")
        #     self.gemini_available = False

        # Initialize Groq
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        if self.groq_api_key:
            self.groq_client = Groq(api_key=self.groq_api_key)
        else:
            print("Warning: GROQ_API_KEY not found.")
            self.groq_client = None


    # Using Groq to send message
    def send_message(self, message, history=None):
        """
        Adapter method to match the interface expected by optimizer.py
        Expects: message (str)
        Returns: dict {"content": str}
        """
        # We use Groq (Llama 3.3) as the default engine for the optimizer
        # because it is fast and smart.
        response_text = self.chat_with_groq(message)
        
        # Optimizer expects a dictionary, not just a string
        return {"content": response_text}



    def chat_with_gemini(self, prompt, model="gemini-2.5-pro"):
        """
        Call the Google Gemini API (Free).
        Args:
            prompt (str): User input
            model (str): check all models by using
                import pprint
                for model in genai.list_models():
                    pprint.pprint(model)
        """
        if not self.gemini_available:
            return "Error: Gemini API key not configured."
        
        try:
            model_instance = genai.GenerativeModel(model)
            response = model_instance.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Gemini API Error: {str(e)}"
        
    def chat_with_groq(self, prompt, model="llama-3.3-70b-versatile"):
        """
        Call Groq API (Running Llama 3).
        
        Args:
            prompt (str): User input.
            model (str): ""llama-3.3-70b-versatile"
        """
        if not self.groq_client:
            return "Error: Groq client not initialized."

        try:
            response = self.groq_client.chat.completions.create(
                messages=[
                    {"role": "user", "content": prompt}
                ],
                model=model,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Groq API Error: {str(e)}"
        
    def chat_with_gpt(self, prompt, model="gpt-4o"):
        """
        Call the ChatGPT API.
        
        Args:
            prompt (str): The user input message.
            model (str): The model version to use (default: gpt-4o).
            
        Returns:
            str: The response text from the model or an error message.
        """
        if not self.openai_client:
            return "Error: OpenAI client not initialized."

        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI API Error: {str(e)}"

    def chat_with_claude(self, prompt, model="claude-3-5-sonnet-20240620"):
        """
        Call the Claude API.
        
        Args:
            prompt (str): The user input message.
            model (str): The model version to use.
            
        Returns:
            str: The response text from the model or an error message.
        """
        if not self.anthropic_client:
            return "Error: Anthropic client not initialized."

        try:
            response = self.anthropic_client.messages.create(
                model=model,
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            return f"Anthropic API Error: {str(e)}"


# --- Test Code (Executes only when running this file directly) ---
if __name__ == "__main__":
    connector = ModelConnector()
    
    # print("--- Testing ChatGPT ---")
    # gpt_reply = connector.chat_with_gpt("Hello GPT, say hi!")
    # print(f"GPT: {gpt_reply}\n")

    # print("--- Testing Claude ---")
    # claude_reply = connector.chat_with_claude("Hello Claude, say hi!")
    # print(f"Claude: {claude_reply}")

    print("--- Testing Free Gemini API ---")
    print(connector.chat_with_gemini("Hello! Please introduce yourself in one sentence."))

    print("\n--- Testing Groq (Fastest) ---")
    print(connector.chat_with_groq("Hello Groq! Why are you so fast?"))