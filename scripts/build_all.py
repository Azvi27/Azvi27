import os, re, json, base64, subprocess
import xml.etree.ElementTree as ET

CARD_W = 420
CARD_H = 480

# =============================================================
# 1. RESTORE GENUINE LAB BENCH ASCII WITH STEPPED TYPEWRITER
# =============================================================
def get_original_sitting_ascii():
    """Mencari commit git yang menyimpan potret lab asli (*+%*====)"""
    res = subprocess.run(["git", "log", "--format=%H", "--", "azvi-ascii.svg"], capture_output=True, text=True)
    commits = [c.strip() for c in res.stdout.strip().split() if c.strip()]
    
    for c in commits:
        show = subprocess.run(["git", "show", f"{c}:azvi-ascii.svg"], capture_output=True, text=True)
        txt = show.stdout
        if "*+%*====" in txt:
            return txt
    return None

def generate_ascii_card():
    raw_svg = get_original_sitting_ascii()
    if not raw_svg:
        print("[!] Gagal menemukan data potret lab asli di riwayat git.")
        return

    # Ekstrak seluruh tag <text> asli yang membentuk gambar ASCII
    # Kebal dari error mismatched tag XML karena diekstrak tag per tag
    all_text_tags = re.findall(r'(<text[^>]*>.*?</text>)', raw_svg, flags=re.DOTALL)
    ascii_tags = []
    y_coords = []

    for tag in all_text_tags:
        if "portrait.sh" in tag or "rendered:" in tag:
            continue
        ascii_tags.append(tag)
        ym = re.search(r'y="([0-9.]+)"', tag)
        if ym:
            y_coords.append(float(ym.group(1)))

    if not ascii_tags:
        print("[!] Gagal mengekstrak baris teks ASCII.")
        return

    # Buat strip mask horizontal per baris sesuai koordinat Y asli
    total_lines = len(ascii_tags)
    anim_dur = 6.8
    type_duration = 4.0

    strips = []
    for i, y_val in enumerate(y_coords):
        t0 = 0.2 + (i / total_lines) * type_duration
        t1 = 0.2 + ((i + 1) / total_lines) * type_duration
        k_start = round(t0 / anim_dur, 4)
        k_end = round(t1 / anim_dur, 4)
        
        # y_val - 8 untuk menutup tinggi karakter teks
        strips.append(f'''      <rect x="0" y="{y_val - 8.5:.1f}" width="0" height="11.5">
        <animate attributeName="width"
                 values="0;0;{CARD_W};{CARD_W};0"
                 keyTimes="0;{k_start};{k_end};0.92;1"
                 dur="{anim_dur}s"
                 repeatCount="indefinite" />
      </rect>''')

    strips_xml = "\n".join(strips)
    ascii_body = "\n    ".join(ascii_tags)

    svg = f'''<svg width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <clipPath id="terminalTypewriterClip">
{strips_xml}
    </clipPath>
  </defs>

  <!-- Frame Kembar -->
  <rect width="{CARD_W}" height="{CARD_H}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>

  <!-- Potret Lab Asli dengan Efek Ketikan Monospace -->
  <g clip-path="url(#terminalTypewriterClip)">
    {ascii_body}
  </g>
</svg>'''

    try:
        ET.fromstring(svg)
        with open("azvi-ascii.svg", "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"[1/3] azvi-ascii.svg BERHASIL DIPULIHKAN & VALID XML ({CARD_W}x{CARD_H}).")
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
# 3. UPDATE README (CACHE BUSTER V10)
# =============================================================
def update_readme():
    content = '''<div align="center">

<!-- DUAL MINIMAL CARDS -->
<img src="./azvi-ascii.svg?v=10" width="414" alt="Azvi Portrait" />
<img src="./assets/build-card.svg?v=10" width="414" alt="Kamen Rider Build" />

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
<img src="./contrib-heatmap.svg?v=10" alt="Aggregated Heatmap" width="840" />

</div>
'''
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("[3/3] README.md diperbarui dengan cache-buster ?v=10.")

if __name__ == "__main__":
    generate_ascii_card()
    generate_build_card()
    update_readme()
