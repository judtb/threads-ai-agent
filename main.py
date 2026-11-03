import os
import requests
from openai import OpenAI

# 1. Ambil API Key dari "brankas" GitHub (Environment Variables)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
THREADS_ACCESS_TOKEN = os.environ.get("THREADS_ACCESS_TOKEN")
THREADS_USER_ID = os.environ.get("THREADS_USER_ID")

# 2. Setup Otak AI (Pakai Gemini)
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def generate_content():
    print("AI lagi mikir mau nulis apa...")
    prompt = "Kamu adalah influencer tech di Threads. Buat 1 postingan singkat (maksimal 200 karakter) tentang tips produktivitas pakai AI. Gaya bahasa santai, gaul, pake kata 'gw' dan 'lu'."
    
    try:
        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error pas bikin konten: {e}")
        return None

def post_to_threads(text):
    print(f"Lagi upload ke Threads: {text}")
    
    # Langkah A: Bikin Kontainer
    url_container = f"https://graph.threads.net/v1.0/{THREADS_USER_ID}/threads"
    payload_container = {
        "media_type": "TEXT",
        "text": text,
        "access_token": THREADS_ACCESS_TOKEN
    }
    
    res_container = requests.post(url_container, data=payload_container)
    creation_id = res_container.json().get("id")
    
    if not creation_id:
        print(f"Gagal bikin kontainer! Pesan dari Meta: {res_container.text}")
        return

    # Langkah B: Publish (Terbitin)
    url_publish = f"https://graph.threads.net/v1.0/{THREADS_USER_ID}/threads_publish"
    payload_publish = {
        "creation_id": creation_id,
        "access_token": THREADS_ACCESS_TOKEN
    }
    
    res_publish = requests.post(url_publish, data=payload_publish)
    
    if res_publish.status_code == 200:
        print("SUKSES! Postingan udah live di Threads.")
    else:
        print(f"Gagal publish! Pesan dari Meta: {res_publish.text}")

if __name__ == "__main__":
    konten = generate_content()
    if konten:
        post_to_threads(konten)
    else:
        print("Batal posting karena AI gagal bikin konten.")
