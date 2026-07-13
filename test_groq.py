import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv(".env")
api_key = os.getenv("GROQ_API_KEY")

print(f"Key loaded: {bool(api_key)}")

try:
    client = Groq(api_key=api_key)
    print("Client initialized. Sending request...")
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": "Bonjour, ceci est un test. Réponds par 'OK' si tu me reçois."}
        ]
    )
    print("Response received:")
    print(completion.choices[0].message.content)
except Exception as e:
    import traceback
    print("Error occurred:")
    traceback.print_exc()
