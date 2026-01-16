"""
Direct Ollama LLM invocation (chat API)
"""

import requests


def run_ollama(
    prompt: str,
    model: str = "deepseek-coder-tuned:latest",
    temperature: float = 0.2,
) -> str:
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "options": {
                "temperature": temperature
            },
            "stream": False,
        },
        timeout=120,
    )

    response.raise_for_status()
    data = response.json()

    return data["message"]["content"]
