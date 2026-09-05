import os, re, json, base64
from datetime import datetime

# =============================================================
# 1. PATCH AZVI-ASCII.SVG (100% LOGIKA KODEMU YANG TERBUKTI TAJAM)
# =============================================================
def patch_ascii_portrait():
    if not os.path.exists("azvi-ascii.svg"):
        return 420, 480

    with open("azvi-ascii.svg", "r", encoding="utf-8") as f:
        content = f.read()

    # Bersihkan tombol titik, header, dan footer rendered
    content = re.sub(r'<circle[^>]*>', '', content)
    content = re.sub(r'<text[^>]*>portrait\.sh</text>', '', content)
    content = re.sub(r'<text[^>]*>rendered:[^<]*</text>', '', content)
    content = re.sub(r'<line[^>]*y1="4[04]"[^>]*/>', '', content)
    content = re.sub(r'<defs>.*?</defs>', '', content, flags=re.DOTALL)
    content = re.sub(r'<g id="type-wrapper"[^>]*>', '', content)
    content = re.sub(r'<g id="type-beam"[^>]*>.*?</g>', '', content, flags=re.DOTALL)
    content = re.sub(r'<g[^>]*clip-path=[^>]*>', '', content)

    w, h = 420, 480
    vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', content)
    if vb:
        w, h = int(vb.group(1)), int(vb.group(2))

    bg_match = re.search(r'(<rect[^>]*fill="#0d1117"[^>]*/>)', content)
    bg_rect = bg_match.group(1) if bg_match else f'<rect width="{w}" height="{h}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>'

    # Pertahankan seluruh struktur font monospace dan karakter secara utuh
    body = content
    body = re.sub(r'<\?xml[^>]*\?>', '', body)
    body = re.sub(r'<svg[^>]*>', '', body)
    body = re.sub(r'</svg>', '', body)
    if bg_match:
        body = body.replace(bg_match.group(1), '')

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

  <!-- Teks ASCII dengan Integritas Monospace Terjaga 100% -->
  <g clip-path="url(#asciiTypeClip)">
    {body.strip()}
  </g>

  <!-- Garis Laser Pemindai Sesuai Kodemu -->
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
    print(f"[1/3] azvi-ascii.svg berhasil diperbarui tajam ({w}x{h}).")
    return w, h

# =============================================================
# 2. GENERATE BUILD CARD
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

  <!-- Kotak Formula & Driver Callout -->
  <g transform="translate(24, {h - 86})">
    <rect width="{w - 48}" height="56" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1"/>
    <text x="{(w - 48)/2}" y="24" text-anchor="middle" font-family="ui-monospace, monospace" font-size="12" font-weight="600">
      <tspan fill="#ff7b72">Rabbit</tspan>
      <tspan fill="#6e7681"> × </tspan>
      <tspan fill="#58a6ff">Tank</tspan>
      <tspan fill="#6e7681"> ➔ </tspan>
      <tspan fill="#3fb950" font-weight="bold">BEST MATCH</tspan>
    </text>
    <text x="{(w - 48)/2}" y="43" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11" fill="#8b949e" letter-spacing="1">
      &gt; &quot;Are you ready?&quot;
    </text>
  </g>
</svg>'''

    with open("assets/build-card.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[2/3] assets/build-card.svg berhasil diperbarui ({w}x{h}).")

# =============================================================
# 3. UPDATE README (CACHE BUSTER V18)
# =============================================================
def update_readme():
    content = '''<div align="center">

<!-- DUAL MINIMAL CARDS -->
<img src="./azvi-ascii.svg?v=18" width="414" alt="Azvi Portrait" />
<img src="./assets/build-card.svg?v=18" width="414" alt="Kamen Rider Build" />

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
<img src="./contrib-heatmap.svg?v=18" alt="Aggregated Heatmap" width="840" />

</div>
'''
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("[3/3] README.md diperbarui dengan cache-buster ?v=18.")

if __name__ == "__main__":
    w, h = patch_ascii_portrait()
    generate_build_card(w, h)
    update_readme()
