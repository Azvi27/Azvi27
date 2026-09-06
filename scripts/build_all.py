import os, re, base64
import xml.etree.ElementTree as ET

CARD_W = 410
CARD_H = 340

# =============================================================
# 1. PATCH AZVI-ASCII.SVG (CLEAN OPERATOR HUD)
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

    # Injeksi HUD Operator
    hud_injection = f'''
  <!-- Terminal Session Header -->
  <text x="18" y="22" font-family="ui-monospace, monospace" font-size="9" fill="#58a6ff" letter-spacing="1.2">SYSTEM://AZVI.LAB <tspan fill="#58a6ff"><animate attributeName="opacity" values="1;0;1" dur="0.9s" repeatCount="indefinite">█</animate></tspan></text>
  <!-- /Terminal Session Header -->

  <!-- OPERATOR HUD -->
  <g id="operator-hud" transform="translate(194, 32)">
    <rect width="204" height="284" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/>

    <rect width="204" height="28" rx="10" fill="#21262d"/>
    <rect y="18" width="204" height="10" fill="#21262d"/>
    
    <circle cx="14" cy="14" r="3.5" fill="#3fb950">
      <animate attributeName="opacity" values="1;0.3;1" dur="1.8s" repeatCount="indefinite"/>
    </circle>
    <text x="24" y="17.5" fill="#3fb950" font-family="ui-monospace, monospace" font-size="9" font-weight="bold" letter-spacing="1">OPERATOR</text>
    <text x="190" y="17.5" text-anchor="end" fill="#58a6ff" font-family="ui-monospace, monospace" font-size="9" font-weight="bold" letter-spacing="0.5">[ ONLINE ]</text>

    <text x="14" y="52" fill="#ffffff" font-family="ui-monospace, monospace" font-size="14" font-weight="bold">M. Khalis Farhan Azvi</text>
    <text x="14" y="70" fill="#58a6ff" font-family="ui-monospace, monospace" font-size="11.5">@Azvi27</text>
    <text x="190" y="70" text-anchor="end" fill="#8b949e" font-family="ui-monospace, monospace" font-size="9.5">UGM</text>

    <line x1="12" y1="82" x2="192" y2="82" stroke="#30363d" stroke-width="1"/>

    <text x="14" y="99" fill="#8b949e" font-family="ui-monospace, monospace" font-size="8.5" font-weight="bold" letter-spacing="0.8">AFFILIATION</text>
    <text x="190" y="99" text-anchor="end" fill="#58a6ff" font-family="ui-monospace, monospace" font-size="8.5" letter-spacing="0.5">ACADEMIC</text>

    <text x="14" y="118" fill="#f0f6fc" font-family="ui-monospace, monospace" font-size="12.5" font-weight="600">Teknik Fisika</text>
    <text x="14" y="135" fill="#8b949e" font-family="ui-monospace, monospace" font-size="10.5">Universitas Gadjah Mada</text>

    <line x1="12" y1="147" x2="192" y2="147" stroke="#30363d" stroke-width="1"/>

    <text x="14" y="164" fill="#8b949e" font-family="ui-monospace, monospace" font-size="8.5" font-weight="bold" letter-spacing="0.8">LABORATORY</text>
    <text x="190" y="164" text-anchor="end" fill="#39d353" font-family="ui-monospace, monospace" font-size="8.5" font-weight="bold">ACTIVE LAB</text>

    <text x="14" y="184" fill="#3fb950" font-family="ui-monospace, monospace" font-size="13.5" font-weight="bold">Lab. SSTK</text>
    <text x="14" y="201" fill="#f0f6fc" font-family="ui-monospace, monospace" font-size="10.8" font-weight="500">Sensor dan Sistem Telekontrol</text>

    <line x1="12" y1="213" x2="192" y2="213" stroke="#30363d" stroke-width="1"/>

    <text x="14" y="230" fill="#8b949e" font-family="ui-monospace, monospace" font-size="8.5" font-weight="bold" letter-spacing="0.8">CURRENT ACTIVITY</text>
    <text x="190" y="230" text-anchor="end" fill="#58a6ff" font-family="ui-monospace, monospace" font-size="8.5" font-weight="600">STATUS</text>

    <text x="14" y="252" fill="#58a6ff" font-family="ui-monospace, monospace" font-size="13" font-weight="bold">Lab Assistant &amp; Intern</text>
    <text x="14" y="270" fill="#c9d1d9" font-family="ui-monospace, monospace" font-size="10.5">Asisten Lab &amp; Magang SSTK</text>
  </g>
  <!-- /OPERATOR HUD -->
'''
    content = re.sub(r'</svg>', f'{hud_injection}\n</svg>', content)

    try:
        ET.fromstring(content)
        with open("azvi-ascii.svg", "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[1/4] azvi-ascii.svg diperbarui ({CARD_W}x{CARD_H}).")
    except ET.ParseError as err:
        print(f"[!] Error XML azvi-ascii: {err}")

