import os
import re
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


# ============================================================
# 1. Load environment variables
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not set. Please check your .env file."
    )


# ============================================================
# 2. Create Groq client
# ============================================================

client = Groq(api_key=API_KEY)


# ============================================================
# 3. System prompt
# ============================================================

SYSTEM_PROMPT = """
You are a Python code generator.

Your job is to convert the user's natural-language programming
request into clean, correct Python code.

Rules:
1. Generate only Python code.
2. Do not explain the code.
3. Do not include Markdown code fences.
4. Write beginner-friendly and readable code.
5. Use functions when appropriate.
6. Make sure the generated Python code is syntactically correct.
"""


# ============================================================
# 4. Clean generated code
# ============================================================

def clean_code(code: str) -> str:
    """Remove Markdown code fences from generated code."""

    code = code.strip()

    # Remove ```python ... ``` or ``` ... ```
    code = re.sub(r"^```(?:python)?\s*", "", code, flags=re.IGNORECASE)
    code = re.sub(r"\s*```$", "", code)

    return code.strip()


# ============================================================
# 5. Generate Python code using Groq
# ============================================================

def generate_code(task: str) -> str:
    """Send the task to Groq and return generated Python code."""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": task,
            },
        ],
    )

    generated_code = response.choices[0].message.content

    return clean_code(generated_code)


# ============================================================
# 6. Save generated code
# ============================================================

def save_code(code: str, task: str) -> Path:
    """Save generated Python code into the generated folder."""

    output_dir = BASE_DIR / "generated"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create a filename from the user's task
    filename = re.sub(r"[^a-zA-Z0-9]+", "_", task.lower()).strip("_")

    # Limit filename length
    filename = filename[:80]

    if not filename:
        filename = "generated_code"

    output_file = output_dir / f"{filename}.py"

    # Avoid overwriting an existing file
    counter = 1

    while output_file.exists():
        output_file = output_dir / f"{filename}_{counter}.py"
        counter += 1

    output_file.write_text(code, encoding="utf-8")

    return output_file


# ============================================================
# 7. Main program
# ============================================================

def main():
    print("=" * 60)
    print("   Natural Language to Python Code Generator")
    print("=" * 60)

    task = input("\nEnter your coding task: ").strip()

    if not task:
        print("Please enter a coding task.")
        return

    print("\nGenerating Python code...\n")

    try:
        code = generate_code(task)

        print("-" * 60)
        print("Generated Python Code:")
        print("-" * 60)
        print(code)
        print("-" * 60)

        output_file = save_code(code, task)

        print(f"\nCode saved to:")
        print(output_file)

    except Exception as error:
        print(f"\nError: {error}")


# ============================================================
# 8. Run program
# ============================================================

if __name__ == "__main__":
    main()