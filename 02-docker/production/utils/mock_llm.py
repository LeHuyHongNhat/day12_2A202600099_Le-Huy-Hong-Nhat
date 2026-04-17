"""
Mock LLM for testing and development.
"""


def ask(question: str) -> str:
    """Simple mock LLM response."""
    return f"Mock answer to: {question}"
