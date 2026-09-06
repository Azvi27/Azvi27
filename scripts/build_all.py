import os, re, base64
import xml.etree.ElementTree as ET

CARD_W = 410
CARD_H = 340

# =============================================================
# 1. PATCH AZVI-ASCII.SVG (TERMINAL OPERATOR ID BADGE)
# =============================================================
def patch_ascii_portrait():
    if not os.path.exists("azvi-ascii.svg"):
        return

    with open("azvi-ascii.svg", "r", encoding="utf-8") as f:
        content = f.read()

    # Bersihkan scanline, footer, header, dan HUD lama
    content = re.sub(r'<!-- OPERATOR HUD -->[\s\S]*?<!-- /OPERATOR HUD -->', '', content)
    content = re.sub(r'<!-- Terminal Session Header -->[\s\S]*?</text>', '', content)
    content = re.sub(r'<line[^>]*stroke="#58a6ff"[^>]*/>', '', content)
    content = re.sub(r'<animateTransform[^>]*type="translate"[^>]*/>', '', content)
    content = re.sub(r'<text[^>]*>rendered:[^<]*</text>', '', content)
    content = re.sub(r'<text[^>]*>SYSTEM://[^<]*</text>', '', content)

    content = re.sub(r'<svg[^>]*>', f'<svg width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}" fill="none" xmlns="http://www.w3.org/2000/svg">', content, count=1)
    content = re.sub(r'<rect[^>]*fill="#0d1117"[^>]*/>', f'<rect width="{CARD_W}" height="{CARD_H}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>', content, count=1)

    # Tangga ketikan 36 baris
    n_lines = 36
    start_y = 30
    end_y = CARD_H - 22
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
      <rect x="0" y="28" width="{CARD_W}" height="0">
        <animate attributeName="height"
                 calcMode="discrete"
                 values="{v_str}"
                 keyTimes="{kt_str}"
                 dur="7.5s"
                 repeatCount="indefinite" />
      </rect>
    </clipPath>'''
    content = re.sub(r'<clipPath id="asciiTypeClip">[\s\S]*?</clipPath>', new_clip, content)

    # Terminal Header
    cursor_header = f'''  <!-- Terminal Session Header -->
  <text x="18" y="22" font-family="ui-monospace, monospace" font-size="9" fill="#58a6ff" letter-spacing="1.2">SYSTEM://AZVI.LAB <tspan fill="#58a6ff"><animate attributeName="opacity" values="1;0;1" dur="0.9s" repeatCount="indefinite">█</animate></tspan></text>'''
    
    # Panel HUD Operator Kontras Tinggi
    hud_overlay = f'''
  <!-- OPERATOR HUD -->
  <g transform="translate(216, 40)">
    <!-- Container Box -->
    <rect width="178" height="264" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1"/>

    <!-- Status Header -->
    <circle cx="14" cy="18" r="3.5" fill="#3fb950">
      <animate attributeName="opacity" values="1;0.3;1" dur="1.8s" repeatCount="indefinite"/>
    </circle>
    <text x="24" y="21" fill="#3fb950" font-family="ui-monospace, monospace" font-size="8.5" font-weight="bold" letter-spacing="1">OPERATOR // ACTIVE</text>
    
    <!-- Identity -->
    <text x="14" y="44" fill="#f0f6fc" font-family="ui-monospace, monospace" font-size="11.5" font-weight="bold">M. Khalis Farhan Azvi</text>
    <text x="14" y="58" fill="#58a6ff" font-family="ui-monospace, monospace" font-size="9.5">@Azvi27</text>

    <line x1="12" y1="68" x2="166" y2="68" stroke="#30363d" stroke-width="1"/>

    <!-- Institution -->
    <text x="14" y="83" fill="#8b949e" font-family="ui-monospace, monospace" font-size="8" letter-spacing="0.8">AFFILIATION</text>
    <text x="14" y="98" fill="#e6edf3" font-family="ui-monospace, monospace" font-size="10.5" font-weight="600">Teknik Fisika</text>
    <text x="14" y="112" fill="#8b949e" font-family="ui-monospace, monospace" font-size="9.5">Universitas Gadjah Mada</text>

    <line x1="12" y1="122" x2="166" y2="122" stroke="#30363d" stroke-width="1"/>

    <!-- Lab SSTK Corrected -->
    <text x="14" y="137" fill="#8b949e" font-family="ui-monospace, monospace" font-size="8" letter-spacing="0.8">LABORATORY</text>
    <text x="14" y="152" fill="#3fb950" font-family="ui-monospace, monospace" font-size="11" font-weight="bold">Lab. SSTK</text>
    <text x="14" y="166" fill="#c9d1d9" font-family="ui-monospace, monospace" font-size="9.5">Sistem Sensor &amp;</text>
    <text x="14" y="179" fill="#c9d1d9" font-family="ui-monospace, monospace" font-size="9.5">Telekontrol</text>

    <line x1="12" y1="189" x2="166" y2="189" stroke="#30363d" stroke-width="1"/>

    <!-- Role / Task -->
    <text x="14" y="204" fill="#8b949e" font-family="ui-monospace, monospace" font-size="8" letter-spacing="0.8">ASSIGNMENT</text>
    <text x="14" y="219" fill="#58a6ff" font-family="ui-monospace, monospace" font-size="10" font-weight="600">Lab Assistant &amp; Intern</text>
    <text x="14" y="234" fill="#8b949e" font-family="ui-monospace, monospace" font-size="9">Embedded Sys. &amp; IoT</text>
    <text x="14" y="247" fill="#8b949e" font-family="ui-monospace, monospace" font-size="9">Software Engineering</text>
  </g>
  <!-- /OPERATOR HUD -->'''

    content = content.replace(f'<rect width="{CARD_W}" height="{CARD_H}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>',
                              f'<rect width="{CARD_W}" height="{CARD_H}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>\n{cursor_header}\n{hud_overlay}')

    try:
        ET.fromstring(content)
        with open("azvi-ascii.svg", "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[1/4] azvi-ascii.svg diperbarui dengan Boxed HUD Lab SSTK ({CARD_W}x{CARD_H}).")
    except ET.ParseError as err:
        print(f"[!] Error XML azvi-ascii: {err}")

