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
    raise Exception(f"Gagal mengambil data: {response.status_code}")

  soup = BeautifulSoup(response.text, "html.parser")

  days_dict = {}
  for td in soup.find_all("td", class_="ContributionCalendar-day"):
    date = td.get("data-date")
    level = td.get("data-level")
    if date and level is not None:
      days_dict[date] = int(level)

  # Urutkan secara kronologis berdasarkan tanggal
  sorted_dates = sorted(days_dict.keys())
  days = [{"date": d, "level": days_dict[d]} for d in sorted_dates]

  # Ambil teks total kontribusi
  h2 = soup.find(
      lambda tag: tag.name in ["h2", "h3"]
      and "contributions" in tag.text.lower()
  )
  total_text = "299 contributions in the last year"
  if h2:
    total_text = " ".join(h2.text.strip().split())

  payload = {"total": total_text, "days": days}

  os.makedirs("data", exist_ok=True)
  with open("data/contributions.json", "w") as f:
    json.dump(payload, f, indent=2)

  print(
      f"Berhasil menyimpan {len(days)} hari (terurut kronologis: {days[0]['date']} s/d {days[-1]['date']})"
  )


if __name__ == "__main__":
  fetch_contributions(GITHUB_USERNAME)