# =============================================================
# 2. GENERATE BUILD CARD (DX BUILD DRIVER SIMULATOR VECTOR)
# =============================================================
def generate_build_card():
    sprite_path = "assets/Build_Capsem_Sprite.webp"
    sprite_b64 = ""
    if os.path.exists(sprite_path):
        with open(sprite_path, "rb") as f:
            sprite_b64 = base64.b64encode(f.read()).decode("utf-8")

    svg = f'''<svg width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Chrome Gradient untuk Knalpot & Bezel -->
    <linearGradient id="chromeGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="35%" stop-color="#cbd5e1"/>
      <stop offset="70%" stop-color="#64748b"/>
      <stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>

    <!-- Pola Garis Bahaya DX (Hazard Stripes 45 Derajat //////) -->
    <pattern id="hazardPattern" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <rect width="7" height="14" fill="#000000"/>
      <rect x="7" width="7" height="14" fill="#dc2626"/>
    </pattern>

    <!-- Clip Kaca Vortex Dynamo -->
    <clipPath id="dynamoClip">
      <circle cx="78" cy="84" r="28"/>
    </clipPath>
  </defs>

  <rect width="{CARD_W}" height="{CARD_H}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>

  <!-- Top Session Header Simetris -->
  <text x="18" y="22" font-family="ui-monospace, monospace" font-size="9" fill="#ff7b72" letter-spacing="1.2">SYSTEM://BUILD.DRIVER <tspan fill="#ff7b72"><animate attributeName="opacity" values="1;0;1" dur="0.9s" repeatCount="indefinite">█</animate></tspan></text>

  <!-- Bagian Atas: Sprite + Quotes -->
  <g transform="translate(18, 34)">
    <g transform="translate(0, 0)">
      <image href="data:image/webp;base64,{sprite_b64}" width="92" height="92"/>
    </g>

    <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif">
      <text x="106" y="15" fill="#58a6ff" font-size="11.5" font-weight="600">さぁ、実験を始めようか？</text>
      <text x="106" y="30" fill="#c9d1d9" font-size="9.5" font-style="italic">Shall we begin the experiment?</text>
      <text x="106" y="44" fill="#8b949e" font-size="8.8">Nah, mari kita mulai eksperimennya!</text>

      <line x1="106" y1="53" x2="{CARD_W - 36}" y2="53" stroke="#21262d" stroke-width="1"/>

      <text x="106" y="69" fill="#ff7b72" font-size="11.5" font-weight="600">勝利の法則は決まった！</text>
      <text x="106" y="84" fill="#c9d1d9" font-size="9.5" font-style="italic">The formula for victory is set!</text>
      <text x="106" y="98" fill="#8b949e" font-size="8.8">Hukum kemenangannya telah ditentukan!</text>
    </g>
  </g>

  <!-- ============================================================== -->
  <!-- BAGIAN BAWAH: DX BUILD DRIVER CONSOLE (BANDAI DX ANIMATED)     -->
  <!-- ============================================================== -->
  <g transform="translate(18, 146)">
    <!-- Chassis Gunmetal Utama -->
    <rect width="374" height="174" rx="10" fill="#070b14" stroke="#30363d" stroke-width="1.5"/>

    <!-- Tali Sabuk Kuning Berlubang (Yellow Belt Straps) -->
    <g>
      <!-- Tali Kiri -->
      <rect x="0" y="52" width="9" height="66" rx="2" fill="#facc15" stroke="#ca8a04" stroke-width="1"/>
      <circle cx="4.5" cy="66" r="1.5" fill="#854d0e"/>
      <circle cx="4.5" cy="85" r="1.5" fill="#854d0e"/>
      <circle cx="4.5" cy="104" r="1.5" fill="#854d0e"/>

      <!-- Tali Kanan -->
      <rect x="365" y="52" width="9" height="66" rx="2" fill="#facc15" stroke="#ca8a04" stroke-width="1"/>
      <circle cx="369.5" cy="66" r="1.5" fill="#854d0e"/>
      <circle cx="369.5" cy="85" r="1.5" fill="#854d0e"/>
      <circle cx="369.5" cy="104" r="1.5" fill="#854d0e"/>
    </g>

    <!-- Bar Status Atas DX Driver -->
    <rect x="12" y="8" width="350" height="18" rx="4" fill="#111827"/>
    <circle cx="22" cy="17" r="3.2" fill="#ef4444">
      <animate attributeName="fill" values="#ef4444;#3b82f6;#3fb950;#ef4444" dur="3s" repeatCount="indefinite"/>
    </circle>
    <text x="30" y="20.5" fill="#facc15" font-family="ui-monospace, monospace" font-size="8" font-weight="bold" letter-spacing="1">DX BUILD DRIVER // NASCITA LAB</text>
    <text x="352" y="20.5" text-anchor="end" fill="#3fb950" font-family="ui-monospace, monospace" font-size="8" font-weight="bold">SYNC: 100%</text>

    <!-- SISI KIRI: VORTEX DYNAMO TACHOMETER (cx: 78, cy: 84) -->
    <circle cx="78" cy="84" r="34" fill="#1e293b" stroke="url(#chromeGrad)" stroke-width="3"/>
    <circle cx="78" cy="84" r="28" fill="#060911"/>

    <!-- Tangki Cairan Ganda Dynamo -->
    <g clip-path="url(#dynamoClip)">
      <rect x="50" y="66" width="28" height="48" fill="#dc2626" opacity="0.85"/>
      <rect x="78" y="66" width="28" height="48" fill="#2563eb" opacity="0.85"/>
      <circle cx="78" cy="84" r="16" fill="#facc15" opacity="0.4">
        <animate attributeName="r" values="10;17;10" dur="1.5s" repeatCount="indefinite"/>
      </circle>
    </g>

    <!-- Turbin Perak Berputar (Tachometer Needle-Gears) -->
    <g>
      <animateTransform attributeName="transform" type="rotate" from="0 78 84" to="360 78 84" dur="2.5s" repeatCount="indefinite"/>
      <line x1="54" y1="84" x2="102" y2="84" stroke="#f8fafc" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="66" y1="63.2" x2="90" y2="104.8" stroke="#f8fafc" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="90" y1="63.2" x2="66" y2="104.8" stroke="#f8fafc" stroke-width="2.5" stroke-linecap="round"/>
      <circle cx="78" cy="84" r="9" fill="#1e293b" stroke="url(#chromeGrad)" stroke-width="2"/>
      <circle cx="78" cy="84" r="3.5" fill="#facc15"/>
    </g>

    <!-- RODA GIGI BERTAUT (Interlocking Auxiliary Gears) -->
    <!-- Gear 1: Berputar Counter-Clockwise -->
    <g>
      <animateTransform attributeName="transform" type="rotate" from="0 124 96" to="-360 124 96" dur="3s" repeatCount="indefinite"/>
      <circle cx="124" cy="96" r="11" fill="#cbd5e1" stroke="#475569" stroke-width="1.2"/>
      <line x1="124" y1="83" x2="124" y2="109" stroke="#475569" stroke-width="2.5"/>
      <line x1="111" y1="96" x2="137" y2="96" stroke="#475569" stroke-width="2.5"/>
      <line x1="115" y1="87" x2="133" y2="105" stroke="#475569" stroke-width="2.5"/>
      <line x1="133" y1="87" x2="115" y2="105" stroke="#475569" stroke-width="2.5"/>
      <circle cx="124" cy="96" r="3.5" fill="#0f172a"/>
    </g>

    <!-- Gear 2: Berputar Clockwise -->
    <g>
      <animateTransform attributeName="transform" type="rotate" from="0 144 110" to="360 144 110" dur="2.1s" repeatCount="indefinite"/>
      <circle cx="144" cy="110" r="8" fill="#94a3b8" stroke="#334155" stroke-width="1.2"/>
      <line x1="144" y1="100" x2="144" y2="120" stroke="#334155" stroke-width="2"/>
      <line x1="134" y1="110" x2="154" y2="110" stroke="#334155" stroke-width="2"/>
      <circle cx="144" cy="110" r="2.5" fill="#0f172a"/>
    </g>

    <!-- TUAS PUTAR CRANK MERAH (Berputar 360 Derajat Penuh) -->
    <g>
      <animateTransform attributeName="transform" type="rotate" from="0 78 84" to="360 78 84" dur="3s" repeatCount="indefinite"/>
      <path d="M 78 80 L 34 71 A 3 3 0 0 0 30 74 L 30 82 A 3 3 0 0 0 34 85 L 78 88 Z" fill="#111827" stroke="#475569" stroke-width="1.2"/>
      <rect x="12" y="67" width="22" height="15" rx="3" fill="#dc2626" stroke="#7f1d1d" stroke-width="1"/>
      <line x1="17" y1="68" x2="17" y2="81" stroke="#7f1d1d" stroke-width="1.2"/>
      <line x1="22" y1="68" x2="22" y2="81" stroke="#7f1d1d" stroke-width="1.2"/>
      <line x1="27" y1="68" x2="27" y2="81" stroke="#7f1d1d" stroke-width="1.2"/>
      <circle cx="78" cy="84" r="7" fill="#1e293b" stroke="#cbd5e1" stroke-width="2"/>
    </g>

    <!-- SISI KANAN: DUA FULLBOTTLE (RABBIT & TANK TERPASANG) -->
    <g transform="translate(178, 30)">
      <!-- Rabbit Fullbottle -->
      <g transform="translate(0, 0)">
        <rect x="26" y="0" width="34" height="10" rx="2" fill="#cbd5e1" stroke="#475569" stroke-width="1"/>
        <rect x="38" y="2" width="10" height="6" fill="#dc2626"/>
        <rect x="10" y="10" width="66" height="68" rx="6" fill="#1a0b0e" stroke="#ef4444" stroke-width="1.5"/>
        <rect x="14" y="24" width="58" height="50" rx="4" fill="#dc2626" opacity="0.9"/>
        <circle cx="43" cy="42" r="5" fill="#f8fafc" stroke="#64748b" stroke-width="1"/>
        <text x="43" y="60" text-anchor="middle" font-size="12">🐰</text>
        <text x="43" y="72" text-anchor="middle" font-family="ui-monospace, monospace" font-size="7.5" font-weight="bold" fill="#ffffff" letter-spacing="1">RABBIT</text>
      </g>

      <!-- Tank Fullbottle -->
      <g transform="translate(92, 0)">
        <rect x="26" y="0" width="34" height="10" rx="2" fill="#cbd5e1" stroke="#475569" stroke-width="1"/>
        <rect x="38" y="2" width="10" height="6" fill="#2563eb"/>
        <rect x="10" y="10" width="66" height="68" rx="6" fill="#091426" stroke="#3b82f6" stroke-width="1.5"/>
        <rect x="14" y="24" width="58" height="50" rx="4" fill="#2563eb" opacity="0.9"/>
        <circle cx="43" cy="42" r="5" fill="#f8fafc" stroke="#64748b" stroke-width="1"/>
        <text x="43" y="60" text-anchor="middle" font-size="12">🛡️</text>
        <text x="43" y="72" text-anchor="middle" font-family="ui-monospace, monospace" font-size="7.5" font-weight="bold" fill="#ffffff" letter-spacing="1">TANK</text>
      </g>
    </g>

    <!-- PLAT GARIS BAHAYA ////// & BEST MATCH BADGE -->
    <g transform="translate(180, 114)">
      <rect width="176" height="24" rx="4" fill="url(#hazardPattern)" stroke="#ef4444" stroke-width="1.5"/>
      <rect x="6" y="4" width="80" height="16" rx="3" fill="#000000" opacity="0.88"/>
      <text x="46" y="15.5" text-anchor="middle" font-family="ui-monospace, monospace" font-size="8.5" font-weight="bold" fill="#facc15" letter-spacing="1">BEST MATCH</text>

      <text x="132" y="16" text-anchor="middle" font-family="ui-monospace, monospace" font-size="8.5" font-weight="bold" fill="#3fb950" letter-spacing="1">
        ARE YOU READY?
      </text>
    </g>

    <!-- PIPA KNALPOT PERAK GANDA (Dual Chrome Exhaust Pipes) -->
    <path d="M 112 147 L 235 147 Q 250 147 250 141 Q 250 137 265 137 L 354 137" stroke="url(#chromeGrad)" stroke-width="4" stroke-linecap="round" fill="none"/>
    <path d="M 122 154 L 230 154 Q 243 154 243 148 Q 243 144 255 144 L 340 144" stroke="url(#chromeGrad)" stroke-width="2.5" stroke-linecap="round" fill="none"/>

    <!-- ANNOUNCEMENT BANNER DI BAGIAN BAWAH -->
    <text x="187" y="163" text-anchor="middle" font-family="ui-monospace, monospace" font-size="8.5" font-weight="bold" letter-spacing="1.2">
      <tspan fill="#ef4444">HAGANE NO MOONSAULT! </tspan>
      <tspan fill="#3b82f6">RABBIT</tspan><tspan fill="#facc15">TANK! </tspan>
      <tspan fill="#3fb950">YEAAHH! ★</tspan>
    </text>
  </g>
</svg>'''

    try:
        ET.fromstring(svg)
        with open("assets/build-card.svg", "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"[2/4] assets/build-card.svg diperbarui dengan Simulator DX Build Driver ({CARD_W}x{CARD_H}).")
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
<img src="./azvi-ascii.svg?v=48" width="{CARD_W}" alt="Azvi Portrait" /><img src="./assets/build-card.svg?v=48" width="{CARD_W}" alt="Kamen Rider Build" />

<!-- RABBIT-TANK GRADIENT DIVIDER -->
<br><br>
<img src="./assets/divider.svg?v=48" width="840" alt="Divider" />
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
<img src="./contrib-heatmap.svg?v=48" alt="Aggregated Heatmap" width="840" />

</div>
'''
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("[4/4] README.md diperbarui dengan versi cache v=48.")

if __name__ == "__main__":
    patch_ascii_portrait()
    generate_build_card()
    generate_divider()
    update_readme()
