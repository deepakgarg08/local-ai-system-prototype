import requests
import sys

OLLAMA_URL = "http://localhost:11434/api/generate"


def main():
    payload = {
        "model": "llama3.1:8b",
        "prompt": "ping",
        "stream": False,
    }

    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=5)
        r.raise_for_status()
        print("✅ Ollama is alive and model responded.")
    except Exception as e:
        print("❌ Ollama not responding:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()

# python -m tools.check_llm_health
# curl -s http://localhost:11434/

