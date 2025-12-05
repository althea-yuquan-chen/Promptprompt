# PromptPrompt: AI-Powered Prompt Optimizer

**PromptPrompt** is an intelligent command-line tool designed to help users refine vague ideas into high-quality, engineered prompts for LLMs (like ChatGPT, Claude, or Gemini).

Instead of guessing how to write a good prompt, PromptPrompt acts as a consultant: it asks you clarifying questions, optimizes your request based on best practices, and automatically launches the refined prompt in your web browser.

## 🚀 Key Features

* **LLM Support**: Connects to **Groq** (Llama 3.3) for ultra-fast reasoning.
* **Interactive Refinement**: Uses an AI "Optimizer" to analyze your draft and ask clarifying questions (Target Audience, Tone, Context).
* **Rich CLI Interface**: Beautiful terminal UI powered by the `rich` library.
* **Auto-Launch**: Automatically opens your default browser (e.g., ChatGPT) and pastes the optimized prompt for immediate use.
* **History Storage**: Saves all optimized prompts locally for future reference.

## 📂 Project Structure

Here is an overview of the file organization:

```text
Promptprompt/
├── main.py                  # [Entry Point] Orchestrates the entire application flow.
├── api_client.py            # Handles API connections (Groq in use, Gemini, OpenAI, Anthropic also supported if you have the API key).
├── cli.py                   # User Interface - Handles inputs, display, and interaction loops.
├── optimizer.py             # Core Logic - Generates clarifying questions and optimizes text.
├── weblauncher.py           # Automation - Opens browser and auto-pastes prompts.
├── storage.py               # Saves prompt history to local txt files.
├── requirements.txt         # List of Python dependencies.
└── prompts/                 # System Instruction Templates
    ├── system.txt                   # The persona for the AI Optimizer.
    ├── prompting_practices.txt      # Best practices injected into the optimization context.
    ├── task_generate_questions.txt  # Instruction for Step 2 (Clarification).
    └── task_optimize.txt            # Instruction for Step 3 (Final Optimization).
```

## ⚙️ Configuration (First Run)

You do not need to manually create config files. The system handles this automatically.

Simply run the program (see Usage below).

On the first launch, the system will detect if API keys are missing.

It will interactively ask for your Groq API Key or Gemini API Key.

It will automatically generate a secure .env file locally.

## 🖥️ Usage

To start the application, simply install dependencies and run the main.py file from your terminal:
```text
pip install -r requirements.txt
python main.py
```

**The Workflow:**

**1. Draft Input:** Enter a rough idea (e.g., "Write an email to my boss about a raise").

**2. Clarification:** The AI will ask you 3-4 specific questions to understand your context (e.g., "What specific achievements should we highlight?").

**3. Optimization:** The system generates a polished, professional prompt based on prompt engineering best practices.

**4. Approval:** You can approve the result or ask for further refinements (e.g., "Make it more polite").

**5. Launch:** Once approved, the tool automatically opens your default browser (e.g., ChatGPT) and pastes the optimized prompt for immediate use.

## Citations:
1. Seongsu used claudeAI to walk me through how to use rich library, the ordering of the methods, and general debugging.
2. Jennifer used OpenAI ChatGPT to refine and to suggest approaches for token counting and ROI-related token metrics.
## Data Sources Used in This Project:
- User-generated prompts (direct CLI input)
- Groq API model outputs:
     openai/gpt-oss-20b
     llama-3.3-70b-versatile

## Other sources used:
# - https://jilltxt.net/llms-fail-at-70-of-simple-office-tasks/#:~:text=The%20code%20is%20on%20Github,and%20autonomously%20automate%20repetitive%20tasks.
# - https://fortune.com/2025/07/20/ai-hampers-productivity-software-developers-productivity-study/
