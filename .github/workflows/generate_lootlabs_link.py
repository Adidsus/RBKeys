import requests
import sys
import os
import time

if len(sys.argv) != 2:
    print("Usage: python3 generate_lootlabs_link.py <KEY>")
    sys.exit(1)

generated_key = sys.argv[1]
api_token = os.getenv("LOOTLABS_API_TOKEN")

if not api_token:
    print("❌ Brak LOOTLABS_API_TOKEN")
    sys.exit(1)

url = "https://be.lootlabs.gg/api/lootlabs/content_locker"
headers = {"Authorization": f"Bearer {api_token}"}
data = {
    "title": "Free Key",
    "url": f"https://example.com/claim?key={generated_key}",
    "tier_id": 1,
    "number_of_tasks": 3,
    "theme": 3,
    "thumbnail": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Thumbnail_Image.jpg/500px-Thumbnail_Image.jpg"
}

last_err = None
for attempt in range(1, 4):
    try:
        r = requests.post(url, headers=headers, json=data, timeout=30)
        if r.status_code >= 500:
            raise requests.HTTPError(f"{r.status_code} Server Error", response=r)

        r.raise_for_status()
        res_json = r.json()
        loot_url = res_json["message"][0]["loot_url"]

        os.makedirs("rbkeys", exist_ok=True)
        with open("rbkeys/lootlabslink.txt", "w", encoding="utf-8") as f:
            f.write(loot_url)

        print("✅ OK")
        sys.exit(0)

    except Exception as e:
        last_err = e
        body = ""
        try:
            body = r.text
        except Exception:
            pass
        print(f"⚠️ Próba {attempt}/3 nieudana: {e}")
        if body:
            print("API:", body)
        if attempt < 3:
            time.sleep(attempt * 5)

print("❌ Błąd końcowy:", last_err)
sys.exit(1)
