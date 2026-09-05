import os, json, base64
import xml.etree.ElementTree as ET
from PIL import Image

CARD_W = 420
CARD_H = 480

# =============================================================
# 1. GENERATE PURE ASCII SVG DIRECTLY FROM assets/avatar.png
# =============================================================
ASCII_CHARS = [" ", ".", ":", "-", "=", "+", "*", "#", "%", "@"]

def image_to_ascii_lines(image_path, target_width=52):
    if not os.path.exists(image_path):
        return []
    
    img = Image.open(image_path).convert("L")
    # Aspek rasio font terminal monospace ~ 0.55
    aspect_ratio = img.height / img.width
    target_height = int(target_width * aspect_ratio * 0.55)
    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    pixels = img.getdata()
    lines = []
    for y in range(target_height):
        line = ""
        for x in range(target_width):
            pixel_val = pixels[y * target_width + x]
            # Kontras sedikit ditingkatkan agar latar belakang gelap menjadi spasi kosong
            if pixel_val < 45:
                line += " "
            else:
                char_idx = int((pixel_val / 255) * (len(ASCII_CHARS) - 1))
                line += ASCII_CHARS[char_idx]
        lines.append(line)
    return lines

def generate_ascii_card():
    lines = image_to_ascii_lines("assets/avatar.png", target_width=54)
    if not lines:
        print("[!] Gagal membaca assets/avatar.png")
        return

    # Hitung posisi teks vertikal di dalam kartu
    start_y = 58
    line_spacing = 9.5
    total_lines = len(lines)
    anim_dur = 7.0
    type_duration = 4.2

    # Buat strip mask horizontal untuk efek ketikan baris demi baris
    strips = []
    for i in range(total_lines):
        y_pos = start_y + (i * line_spacing) - 8
        t0 = 0.2 + (i / total_lines) * type_duration
        t1 = 0.2 + ((i + 1) / total_lines) * type_duration
        k_start = round(t0 / anim_dur, 4)
        k_end = round(t1 / anim_dur, 4)

        strips.append(f'''      <rect x="0" y="{y_pos:.1f}" width="0" height="{line_spacing + 1.0:.1f}">
        <animate attributeName="width"
                 values="0;0;{CARD_W};{CARD_W};0"
                 keyTimes="0;{k_start};{k_end};0.93;1"
                 dur="{anim_dur}s"
                 repeatCount="indefinite" />
      </rect>''')

    strips_xml = "\n".join(strips)

    # Render baris-baris ASCII
    text_spans = []
    for i, line in enumerate(lines):
        y_pos = start_y + (i * line_spacing)
        # Escape karakter khusus XML
        safe_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        text_spans.append(f'    <text x="24" y="{y_pos:.1f}">{safe_line}</text>')

    text_content = "\n".join(text_spans)

    svg = f'''<svg width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <clipPath id="asciiTypewriterClip">
{strips_xml}
    </clipPath>
  </defs>

  <!-- Frame Kembar -->
  <rect width="{CARD_W}" height="{CARD_H}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>

  <!-- Teks ASCII dari assets/avatar.png dengan Efek Ketikan -->
  <g clip-path="url(#asciiTypewriterClip)" font-family="ui-monospace, SFMono-Regular, monospace" font-size="8.8" fill="#e6edf3" xml:space="preserve">
{text_content}
  </g>
</svg>'''

    try:
        ET.fromstring(svg)
        with open("azvi-ascii.svg", "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"[1/3] azvi-ascii.svg BERHASIL DIGENERATE DARI assets/avatar.png ({CARD_W}x{CARD_H}).")
    except ET.ParseError as err:
        print(f"[!] Error XML azvi-ascii.svg: {err}")

# =============================================================
# 2. GENERATE BUILD CARD (TWIN 420x480)
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
  <g transform="translate(16, 68)">
    <image href="data:image/webp;base64,{sprite_b64}" width="128" height="128"/>
  </g>

  <!-- Quotes 3 Bahasa -->
  <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif">
    <text x="150" y="86" fill="#58a6ff" font-size="13" font-weight="600">さぁ、実験を始めようか？</text>
    <text x="150" y="105" fill="#c9d1d9" font-size="11" font-style="italic">Shall we begin the experiment?</text>
    <text x="150" y="123" fill="#8b949e" font-size="10">Nah, mari kita mulai eksperimennya!</text>

    <line x1="150" y1="140" x2="{CARD_W - 20}" y2="140" stroke="#21262d" stroke-width="1"/>

    <text x="150" y="164" fill="#ff7b72" font-size="13" font-weight="600">勝利の法則は決まった！</text>
    <text x="150" y="183" fill="#c9d1d9" font-size="11" font-style="italic">The formula for victory is set!</text>
    <text x="150" y="201" fill="#8b949e" font-size="10">Hukum kemenangannya telah ditentukan!</text>
  </g>

  <!-- Kotak Formula & Driver Callout -->
  <g transform="translate(24, {CARD_H - 96})">
    <rect width="{CARD_W - 48}" height="58" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1"/>
    <text x="{(CARD_W - 48)/2}" y="25" text-anchor="middle" font-family="ui-monospace, monospace" font-size="12" font-weight="600">
      <tspan fill="#ff7b72">Rabbit</tspan>
      <tspan fill="#6e7681"> × </tspan>
      <tspan fill="#58a6ff">Tank</tspan>
      <tspan fill="#6e7681"> ➔ </tspan>
      <tspan fill="#3fb950" font-weight="bold">BEST MATCH</tspan>
    </text>
    <text x="{(CARD_W - 48)/2}" y="44" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11" fill="#8b949e" letter-spacing="1">
      &gt; &quot;Are you ready?&quot;
    </text>
  </g>
</svg>'''

    try:
        ET.fromstring(svg)
        with open("assets/build-card.svg", "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"[2/3] assets/build-card.svg 100% VALID & sinkron ({CARD_W}x{CARD_H}).")
    except ET.ParseError as err:
        print(f"[!] Error XML build-card.svg: {err}")

# =============================================================
# 3. UPDATE README (CACHE BUSTER V9)
# =============================================================
def update_readme():
    content = '''<div align="center">

<!-- DUAL MINIMAL CARDS -->
<img src="./azvi-ascii.svg?v=9" width="414" alt="Azvi Portrait" />
<img src="./assets/build-card.svg?v=9" width="414" alt="Kamen Rider Build" />

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
<img src="./contrib-heatmap.svg?v=9" alt="Aggregated Heatmap" width="840" />

</div>
'''
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("[3/3] README.md diperbarui dengan cache-buster ?v=9.")

if __name__ == "__main__":
    generate_ascii_card()
    generate_build_card()
    update_readme()
