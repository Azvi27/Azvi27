import os, re, json, base64, subprocess
import xml.etree.ElementTree as ET

CARD_W = 420
CARD_H = 480

# =============================================================
# 1. RESTORE FULL SHARP ASCII & APPLY STEPPED TERMINAL PRINT
# =============================================================
def get_pristine_ascii():
    """Mengambil master potret asli yang tajam dan utuh dari riwayat git"""
    res = subprocess.run(["git", "log", "-S", "*+%*====", "--format=%H", "--", "azvi-ascii.svg"], capture_output=True, text=True)
    commits = [c.strip() for c in res.stdout.strip().split() if c.strip()]
    if commits:
        show = subprocess.run(["git", "show", f"{commits[-1]}:azvi-ascii.svg"], capture_output=True, text=True)
        if "*+%*====" in show.stdout:
            return show.stdout
    return None

def patch_ascii_portrait():
    raw_svg = get_pristine_ascii()
    if not raw_svg:
        print("[!] Gagal memuat data master ASCII.")
        return

    # 1. Bersihkan tombol bulat, teks header, footer rendered, dan garis pemindai
    clean = re.sub(r'<circle[^>]*>', '', raw_svg)
    clean = re.sub(r'<text[^>]*>portrait\.sh</text>', '', clean)
    clean = re.sub(r'<text[^>]*>rendered:[^<]*</text>', '', clean)
    clean = re.sub(r'<line[^>]*y1="4[04]"[^>]*/>', '', clean)
    clean = re.sub(r'<line[^>]*stroke="#58a6ff"[^>]*/>', '', clean)

    # 2. Ekstrak grup konten potret asli (tanpa merusak font, spasi, dan detail karakter)
    body_match = re.search(r'(<g[^>]*xml:space="preserve"[^>]*>.*?</g>)', clean, flags=re.DOTALL)
    if not body_match:
        body_match = re.search(r'(<g[^>]*font-family[^>]*>.*?</g>)', clean, flags=re.DOTALL)
    
    if body_match:
        body_content = body_match.group(1)
    else:
        # Fallback jika tag g terpisah
        body_content = clean
        body_content = re.sub(r'<\?xml[^>]*\?>', '', body_content)
        body_content = re.sub(r'<svg[^>]*>', '', body_content)
        body_content = re.sub(r'</svg>', '', body_content)
        body_content = re.sub(r'<rect[^>]*fill="#0d1117"[^>]*/>', '', body_content)

    # 3. Buat animasi ketikan bertingkat (discrete step per baris, bukan tirai scanner halus)
    # Total siklus 7.5s: 4 detik mengetik bertahap -> 2.8 detik diam tampil penuh -> reset
    step_values = "; ".join([str(int(i * 12.5)) for i in range(33)] + ["480", "480", "480", "0"])
    step_times = []
    # 33 langkah selama 0 s/d 0.54 (4 detik)
    for i in range(33):
        step_times.append(f"{round((i / 33) * 0.54, 3)}")
    step_times.extend(["0.58", "0.92", "0.97", "1"])
    key_times_str = "; ".join(step_times)

    new_svg = f'''<svg width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Stepped Terminal Reveal: Mengetik baris demi baris secara diskrit -->
    <clipPath id="terminalTypewriterClip">
      <rect x="0" y="0" width="{CARD_W}" height="0">
        <animate attributeName="height"
                 calcMode="discrete"
                 values="{step_values}"
                 keyTimes="{key_times_str}"
                 dur="7.5s"
                 repeatCount="indefinite" />
      </rect>
    </clipPath>
  </defs>

  <!-- Frame Kembar Bersih -->
  <rect width="{CARD_W}" height="{CARD_H}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>

  <!-- Potret Lab Asli yang Tajam & Terpusat -->
  <g clip-path="url(#terminalTypewriterClip)" transform="translate(35, 48)">
    {body_content.strip()}
  </g>
</svg>'''

    try:
        ET.fromstring(new_svg)
        with open("azvi-ascii.svg", "w", encoding="utf-8") as f:
            f.write(new_svg)
        print(f"[1/3] azvi-ascii.svg berhasil dipulihkan tajam & penuh ({CARD_W}x{CARD_H}).")
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
    print(f"[2/3] assets/build-card.svg valid & diperbarui ({CARD_W}x{CARD_H}).")

# =============================================================
# 3. UPDATE README (CACHE BUSTER V13)
# =============================================================
def update_readme():
    content = '''<div align="center">

<!-- DUAL MINIMAL CARDS -->
<img src="./azvi-ascii.svg?v=13" width="414" alt="Azvi Portrait" />
<img src="./assets/build-card.svg?v=13" width="414" alt="Kamen Rider Build" />

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
<img src="./contrib-heatmap.svg?v=13" alt="Aggregated Heatmap" width="840" />

</div>
'''
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("[3/3] README.md diperbarui dengan cache-buster ?v=13.")

if __name__ == "__main__":
    patch_ascii_portrait()
    generate_build_card()
    update_readme()
