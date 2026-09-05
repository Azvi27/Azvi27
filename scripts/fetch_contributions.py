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
    raise Exception(
        f"Gagal mengambil data kontribusi: Status {response.status_code}"
    )

  soup = BeautifulSoup(response.text, "html.parser")
  days = []

  # Ambil elemen kotak kontribusi GitHub
  for td in soup.find_all("td", class_="ContributionCalendar-day"):
    date = td.get("data-date")
    level = td.get("data-level", "0")
    if date:
      days.append({"date": date, "level": int(level)})

  os.makedirs("data", exist_ok=True)
  with open("data/contributions.json", "w") as f:
    json.dump(days, f, indent=2)

  print(
      f"Berhasil menyimpan {len(days)} hari kontribusi ke"
      " data/contributions.json"
  )


if __name__ == "__main__":
  fetch_contributions(GITHUB_USERNAME)
