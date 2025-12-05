import mimetypes
# Forcefully patch to bypass Windows registry initialization issue causing hangs
mimetypes.MimeTypes.read_windows_registry = lambda self, strict=True: None

import os
from dotenv import load_dotenv
from groq import Groq
load_dotenv()

class ModelConnector:
    def __init__(self):
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
        # We use Groq as the default engine for the optimizer
        # because it is fast and smart.
        response_text = self.chat_with_groq(message)
        
        # Optimizer expects a dictionary, not just a string
        return {"content": response_text}

        
    def chat_with_groq(self, prompt, model="openai/gpt-oss-20b"):
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

if __name__ == "__main__":
    connector = ModelConnector()

    print("\n--- Testing Groq (Fastest) ---")
    print(connector.chat_with_groq("Hello Groq! Why are you so fast?"))