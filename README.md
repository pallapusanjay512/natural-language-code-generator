# Natural Language to Code Generator

A Python CLI tool that converts natural-language programming tasks into Python code using the Groq LLM API.

## Features

- Accepts coding tasks in plain English
- Uses Groq LLM to generate Python code
- Prints generated code in the terminal
- Automatically saves generated code as a `.py` file
- Removes Markdown code fences from the generated response
- Uses a system prompt that instructs the LLM to return only Python code
- Supports different types of tasks including string, mathematical, list, and dictionary operations

## Project Structure

```text
natural-language-to-code-generator/
│
├── agent.py
├── requirements.py
├── README.md
├── .gitignore
├── .env
├── generated/
└── venv/