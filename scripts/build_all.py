import os, re, base64
import xml.etree.ElementTree as ET

CARD_W = 410
CARD_H = 340

# =============================================================
# 1. PATCH AZVI-ASCII.SVG (FULL-WIDTH CYBER TELEMETRY GRID)
# =============================================================
def patch_ascii_portrait():
    if not os.path.exists("azvi-ascii.svg"):
        return

    with open("azvi-ascii.svg", "r", encoding="utf-8") as f:
        content = f.read()

    # Bersihkan elemen lama
    content = re.sub(r'<!-- (?:OPERATOR HUD|Terminal Session Header) -->[\s\S]*?<!-- /(?:OPERATOR HUD|Terminal Session Header) -->', '', content)
    content = re.sub(r'<text[^>]*SYSTEM://AZVI\.LAB[\s\S]*?</text>', '', content)
    content = re.sub(r'<g[^>]*id="operator-hud"[\s\S]*?</g>', '', content)
    content = re.sub(r'<line[^>]*stroke="#58a6ff"[^>]*/>', '', content)
    content = re.sub(r'<animateTransform[^>]*type="translate"[^>]*/>', '', content)
    content = re.sub(r'<text[^>]*>rendered:[^<]*</text>', '', content)

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

    # Injeksi Panel Operator Full-Width yang Mengisi Seluruh Ruang
    hud_injection = f'''
  <!-- Terminal Session Header -->
  <text x="18" y="22" font-family="ui-monospace, monospace" font-size="9" fill="#58a6ff" letter-spacing="1.2">SYSTEM://AZVI.LAB <tspan fill="#58a6ff"><animate attributeName="opacity" values="1;0;1" dur="0.9s" repeatCount="indefinite">█</animate></tspan></text>
  <!-- /Terminal Session Header -->

  <!-- OPERATOR HUD -->
  <g id="operator-hud" transform="translate(194, 32)">
    <!-- Container Box -->
    <rect width="204" height="284" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/>

    <!-- Header Bar: Full Width -->
    <rect width="204" height="28" rx="10" fill="#21262d"/>
    <rect y="18" width="204" height="10" fill="#21262d"/>
    
    <circle cx="14" cy="14" r="3.5" fill="#3fb950">
      <animate attributeName="opacity" values="1;0.3;1" dur="1.8s" repeatCount="indefinite"/>
    </circle>
    <text x="23" y="17.5" fill="#3fb950" font-family="ui-monospace, monospace" font-size="9" font-weight="bold" letter-spacing="1">OPERATOR</text>
    <text x="190" y="17.5" text-anchor="end" fill="#58a6ff" font-family="ui-monospace, monospace" font-size="9" font-weight="bold" letter-spacing="0.5">[ ONLINE ]</text>

    <!-- Identity Area: Full Width -->
    <text x="12" y="47" fill="#ffffff" font-family="ui-monospace, monospace" font-size="13.5" font-weight="bold">M. Khalis Farhan Azvi</text>
    
    <!-- Username + Cohort Pill -->
    <text x="12" y="63" fill="#58a6ff" font-family="ui-monospace, monospace" font-size="10.5">@Azvi27</text>
    <rect x="136" y="51" width="56" height="16" rx="4" fill="#0d1117" stroke="#30363d" stroke-width="0.8"/>
    <text x="164" y="62.5" text-anchor="middle" fill="#8b949e" font-family="ui-monospace, monospace" font-size="8.5" font-weight="bold">TF &apos;22</text>

    <line x1="10" y1="73" x2="194" y2="73" stroke="#30363d" stroke-width="1"/>

    <!-- Section 1: Affiliation (Left Info + Right Metas) -->
    <text x="12" y="88" fill="#8b949e" font-family="ui-monospace, monospace" font-size="8" font-weight="bold" letter-spacing="0.8">AFFILIATION</text>
    <text x="190" y="88" text-anchor="end" fill="#58a6ff" font-family="ui-monospace, monospace" font-size="8" letter-spacing="0.5">ACADEMIC</text>

    <text x="12" y="104" fill="#f0f6fc" font-family="ui-monospace, monospace" font-size="11.5" font-weight="600">Teknik Fisika</text>
    <text x="190" y="104" text-anchor="end" fill="#8b949e" font-family="ui-monospace, monospace" font-size="9.5">UGM</text>

    <text x="12" y="119" fill="#8b949e" font-family="ui-monospace, monospace" font-size="9.5">Universitas Gadjah Mada</text>
    <text x="190" y="119" text-anchor="end" fill="#3fb950" font-family="ui-monospace, monospace" font-size="9">● YOGYA</text>

    <line x1="10" y1="129" x2="194" y2="129" stroke="#30363d" stroke-width="1"/>

    <!-- Section 2: Laboratory (Left Info + Right Active Badge) -->
    <text x="12" y="144" fill="#8b949e" font-family="ui-monospace, monospace" font-size="8" font-weight="bold" letter-spacing="0.8">LABORATORY</text>
    <rect x="132" y="134" width="60" height="15" rx="3" fill="#0e4429" stroke="#26a641" stroke-width="0.8"/>
    <text x="162" y="144.5" text-anchor="middle" fill="#39d353" font-family="ui-monospace, monospace" font-size="8" font-weight="bold">ACTIVE LAB</text>

    <text x="12" y="162" fill="#3fb950" font-family="ui-monospace, monospace" font-size="12.5" font-weight="bold">Lab. SSTK</text>
    <text x="190" y="162" text-anchor="end" fill="#8b949e" font-family="ui-monospace, monospace" font-size="8.5">DEB // LAB</text>

    <text x="12" y="177" fill="#f0f6fc" font-family="ui-monospace, monospace" font-size="10" font-weight="500">Sistem Sensor &amp; Telekontrol</text>

    <line x1="10" y1="188" x2="194" y2="188" stroke="#30363d" stroke-width="1"/>

    <!-- Section 3: Role & Tech Badges (Mengisi Seluruh Ruang Bawah) -->
    <text x="12" y="203" fill="#8b949e" font-family="ui-monospace, monospace" font-size="8" font-weight="bold" letter-spacing="0.8">ROLE &amp; FOCUS</text>
    <text x="190" y="203" text-anchor="end" fill="#58a6ff" font-family="ui-monospace, monospace" font-size="8.5" font-weight="600">STAFF / INTERN</text>

    <text x="12" y="220" fill="#58a6ff" font-family="ui-monospace, monospace" font-size="11" font-weight="600">Lab Assistant &amp; Intern</text>

    <!-- Baris 1 Badge Domain -->
    <g transform="translate(10, 232)">
      <rect x="0" y="0" width="58" height="18" rx="4" fill="#0d1117" stroke="#30363d" stroke-width="1"/>
      <text x="29" y="12.5" text-anchor="middle" fill="#c9d1d9" font-family="ui-monospace, monospace" font-size="8.5">Sensors</text>

      <rect x="63" y="0" width="56" height="18" rx="4" fill="#0d1117" stroke="#30363d" stroke-width="1"/>
      <text x="91" y="12.5" text-anchor="middle" fill="#c9d1d9" font-family="ui-monospace, monospace" font-size="8.5">Embedded</text>

      <rect x="124" y="0" width="60" height="18" rx="4" fill="#0d1117" stroke="#30363d" stroke-width="1"/>
      <text x="154" y="12.5" text-anchor="middle" fill="#3fb950" font-family="ui-monospace, monospace" font-size="8.5">IoT Sys.</text>
    </g>

    <!-- Baris 2 Badge Tech Stack -->
    <g transform="translate(10, 255)">
      <rect x="0" y="0" width="42" height="18" rx="4" fill="#0d1117" stroke="#30363d" stroke-width="1"/>
      <text x="21" y="12.5" text-anchor="middle" fill="#ff7b72" font-family="ui-monospace, monospace" font-size="8.5">Go</text>

      <rect x="47" y="0" width="56" height="18" rx="4" fill="#0d1117" stroke="#30363d" stroke-width="1"/>
      <text x="75" y="12.5" text-anchor="middle" fill="#58a6ff" font-family="ui-monospace, monospace" font-size="8.5">Python</text>

      <rect x="108" y="0" width="76" height="18" rx="4" fill="#0d1117" stroke="#30363d" stroke-width="1"/>
      <text x="146" y="12.5" text-anchor="middle" fill="#c9d1d9" font-family="ui-monospace, monospace" font-size="8.5">KiCad/PCB</text>
    </g>
  </g>
  <!-- /OPERATOR HUD -->
'''
    content = re.sub(r'</svg>', f'{hud_injection}\n</svg>', content)

    try:
        ET.fromstring(content)
        with open("azvi-ascii.svg", "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[1/4] azvi-ascii.svg diperbarui dengan Full-Width HUD ({CARD_W}x{CARD_H}).")
    except ET.ParseError as err:
        print(f"[!] Error XML azvi-ascii: {err}")

