import requests
import sys

# Pobierz klucz jako parametr
if len(sys.argv) != 2:
    print("Usage: python3 generate_lootlabs_link.py <KEY>")
    sys.exit(1)

generated_key = sys.argv[1]

# API LootLabs
url = "https://be.lootlabs.gg/api/lootlabs/content_locker"
headers = {
    "Authorization": "Bearer YOUR_API_TOKEN"  # <- zamień na Twój token lub wrzuć jako GH_SECRET
}

data = {
    "title": "Free Key",
    "url": f"https://example.com/claim?key={generated_key}",
    "tier_id": 1,
    "number_of_tasks": 3,
    "theme": 3,
    "thumbnail": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Thumbnail_Image.jpg/500px-Thumbnail_Image.jpg"
}

response = requests.post(url, headers=headers, json=data)
res_json = response.json()

try:
    loot_url = res_json["message"][0]["loot_url"]
    with open("rbkeys/lootlabslink.txt", "w") as f:
        f.write(loot_url)
except Exception as e:
    print("❌ Błąd generowania linku:", e)
    print("🔁 Odpowiedź z API:", res_json)
    sys.exit(1)
