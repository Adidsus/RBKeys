import os
import sys
import time
import requests

# Użycie: python .github/workflows/generate_lootlabs_link.py <KEY>
if len(sys.argv) != 2:
    print("Usage: python .github/workflows/generate_lootlabs_link.py <KEY>")
    sys.exit(1)

generated_key = sys.argv[1]
api_token = os.getenv("LOOTLABS_API_TOKEN")

if not api_token:
    print("❌ Brak LOOTLABS_API_TOKEN w secrets/env")
    sys.exit(1)

url = "https://creators.lootlabs.gg/api/public/content_locker"
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

payload = {
    "title": "Free Key",
    "url": f"https://example.com/claim?key={generated_key}",
    "tier_id": 1,
    "number_of_tasks": 3,
    "theme": 3,
    "thumbnail": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Thumbnail_Image.jpg/500px-Thumbnail_Image.jpg",
}

out_path = "rbkeys/lootlabslink.txt"
max_attempts = 3
last_error = None

for attempt in range(1, max_attempts + 1):
    response = None
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        status = response.status_code
        body_text = response.text

        # Retry tylko dla 5xx
        if status >= 500:
            raise requests.HTTPError(f"{status} Server Error", response=response)

        # Dla 4xx od razu fail (zły token/payload)
        response.raise_for_status()

        data = response.json()

        # Oczekiwany format:
        # {"type":"created","message":[{"loot_url":"..."}]}
        message = data.get("message")
        if not isinstance(message, list) or len(message) == 0:
            raise ValueError(f"Nieoczekiwany format 'message': {message}")

        first_item = message[0]
        if not isinstance(first_item, dict) or "loot_url" not in first_item:
            raise ValueError(f"Brak 'loot_url' w message[0]: {first_item}")

        loot_url = first_item["loot_url"]

        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(loot_url)

        print("✅ Wygenerowano loot_url:", loot_url)
        sys.exit(0)

    except Exception as e:
        last_error = e
        print(f"⚠️ Próba {attempt}/{max_attempts} nieudana: {e}")
        if response is not None:
            try:
                print("API:", response.text)
            except Exception:
                pass

        if attempt < max_attempts:
            time.sleep(attempt * 3)

print("❌ Błąd końcowy:", last_error)
sys.exit(1)
