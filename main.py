#!/usr/bin/env python3
"""
Emoji Rephraser - Main Application

A command-line application that enhances natural language with emojis
using the Strands SDK.
"""

import sys
from emoji_rephraser.terminal import TerminalInterface
from emoji_rephraser.rephraser import EmojiRephraserAgent


def main():
    """Main entry point for the application."""
    terminal = TerminalInterface()
    terminal.display_welcome()
    
    try:
        # Initialize the rephraser agent
        terminal.display_message("Initializing emoji rephraser agent...")
        agent = EmojiRephraserAgent()
        
        # Run the conversation loop
        run_conversation_loop(terminal, agent)
    except KeyboardInterrupt:
        print("\nApplication terminated by user.")
        return 0
    except Exception as e:
        terminal.display_error(f"An error occurred: {str(e)}")
        return 1
    finally:
        # Use emoji only if terminal supports it
        wave = "👋" if terminal.emoji_support else "!"
        terminal.display_message(f"Thank you for using Emoji Rephraser! Goodbye{wave}")
    
    return 0


def run_conversation_loop(terminal, agent):
    """Run the main conversation loop."""
    while True:
        # Get user input
        user_input = terminal.get_user_input()
        
        # Check for exit command
        if user_input == "EXIT":
            if terminal.confirm_exit():
                break
            else:
                continue
        
        # Skip empty input or special commands that were handled
        if not user_input:
            continue
        
        # Process with agent
        try:
            terminal.display_loading()
            rephrased_text = agent.rephrase(user_input)
            terminal.display_rephrasing(rephrased_text)
        except KeyboardInterrupt:
            terminal.display_message("Rephrasing cancelled")
        except Exception as e:
            terminal.display_error(f"Rephrasing error: {str(e)}")


if __name__ == "__main__":
    sys.exit(main())