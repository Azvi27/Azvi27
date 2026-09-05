from datetime import datetime, timedelta
import json
import os
from bs4 import BeautifulSoup
import requests

GITHUB_USERNAME = "Azvi27"
GITLAB_HOST = "gitlab.azvibelajar.my.id"
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN", "")


def get_github_data(username):
  url = f"https://github.com/users/{username}/contributions"
  headers = {"User-Agent": "Mozilla/5.0"}
  res = requests.get(url, headers=headers)
  if res.status_code != 200:
    return {}

  soup = BeautifulSoup(res.text, "html.parser")
  gh_dict = {}

  for td in soup.find_all("td", class_="ContributionCalendar-day"):
    date = td.get("data-date")
    level = td.get("data-level")
    if date and level is not None:
      lvl = int(level)
      gh_dict[date] = {0: 0, 1: 1, 2: 3, 3: 6, 4: 10}.get(lvl, 0)

  return gh_dict


def get_gitlab_data(host, token):
  if not token:
    print("GitLab Token kosong! Melewati data GitLab.")
    return {}

  headers = {"PRIVATE-TOKEN": token, "User-Agent": "Mozilla/5.0"}

  # 1. Verifikasi token & ambil username resmi dari server
  try:
    user_res = requests.get(
        f"https://{host}/api/v4/user", headers=headers, timeout=10
    )
    if user_res.status_code != 200:
      print(f"Autentikasi GitLab gagal (Status {user_res.status_code})")
      return {}
    user_info = user_res.json()
    print(f"Terhubung ke GitLab sebagai: @{user_info.get('username')}")
  except Exception as e:
    print(f"Gagal menghubungi API GitLab: {e}")
    return {}

  # 2. Ambil seluruh riwayat aktivitas (events) dalam 1 tahun terakhir
  one_year_ago = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
  gl_dict = {}
  page = 1

  while page <= 10:  # Batas aman hingga 1000 aktivitas
    url = f"https://{host}/api/v4/events?after={one_year_ago}&per_page=100&page={page}"
    try:
      res = requests.get(url, headers=headers, timeout=10)
      if res.status_code != 200:
        break
      events = res.json()
      if not events:
        break
      for ev in events:
        date = ev.get("created_at", "")[:10]
        if date:
          gl_dict[date] = gl_dict.get(date, 0) + 1
      if len(events) < 100:
        break
      page += 1
    except Exception as e:
      print(f"Error parsing GitLab events: {e}")
      break

  return gl_dict


def count_to_level(count):
  if count <= 0:
    return 0
  elif count <= 2:
    return 1
  elif count <= 5:
    return 2
  elif count <= 9:
    return 3
  return 4


def sync_contributions():
  print("Mengambil data GitHub...")
  gh_data = get_github_data(GITHUB_USERNAME)

  print(f"Mengambil data GitLab API ({GITLAB_HOST})...")
  gl_data = get_gitlab_data(GITLAB_HOST, GITLAB_TOKEN)
  print(f"Aktivitas GitLab ditemukan: {len(gl_data)} tanggal aktif")

  sorted_dates = sorted(gh_data.keys())
  combined_days = []
  total_contributions = 0

  for date in sorted_dates:
    gh_count = gh_data.get(date, 0)
    gl_count = gl_data.get(date, 0)
    total_day = gh_count + gl_count

    total_contributions += total_day
    combined_days.append({"date": date, "level": count_to_level(total_day)})

  payload = {
      "total": f"{total_contributions} contributions in the last year",
      "days": combined_days,
  }

  os.makedirs("data", exist_ok=True)
  with open("data/contributions.json", "w") as f:
    json.dump(payload, f, indent=2)

  print(
      f"Selesai! Total gabungan: {total_contributions} kontribusi (GitHub +"
      " GitLab)"
  )


if __name__ == "__main__":
  sync_contributions()
