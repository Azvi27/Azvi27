from datetime import datetime, timedelta
import json
import os
import re
from bs4 import BeautifulSoup
import requests

GITHUB_USERNAME = "Azvi27"
GITLAB_HOST = "gitlab.azvibelajar.my.id"

# Masukkan token GitLab publikmu di antara tanda kutip jika ingin otomatis terbaca
DEFAULT_GITLAB_TOKEN = "glpat-uBilYYf3L09IIL4KIBNWCG86MQp1OjEH.01.0w0d5eg2d"
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN", DEFAULT_GITLAB_TOKEN)


def get_github_data(username):
  url = f"https://github.com/users/{username}/contributions"
  headers = {"User-Agent": "Mozilla/5.0"}
  res = requests.get(url, headers=headers)
  if res.status_code != 200:
    print(f"   [!] Gagal mengambil data GitHub (Status {res.status_code})")
    return {}

  soup = BeautifulSoup(res.text, "html.parser")
  gh_dict = {}

  # Ekstrak jumlah kontribusi presisi dari tooltip GitHub
  tooltips = {}
  for tip in soup.find_all(["tool-tip", "div"], attrs={"for": True}):
    target_id = tip.get("for")
    text = tip.get_text(strip=True)
    match = re.search(r"(\d+)\s+contribution", text)
    if match:
      tooltips[target_id] = int(match.group(1))
    elif "No contribution" in text:
      tooltips[target_id] = 0

  for td in soup.find_all("td", class_="ContributionCalendar-day"):
    date = td.get("data-date")
    td_id = td.get("id")
    level = td.get("data-level")

    if date:
      # 1. Cek nilai dari tooltip (paling akurat)
      if td_id and td_id in tooltips:
        gh_dict[date] = tooltips[td_id]
      # 2. Cek atribut data-count bawaan
      elif td.get("data-count"):
        gh_dict[date] = int(td.get("data-count"))
      # 3. Fallback level jika struktur HTML berubah
      elif level is not None:
        lvl = int(level)
        gh_dict[date] = {0: 0, 1: 1, 2: 3, 3: 6, 4: 10}.get(lvl, 0)

  return gh_dict


def get_gitlab_data(host, token):
  if not token or "PASTE_TOKEN" in token:
    print("   [!] Peringatan: Token GitLab Publik kosong. Melewati sumber ini.")
    return {}

  headers = {"PRIVATE-TOKEN": token, "User-Agent": "Mozilla/5.0"}
  one_year_ago = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
  gl_dict = {}
  page = 1

  while page <= 10:
    url = f"https://{host}/api/v4/events?after={one_year_ago}&per_page=100&page={page}"
    try:
      res = requests.get(url, headers=headers, timeout=10)
      if res.status_code != 200:
        print(f"   [!] Gagal akses GitLab Publik (Status {res.status_code})")
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
      print(f"   [!] Error GitLab Publik: {e}")
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
  print("1. Mengambil data GitHub asli...")
  gh_data = get_github_data(GITHUB_USERNAME)
  total_gh = sum(gh_data.values())
  print(f"   -> GitHub: {total_gh} kontribusi ({len(gh_data)} hari)")

  print(f"2. Mengambil data GitLab Publik ({GITLAB_HOST})...")
  gl_data = get_gitlab_data(GITLAB_HOST, GITLAB_TOKEN)
  total_gl = sum(gl_data.values())
  print(f"   -> GitLab Publik: {total_gl} kontribusi ({len(gl_data)} hari aktif)")

  print("3. Membaca data GitLab Lab Lokal...")
  local_gl_data = {}
  local_path = "data/gitlab_local.json"
  if os.path.exists(local_path):
    with open(local_path, "r") as f:
      local_gl_data = json.load(f)
  total_local = sum(local_gl_data.values())
  print(
      f"   -> GitLab Lokal: {total_local} kontribusi ({len(local_gl_data)} hari"
      " aktif)"
  )

  # Gabungkan ketiga data sumber
  all_dates = (
      set(gh_data.keys()) | set(gl_data.keys()) | set(local_gl_data.keys())
  )
  sorted_dates = sorted(all_dates)

  combined_days = []
  total_contributions = 0

  for date in sorted_dates:
    c_gh = gh_data.get(date, 0)
    c_gl = gl_data.get(date, 0)
    c_loc = local_gl_data.get(date, 0)

    day_total = c_gh + c_gl + c_loc
    total_contributions += day_total
    combined_days.append({"date": date, "level": count_to_level(day_total)})

  payload = {
      "total": f"{total_contributions} contributions in the last year",
      "days": combined_days,
  }

  os.makedirs("data", exist_ok=True)
  with open("data/contributions.json", "w") as f:
    json.dump(payload, f, indent=2)

  print("-" * 50)
  print(f"TOTAL GABUNGAN 3 PLATFORM: {total_contributions} KONTRIBUSI")


if __name__ == "__main__":
  sync_contributions()
