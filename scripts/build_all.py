import os, re, json, base64
from datetime import datetime

# =============================================================
# 1. PATCH AZVI-ASCII.SVG (TYPEWRITER LINE-BY-LINE ANIMATION)
# =============================================================
def patch_ascii_portrait():
    if not os.path.exists("azvi-ascii.svg"):
        return 420, 480

    with open("azvi-ascii.svg", "r", encoding="utf-8") as f:
        content = f.read()

    # Bersihkan header lama
    content = re.sub(r'<circle[^>]*>', '', content)
    content = re.sub(r'<text[^>]*>portrait\.sh</text>', '', content)
    content = re.sub(r'<line[^>]*y1="4[04]"[^>]*/>', '', content)
    content = re.sub(r'<defs>.*?</defs>', '', content, flags=re.DOTALL)
    content = re.sub(r'<g id="type-wrapper"[^>]*>', '', content)
    content = re.sub(r'<g id="type-beam"[^>]*>.*?</g>', '', content, flags=re.DOTALL)

    w, h = 420, 480
    vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', content)
    if vb:
        w, h = int(vb.group(1)), int(vb.group(2))

    # Ekstrak elemen dalam svg
    # Pisahkan rect background dan konten teks
    bg_match = re.search(r'(<rect[^>]*fill="#0d1117"[^>]*/>)', content)
    bg_rect = bg_match.group(1) if bg_match else f'<rect width="{w}" height="{h}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>'

    # Ambil seluruh isi lainnya (teks ascii dan footer)
    body = content
    body = re.sub(r'<\?xml[^>]*\?>', '', body)
    body = re.sub(r'<svg[^>]*>', '', body)
    body = re.sub(r'</svg>', '', body)
    if bg_match:
        body = body.replace(bg_match.group(1), '')

    # Rakit SVG baru dengan SMIL Typewriter Mask & Scanner Line
    new_svg = f'''<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <clipPath id="asciiTypeClip">
      <rect x="0" y="30" width="{w}" height="0">
        <animate attributeName="height"
                 values="0; 0; {h-40}; {h-40}; 0; 0"
                 keyTimes="0; 0.04; 0.45; 0.85; 0.92; 1"
                 dur="7s"
                 repeatCount="indefinite" />
      </rect>
    </clipPath>
  </defs>

  {bg_rect}

  <!-- Teks ASCII dengan Animasi Terbuka Baris Demi Baris -->
  <g clip-path="url(#asciiTypeClip)">
    {body.strip()}
  </g>

  <!-- Garis Pemindai Ketikan di Tepi Baris -->
  <g>
    <animateTransform attributeName="transform"
                      type="translate"
                      values="0 30; 0 30; 0 {h-10}; 0 {h-10}; 0 30; 0 30"
                      keyTimes="0; 0.04; 0.45; 0.85; 0.92; 1"
                      dur="7s"
                      repeatCount="indefinite" />
    <line x1="24" y1="0" x2="{w-24}" y2="0" stroke="#58a6ff" stroke-width="1.5" opacity="0.65" />
  </g>
</svg>'''

    with open("azvi-ascii.svg", "w", encoding="utf-8") as f:
        f.write(new_svg)
    print(f"[1/3] azvi-ascii.svg berhasil disuntik animasi ketikan ({w}x{h}).")
    return w, h

