# Emoji Rephraser 🎭✨

A command-line application that enhances your text with relevant emojis while preserving all original words. Make your messages more expressive and fun!

## 🌟 Features

- **Text Enhancement**: Add relevant emojis to your text while preserving all original words
- **Quality Control**: Ensures responses are appropriate and high-quality
- **Terminal Interface**: Easy-to-use command-line interface
- **AI-Powered**: Uses the Strands SDK to intelligently place emojis
- **Customizable**: Configurable temperature for more or less creative outputs

## 📋 Requirements

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) for dependency management
- [Strands SDK](https://strandsagents.com/)

## 🚀 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/emoji-rephraser.git
   cd emoji-rephraser
   ```

2. Install dependencies using uv:
   ```bash
   uv pip install -e .
   ```

   Or using pip:
   ```bash
   pip install -e .
   ```

## 💻 Usage

Run the application:
```bash
python -m emoji_rephraser.main
```

### Commands

- Type any text to get it enhanced with emojis
- Type `help` or `?` to display help information
- Type `clear` or `cls` to clear the screen
- Type `exit`, `quit`, `bye`, or `q` to exit the application

### Examples

Input:
```
I love coding in Python
```

Output:
```
I ❤️ love coding 💻 in Python 🐍
```

Input:
```
The weather is beautiful today
```

Output:
```
The weather is beautiful ☀️ today 🌈
```

## 🛠️ Project Structure

```
emoji_rephraser/
├── __init__.py          # Package initialization
├── main.py              # Main application entry point
├── rephraser.py         # Emoji rephrasing logic using Strands SDK
├── terminal.py          # Terminal interface for user interaction
└── pyproject.toml       # Project configuration and dependencies
```

## 🧩 How It Works

1. **Input Processing**: The application takes user input from the terminal
2. **AI Enhancement**: The Strands SDK analyzes the text and adds relevant emojis
3. **Quality Validation**: The response is validated to ensure it meets quality standards
4. **Display**: The enhanced text is displayed to the user

## 🔍 Quality Control

The Emoji Rephraser includes several quality control mechanisms:

- **Original Word Preservation**: Ensures all words from the original text are preserved
- **Non-Latin Character Detection**: Filters out responses with non-Latin characters
- **Emoji Presence**: Confirms that the response contains at least one emoji
- **Length Validation**: Makes sure the response isn't too short compared to the original text
- **Negative Emoji Detection**: Identifies and removes potentially negative or inappropriate emojis

## 🔧 Configuration

You can customize the behavior of the Emoji Rephraser by modifying the `agent_config` in `rephraser.py`:

```python
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
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📬 Contact

Project Link: [https://github.com/yourusername/emoji-rephraser](https://github.com/yourusername/emoji-rephraser)

## 🙏 Acknowledgements

- [Strands SDK](https://strandsagents.com/) for providing the AI capabilities
- [uv](https://github.com/astral-sh/uv) for dependency management