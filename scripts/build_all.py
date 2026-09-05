import os, re, json, base64, subprocess
import xml.etree.ElementTree as ET

CARD_W = 420
CARD_H = 480

# =============================================================
# 1. PURE TERMINAL TYPEWRITER (LEFT-TO-RIGHT, LINE-BY-LINE)
# =============================================================
def get_original_sitting_ascii():
    """Mengambil data teks ASCII meja lab asli (*+%*====)"""
    if os.path.exists("azvi-ascii.svg"):
        with open("azvi-ascii.svg", "r", encoding="utf-8") as f:
            txt = f.read()
            if "*+%*====" in txt:
                return txt

    res = subprocess.run(["git", "log", "-S", "*+%*====", "--format=%H", "--", "azvi-ascii.svg"], capture_output=True, text=True)
    commits = [c.strip() for c in res.stdout.strip().split() if c.strip()]
    for c in commits:
        show = subprocess.run(["git", "show", f"{c}:azvi-ascii.svg"], capture_output=True, text=True)
        if "*+%*====" in show.stdout:
            return show.stdout
    return None

def patch_ascii_portrait():
    raw_svg = get_original_sitting_ascii()
    if not raw_svg:
        print("[!] Gagal memuat data ASCII asli.")
        return

    # Ekstrak HANYA teks baris ASCII murni (buang tombol, garis biru, scanner, dan footer rendered)
    raw_lines = re.findall(r'<text[^>]*y="([0-9.]+)"[^>]*>(.*?)</text>', raw_svg, flags=re.DOTALL)
    ascii_rows = []
    for y_str, content in raw_lines:
        if "portrait.sh" in content or "rendered:" in content or "kernel:" in content:
            continue
        ascii_rows.append((float(y_str), content))

    if not ascii_rows:
        print("[!] Baris teks ASCII tidak ditemukan.")
        return

    total_rows = len(ascii_rows)
    total_dur = 8.0       # Siklus total 8 detik
    type_phase = 5.0      # Mengetik selesai di detik ke-5.0

    defs_clips = []
    body_groups = []

    for idx, (y_val, text_str) in enumerate(ascii_rows):
        clip_id = f"tw_line_{idx}"
        # Waktu mulai dan selesai ketikan per baris (kiri -> kanan)
        t_start = (idx / total_rows) * type_phase
        t_end = ((idx + 1) / total_rows) * type_phase

        k0 = round(t_start / total_dur, 4)
        k1 = round(t_end / total_dur, 4)
        k_hold = 0.92   # Tetap tampil utuh sampai detik 7.36 sebelum reset

        if idx == 0:
            key_times = f"0;{k1};{k_hold};1"
            anim_vals = f"0;{CARD_W};{CARD_W};0"
        else:
            key_times = f"0;{k0};{k1};{k_hold};1"
            anim_vals = f"0;0;{CARD_W};{CARD_W};0"

        # Masking per baris: lebar bergerak dari 0 ke CARD_W (kiri ke kanan)
        defs_clips.append(f'''    <clipPath id="{clip_id}">
      <rect x="0" y="{y_val - 8.5:.1f}" width="0" height="11.5">
        <animate attributeName="width"
                 values="{anim_vals}"
                 keyTimes="{key_times}"
                 dur="{total_dur}s"
                 repeatCount="indefinite" />
      </rect>
    </clipPath>''')

        body_groups.append(f'    <g clip-path="url(#{clip_id})">\n      <text x="24" y="{y_val:.1f}">{text_str}</text>\n    </g>')

    all_clips_xml = "\n".join(defs_clips)
    all_body_xml = "\n".join(body_groups)

    new_svg = f'''<svg width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
{all_clips_xml}
  </defs>

  <!-- Frame Kembar Minimalis Bersih -->
  <rect width="{CARD_W}" height="{CARD_H}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>

  <!-- Teks Potret Lab Diketik Berurutan Baris Demi Baris -->
  <g font-family="ui-monospace, SFMono-Regular, monospace" font-size="8.8" fill="#c9d1d9" xml:space="preserve">
{all_body_xml}
  </g>
</svg>'''

    try:
        ET.fromstring(new_svg)
        with open("azvi-ascii.svg", "w", encoding="utf-8") as f:
            f.write(new_svg)
        print(f"[1/3] azvi-ascii.svg sukses: animasi ketikan baris demi baris, garis biru lenyap total.")
    except ET.ParseError as err:
        print(f"[!] Error XML: {err}")

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

    with open("assets/build-card.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[2/3] assets/build-card.svg diperbarui ({CARD_W}x{CARD_H}).")

# =============================================================
# 3. UPDATE README (CACHE BUSTER V12)
# =============================================================
def update_readme():
    content = '''<div align="center">

<!-- DUAL MINIMAL CARDS -->
<img src="./azvi-ascii.svg?v=12" width="414" alt="Azvi Portrait" />
<img src="./assets/build-card.svg?v=12" width="414" alt="Kamen Rider Build" />

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
<img src="./contrib-heatmap.svg?v=12" alt="Aggregated Heatmap" width="840" />

</div>
'''
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("[3/3] README.md diperbarui dengan cache-buster ?v=12.")

if __name__ == "__main__":
    patch_ascii_portrait()
    generate_build_card()
    update_readme()
