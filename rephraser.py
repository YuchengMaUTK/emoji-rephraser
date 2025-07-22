"""
Emoji Rephraser Agent

Uses Strands SDK to enhance text with emojis while preserving the original words.
"""

import time
import logging
from typing import Optional, Dict, Any
from strands.models import BedrockModel  

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("emoji_rephraser")

# Try to import Strands SDK
try:
    from strands import Agent
    STRANDS_AVAILABLE = True
except ImportError:
    STRANDS_AVAILABLE = False
    logger.warning(
        "Strands SDK not found. Please install it using: uv pip install strands-agents"
    )


class EmojiRephraserAgent:
    """Agent that enhances text with emojis while preserving the original words."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the agent with configuration.
        
        Args:
            config: Optional configuration dictionary to override defaults
        
        Raises:
            ImportError: If Strands SDK is not installed
            ConnectionError: If agent initialization fails
        """
        if not STRANDS_AVAILABLE:
            raise ImportError(
                "Strands SDK not found. Please install it using: uv pip install strands-agents"
            )
        
        # Default configuration
        self.agent_config = {
            "system_prompt": (
                "You are an emoji rephraser. Your job is to enhance user input with relevant emojis "
                "while preserving all the original words. Add emojis before or after relevant words "
                "or at the beginning/end of sentences to make the text more expressive and fun. "
                "Do not remove or change any words from the original text. "
                "For example, 'I love pizza' should be rephrased as 'I ❤️ love pizza 🍕' or 'I love pizza 🍕❤️'. "
                "Be creative but relevant with emoji choices."
            ),
            "temperature": 0.7,  # Higher temperature for more creative outputs
        }
        
        # Override with user-provided config if any
        if config:
            self.agent_config.update(config)
        
        # Initialize Strands agent with retry logic
        self.agent = None
        self._initialize_agent()
    
    def _initialize_agent(self, max_retries: int = 3, retry_delay: float = 1.0):
        """Initialize the Strands agent with retry logic.
        
        Args:
            max_retries: Maximum number of connection attempts
            retry_delay: Delay between retries in seconds
            
        Raises:
            ConnectionError: If all connection attempts fail
        """
        retries = 0
        last_error = None
        
        while retries < max_retries:
            try:  
                logger.info(f"Initializing Strands agent (attempt {retries + 1}/{max_retries})")  
                
                # Create model with temperature configuration  
                model = BedrockModel(
                    model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",
                    region_name="us-west-2",
                    temperature=self.agent_config["temperature"]
                )  
                
                self.agent = Agent(  
                    model=model,  
                    system_prompt=self.agent_config["system_prompt"]  
                )  
                logger.info("✅ Emoji Rephraser Agent initialized successfully")  
                return  
            except Exception as e:  
                last_error = e
                retries += 1
                if retries < max_retries:
                    logger.warning(f"Failed to initialize agent: {str(e)}. Retrying in {retry_delay}s...")
                    time.sleep(retry_delay)
                    # Increase delay for next retry (exponential backoff)
                    retry_delay *= 2
        
        # If we get here, all retries failed
        error_msg = f"Failed to initialize Strands agent after {max_retries} attempts: {str(last_error)}"
        logger.error(error_msg)
        raise ConnectionError(error_msg)
    
    def rephrase(self, text: str) -> str:
        """Enhance text with emojis while preserving the original words.
        
        Args:
            text: The text to enhance with emojis
            
        Returns:
            The original text enhanced with emojis
            
        Raises:
            RuntimeError: If rephrasing fails
        """
        if not text:
            return text  # Return original text if empty
        
        if not self.agent:
            try:
                self._initialize_agent()
            except ConnectionError as e:
                raise RuntimeError(f"Agent unavailable: {str(e)}")
        
        try:
            # Prepare the prompt for rephrasing with emojis
            prompt = f"Enhance this text with emojis while preserving all original words: {text}"
            
            # Use Strands agent to rephrase text with emojis
            logger.debug(f"Sending rephrasing request: {text}")
            
            # Based on the Strands documentation, we can call the agent directly as a function
            logger.info("Calling agent directly as a function")
            response = self.agent(prompt)
            
            # Extract text from response
            response_text = str(response)
                
            logger.info(f"Response received: {response_text}")
            
            # If response is empty, return the original text
            if not response_text or not response_text.strip():
                logger.warning("Received empty rephrasing response")
                return text
            
            # Validate the response quality
            validated_response = self._validate_response(text, response_text.strip())
            return validated_response
        except Exception as e:
            error_msg = f"Rephrasing failed: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
    
    def _validate_response(self, original_text: str, response: str) -> str:
        """Validate the response quality to ensure it's appropriate for users.
        
        Args:
            original_text: The original text input by the user
            response: The response from the agent
            
        Returns:
            Validated response or original text with basic emojis if validation fails
        """
        import re
        
        # Check if response is too short
        if len(response) < len(original_text) / 2:
            logger.warning(f"Response too short: {response}")
            return original_text + " 👍"  # Return original with basic emoji
            
        # Check if all original words are preserved
        # Split by common word boundaries and remove empty strings
        original_words = [w.lower() for w in re.split(r'[\s.,!?;:"\'\(\)\[\]]', original_text) if w]
        
        # Check if each original word is in the response (case insensitive)
        response_lower = response.lower()
            
        # Check if response has at least one emoji
        emoji_pattern = r'[\U0001F000-\U0001F9FF\u2600-\u26FF\u2700-\u27BF]+'
        emojis = re.findall(emoji_pattern, response)
        
        if not emojis:
            logger.warning("Response doesn't contain any emojis")
            return original_text + " 👍"  # Return original with basic emoji
        
        # Check for potentially negative or inappropriate emojis
        negative_emojis = ['💀', '☠️', '🤬', '💩', '🤮', '🤢', '😡']
        for emoji in negative_emojis:
            if emoji in response:
                logger.warning(f"Response contains potentially negative emoji: {emoji}")
                # Replace the negative emoji with a more positive one
                response = response.replace(emoji, '')
        
        # Check for excessive emojis (more than 1 emoji per 3 words)
        word_count = len(original_text.split())
        emoji_count = len(emojis)
        
        if emoji_count > word_count / 2 + 2:  # Allow some extra emojis, but not too many
            logger.warning(f"Response contains too many emojis: {emoji_count} emojis for {word_count} words")
            # Keep the response but log the warning - we don't want to be too strict
        
        # If all checks pass, return the validated response
        logger.info("Response validation passed")
        return response
        
    def _clean_response(self, response: str) -> str:
        """Clean the response to ensure it contains only emojis.
        
        This is a simple implementation that might need refinement based on
        actual response patterns from the Strands SDK.
        
        Args:
            response: The raw response from the agent
            
        Returns:
            Cleaned response with only emojis if possible
        """
        # Remove any leading/trailing whitespace
        cleaned = response.strip()
        
        # If the response contains explanatory text, try to extract just the emojis
        # This is a simple heuristic and might need adjustment
        if len(cleaned) > 100:  # If response is very long, it probably contains text
            import re
            # Try to extract emoji sequences
            emoji_pattern = r'[\U0001F000-\U0001F9FF\u2600-\u26FF\u2700-\u27BF]+'
            emojis = re.findall(emoji_pattern, cleaned)
            if emojis:
                return ''.join(emojis)
        
        return cleaned
    
    def shutdown(self):
        """Clean up resources."""
        logger.info("Shutting down Emoji Rephraser Agent")
        # Perform any necessary cleanup for the Strands agent
        self.agent = None