# =============================================================
# 2. GENERATE BUILD CARD (ANIMATED FULLBOTTLE INSERTION)
# =============================================================
def generate_build_card():
    sprite_path = "assets/Build_Capsem_Sprite.webp"
    sprite_b64 = ""
    if os.path.exists(sprite_path):
        with open(sprite_path, "rb") as f:
            sprite_b64 = base64.b64encode(f.read()).decode("utf-8")

    svg = f'''<svg width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="{CARD_W}" height="{CARD_H}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>

  <!-- Micro Console Header Simetris -->
  <text x="18" y="22" font-family="ui-monospace, monospace" font-size="9" fill="#ff7b72" letter-spacing="1.2">SYSTEM://BUILD.DRIVER <tspan fill="#ff7b72"><animate attributeName="opacity" values="1;0;1" dur="0.9s" repeatCount="indefinite">█</animate></tspan></text>

  <!-- Bagian Atas: Sprite + Teks Quotes Proporsional -->
  <g transform="translate(18, 36)">
    <g transform="translate(0, 2)">
      <image href="data:image/webp;base64,{sprite_b64}" width="96" height="96"/>
    </g>

    <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif">
      <text x="110" y="16" fill="#58a6ff" font-size="11.5" font-weight="600">さぁ、実験を始めようか？</text>
      <text x="110" y="31" fill="#c9d1d9" font-size="9.5" font-style="italic">Shall we begin the experiment?</text>
      <text x="110" y="45" fill="#8b949e" font-size="8.8">Nah, mari kita mulai eksperimennya!</text>

      <line x1="110" y1="55" x2="{CARD_W - 36}" y2="55" stroke="#21262d" stroke-width="1"/>

      <text x="110" y="71" fill="#ff7b72" font-size="11.5" font-weight="600">勝利の法則は決まった！</text>
      <text x="110" y="86" fill="#c9d1d9" font-size="9.5" font-style="italic">The formula for victory is set!</text>
      <text x="110" y="100" fill="#8b949e" font-size="8.8">Hukum kemenangannya telah ditentukan!</text>
    </g>
  </g>

  <!-- Konsol Driver dengan Animasi Fullbottle Insertion -->
  <g transform="translate(18, 154)">
    <rect width="{CARD_W - 36}" height="154" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1">
      <animate attributeName="stroke"
               values="#30363d; #30363d; #ff7b72; #58a6ff; #3fb950; #3fb950; #30363d"
               keyTimes="0; 0.12; 0.20; 0.34; 0.42; 0.85; 1"
               dur="7s" repeatCount="indefinite"/>
    </rect>

    <text x="16" y="20" font-family="ui-monospace, monospace" font-size="8.5" fill="#8b949e" letter-spacing="1">DRIVER // CHAMBER</text>
    <text x="{CARD_W - 52}" y="20" text-anchor="end" font-family="ui-monospace, monospace" font-size="8.5" font-weight="bold">
      <animate attributeName="fill"
               values="#8b949e; #8b949e; #ff7b72; #58a6ff; #3fb950; #3fb950; #8b949e"
               keyTimes="0; 0.12; 0.20; 0.34; 0.42; 0.85; 1"
               dur="7s" repeatCount="indefinite"/>
      SYNC: 100%
    </text>

    <line x1="14" y1="28" x2="{CARD_W - 50}" y2="28" stroke="#21262d" stroke-width="1"/>

    <defs>
      <clipPath id="slotClip">
        <rect x="10" y="30" width="354" height="42" rx="4"/>
      </clipPath>
    </defs>

    <!-- Empty Slot Bay Background -->
    <g transform="translate(14, 36)">
      <rect x="0" y="0" width="158" height="28" rx="6" fill="#0d1117" stroke="#30363d" stroke-dasharray="3 3" stroke-width="1"/>
      <text x="79" y="18" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9.5" fill="#484f58">[ SLOT 1 ]</text>

      <text x="173" y="19" text-anchor="middle" font-family="ui-monospace, monospace" font-size="14" fill="#484f58" font-weight="bold">×</text>

      <rect x="188" y="0" width="158" height="28" rx="6" fill="#0d1117" stroke="#30363d" stroke-dasharray="3 3" stroke-width="1"/>
      <text x="267" y="18" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9.5" fill="#484f58">[ SLOT 2 ]</text>
    </g>

    <!-- ANIMATED FULLBOTTLES (Meluncur Masuk ke Driver) -->
    <g clip-path="url(#slotClip)">
      <!-- RABBIT BOTTLE (Slot 1) -->
      <g transform="translate(14, 36)">
        <g>
          <animateTransform attributeName="transform"
                            type="translate"
                            values="0,-40; 0,-40; 0,0; 0,0; 0,-40; 0,-40"
                            keyTimes="0; 0.08; 0.18; 0.85; 0.94; 1"
                            dur="7s" repeatCount="indefinite" />
          <animate attributeName="opacity"
                   values="0; 0; 1; 1; 0; 0"
                   keyTimes="0; 0.08; 0.18; 0.85; 0.94; 1"
                   dur="7s" repeatCount="indefinite" />
          
          <rect x="0" y="0" width="158" height="28" rx="6" fill="#1f1315" stroke="#ff7b72" stroke-width="1.5"/>
          <text x="79" y="18" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11" font-weight="bold" fill="#ff7b72" letter-spacing="1.5">
            ◆ RABBIT
          </text>
        </g>
      </g>

      <!-- TANK BOTTLE (Slot 2) -->
      <g transform="translate(14, 36)">
        <g>
          <animateTransform attributeName="transform"
                            type="translate"
                            values="0,-40; 0,-40; 0,0; 0,0; 0,-40; 0,-40"
                            keyTimes="0; 0.22; 0.32; 0.85; 0.94; 1"
                            dur="7s" repeatCount="indefinite" />
          <animate attributeName="opacity"
                   values="0; 0; 1; 1; 0; 0"
                   keyTimes="0; 0.22; 0.32; 0.85; 0.94; 1"
                   dur="7s" repeatCount="indefinite" />

          <rect x="188" y="0" width="158" height="28" rx="6" fill="#0f1923" stroke="#58a6ff" stroke-width="1.5"/>
          <text x="267" y="18" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11" font-weight="bold" fill="#58a6ff" letter-spacing="1.5">
            TANK ◆
          </text>
        </g>
      </g>
    </g>

    <!-- BEST MATCH BURST -->
    <g>
      <animate attributeName="opacity"
               values="0.2; 0.2; 0.2; 1; 1; 0.2; 0.2"
               keyTimes="0; 0.18; 0.32; 0.40; 0.85; 0.94; 1"
               dur="7s" repeatCount="indefinite" />
      
      <text x="{(CARD_W - 36)/2}" y="98" text-anchor="middle" font-family="ui-monospace, monospace" font-size="14.5" font-weight="bold">
        <tspan fill="#6e7681">=</tspan>
        <tspan fill="#3fb950" letter-spacing="3"> BEST MATCH ! 
          <animate attributeName="fill" values="#3fb950;#56d364;#2ea043;#3fb950" dur="2s" repeatCount="indefinite"/>
        </tspan>
        <tspan fill="#6e7681">=</tspan>
      </text>
    </g>

    <line x1="14" y1="112" x2="{CARD_W - 50}" y2="112" stroke="#21262d" stroke-width="1"/>

    <!-- Telemetry Sub-details -->
    <text x="16" y="129" font-family="ui-monospace, monospace" font-size="8.5" fill="#8b949e">
      HAZARD LEVEL: <tspan fill="#ff7b72" font-weight="bold">4.2</tspan>
    </text>
    <text x="{CARD_W - 52}" y="129" text-anchor="end" font-family="ui-monospace, monospace" font-size="8.5" fill="#58a6ff">
      FORMULA: <tspan fill="#c9d1d9">MOEBIUS × TANK</tspan>
    </text>
    
    <text x="{(CARD_W - 36)/2}" y="145" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9.5" letter-spacing="1.5">
      <animate attributeName="fill"
               values="#484f58; #484f58; #484f58; #ff7b72; #3fb950; #3fb950; #484f58"
               keyTimes="0; 0.18; 0.32; 0.42; 0.50; 0.85; 1"
               dur="7s" repeatCount="indefinite" />
      [ DRIVER: &quot;ARE YOU READY?&quot; ]
    </text>
  </g>
</svg>'''

    try:
        ET.fromstring(svg)
        with open("assets/build-card.svg", "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"[2/4] assets/build-card.svg dibuat dengan animasi Fullbottle Driver ({CARD_W}x{CARD_H}).")
    except ET.ParseError as err:
        print(f"[!] Error XML build-card: {err}")

# =============================================================
# 3. GENERATE DIVIDER
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
# 4. UPDATE README CACHE BUSTER
# =============================================================
def update_readme():
    content = f'''<div align="center">

<!-- DUAL MINIMAL CARDS -->
<img src="./azvi-ascii.svg?v=45" width="{CARD_W}" alt="Azvi Portrait" /><img src="./assets/build-card.svg?v=45" width="{CARD_W}" alt="Kamen Rider Build" />

<!-- RABBIT-TANK GRADIENT DIVIDER -->
<br><br>
<img src="./assets/divider.svg?v=45" width="840" alt="Divider" />
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
<img src="./contrib-heatmap.svg?v=45" alt="Aggregated Heatmap" width="840" />

</div>
'''
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("[4/4] README.md diperbarui dengan versi cache v=45.")

if __name__ == "__main__":
    patch_ascii_portrait()
    generate_build_card()
    generate_divider()
    update_readme()
