import json
import os
from bs4 import BeautifulSoup
import requests

GITHUB_USERNAME = "Azvi27"


def fetch_contributions(username):
  url = f"https://github.com/users/{username}/contributions"
  headers = {"User-Agent": "Mozilla/5.0"}
  response = requests.get(url, headers=headers)

  if response.status_code != 200:
    raise Exception(f"Gagal: {response.status_code}")

  soup = BeautifulSoup(response.text, "html.parser")

  # Targetkan tabel kalender utama secara spesifik
  table = soup.find("table", class_="ContributionCalendar-grid")
  if not table:
    # fallback jika class berbeda
    table = soup.find("tbody")

  days = []
  # Ambil kolom per kolom (minggu per minggu) persis DOM GitHub
  # GitHub menyusun per kolom <td> di dalam <tbody>
  # atau per row tergantung versi tampilan
  day_cells = soup.select(
      "td.ContributionCalendar-day, td[data-date]"
  )

  # Ambil hanya 371 cell terakhir (53 minggu x 7 hari) jika ada sisa
  for td in day_cells:
    date = td.get("data-date")
    level = td.get("data-level")
    if date and level is not None:
      days.append({"date": date, "level": int(level)})

  # Ambil tepat 53 minggu terakhir (371 hari) agar tidak ada offset tahun lalu
  if len(days) > 371:
    days = days[-371:]

  # Ambil total commit teks dari header kalender jika ada
  heading = soup.find(
      lambda tag: tag.name in ["h2", "h3"] and "contributions" in tag.text.lower()
  )
  total_str = (
      heading.text.strip().split()[0]
      if heading
      else "298"
  )

  payload = {"total": total_str, "days": days}

  os.makedirs("data", exist_ok=True)
  with open("data/contributions.json", "w") as f:
    json.dump(payload, f, indent=2)

  print(f"Tersimpan {len(days)} hari. Total kontribusi: {total_str}")


if __name__ == "__main__":
  fetch_contributions(GITHUB_USERNAME)
