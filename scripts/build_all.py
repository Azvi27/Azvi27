import os, re, json, base64
from datetime import datetime

CARD_W = 420
CARD_H = 450

# =============================================================
# 1. PROCESS AZVI-ASCII.SVG (CLEAN TWIN + DISCRETE TYPING)
# =============================================================
def patch_ascii_portrait():
    if not os.path.exists("azvi-ascii.svg"):
        print("azvi-ascii.svg tidak ditemukan.")
        return

    with open("azvi-ascii.svg", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Hapus titik terminal, header, footer rendered, dan garis pemindai lama
    content = re.sub(r'<circle[^>]*>', '', content)
    content = re.sub(r'<text[^>]*>portrait\.sh</text>', '', content)
    content = re.sub(r'<text[^>]*>rendered:[^<]*</text>', '', content)
    content = re.sub(r'<line[^>]*y1="4[04]"[^>]*/>', '', content)
    content = re.sub(r'<line[^>]*stroke="#58a6ff"[^>]*/>', '', content)

    # 2. Samakan ukuran viewBox dan root svg
    content = re.sub(r'<svg[^>]*>', f'<svg width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}" fill="none" xmlns="http://www.w3.org/2000/svg">', content, count=1)

    # 3. Samakan frame background card (rx=16, stroke=#30363d)
    content = re.sub(r'<rect[^>]*fill="#0d1117"[^>]*/>', f'<rect width="{CARD_W}" height="{CARD_H}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>', content, count=1)

    # 4. Sisipkan CSS Stepped Typewriter (animasi ketikan terminal diskrit tanpa garis scan)
    typing_style = """
  <defs>
    <style>
      @keyframes terminalTypewriter {
        0% { clip-path: inset(0 100% 100% 0); }
        15% { clip-path: inset(0 0 80% 0); }
        30% { clip-path: inset(0 0 62% 0); }
        45% { clip-path: inset(0 0 45% 0); }
        60% { clip-path: inset(0 0 28% 0); }
        75% { clip-path: inset(0 0 10% 0); }
        85%, 94% { clip-path: inset(0 0 0% 0); }
        100% { clip-path: inset(0 100% 100% 0); }
      }
      .ascii-typing {
        animation: terminalTypewriter 7s steps(12, end) infinite;
      }
    </style>
  </defs>"""

    # Sisipkan defs style jika belum ada
    if "terminalTypewriter" not in content:
        content = content.replace("<rect width=", typing_style + "\n  <rect width=", 1)

    # Pasang class animasi ke elemen pembungkus teks
    content = re.sub(r'<g([^>]*)font-family', r'<g\1class="ascii-typing" font-family', content, count=1)

    with open("azvi-ascii.svg", "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[1/3] azvi-ascii.svg berhasil diperbarui ({CARD_W}x{CARD_H}) dengan efek ketikan diskrit.")

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
  <!-- Card Frame Kembar Identik -->
  <rect width="{CARD_W}" height="{CARD_H}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>

  <!-- Sprite Build -->
  <g transform="translate(16, 56)">
    <image href="data:image/webp;base64,{sprite_b64}" width="126" height="126"/>
  </g>

  <!-- Quotes 3 Bahasa -->
  <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif">
    <!-- Quote 1 -->
    <text x="150" y="74" fill="#58a6ff" font-size="13" font-weight="600">さぁ、実験を始めようか？</text>
    <text x="150" y="93" fill="#c9d1d9" font-size="11" font-style="italic">Shall we begin the experiment?</text>
    <text x="150" y="111" fill="#8b949e" font-size="10">Nah, mari kita mulai eksperimennya!</text>

    <line x1="150" y1="128" x2="{CARD_W - 20}" y2="128" stroke="#21262d" stroke-width="1"/>

    <!-- Quote 2 -->
    <text x="150" y="152" fill="#ff7b72" font-size="13" font-weight="600">勝利の法則は決まった！</text>
    <text x="150" y="171" fill="#c9d1d9" font-size="11" font-style="italic">The formula for victory is set!</text>
    <text x="150" y="189" fill="#8b949e" font-size="10">Hukum kemenangannya telah ditentukan!</text>
  </g>

  <!-- Konsol Formula (Best Match Dulu, Baru Are you ready) -->
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

    with open("assets/build-card.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[2/3] assets/build-card.svg diperbarui ({CARD_W}x{CARD_H}) tanpa teks footer.")

# =============================================================
# 3. UPDATE README (CACHE BUSTER V5)
# =============================================================
def update_readme():
    content = '''<div align="center">

<!-- DUAL MINIMAL CARDS -->
<img src="./azvi-ascii.svg?v=5" width="414" alt="Azvi Portrait" />
<img src="./assets/build-card.svg?v=5" width="414" alt="Kamen Rider Build" />

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
<img src="./contrib-heatmap.svg?v=5" alt="Aggregated Heatmap" width="840" />

</div>
'''
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("[3/3] README.md diperbarui dengan cache-buster ?v=5.")

if __name__ == "__main__":
    patch_ascii_portrait()
    generate_build_card()
    update_readme()