# =============================================================
# 2. GENERATE BUILD CARD (BEST MATCH FIRST, LALU ARE YOU READY)
# =============================================================
def generate_build_card(w, h):
    sprite_path = "assets/Build_Capsem_Sprite.webp"
    sprite_b64 = ""
    if os.path.exists(sprite_path):
        with open(sprite_path, "rb") as f:
            sprite_b64 = base64.b64encode(f.read()).decode("utf-8")

    svg = f'''<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="{w}" height="{h}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>

  <!-- Sprite Build -->
  <g transform="translate(18, 56)">
    <image href="data:image/webp;base64,{sprite_b64}" width="136" height="136"/>
  </g>

  <!-- Quotes 3 Bahasa -->
  <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif">
    <text x="162" y="74" fill="#58a6ff" font-size="13" font-weight="600">さぁ、実験を始めようか？</text>
    <text x="162" y="93" fill="#c9d1d9" font-size="11.5" font-style="italic">Shall we begin the experiment?</text>
    <text x="162" y="111" fill="#8b949e" font-size="10.5">Nah, mari kita mulai eksperimennya!</text>

    <line x1="162" y1="128" x2="{w - 24}" y2="128" stroke="#21262d" stroke-width="1"/>

    <text x="162" y="152" fill="#ff7b72" font-size="13" font-weight="600">勝利の法則は決まった！</text>
    <text x="162" y="171" fill="#c9d1d9" font-size="11.5" font-style="italic">The formula for victory is set!</text>
    <text x="162" y="189" fill="#8b949e" font-size="10.5">Hukum kemenangannya telah ditentukan!</text>
  </g>

  <!-- KONSOL MINIMALIS: Best Match Dulu, Baru Are You Ready -->
  <g transform="translate(24, {h - 86})">
    <rect width="{w - 48}" height="56" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1"/>

    <!-- 1. FORMULA / BEST MATCH (DI ATAS) -->
    <text x="{(w - 48)/2}" y="24" text-anchor="middle" font-family="ui-monospace, SFMono-Regular, monospace" font-size="12" font-weight="600">
      <tspan fill="#ff7b72">Rabbit</tspan>
      <tspan fill="#6e7681"> × </tspan>
      <tspan fill="#58a6ff">Tank</tspan>
      <tspan fill="#6e7681"> ➔ </tspan>
      <tspan fill="#3fb950" font-weight="bold">BEST MATCH</tspan>
    </text>

    <!-- 2. DRIVER CALLOUT (DI BAWAH) -->
    <text x="{(w - 48)/2}" y="43" text-anchor="middle" font-family="ui-monospace, SFMono-Regular, monospace" font-size="11" fill="#8b949e" letter-spacing="1">
      &gt; &quot;Are you ready?&quot;
    </text>
  </g>
</svg>'''

    with open("assets/build-card.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[2/3] assets/build-card.svg berhasil diperbarui (Best Match duluan, tanpa teks kernel).")

