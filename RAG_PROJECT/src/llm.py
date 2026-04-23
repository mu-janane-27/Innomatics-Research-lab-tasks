import requests

#  HARDCODE YOUR REAL KEY HERE
API_KEY = "YOUR_API_KEY_HERE"

def call_llm(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }

    response = requests.post(url, headers=headers, json=payload)

    data = response.json()

    if "choices" not in data:
        return f"API ERROR: {data}"

    return data["choices"][0]["message"]["content"]
