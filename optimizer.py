# optimizer.py
from pathlib import Path
from typing import List, Dict

class OptimizationError(Exception):
    """Raised when prompt optimization fails"""
    pass

class PromptOptimizer:
    """Optimizes prompts using AI with conversation context"""

    def __init__(self, api_client):
        """
        Initialize optimizer with API client

        Args:
            api_client: An instance of LLM
        """
        self.api_client = api_client
        self.conversation_history = []

        # Path to prompts directory
        self.prompts_dir = Path(__file__).parent / "prompts"

        # Load reusable parts once at initialization
        self.system_prompt = self._load_prompt("system.txt")
        self.prompting_practices = self._load_prompt("prompting_practices.txt")

    def _load_prompt(self, filename: str) -> str:
        """
        Load a prompt template from file

        Args:
            filename: Name of the prompt file

        Returns:
            Prompt text as string
        """
        prompt_file = self.prompts_dir / filename

        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            raise OptimizationError(f"Prompt file not found: {filename}")
        except Exception as e:
            raise OptimizationError(f"Error loading prompt: {e}")

    def clarify(self, draft_prompt: str) -> List[str]:
        """
        Generate clrifying questions for a draft prompt (STEP 2)

        Args:
            draft_prompt: The user's original prompt

        Returns:
            List of clarifying questions
        """
        task_instruction = self._load_prompt("task_generate_questions.txt")

        # Build message: System prompt + instructions
        message = f"{self.system_prompt}\n\n{task_instruction}".format(
            draft_prompt=draft_prompt
        )

        # First API call
        response = self.api_client.send_message(message)

        # Save to conversation history for context
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        self.conversation_history.append({
            "role": "assistant",
            "content": response["content"]
        })

        # Parse questions from response
        # Helpd with claude ai
        questions = [q.strip() for q in response["content"].strip().split("\n") if q.strip()]

        return questions

    def generate_optimized_prompt(self, draft_prompt: str, questions: List[str], answers: List[str]) -> str:
        """
        Generate optimized prompt based on user answers (STEPS 3-5)

        Args:
            draft_prompt: Original prompt
            questions: Questions that were asked
            answers: User's answers

        Returns:
            Optimized prompt as a string
        """
        # Load task instruction for optimization
        task_instruction = self._load_prompt("task_optimize.txt")

        # Build Q&A pairs
        #Help of claude ai
        qa_pairs = "\n".join([
            f"Q{i+1}: {q}\nA{i+1}: {a}"
            for i, (q, a) in enumerate(zip(questions, answers))
        ])

        # Build message: Practices + Task + Context
        #help of claude AI
        message = (
            f"PROMPTING PRACTICES\n"
            f"{self.prompting_practices}\n"
            f"END PRACTICES-\n\n"
            f"{task_instruction}\n\n"
            f"Original draft prompt: {draft_prompt}\n\n"
            f"Clarifying Questions & Answers:\n{qa_pairs}"
        )

        # Second API call WITH conversation history
        response = self.api_client.send_message(
            message,
            self.conversation_history
        )

        # Save to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        self.conversation_history.append({
            "role": "assistant",
            "content": response["content"]
        })

        return response["content"].strip()
