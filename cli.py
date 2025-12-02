# Citation: I used claudeAI to walk me through how to use rich library, the ordering
# of the methods, and general debugging.

# Bring in the Console class from the rich library
from rich.console import Console
from rich.panel import Panel
from datetime import datetime
from launcher import ChatLauncher

class CLI:
    # Console manager class for I/O - handles all user interaction

    def __init__(self, optimizer, storage, launcher): #need to add the hashed parameters below later
        # This runs when you create a CLI object
        self.console = Console()
        # self.config = config
        self.optimizer = optimizer
        self.storage = storage
        self.launcher = launcher
        self.console.print("[bold blue] CLI Initialized![/bold blue]")

    def get_ai_choice(self):
        #Ask user which AI tool they want to use
        self.console.print("\n[bold cyan]Which AI tool would you like to use?[/bold cyan]")
        self.console.print("  1. Claude")
        self.console.print("  2. Gemini")
        self.console.print("  3. GPT-4")
        self.console.print("  4. Codex")

        choice = input("\nEnter your choice (1-4): ").strip()

        model_map = {
            "1": "claude",
            "2": "gemini",
            "3": "gpt-4",
            "4": "codex"
        }

        while choice not in model_map:
            self.console.print("[red]Please enter 1, 2, 3, or 4[/red]")
            choice = input("Enter your choice (1-4): ").strip()

        return model_map[choice]

    def run(self, draft_prompt=None):
        # Main method - this is what starts everything
        self.console.print("[bold magenta] Welcome to PromptPrompt! [/bold magenta]")

        # Ask user which AI tool first
        model_choice = self.get_ai_choice()
        self.console.print(f"\n[green]✓ Selected: {model_choice.upper()}[/green]")

        # Create launcher with their choice
        self.launcher = ChatLauncher(default_model=model_choice)

        # Get the draft prompt (either from parameter or ask user)
        if draft_prompt is None:
            draft_prompt = self.get_draft_prompt()

        # Generate questions from optimizer
        questions = self.optimizer.clarify(draft_prompt)
        # These are the hard-coded questions to test for now. Will remove during integration:
        # questions = [
        #     "What is the main topic?",
        #     "Who is your target audience?",
        #     "What tone should it have?"
        # ]

        # Ask questions
        answers = self.collect_answers(questions)

        # Refinement loop - keep improving until user approves
        improved_prompt = self.refinement_loop(draft_prompt, questions, answers)

        # User approved if we get here
        self.console.print("\n[bold green] Prompt Approved! Moving forward...[/bold green]")

        # Save prompts
        self.console.print("\n Saving prompts...")
        prompt_pair = {
            "original": draft_prompt,
            "optimized": improved_prompt,
            "timestamp": datetime.now().isoformat()
        }
        file_path = self.storage.save_prompts(prompt_pair)
        self.console.print(f"✓ Saved to: {file_path}")

        # Launch AI Session
        #* self.launcher.launch(improved_prompt)
        self.console.print(f"\n Launching {model_choice.upper()} with your optimized prompt...")
        # Add error handling around the launch
        if self.launcher:
            try:
                self.launcher.launch(improved_prompt)
            except Exception as e:
                self.console.print(f"[red]Error launching {model_choice}: {e}[/red]")
        else:
            self.console.print("[yellow]No launcher configured - skipping AI session[/yellow]")

        # Exit message
        self.console.print("\n" + "="*60)
        self.console.print("[bold green] PromptPrompt Complete![/bold green]")
        self.console.print("\n[dim]Summary:[/dim]")
        self.console.print(f"   • Original prompt optimized")
        self.console.print(f"   • AI tool selected: {model_choice.upper()}")
        self.console.print(f"   • Prompts saved to ~/.promptprompt/prompts/")
        self.console.print(f"   • AI session launched with optimized prompt")
        self.console.print("\n[dim]Returning terminal control to you...[/dim]")
        self.console.print("=" * 60 + "\n")

    def get_draft_prompt(self):
        # Get the user's initial prompt
        self.console.print("\n[cyan] What would you like help with? [/cyan]")
        prompt = input("→ ")

        # Check if they actually input something
        if not prompt.strip(): # If the user didn't type anything
            self.console.print("[red] You need to enter something! [/red]")
            return self.get_draft_prompt() # Ask again

        return prompt.strip() # Removes extra spaces from beginning and end of prompt

    def collect_answers(self, questions):
        # Ask clarifying questions and collect answers
        #* INPUT PROMPT OPTIMIZER: questions = self.optimizer.clarify(draft_prompt)

        answers = []

        self.console.print("\n[bold yellow] Let me ask a few questions to improve your prompt:[/bold yellow]\n")

        # Loop through each question
        for i, question in enumerate(questions, 1):
            # Ask the question
            self.console.print(f"[cyan]{i}. {question}[/cyan]")
            answer = input("   → ")

            # Make sure they answered
            while not answer.strip():
                self.console.print("  [red]Please provide an answer.[/red]")
                answer = input("   → ")

            # Add the answer to our list
            answers.append(answer.strip())

        return answers

    def show_comparison(self, original_prompt, improved_prompt):
        # Show before and after prompts with Rich panels
        self.console.print() # Blank line

        # Original prompt panel
        self.console.print(
            Panel(
                original_prompt,
                title="ORIGINAL PROMPT",
                style="cyan",
                border_style="cyan"
            )
        )

        # Improved prompt panel
        self.console.print(
            Panel(
                improved_prompt,
                title="OPTIMIZED PROMPT",
                style="green",
                border_style="green"
            )
        )

    def get_approval(self):
        # Ask user if they approve the optimized prompt
        response = input("\nDo you approve this prompt? (y/n): ").lower().strip()

        # Keep asking until user enters 'y' or 'n'
        while response not in ['y', 'n']:
            self.console.print("[red]Please enter 'y' for yes or 'n' for no.[/red]")
            response = input("Do you approve this prompt? (y/n): ").lower().strip()

        return response == 'y' # Returns True if 'y', False if 'n'

    def refinement_loop(self, draft_prompt, questions, answers):
        # Keep improving the prompt until user approves
        refinements = [] # Store refinement requests

        while True: # Loop until we return (when user approves)

            # Generate improved prompt
            # For now, using fake, improved prompt.
            #* when integrating take out if/else statement below and add:
            #* improved_prompt = self.optimizer.generate_optimized_prompt(draft_prompt, questions, answers, refinements)
            # need to add refinements as the 4th parameter so that is included in the prompt if user want it

            if refinements:
                # If there are refinements, add them to the prompt
                # refinement_text = " Also: " + ", ".join(refinements)
                improved_prompt = self.optimizer.generate_optimized_prompt(draft_prompt, questions, answers, refinements)
                # improved_prompt = f"Write a detailed {draft_prompt} about {answers[0]} for {answers[1]} in a {answers[2]} tone.{refinement_text}"
            else:
                # First time, no refinements yet
                improved_prompt = self.optimizer.generate_optimized_prompt(draft_prompt, questions, answers)
                # improved_prompt = f"Write a detailed {draft_prompt} about {answers[0]} for {answers[1]} in a {answers[2]} tone."

            self.show_comparison(draft_prompt, improved_prompt)

            # Get approval
            approved = self.get_approval()

            if approved:
                # Return the improved prompt
                return improved_prompt
            else:
                # Ask what to change
                refinement = self.get_refinement()
                refinements.append(refinement)
                # Loop continues - generates a new prompt with refinements

    def get_refinement(self):
        # Ask user what they want to refine
        self.console.print("\n[bold yellow] What would you like to refine?[/bold yellow]")
        self.console.print("[dim]Example: 'Make it more technical' or 'Add focus on security'[/dim]")

        refinement = input("\n→ ")

        # Make sure user types something
        while not refinement.strip():
            self.console.print("[red]Please tell us what you'd like to change.[/red]")
            refinement = input("\n→ ")

        return refinement.strip()

if __name__ == "__main__":
    cli.run()