# =============================================================
# 3. HEATMAP WITH PING-PONG RADAR (FILL ON FORWARD, WIPE ON REVERSE)
# =============================================================
def render_heatmap():
    if not os.path.exists("data/contributions.json"):
        print("data/contributions.json tidak ditemukan.")
        return

    with open("data/contributions.json") as f:
        data = json.load(f)

    days = data.get("days", [])
    total_str = data.get("total", "454 contributions in the last year")
    colors = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

    weeks = []
    current_week = []
    for d in days:
        dt = datetime.strptime(d["date"], "%Y-%m-%d")
        w_day = (dt.weekday() + 1) % 7 
        current_week.append((w_day, d.get("level", 0)))
        if w_day == 6:
            weeks.append(current_week)
            current_week = []
    if current_week:
        weeks.append(current_week)

    width = 840
    height = 195
    grid_w = len(weeks) * 14

    svg = []
    svg.append(f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">')
    svg.append(f'  <rect width="{width}" height="{height}" rx="12" fill="#0d1117" stroke="#30363d" stroke-width="1"/>')
    
    # ClipPath & Animasi SMIL Ping-Pong (Forward: Fill, Reverse: Wipe)
    svg.append(f'''  <defs>
    <clipPath id="heatmapWipeClip">
      <rect x="55" y="30" width="0" height="115">
        <animate attributeName="width"
                 values="0; 0; {grid_w}; {grid_w}; 0; 0"
                 keyTimes="0; 0.05; 0.48; 0.58; 0.95; 1"
                 dur="7s"
                 repeatCount="indefinite" />
      </rect>
    </clipPath>
  </defs>''')

    # Month Labels
    months = ["Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"]
    for i, m in enumerate(months):
        x = 55 + (i * 64)
        svg.append(f'  <text x="{x}" y="22" fill="#8b949e" font-size="10" font-family="ui-monospace, monospace">{m}</text>')

    # Day labels
    svg.append('  <text x="24" y="58" fill="#8b949e" font-size="9" font-family="ui-monospace, monospace">Mon</text>')
    svg.append('  <text x="24" y="88" fill="#8b949e" font-size="9" font-family="ui-monospace, monospace">Wed</text>')
    svg.append('  <text x="24" y="118" fill="#8b949e" font-size="9" font-family="ui-monospace, monospace">Fri</text>')

    # LAPISAN 1: GRID KOSONG (Default Abu-Abu #161b22 Selalu Ada di Dasar)
    svg.append('  <g id="base-empty-grid">')
    for c_idx, w in enumerate(weeks):
        x = 55 + (c_idx * 14)
        for r_day, _ in w:
            y = 35 + (r_day * 14)
            svg.append(f'    <rect x="{x}" y="{y}" width="10.5" height="10.5" rx="2" fill="#161b22" />')
    svg.append('  </g>')

    # LAPISAN 2: GRID BERWARNA (HANYA MUNCUL DI BELAKANG SINAR SCAN)
    svg.append('  <g clip-path="url(#heatmapWipeClip)">')
    for c_idx, w in enumerate(weeks):
        x = 55 + (c_idx * 14)
        for r_day, lvl in w:
            if lvl > 0:
                y = 35 + (r_day * 14)
                svg.append(f'    <rect x="{x}" y="{y}" width="10.5" height="10.5" rx="2" fill="{colors[min(lvl, 4)]}" />')
    svg.append('  </g>')

    # LAPISAN 3: GARIS PEMINDAI PING-PONG (SEJAJAR PERSIS DENGAN TEPI RECT)
    svg.append(f'''  <g>
    <animateTransform attributeName="transform"
                      type="translate"
                      values="0 0; 0 0; {grid_w} 0; {grid_w} 0; 0 0; 0 0"
                      keyTimes="0; 0.05; 0.48; 0.58; 0.95; 1"
                      dur="7s"
                      repeatCount="indefinite" />
    <line x1="55" y1="30" x2="55" y2="145" stroke="#39d353" stroke-width="2" />
    <line x1="55" y1="30" x2="55" y2="145" stroke="#39d353" stroke-width="8" opacity="0.35" />
  </g>''')

    # Footer
    svg.append(f'  <text x="55" y="172" fill="#c9d1d9" font-size="11" font-family="ui-monospace, monospace">{total_str}</text>')
    svg.append('  <g transform="translate(680, 162)">')
    svg.append('    <text x="-32" y="10" fill="#8b949e" font-size="10" font-family="ui-monospace, monospace">Less</text>')
    for idx, c in enumerate(colors):
        svg.append(f'    <rect x="{idx * 14}" y="0" width="10.5" height="10.5" rx="2" fill="{c}" />')
    svg.append('    <text x="76" y="10" fill="#8b949e" font-size="10" font-family="ui-monospace, monospace">More</text>')
    svg.append('  </g>')
    svg.append('</svg>')

    with open("contrib-heatmap.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print("[3/3] contrib-heatmap.svg berhasil dibuat dengan animasi ping-pong fill & wipe.")

def update_readme():
    content = '''<div align="center">

<!-- DUAL MINIMAL CARDS -->
<img src="./azvi-ascii.svg?v=3" width="414" alt="Azvi Portrait" />
<img src="./assets/build-card.svg?v=3" width="414" alt="Kamen Rider Build" />

<br><br>

<!-- DATA SOURCES STATUS BAR -->
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
<img src="./contrib-heatmap.svg?v=3" alt="Aggregated Heatmap" width="840" />

</div>
'''
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    w, h = patch_ascii_portrait()
    generate_build_card(w, h)
    render_heatmap()
    update_readme()
