import os, json, requests, urllib3
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CACHE_FILE = "data/gitlab_local.json"

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
        return None

    print(f"[+] Menghubungi {name} ({base_url})...")
    headers = {"PRIVATE-TOKEN": token, "User-Agent": "Mozilla/5.0"}
    one_year_ago = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    instance_dict = {}
    page = 1

    while page <= 10:
        url = f"{base_url}/api/v4/events?after={one_year_ago}&per_page=100&page={page}"
        try:
            res = requests.get(url, headers=headers, verify=False, timeout=4)
            if res.status_code != 200:
                print(f"    Gagal akses (Status {res.status_code})")
                return None
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
            print(f"    Tidak dapat menjangkau {name} (Offline / Di luar jaringan lab)")
            return None

    total = sum(instance_dict.values())
    print(f"    -> Ditemukan: {total} kontribusi ({len(instance_dict)} hari aktif)")
    return instance_dict

def main():
    os.makedirs("data", exist_ok=True)
    
    # Baca cache lama jika ada
    cached_data = {}
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                cached_data = json.load(f)
        except Exception:
            cached_data = {}

    combined = {}
    any_success = False

    for inst in LOCAL_INSTANCES:
        data = fetch_from_instance(inst)
        if data is not None:
            any_success = True
            for d, count in data.items():
                combined[d] = combined.get(d, 0) + count

    # Jika kedua lab gagal dihubungi (misal di luar WiFi lab), pertahankan cache lama!
    if not any_success and cached_data:
        print(f"[i] Menggunakan cache lokal tersimpan: {sum(cached_data.values())} kontribusi tetap dipertahankan.")
        return

    # Jika berhasil menarik data baru, simpan ke file
    with open(CACHE_FILE, "w") as f:
        json.dump(combined, f, indent=2)

    print(f"Selesai! Total {sum(combined.values())} kontribusi lokal tersimpan.")

if __name__ == "__main__":
    main()