# =============================================================
# 2. GENERATE BUILD CARD (COMPACT, DENSE & HIGH-TECH)
# =============================================================
def generate_build_card():
    sprite_path = "assets/Build_Capsem_Sprite.webp"
    sprite_b64 = ""
    if os.path.exists(sprite_path):
        with open(sprite_path, "rb") as f:
            sprite_b64 = base64.b64encode(f.read()).decode("utf-8")

    svg = f'''<svg width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="{CARD_W}" height="{CARD_H}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>

  <!-- Wireframe Symmetry Header -->
  <text x="18" y="22" font-family="ui-monospace, monospace" font-size="9" fill="#ff7b72" letter-spacing="1.2">SYSTEM://BUILD.DRIVER <tspan fill="#ff7b72"><animate attributeName="opacity" values="1;0;1" dur="0.9s" repeatCount="indefinite">█</animate></tspan></text>

  <!-- Sprite Kamen Rider Build -->
  <g transform="translate(16, 30)">
    <image href="data:image/webp;base64,{sprite_b64}" width="112" height="112"/>
  </g>

  <!-- Quotes 3 Bahasa Sento Kiryu -->
  <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif">
    <text x="142" y="46" fill="#58a6ff" font-size="12.5" font-weight="bold">さぁ、実験を始めようか？</text>
    <text x="142" y="63" fill="#c9d1d9" font-size="10.8" font-style="italic">Shall we begin the experiment?</text>
    <text x="142" y="78" fill="#8b949e" font-size="9.5">Nah, mari kita mulai eksperimennya!</text>

    <line x1="142" y1="90" x2="{CARD_W - 18}" y2="90" stroke="#21262d" stroke-width="1"/>

    <text x="142" y="108" fill="#ff7b72" font-size="12.5" font-weight="bold">勝利の法則は決まった！</text>
    <text x="142" y="125" fill="#c9d1d9" font-size="10.8" font-style="italic">The formula for victory is set!</text>
    <text x="142" y="140" fill="#8b949e" font-size="9.5">Hukum kemenangannya telah ditentukan!</text>
  </g>

  <!-- Kotak Konsol Padat & Futuristik -->
  <g transform="translate(18, 154)">
    <rect width="{CARD_W - 36}" height="166" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1"/>

    <!-- Bar Status Internal Driver -->
    <text x="16" y="22" font-family="ui-monospace, monospace" font-size="8.5" fill="#8b949e" letter-spacing="1">FULLBOTTLE ENGAGED</text>
    <text x="{CARD_W - 52}" y="22" text-anchor="end" font-family="ui-monospace, monospace" font-size="8.5" fill="#3fb950" font-weight="bold">SYNC: 100%</text>

    <line x1="14" y1="30" x2="{CARD_W - 50}" y2="30" stroke="#21262d" stroke-width="1"/>

    <!-- Fullbottle Slots Visual Badge -->
    <g transform="translate(16, 40)">
      <!-- Rabbit Slot -->
      <rect x="0" y="0" width="155" height="28" rx="6" fill="#0d1117" stroke="#ff7b72" stroke-width="1.2"/>
      <text x="77" y="18" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11" font-weight="bold" fill="#ff7b72" letter-spacing="1.5">
        ◆ RABBIT
      </text>

      <!-- Multiply Sign -->
      <text x="171" y="19" text-anchor="middle" font-family="ui-monospace, monospace" font-size="14" fill="#6e7681" font-weight="bold">×</text>

      <!-- Tank Slot -->
      <rect x="187" y="0" width="155" height="28" rx="6" fill="#0d1117" stroke="#58a6ff" stroke-width="1.2"/>
      <text x="264" y="18" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11" font-weight="bold" fill="#58a6ff" letter-spacing="1.5">
        TANK ◆
      </text>
    </g>

    <!-- Best Match with Breathing Pulse -->
    <text x="{(CARD_W - 36)/2}" y="100" text-anchor="middle" font-family="ui-monospace, monospace" font-size="15" font-weight="bold">
      <tspan fill="#6e7681">=</tspan>
      <tspan fill="#3fb950" letter-spacing="3"> BEST MATCH ! 
        <animate attributeName="fill" values="#3fb950;#56d364;#2ea043;#3fb950" dur="2.5s" repeatCount="indefinite"/>
      </tspan>
      <tspan fill="#6e7681">=</tspan>
    </text>

    <line x1="14" y1="114" x2="{CARD_W - 50}" y2="114" stroke="#21262d" stroke-width="1"/>

    <!-- Bottom Telemetry Specs (Density) -->
    <text x="16" y="132" font-family="ui-monospace, monospace" font-size="9" fill="#8b949e" letter-spacing="0.5">
      HAZARD LEVEL: <tspan fill="#ff7b72" font-weight="bold">4.2</tspan>
    </text>
    <text x="{CARD_W - 52}" y="132" text-anchor="end" font-family="ui-monospace, monospace" font-size="9" fill="#58a6ff" letter-spacing="0.5">
      FORMULA: <tspan fill="#c9d1d9">MOEBIUS × TANK</tspan>
    </text>
    <text x="{(CARD_W - 36)/2}" y="152" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9.5" fill="#8b949e" letter-spacing="1.5">
      [ DRIVER: &quot;ARE YOU READY?&quot; ]
    </text>
  </g>
</svg>'''

    try:
        ET.fromstring(svg)
        with open("assets/build-card.svg", "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"[2/4] assets/build-card.svg dipadatkan secara simetris ({CARD_W}x{CARD_H}).")
    except ET.ParseError as err:
        print(f"[!] Error XML build-card: {err}")

# =============================================================
# 3. GENERATE SLEEK RABBIT-TANK DIVIDER SVG
# =============================================================
def generate_divider():
    svg = '''<svg width="840" height="8" viewBox="0 0 840 8" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="rtGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ff7b72" stop-opacity="0.85"/>
      <stop offset="25%" stop-color="#ff7b72" stop-opacity="0.3"/>
      <stop offset="50%" stop-color="#3fb950" stop-opacity="0.75"/>
      <stop offset="75%" stop-color="#58a6ff" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#58a6ff" stop-opacity="0.85"/>
    </linearGradient>
  </defs>
  <rect x="20" y="3" width="800" height="2" rx="1" fill="url(#rtGrad)"/>
  <circle cx="420" cy="4" r="2.5" fill="#3fb950"/>
</svg>'''
    with open("assets/divider.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("[3/4] assets/divider.svg berhasil dibuat.")

# =============================================================
# 4. UPDATE README
# =============================================================
def update_readme():
    content = f'''<div align="center">

<!-- DUAL MINIMAL CARDS -->
<img src="./azvi-ascii.svg?v=42" width="{CARD_W}" alt="Azvi Portrait" /><img src="./assets/build-card.svg?v=42" width="{CARD_W}" alt="Kamen Rider Build" />

<!-- RABBIT-TANK GRADIENT DIVIDER -->
<br><br>
<img src="./assets/divider.svg?v=42" width="840" alt="Divider" />
<br><br>

<!-- DATA SOURCES STATUS BAR -->
<p align="center">
  <img src="https://img.shields.io/badge/GitHub-Azvi27-161b22?style=flat-square&logo=github&logoColor=white" alt="GitHub Core" />
  &nbsp;
  <img src="https://img.shields.io/badge/GitLab%20Cloud-gitlab.azvibelajar.my.id-161b22?style=flat-square&logo=gitlab&logoColor=fc6d26" alt="GitLab Cloud" />
  &nbsp;
  <img src="https://img.shields.io/badge/GitLab-Lab.%20SSTK%201-161b22?style=flat-square&logo=gitlab&logoColor=fc6d26" alt="GitLab Lab SSTK 1" />
  &nbsp;
  <img src="https://img.shields.io/badge/GitLab-Lab.%20SSTK%202-161b22?style=flat-square&logo=gitlab&logoColor=fc6d26" alt="GitLab Lab SSTK 2" />
</p>

<!-- AGGREGATED HEATMAP -->
<img src="./contrib-heatmap.svg?v=42" alt="Aggregated Heatmap" width="840" />

</div>
'''
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("[4/4] README.md diperbarui dengan versi cache v=42.")

if __name__ == "__main__":
    patch_ascii_portrait()
    generate_build_card()
    generate_divider()
    update_readme()
