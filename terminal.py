"""
Terminal Interface for Emoji Rephraser

Handles user interaction through the terminal.
"""
import os
import sys
import time


class TerminalInterface:
    """Manages terminal-based user interaction."""
    
    def __init__(self):
        """Initialize the terminal interface."""
        self.exit_commands = ['exit', 'quit', 'bye', 'q']
        self.help_commands = ['help', '?', 'h']
        # Check if terminal supports emojis
        self.emoji_support = self._check_emoji_support()
        
    def _check_emoji_support(self):
        """Check if the terminal supports emoji display."""
        # Simple check based on platform and environment
        # This is a basic check and might not be 100% accurate
        if os.name == 'nt':  # Windows
            return 'WT_SESSION' in os.environ or 'CMDER_ROOT' in os.environ
        return True  # Most Unix-based terminals support emojis
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_welcome(self):
        """Display welcome message and instructions."""
        self.clear_screen()
        
        # Use simpler symbols if emoji support is questionable
        star = "✨" if self.emoji_support else "*"
        rocket = "🚀" if self.emoji_support else ">"
        
        welcome_message = f"""
        {star} Welcome to Emoji Rephraser! {star}
        
        Type your message and get it enhanced with emojis.
        Type '{self.exit_commands[0]}' to exit the application.
        Type '{self.help_commands[0]}' for instructions.
        
        Let's start rephrasing! {rocket}
        """
        print(welcome_message)
    
    def display_help(self):
        """Display help information."""
        help_message = """
        📚 Help Information 📚
        
        - Type any text to get it enhanced with emojis
        - The rephraser will add emojis while preserving your original words
        - Commands:
          - exit, quit, bye, q: Exit the application
          - help, ?, h: Display this help information
          - clear, cls: Clear the screen
        
        Happy rephrasing! 😊
        """
        print(help_message if self.emoji_support else help_message.replace('📚', '#').replace('😊', ':)'))
    
    def get_user_input(self):
        """Get input from the user."""
        try:
            prompt = "\n🗣️  " if self.emoji_support else "\n> "
            user_input = input(f"{prompt}Enter text to rephrase: ").strip()
            
            # Handle special commands
            if user_input.lower() in self.exit_commands:
                return "EXIT"
            elif user_input.lower() in self.help_commands:
                self.display_help()
                return ""
            elif user_input.lower() in ['clear', 'cls']:
                self.clear_screen()
                return ""
                
            return user_input
        except KeyboardInterrupt:
            print("\nDetected Ctrl+C. Exiting...")
            return "EXIT"
        except EOFError:
            print("\nDetected EOF. Exiting...")
            return "EXIT"
    
    def display_rephrasing(self, rephrased_text):
        """Display emoji rephrased text to the user."""
        if not rephrased_text:
            self.display_error("No rephrasing available")
            return
            
        prefix = "\n🔄 " if self.emoji_support else "\n=> "
        print(f"{prefix}Rephrased: {rephrased_text}")
    
    def display_error(self, message):
        """Display error message."""
        prefix = "\n❌ " if self.emoji_support else "\n[ERROR] "
        print(f"{prefix}Error: {message}")
    
    def display_message(self, message):
        """Display a general message."""
        print(f"\n{message}")
        
    def display_loading(self, message="Rephrasing"):
        """Display a loading animation."""
        if not sys.stdout.isatty():
            print(f"{message}...")
            return
            
        try:
            print(f"{message}", end="", flush=True)
            for _ in range(3):
                time.sleep(0.3)
                print(".", end="", flush=True)
            print()  # New line after loading
        except KeyboardInterrupt:
            print("\nOperation cancelled")
            
    def confirm_exit(self):
        """Confirm if the user wants to exit."""
        try:
            response = input("\nAre you sure you want to exit? (y/n): ").strip().lower()
            return response in ['y', 'yes']
        except (KeyboardInterrupt, EOFError):
            return True