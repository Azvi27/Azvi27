import os, re, json, base64
from datetime import datetime

# -------------------------------------------------------------
# 1. GENERATE BUILD CARD (MINIMALIST & CLEAN)
# -------------------------------------------------------------
def build_card():
    w, h = 420, 480
    if os.path.exists("azvi-ascii.svg"):
        with open("azvi-ascii.svg", "r", encoding="utf-8") as f:
            c = f.read()
            # Pastikan ascii card bersih dari tombol terminal
            c = re.sub(r'<circle[^>]*>', '', c)
            c = re.sub(r'<text[^>]*>portrait\.sh</text>', '', c)
            c = re.sub(r'<line[^>]*y1="4[04]"[^>]*/>', '', c)
            vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', c)
            if vb:
                w, h = int(vb.group(1)), int(vb.group(2))
        with open("azvi-ascii.svg", "w", encoding="utf-8") as f:
            f.write(c)

    sprite_b64 = ""
    sprite_path = "assets/Build_Capsem_Sprite.webp"
    if os.path.exists(sprite_path):
        with open(sprite_path, "rb") as f:
            sprite_b64 = base64.b64encode(f.read()).decode("utf-8")

    cx = w / 2
    svg = f'''<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="{w}" height="{h}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>

  <!-- Sprite Build -->
  <g transform="translate(18, 56)">
    <image href="data:image/webp;base64,{sprite_b64}" width="136" height="136"/>
  </g>

  <!-- Quotes -->
  <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif">
    <text x="162" y="74" fill="#58a6ff" font-size="13" font-weight="600">さぁ、実験を始めようか？</text>
    <text x="162" y="93" fill="#c9d1d9" font-size="11.5" font-style="italic">Shall we begin the experiment?</text>
    <text x="162" y="111" fill="#8b949e" font-size="10.5">Nah, mari kita mulai eksperimennya!</text>

    <line x1="162" y1="128" x2="{w - 24}" y2="128" stroke="#21262d" stroke-width="1"/>

    <text x="162" y="152" fill="#ff7b72" font-size="13" font-weight="600">勝利の法則は決まった！</text>
    <text x="162" y="171" fill="#c9d1d9" font-size="11.5" font-style="italic">The formula for victory is set!</text>
    <text x="162" y="189" fill="#8b949e" font-size="10.5">Hukum kemenangannya telah ditentukan!</text>
  </g>

  <!-- Clean Console Formula Box -->
  <g transform="translate(24, {h - 86})">
    <rect width="{w - 48}" height="54" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1"/>
    <text x="{(w - 48)/2}" y="22" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11" fill="#8b949e">
      system &gt; &quot;Are you ready?&quot;
    </text>
    <text x="{(w - 48)/2}" y="40" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11.5" font-weight="bold">
      <tspan fill="#ff7b72">Rabbit</tspan>
      <tspan fill="#6e7681"> × </tspan>
      <tspan fill="#58a6ff">Tank</tspan>
      <tspan fill="#6e7681"> ➔ </tspan>
      <tspan fill="#3fb950">BEST MATCH</tspan>
    </text>
  </g>
</svg>'''
    with open("assets/build-card.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("[1/3] assets/build-card.svg berhasil diperbarui.")

# -------------------------------------------------------------
# 2. GENERATE HEATMAP WITH RADAR SWEEP ANIMATION
# -------------------------------------------------------------
def build_heatmap():
    if not os.path.exists("data/contributions.json"):
        print("data/contributions.json tidak ada.")
        return

    with open("data/contributions.json") as f:
        d = json.load(f)

    days = d.get("days", [])
    total = d.get("total", "454 contributions in the last year")
    colors = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

    weeks, cur = [], []
    for item in days:
        dt = datetime.strptime(item["date"], "%Y-%m-%d")
        w_day = (dt.weekday() + 1) % 7
        cur.append((w_day, item.get("level", 0)))
        if w_day == 6:
            weeks.append(cur)
            cur = []
    if cur:
        weeks.append(cur)

    w, h = 840, 195
    lines = []
    lines.append(f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" xmlns="http://www.w3.org/2000/svg">')
    lines.append(f'  <rect width="{w}" height="{h}" rx="12" fill="#0d1117" stroke="#30363d" stroke-width="1"/>')
    lines.append('''  <defs>
    <linearGradient id="sweepGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#3fb950" stop-opacity="0" />
      <stop offset="70%" stop-color="#3fb950" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#3fb950" stop-opacity="0.35" />
    </linearGradient>
    <clipPath id="sweepClip">
      <rect x="52" y="30" width="765" height="115" rx="4" />
    </clipPath>
    <style>
      @keyframes radarMove {
        0% { transform: translateX(0px); }
        50% { transform: translateX(820px); }
        100% { transform: translateX(820px); }
      }
      .scanner-beam {
        animation: radarMove 4.5s ease-in-out infinite;
      }
    </style>
  </defs>''')

    months = ["Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"]
    for i, m in enumerate(months):
        lines.append(f'  <text x="{55 + i * 64}" y="22" fill="#8b949e" font-size="10" font-family="ui-monospace, monospace">{m}</text>')

    lines.append('  <text x="24" y="58" fill="#8b949e" font-size="9" font-family="ui-monospace, monospace">Mon</text>')
    lines.append('  <text x="24" y="88" fill="#8b949e" font-size="9" font-family="ui-monospace, monospace">Wed</text>')
    lines.append('  <text x="24" y="118" fill="#8b949e" font-size="9" font-family="ui-monospace, monospace">Fri</text>')

    lines.append('  <g id="heatmap-cells">')
    for c_idx, wk in enumerate(weeks):
        x = 55 + (c_idx * 14)
        for r_day, lvl in wk:
            y = 35 + (r_day * 14)
            lines.append(f'    <rect x="{x}" y="{y}" width="10.5" height="10.5" rx="2" fill="{colors[min(lvl, 4)]}" />')
    lines.append('  </g>')

    # Radar Line Sweep
    lines.append('''  <g clip-path="url(#sweepClip)">
    <g class="scanner-beam">
      <rect x="-80" y="30" width="80" height="115" fill="url(#sweepGrad)" />
      <line x1="0" y1="30" x2="0" y2="145" stroke="#3fb950" stroke-width="1.5" opacity="0.8" />
    </g>
  </g>''')

    lines.append(f'  <text x="55" y="172" fill="#c9d1d9" font-size="11" font-family="ui-monospace, monospace">{total}</text>')
    lines.append('  <g transform="translate(680, 162)">')
    lines.append('    <text x="-32" y="10" fill="#8b949e" font-size="10" font-family="ui-monospace, monospace">Less</text>')
    for idx, c in enumerate(colors):
        lines.append(f'    <rect x="{idx * 14}" y="0" width="10.5" height="10.5" rx="2" fill="{c}" />')
    lines.append('    <text x="76" y="10" fill="#8b949e" font-size="10" font-family="ui-monospace, monospace">More</text>')
    lines.append('  </g></svg>')

    with open("contrib-heatmap.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("[2/3] contrib-heatmap.svg berhasil di-render dengan radar sweep.")

# -------------------------------------------------------------
# 3. UPDATE README WITH CACHE BUSTING
# -------------------------------------------------------------
def update_readme():
    readme_content = '''<div align="center">

<!-- DUAL CARDS -->
<img src="./azvi-ascii.svg?v=2" width="414" alt="Azvi Portrait" />
<img src="./assets/build-card.svg?v=2" width="414" alt="Kamen Rider Build" />

<br><br>

<!-- OFFICIAL BADGES -->
<p align="center">
  <img src="https://img.shields.io/badge/GitHub-Azvi27-161b22?style=flat-square&logo=github&logoColor=white" alt="GitHub Core" />
  &nbsp;
  <img src="https://img.shields.io/badge/GitLab%20Cloud-gitlab.azvibelajar.my.id-161b22?style=flat-square&logo=gitlab&logoColor=fc6d26" alt="GitLab Cloud" />
  &nbsp;
  <img src="https://img.shields.io/badge/GitLab%20Lab%201-Lab. SSTK 1-161b22?style=flat-square&logo=gitlab&logoColor=fc6d26" alt="GitLab Lab 1" />
  &nbsp;
  <img src="https://img.shields.io/badge/GitLab%20Lab%202-Lab. SSTK 2-161b22?style=flat-square&logo=gitlab&logoColor=fc6d26" alt="GitLab Lab 2" />
</p>

<!-- AGGREGATED HEATMAP -->
<img src="./contrib-heatmap.svg?v=2" alt="Aggregated Heatmap" width="840" />

</div>
'''
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("[3/3] README.md diperbarui dengan cache-buster ?v=2.")

if __name__ == "__main__":
    build_card()
    build_heatmap()
    update_readme()
