import os, re, json, base64
from datetime import datetime

CARD_W = 420
CARD_H = 450

# =============================================================
# 1. PATCH AZVI-ASCII.SVG (TERMINAL TYPEWRITER EFFECT)
# =============================================================
def patch_ascii_portrait():
    if not os.path.exists("azvi-ascii.svg"):
        return

    with open("azvi-ascii.svg", "r", encoding="utf-8") as f:
        content = f.read()

    # Bersihkan header terminal lama, footer rendered, dan scanner lama
    content = re.sub(r'<circle[^>]*>', '', content)
    content = re.sub(r'<text[^>]*>portrait\.sh</text>', '', content)
    content = re.sub(r'<text[^>]*>rendered:[^<]*</text>', '', content)
    content = re.sub(r'<line[^>]*y1="4[04]"[^>]*/>', '', content)
    content = re.sub(r'<defs>.*?</defs>', '', content, flags=re.DOTALL)
    content = re.sub(r'<g[^>]*clip-path=[^>]*>', '', content)
    content = re.sub(r'<g id="type-[^>]*>.*?</g>', '', content, flags=re.DOTALL)

    # Ekstrak seluruh teks ASCII murni (buang tag svg luar dan rect lama)
    body = content
    body = re.sub(r'<\?xml[^>]*\?>', '', body)
    body = re.sub(r'<svg[^>]*>', '', body)
    body = re.sub(r'</svg>', '', body)
    body = re.sub(r'<rect[^>]*fill="#0d1117"[^>]*/>', '', body)

    # Susun ulang SVG dengan masking diagonal stepped (kiri-ke-kanan, atas-ke-bawah)
    new_svg = f'''<svg width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Stepped polygon clip revealing Left-to-Right then Top-to-Bottom -->
    <clipPath id="typewriterClip">
      <polygon points="0,0 0,0 0,0 0,0">
        <animate attributeName="points"
                 calcMode="discrete"
                 values="
                   0,0 0,0 0,0 0,0;
                   0,0 120,0 0,80 0,0;
                   0,0 280,0 60,160 0,160;
                   0,0 420,0 180,240 0,240;
                   0,0 420,0 320,320 0,320;
                   0,0 420,0 420,380 0,380;
                   0,0 420,0 420,{CARD_H} 0,{CARD_H};
                   0,0 420,0 420,{CARD_H} 0,{CARD_H};
                   0,0 0,0 0,0 0,0
                 "
                 keyTimes="0; 0.05; 0.12; 0.22; 0.35; 0.50; 0.65; 0.90; 1"
                 dur="6.5s"
                 repeatCount="indefinite" />
      </polygon>
    </clipPath>
  </defs>

  <!-- Card Frame Identik -->
  <rect width="{CARD_W}" height="{CARD_H}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>

  <!-- Teks ASCII dengan Animasi Ketikan Terminal -->
  <g clip-path="url(#typewriterClip)">
    {body.strip()}
  </g>
</svg>'''

    with open("azvi-ascii.svg", "w", encoding="utf-8") as f:
        f.write(new_svg)
    print(f"[1/3] azvi-ascii.svg diperbarui ({CARD_W}x{CARD_H}) dengan efek ketikan diskrit.")

# =============================================================
# 2. GENERATE BUILD CARD (CLEAN & PERFECT ALIGNMENT)
# =============================================================
def generate_build_card():
    sprite_path = "assets/Build_Capsem_Sprite.webp"
    sprite_b64 = ""
    if os.path.exists(sprite_path):
        with open(sprite_path, "rb") as f:
            sprite_b64 = base64.b64encode(f.read()).decode("utf-8")

    svg = f'''<svg width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Card Frame Identik -->
  <rect width="{CARD_W}" height="{CARD_H}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>

  <!-- SISI KIRI: Sprite Build -->
  <g transform="translate(16, 58)">
    <image href="data:image/webp;base64,{sprite_b64}" width="124" height="124"/>
  </g>

  <!-- SISI KANAN: Quotes 3 Bahasa (Margin Aman dari Tepi Kanan) -->
  <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif">
    <!-- Quote 1 -->
    <text x="148" y="74" fill="#58a6ff" font-size="13" font-weight="600">さぁ、実験を始めようか？</text>
    <text x="148" y="93" fill="#c9d1d9" font-size="11" font-style="italic">Shall we begin the experiment?</text>
    <text x="148" y="111" fill="#8b949e" font-size="10">Nah, mari kita mulai eksperimennya!</text>

    <!-- Divider halus -->
    <line x1="148" y1="128" x2="{CARD_W - 20}" y2="128" stroke="#21262d" stroke-width="1"/>

    <!-- Quote 2 -->
    <text x="148" y="152" fill="#ff7b72" font-size="13" font-weight="600">勝利の法則は決まった！</text>
    <text x="148" y="171" fill="#c9d1d9" font-size="11" font-style="italic">The formula for victory is set!</text>
    <text x="148" y="189" fill="#8b949e" font-size="10">Hukum kemenangannya telah ditentukan!</text>
  </g>

  <!-- KONSOL MINIMALIS: Best Match Dulu, Baru Are You Ready -->
  <g transform="translate(24, {CARD_H - 92})">
    <rect width="{CARD_W - 48}" height="56" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1"/>

    <!-- 1. FORMULA / BEST MATCH (DI ATAS) -->
    <text x="{(CARD_W - 48)/2}" y="24" text-anchor="middle" font-family="ui-monospace, monospace" font-size="12" font-weight="600">
      <tspan fill="#ff7b72">Rabbit</tspan>
      <tspan fill="#6e7681"> × </tspan>
      <tspan fill="#58a6ff">Tank</tspan>
      <tspan fill="#6e7681"> ➔ </tspan>
      <tspan fill="#3fb950" font-weight="bold">BEST MATCH</tspan>
    </text>

    <!-- 2. DRIVER CALLOUT (DI BAWAH) -->
    <text x="{(CARD_W - 48)/2}" y="43" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11" fill="#8b949e" letter-spacing="1">
      &gt; &quot;Are you ready?&quot;
    </text>
  </g>
</svg>'''

    with open("assets/build-card.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[2/3] assets/build-card.svg diperbarui ({CARD_W}x{CARD_H}) tanpa teks footer.")

# =============================================================
# 3. UPDATE README (CACHE BUSTER V4)
# =============================================================
def update_readme():
    content = '''<div align="center">

<!-- DUAL MINIMAL CARDS -->
<img src="./azvi-ascii.svg?v=4" width="414" alt="Azvi Portrait" />
<img src="./assets/build-card.svg?v=4" width="414" alt="Kamen Rider Build" />

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
<img src="./contrib-heatmap.svg?v=4" alt="Aggregated Heatmap" width="840" />

</div>
'''
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("[3/3] README.md diperbarui dengan cache-buster ?v=4.")

if __name__ == "__main__":
    patch_ascii_portrait()
    generate_build_card()
    update_readme()
