import os, re, json, base64, subprocess
import xml.etree.ElementTree as ET

# Kunci dimensi asli yang padat, proporsional, dan bebas ruang kosong
CARD_W = 350
CARD_H = 340

# =============================================================
# 1. PROCESS AZVI-ASCII.SVG (EXTRACT TEXT TAGS - 100% VALID XML)
# =============================================================
def get_pristine_ascii_raw():
    res = subprocess.run(["git", "log", "-S", "*+%*====", "--format=%H", "--", "azvi-ascii.svg"], capture_output=True, text=True)
    commits = [c.strip() for c in res.stdout.strip().split() if c.strip()]
    for c in commits:
        show = subprocess.run(["git", "show", f"{c}:azvi-ascii.svg"], capture_output=True, text=True)
        if "*+%*====" in show.stdout:
            return show.stdout
    if os.path.exists("azvi-ascii.svg"):
        with open("azvi-ascii.svg", "r", encoding="utf-8") as f:
            return f.read()
    return ""

def patch_ascii_portrait():
    raw_content = get_pristine_ascii_raw()
    if not raw_content:
        print("[!] Gagal memuat data asli azvi-ascii.svg.")
        return

    # Ekstrak HANYA elemen <text>...</text> murni (bebas dari tag <g> yatim piatu)
    all_tags = re.findall(r'<text\b[^>]*>.*?</text>', raw_content, flags=re.DOTALL)
    clean_text_tags = []
    for tag in all_tags:
        if any(x in tag for x in ["portrait.sh", "rendered:", "kernel:"]):
            continue
        clean_text_tags.append(tag)

    if not clean_text_tags:
        print("[!] Tag teks ASCII tidak ditemukan.")
        return

    ascii_body = "\n    ".join(clean_text_tags)

    # Susun SVG baru 350x340 dengan animasi reveal halus tanpa garis laser biru
    new_svg = f'''<svg width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Reveal halus vertikal: mengalir ke bawah, tampil utuh diam ~3.5 detik, lalu loop -->
    <clipPath id="asciiRevealClip">
      <rect x="0" y="20" width="{CARD_W}" height="0">
        <animate attributeName="height"
                 values="0; {CARD_H - 25}; {CARD_H - 25}; 0"
                 keyTimes="0; 0.45; 0.92; 1"
                 dur="7s"
                 repeatCount="indefinite" />
      </rect>
    </clipPath>
  </defs>

  <!-- Frame Kembar 350x340 -->
  <rect width="{CARD_W}" height="{CARD_H}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>

  <!-- Konten ASCII Meja Lab (Tajam, Presisi, Tanpa Garis Laser) -->
  <g clip-path="url(#asciiRevealClip)">
    {ascii_body}
  </g>
</svg>'''

    try:
        ET.fromstring(new_svg)
        with open("azvi-ascii.svg", "w", encoding="utf-8") as f:
            f.write(new_svg)
        print(f"[1/3] azvi-ascii.svg 100% VALID XML & padat ({CARD_W}x{CARD_H}).")
    except ET.ParseError as err:
        print(f"[!] Error XML azvi-ascii.svg: {err}")

# =============================================================
# 2. GENERATE BUILD CARD (TWIN 350x340 - RAPAT TANPA GAP KOSONG)
# =============================================================
def generate_build_card():
    sprite_path = "assets/Build_Capsem_Sprite.webp"
    sprite_b64 = ""
    if os.path.exists(sprite_path):
        with open(sprite_path, "rb") as f:
            sprite_b64 = base64.b64encode(f.read()).decode("utf-8")

    svg = f'''<svg width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Frame Kembar 350x340 -->
  <rect width="{CARD_W}" height="{CARD_H}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>

  <!-- Sprite Kamen Rider Build -->
  <g transform="translate(16, 42)">
    <image href="data:image/webp;base64,{sprite_b64}" width="112" height="112"/>
  </g>

  <!-- Quotes 3 Bahasa Sento Kiryu -->
  <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif">
    <text x="136" y="54" fill="#58a6ff" font-size="12" font-weight="600">さぁ、実験を始めようか？</text>
    <text x="136" y="72" fill="#c9d1d9" font-size="10.5" font-style="italic">Shall we begin the experiment?</text>
    <text x="136" y="89" fill="#8b949e" font-size="9.5">Nah, mari kita mulai eksperimennya!</text>

    <line x1="136" y1="102" x2="{CARD_W - 18}" y2="102" stroke="#21262d" stroke-width="1"/>

    <text x="136" y="122" fill="#ff7b72" font-size="12" font-weight="600">勝利の法則は決まった！</text>
    <text x="136" y="140" fill="#c9d1d9" font-size="10.5" font-style="italic">The formula for victory is set!</text>
    <text x="136" y="157" fill="#8b949e" font-size="9.5">Hukum kemenangannya telah ditentukan!</text>
  </g>

  <!-- Kotak Formula & Driver Callout (Posisi Pas di Bawah Quotes) -->
  <g transform="translate(20, 238)">
    <rect width="{CARD_W - 40}" height="64" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1"/>

    <!-- Baris 1: BEST MATCH -->
    <text x="{(CARD_W - 40)/2}" y="27" text-anchor="middle" font-family="ui-monospace, monospace" font-size="12" font-weight="600">
      <tspan fill="#ff7b72">Rabbit</tspan>
      <tspan fill="#6e7681"> × </tspan>
      <tspan fill="#58a6ff">Tank</tspan>
      <tspan fill="#6e7681"> ➔ </tspan>
      <tspan fill="#3fb950" font-weight="bold">BEST MATCH</tspan>
    </text>

    <!-- Baris 2: DRIVER CALLOUT -->
    <text x="{(CARD_W - 40)/2}" y="48" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11" fill="#8b949e" letter-spacing="1">
      &gt; &quot;Are you ready?&quot;
    </text>
  </g>
</svg>'''

    try:
        ET.fromstring(svg)
        with open("assets/build-card.svg", "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"[2/3] assets/build-card.svg 100% VALID & proporsional ({CARD_W}x{CARD_H}).")
    except ET.ParseError as err:
        print(f"[!] Error XML assets/build-card.svg: {err}")

# =============================================================
# 3. UPDATE README (CACHE BUSTER V15)
# =============================================================
def update_readme():
    content = '''<div align="center">

<!-- DUAL MINIMAL CARDS -->
<img src="./azvi-ascii.svg?v=15" width="414" alt="Azvi Portrait" />
<img src="./assets/build-card.svg?v=15" width="414" alt="Kamen Rider Build" />

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
<img src="./contrib-heatmap.svg?v=15" alt="Aggregated Heatmap" width="840" />

</div>
'''
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("[3/3] README.md diperbarui dengan cache-buster ?v=15.")

if __name__ == "__main__":
    patch_ascii_portrait()
    generate_build_card()
    update_readme()
