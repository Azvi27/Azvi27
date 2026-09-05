import os, re, json, base64, subprocess
import xml.etree.ElementTree as ET
from datetime import datetime

CARD_W = 420
CARD_H = 450

# =============================================================
# 1. PROCESS AZVI-ASCII.SVG (RESTORE + MULTI-STRIP TYPEWRITER)
# =============================================================
def get_original_ascii_from_git():
    """Mengambil file azvi-ascii.svg asli yang bersih dari commit awal git"""
    res = subprocess.run(["git", "log", "--format=%H", "--", "azvi-ascii.svg"], capture_output=True, text=True)
    commits = [c.strip() for c in res.stdout.strip().split() if c.strip()]
    
    if commits:
        for commit_hash in reversed(commits):
            c_res = subprocess.run(["git", "show", f"{commit_hash}:azvi-ascii.svg"], capture_output=True, text=True)
            if c_res.returncode == 0 and "<text" in c_res.stdout:
                return c_res.stdout

    if os.path.exists("azvi-ascii.svg"):
        with open("azvi-ascii.svg", "r", encoding="utf-8") as f:
            return f.read()
    return None

def patch_ascii_portrait():
    raw_content = get_original_ascii_from_git()
    if not raw_content:
        print("[!] Gagal memulihkan azvi-ascii.svg dari riwayat git.")
        return

    # Bersihkan header 3 titik, nama file portrait.sh, divider, dan footer
    raw_content = re.sub(r'<circle[^>]*>', '', raw_content)
    raw_content = re.sub(r'<text[^>]*>portrait\.sh</text>', '', raw_content)
    raw_content = re.sub(r'<text[^>]*>rendered:[^<]*</text>', '', raw_content)
    raw_content = re.sub(r'<line[^>]*y1="4[04]"[^>]*/>', '', raw_content)
    raw_content = re.sub(r'<defs>.*?</defs>', '', raw_content, flags=re.DOTALL)
    raw_content = re.sub(r'<rect[^>]*fill="#0d1117"[^>]*/>', '', raw_content)
    raw_content = re.sub(r'<\?xml[^>]*\?>', '', raw_content)
    raw_content = re.sub(r'<svg[^>]*>', '', raw_content)
    raw_content = re.sub(r'</svg>', '', raw_content)
    raw_content = re.sub(r'<g[^>]*clip-path=[^>]*>', '', raw_content)

    # Buat 32 strip mask untuk mengetik per baris (kiri ke kanan, atas ke bawah)
    N = 32
    y_start = 52.0
    y_end = 412.0
    strip_h = (y_end - y_start) / N
    total_dur = 7.0
    t_type_start = 0.3
    t_type_end = 4.3

    strip_elements = []
    for i in range(N):
        y_pos = y_start + (i * strip_h)
        t0 = t_type_start + (i / N) * (t_type_end - t_type_start)
        t1 = t_type_start + ((i + 1) / N) * (t_type_end - t_type_start)

        k_start = round(t0 / total_dur, 4)
        k_end = round(t1 / total_dur, 4)

        strip_elements.append(f'''      <rect x="0" y="{y_pos:.1f}" width="0" height="{strip_h + 1.2:.1f}">
        <animate attributeName="width"
                 values="0;0;{CARD_W};{CARD_W};0"
                 keyTimes="0;{k_start};{k_end};0.93;1"
                 dur="{total_dur}s"
                 repeatCount="indefinite" />
      </rect>''')

    strips_xml = "\n".join(strip_elements)

    svg_content = f'''<svg width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <clipPath id="terminalTypewriterClip">
{strips_xml}
    </clipPath>
  </defs>

  <!-- Frame Kembar Identik -->
  <rect width="{CARD_W}" height="{CARD_H}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>

  <!-- Konten ASCII dengan Masking Ketikan Terminal -->
  <g clip-path="url(#terminalTypewriterClip)">
    {raw_content.strip()}
  </g>
</svg>'''

    # Validasi sintaks XML sebelum disimpan
    try:
        ET.fromstring(svg_content)
        with open("azvi-ascii.svg", "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"[1/3] azvi-ascii.svg valid & diperbarui ({CARD_W}x{CARD_H}) dengan ketikan per baris.")
    except ET.ParseError as e:
        print(f"[!] Error validasi XML azvi-ascii.svg: {e}")

# =============================================================
# 2. GENERATE BUILD CARD (TWIN FRAME & CLEAN CONSOLE)
# =============================================================
def generate_build_card():
    sprite_path = "assets/Build_Capsem_Sprite.webp"
    sprite_b64 = ""
    if os.path.exists(sprite_path):
        with open(sprite_path, "rb") as f:
            sprite_b64 = base64.b64encode(f.read()).decode("utf-8")

    svg = f'''<svg width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="{CARD_W}" height="{CARD_H}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>

  <!-- Sprite Build -->
  <g transform="translate(16, 56)">
    <image href="data:image/webp;base64,{sprite_b64}" width="126" height="126"/>
  </g>

  <!-- Quotes 3 Bahasa -->
  <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif">
    <text x="150" y="74" fill="#58a6ff" font-size="13" font-weight="600">さぁ、実験を始めようか？</text>
    <text x="150" y="93" fill="#c9d1d9" font-size="11.5" font-style="italic">Shall we begin the experiment?</text>
    <text x="150" y="111" fill="#8b949e" font-size="10">Nah, mari kita mulai eksperimennya!</text>

    <line x1="150" y1="128" x2="{CARD_W - 20}" y2="128" stroke="#21262d" stroke-width="1"/>

    <text x="150" y="152" fill="#ff7b72" font-size="13" font-weight="600">勝利の法則は決まった！</text>
    <text x="150" y="171" fill="#c9d1d9" font-size="11.5" font-style="italic">The formula for victory is set!</text>
    <text x="150" y="189" fill="#8b949e" font-size="10">Hukum kemenangannya telah ditentukan!</text>
  </g>

  <!-- Formula & Driver Callout -->
  <g transform="translate(24, {CARD_H - 92})">
    <rect width="{CARD_W - 48}" height="56" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1"/>
    <text x="{(CARD_W - 48)/2}" y="24" text-anchor="middle" font-family="ui-monospace, monospace" font-size="12" font-weight="600">
      <tspan fill="#ff7b72">Rabbit</tspan>
      <tspan fill="#6e7681"> × </tspan>
      <tspan fill="#58a6ff">Tank</tspan>
      <tspan fill="#6e7681"> ➔ </tspan>
      <tspan fill="#3fb950" font-weight="bold">BEST MATCH</tspan>
    </text>
    <text x="{(CARD_W - 48)/2}" y="43" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11" fill="#8b949e" letter-spacing="1">
      &gt; &quot;Are you ready?&quot;
    </text>
  </g>
</svg>'''

    try:
        ET.fromstring(svg)
        with open("assets/build-card.svg", "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"[2/3] assets/build-card.svg valid & diperbarui ({CARD_W}x{CARD_H}).")
    except ET.ParseError as e:
        print(f"[!] Error XML build-card.svg: {e}")

# =============================================================
# 3. UPDATE README (CACHE BUSTER V6)
# =============================================================
def update_readme():
    content = '''<div align="center">

<!-- DUAL MINIMAL CARDS -->
<img src="./azvi-ascii.svg?v=6" width="414" alt="Azvi Portrait" />
<img src="./assets/build-card.svg?v=6" width="414" alt="Kamen Rider Build" />

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
<img src="./contrib-heatmap.svg?v=6" alt="Aggregated Heatmap" width="840" />

</div>
'''
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("[3/3] README.md diperbarui dengan cache-buster ?v=6.")

if __name__ == "__main__":
    patch_ascii_portrait()
    generate_build_card()
    update_readme()
