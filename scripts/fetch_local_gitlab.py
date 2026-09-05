from datetime import datetime, timedelta
import json
import os
import requests
import urllib3

# Nonaktifkan peringatan SSL sertifikat self-signed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

GITLAB_LOCAL_URL = "https://Lab. SSTK 1"
LOCAL_TOKEN = os.getenv("GITLAB_LOCAL_TOKEN", "")


def fetch_local():
  if not LOCAL_TOKEN:
    print("Error: GITLAB_LOCAL_TOKEN belum diisi!")
    return

  headers = {"PRIVATE-TOKEN": LOCAL_TOKEN, "User-Agent": "Mozilla/5.0"}
  one_year_ago = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

  print("Menghubungi GitLab Lokal (Lab. SSTK 1)...")
  local_dict = {}
  page = 1

  while page <= 10:
    url = f"{GITLAB_LOCAL_URL}/api/v4/events?after={one_year_ago}&per_page=100&page={page}"
    try:
      res = requests.get(url, headers=headers, verify=False, timeout=10)
      if res.status_code != 200:
        print(f"Gagal mengambil data, status HTTP: {res.status_code}")
        break

      events = res.json()
      if not events:
        break

      for ev in events:
        date = ev.get("created_at", "")[:10]
        if date:
          local_dict[date] = local_dict.get(date, 0) + 1

      if len(events) < 100:
        break
      page += 1
    except Exception as e:
      print(f"Error koneksi ke GitLab lokal: {e}")
      break

  os.makedirs("data", exist_ok=True)
  with open("data/gitlab_local.json", "w") as f:
    json.dump(local_dict, f, indent=2)

  total_local = sum(local_dict.values())
  print(
      f"Sukses! Tersimpan {total_local} kontribusi ({len(local_dict)} tanggal"
      " aktif) ke data/gitlab_local.json"
  )


if __name__ == "__main__":
  fetch_local()
