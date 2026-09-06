import os, re, json, base64
import xml.etree.ElementTree as ET

# KUNCI DIMENSI KEMBAR IDENTIK (PADAT, RAPI, TANPA RUANG KOSONG)
CARD_W = 410
CARD_H = 340

# =============================================================
# 1. PATCH AZVI-ASCII.SVG (KUNCI 410x340 + ANIMASI KETIKAN BERTAHAP)
# =============================================================
def patch_ascii_portrait():
    if not os.path.exists("azvi-ascii.svg"):
        return

    with open("azvi-ascii.svg", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Pastikan bersih dari garis laser biru, footer rendered, dan scanner lama
    content = re.sub(r'<line[^>]*stroke="#58a6ff"[^>]*/>', '', content)
    content = re.sub(r'<animateTransform[^>]*type="translate"[^>]*/>', '', content)
    content = re.sub(r'<text[^>]*>rendered:[^<]*</text>', '', content)

    # 2. Samakan root SVG & viewBox ke 410x340
    content = re.sub(r'<svg[^>]*>', f'<svg width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}" fill="none" xmlns="http://www.w3.org/2000/svg">', content, count=1)

    # 3. Samakan frame background rect
    content = re.sub(r'<rect[^>]*fill="#0d1117"[^>]*/>', f'<rect width="{CARD_W}" height="{CARD_H}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>', content, count=1)

    # 4. Hitung tangga ketikan terminal bertahap pas dengan tinggi 340px
    n_lines = 36
    start_y = 20
    end_y = CARD_H - 25
    line_h = (end_y - start_y) / n_lines

    heights = [0]
    times = [0.0]
    for i in range(1, n_lines + 1):
        h = int(start_y + (i * line_h))
        t = round(0.04 + (i / n_lines) * 0.46, 3)
        heights.append(h)
        times.append(t)

    heights.extend([CARD_H, CARD_H, 0])
    times.extend([0.55, 0.92, 1.0])

    v_str = "; ".join(str(h) for h in heights)
    kt_str = "; ".join(str(t) for t in times)

    new_clip = f'''<clipPath id="asciiTypeClip">
      <rect x="0" y="20" width="{CARD_W}" height="0">
        <animate attributeName="height"
                 calcMode="discrete"
                 values="{v_str}"
                 keyTimes="{kt_str}"
                 dur="7.5s"
                 repeatCount="indefinite" />
      </rect>
    </clipPath>'''

    content = re.sub(r'<clipPath id="asciiTypeClip">[\s\S]*?</clipPath>', new_clip, content)

    # Validasi XML
    try:
        ET.fromstring(content)
        with open("azvi-ascii.svg", "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[1/3] azvi-ascii.svg 100% VALID & padat ({CARD_W}x{CARD_H}).")
    except ET.ParseError as err:
        print(f"[!] Error XML azvi-ascii: {err}")

# =============================================================
# 2. GENERATE BUILD CARD (KUNCI 410x340 - BEBAS RUANG KOSONG)
# =============================================================
def generate_build_card():
    sprite_path = "assets/Build_Capsem_Sprite.webp"
    sprite_b64 = ""
    if os.path.exists(sprite_path):
        with open(sprite_path, "rb") as f:
            sprite_b64 = base64.b64encode(f.read()).decode("utf-8")

    svg = f'''<svg width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Frame Kembar 410x340 -->
  <rect width="{CARD_W}" height="{CARD_H}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>

  <!-- Sprite Kamen Rider Build (Sisi Kiri Atas) -->
  <g transform="translate(16, 26)">
    <image href="data:image/webp;base64,{sprite_b64}" width="116" height="116"/>
  </g>

  <!-- Quotes 3 Bahasa Sento Kiryu (Sisi Kanan Atas) -->
  <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif">
    <!-- Quote 1 -->
    <text x="146" y="44" fill="#58a6ff" font-size="13" font-weight="600">さぁ、実験を始めようか？</text>
    <text x="146" y="63" fill="#c9d1d9" font-size="11.2" font-style="italic">Shall we begin the experiment?</text>
    <text x="146" y="80" fill="#8b949e" font-size="10">Nah, mari kita mulai eksperimennya!</text>

    <!-- Divider halus -->
    <line x1="146" y1="94" x2="{CARD_W - 18}" y2="94" stroke="#21262d" stroke-width="1"/>

    <!-- Quote 2 -->
    <text x="146" y="114" fill="#ff7b72" font-size="13" font-weight="600">勝利の法則は決まった！</text>
    <text x="146" y="133" fill="#c9d1d9" font-size="11.2" font-style="italic">The formula for victory is set!</text>
    <text x="146" y="150" fill="#8b949e" font-size="10">Hukum kemenangannya telah ditentukan!</text>
  </g>

  <!-- Kotak Konsol Formula & Callout (Mengisi Area Bawah Secara Pas & Seimbang) -->
  <g transform="translate(18, 178)">
    <rect width="{CARD_W - 36}" height="128" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1"/>

    <!-- 1. BEST MATCH FORMULA (DI ATAS) -->
    <text x="{(CARD_W - 36)/2}" y="34" text-anchor="middle" font-family="ui-monospace, monospace" font-size="12.5" font-weight="bold">
      <tspan fill="#ff7b72">◆ Rabbit [Fisika]</tspan>
      <tspan fill="#6e7681"> × </tspan>
      <tspan fill="#58a6ff">Tank [Kode] ◆</tspan>
    </text>

    <!-- 2. BEST MATCH ACCENT -->
    <text x="{(CARD_W - 36)/2}" y="65" text-anchor="middle" font-family="ui-monospace, monospace" font-size="14.5" font-weight="bold">
      <tspan fill="#6e7681">=</tspan>
      <tspan fill="#3fb950" letter-spacing="2.5"> BEST MATCH ! </tspan>
      <tspan fill="#6e7681">=</tspan>
    </text>

    <!-- Divider konsol -->
    <line x1="20" y1="84" x2="{CARD_W - 56}" y2="84" stroke="#21262d" stroke-width="1"/>

    <!-- 3. DRIVER CALLOUT (DI BAWAH) -->
    <text x="{(CARD_W - 36)/2}" y="108" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11" fill="#8b949e" letter-spacing="1.5">
      [ DRIVER: &quot;ARE YOU READY?&quot; ]
    </text>
  </g>
</svg>'''

    try:
        ET.fromstring(svg)
        with open("assets/build-card.svg", "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"[2/3] assets/build-card.svg 100% VALID & padat ({CARD_W}x{CARD_H}).")
    except ET.ParseError as err:
        print(f"[!] Error XML build-card: {err}")

# =============================================================
# 3. UPDATE README (CACHE BUSTER V30)
# =============================================================
def update_readme():
    content = f'''<div align="center">

<!-- DUAL MINIMAL CARDS (IDENTIK 410x340 SEJAJAR BERDAMPINGAN) -->
<img src="./azvi-ascii.svg?v=30" width="{CARD_W}" alt="Azvi Portrait" /><img src="./assets/build-card.svg?v=30" width="{CARD_W}" alt="Kamen Rider Build" />

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
<img src="./contrib-heatmap.svg?v=30" alt="Aggregated Heatmap" width="840" />

</div>
'''
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("[3/3] README.md diperbarui dengan cache-buster ?v=30.")

if __name__ == "__main__":
    patch_ascii_portrait()
    generate_build_card()
    update_readme()
