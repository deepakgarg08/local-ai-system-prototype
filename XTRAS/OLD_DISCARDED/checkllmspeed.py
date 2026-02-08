import requests
import json
import time
import csv
from datetime import datetime

# Your specific model list
MODELS = [
    "smollm:135m",
    "smollm2:latest",
    "deepseek-coder:6.7b",
    "deepseek-coder-tuned:latest"
]

def benchmark_models(model_list, prompt="What is blockchain explain in 200 words."):
    results = []
    url = "http://localhost:11434/api/generate"
    
    for model in model_list:
        print(f"\n🚀 Testing Model: {model}")
        
        # 1. WARM UP (Loading the model into VRAM/RAM)
        print(f"   Warming up {model}...")
        requests.post(url, json={"model": model, "prompt": "hi", "stream": False})

        # 2. THE ACTUAL BENCHMARK
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            start_wall_time = time.time()
            response = requests.post(url, json=payload, timeout=120)
            end_wall_time = time.time()
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract metrics (Ollama returns these in nanoseconds)
                tokens = data.get("eval_count", 0)
                duration_ns = data.get("eval_duration", 1) # avoid div by zero
                prompt_tokens = data.get("prompt_eval_count", 0)
                prompt_duration_ns = data.get("prompt_eval_duration", 1)
                
                # Calculate human-readable stats
                tps = (tokens / duration_ns) * 10**9
                prompt_tps = (prompt_tokens / prompt_duration_ns) * 10**9
                total_time = end_wall_time - start_wall_time
                
                print(f"   ✅ Done: {tps:.2f} tokens/sec | Total: {total_time:.2f}s")
                
                results.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "model": model,
                    "eval_rate_tps": round(tps, 2),
                    "prompt_eval_rate_tps": round(prompt_tps, 2),
                    "response_tokens": tokens,
                    "total_duration_sec": round(total_time, 2)
                })
            else:
                print(f"   ❌ Error: Status Code {response.status_code}")
        except Exception as e:
            print(f"   ❌ Failed to connect: {e}")

    # 3. SAVE TO CSV
    keys = results[0].keys() if results else []
    if keys:
        filename = "ollama_benchmark_results.csv"
        with open(filename, 'w', newline='') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(results)
        print(f"\n📊 Benchmark complete! Results saved to: {filename}")

if __name__ == "__main__":
    benchmark_models(MODELS)