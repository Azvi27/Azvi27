import os, json, re, requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

GITHUB_USERNAME = "Azvi27"
GITLAB_HOST = "gitlab.azvibelajar.my.id"
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN", "").strip()

def get_github_data(username):
    url = f"https://github.com/users/{username}/contributions"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if res.status_code != 200:
        return {}
    soup = BeautifulSoup(res.text, "html.parser")
    gh_dict = {}
    tooltips = {}
    for tip in soup.find_all(["tool-tip", "div"], attrs={"for": True}):
        target_id = tip.get("for")
        text = tip.get_text(strip=True)
        m = re.search(r"(\d+)\s+contribution", text)
        if m:
            tooltips[target_id] = int(m.group(1))
        elif "No contribution" in text:
            tooltips[target_id] = 0

    for td in soup.find_all("td", class_="ContributionCalendar-day"):
        d = td.get("data-date")
        t_id = td.get("id")
        lvl = td.get("data-level")
        if d:
            if t_id and t_id in tooltips:
                gh_dict[d] = tooltips[t_id]
            elif td.get("data-count"):
                gh_dict[d] = int(td.get("data-count"))
            elif lvl is not None:
                gh_dict[d] = {0: 0, 1: 1, 2: 3, 3: 6, 4: 10}.get(int(lvl), 0)
    return gh_dict

def get_gitlab_data(host, token):
    if not token:
        print("   [!] Token GitLab Publik kosong.")
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
                d = ev.get("created_at", "")[:10]
                if d:
                    gl_dict[d] = gl_dict.get(d, 0) + 1
            if len(events) < 100:
                break
            page += 1
        except Exception as e:
            print(f"   [!] Error GitLab Publik: {e}")
            break
    return gl_dict

def count_to_level(c):
    if c <= 0: return 0
    if c <= 2: return 1
    if c <= 5: return 2
    if c <= 9: return 3
    return 4

def sync_contributions():
    print("1. Mengambil data GitHub...")
    gh_data = get_github_data(GITHUB_USERNAME)
    print(f"   -> GitHub: {sum(gh_data.values())} kontribusi")

    print(f"2. Mengambil data GitLab Publik ({GITLAB_HOST})...")
    gl_data = get_gitlab_data(GITLAB_HOST, GITLAB_TOKEN)
    print(f"   -> GitLab Publik: {sum(gl_data.values())} kontribusi")

    print("3. Membaca data GitLab Lab Lokal...")
    local_data = {}
    if os.path.exists("data/gitlab_local.json"):
        with open("data/gitlab_local.json") as f:
            local_data = json.load(f)
    print(f"   -> GitLab Lokal: {sum(local_data.values())} kontribusi")

    all_dates = sorted(set(gh_data.keys()) | set(gl_data.keys()) | set(local_data.keys()))
    combined_days = []
    total = 0
    for d in all_dates:
        day_total = gh_data.get(d, 0) + gl_data.get(d, 0) + local_data.get(d, 0)
        total += day_total
        combined_days.append({"date": d, "level": count_to_level(day_total)})

    os.makedirs("data", exist_ok=True)
    with open("data/contributions.json", "w") as f:
        json.dump({"total": f"{total} contributions in the last year", "days": combined_days}, f, indent=2)

    print("-" * 50)
    print(f"TOTAL GABUNGAN 4 SUMBER: {total} KONTRIBUSI")

if __name__ == "__main__":
    sync_contributions()
