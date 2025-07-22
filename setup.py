from setuptools import setup, find_packages

setup(
    name="emoji_rephraser",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "strands-agents>=1.0.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "emoji-rephraser=emoji_rephraser.main:main",
        ],
    },
    author="Emoji Rephraser Team",
    author_email="your.email@example.com",
    description="A command-line application that enhances text with emojis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/emoji-rephraser",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)