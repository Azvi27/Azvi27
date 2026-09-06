import os, json, requests, urllib3
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Muat variabel environment dari .env di root
load_dotenv()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LOCAL_INSTANCES = [
    {
        "name": "GitLab Lab SSTK 1",
        "url": os.getenv("GITLAB_LOCAL_URL_1", "").rstrip("/"),
        "token": os.getenv("GITLAB_LOCAL_TOKEN_1", "").strip()
    },
    {
        "name": "GitLab Lab SSTK 2",
        "url": os.getenv("GITLAB_LOCAL_URL_2", "").rstrip("/"),
        "token": os.getenv("GITLAB_LOCAL_TOKEN_2", "").strip()
    }
]

def fetch_from_instance(instance):
    name = instance["name"]
    base_url = instance["url"]
    token = instance["token"]

    if not base_url or not token:
        print(f"[-] Melewati {name}: URL atau Token tidak ditemukan di .env")
        return {}

    print(f"[+] Menghubungi {name} ({base_url})...")
    headers = {"PRIVATE-TOKEN": token, "User-Agent": "Mozilla/5.0"}
    one_year_ago = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    instance_dict = {}
    page = 1

    while page <= 10:
        url = f"{base_url}/api/v4/events?after={one_year_ago}&per_page=100&page={page}"
        try:
            res = requests.get(url, headers=headers, verify=False, timeout=10)
            if res.status_code != 200:
                print(f"    Gagal akses (Status {res.status_code})")
                break
            events = res.json()
            if not events:
                break
            for ev in events:
                d = ev.get("created_at", "")[:10]
                if d:
                    instance_dict[d] = instance_dict.get(d, 0) + 1
            if len(events) < 100:
                break
            page += 1
        except Exception as e:
            print(f"    Error {name}: {e}")
            break

    total = sum(instance_dict.values())
    print(f"    -> Ditemukan: {total} kontribusi ({len(instance_dict)} hari aktif)")
    return instance_dict

def main():
    combined = {}
    for inst in LOCAL_INSTANCES:
        data = fetch_from_instance(inst)
        for d, count in data.items():
            combined[d] = combined.get(d, 0) + count

    os.makedirs("data", exist_ok=True)
    with open("data/gitlab_local.json", "w") as f:
        json.dump(combined, f, indent=2)

    print(f"Selesai! Total {sum(combined.values())} kontribusi lokal tersimpan.")

if __name__ == "__main__":
    main()
