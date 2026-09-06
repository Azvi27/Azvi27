import os, re, base64
import xml.etree.ElementTree as ET

CARD_L_W = 455
CARD_R_W = 375
CARD_H = 340

# =============================================================
# 1. PATCH AZVI-ASCII.SVG (MASSIVE BOLD TYPOGRAPHY)
# =============================================================
def patch_ascii_portrait():
    if not os.path.exists("azvi-ascii.svg"):
        return

    with open("azvi-ascii.svg", "r", encoding="utf-8") as f:
        content = f.read()

    content = re.sub(r'<!-- (?:OPERATOR HUD|Terminal Session Header) -->[\s\S]*?<!-- /(?:OPERATOR HUD|Terminal Session Header) -->', '', content)
    content = re.sub(r'<text[^>]*SYSTEM://AZVI\.LAB[\s\S]*?</text>', '', content)
    content = re.sub(r'<g[^>]*id="operator-hud"[\s\S]*?</g>', '', content)
    content = re.sub(r'<line[^>]*stroke="#58a6ff"[^>]*/>', '', content)
    content = re.sub(r'<animateTransform[^>]*type="translate"[^>]*/>', '', content)
    content = re.sub(r'<text[^>]*>rendered:[^<]*</text>', '', content)

    content = re.sub(r'<svg[^>]*>', f'<svg width="{CARD_L_W}" height="{CARD_H}" viewBox="0 0 {CARD_L_W} {CARD_H}" fill="none" xmlns="http://www.w3.org/2000/svg">', content, count=1)
    content = re.sub(r'<rect[^>]*fill="#0d1117"[^>]*/>', f'<rect width="{CARD_L_W}" height="{CARD_H}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>', content, count=1)

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
      <rect x="0" y="28" width="180" height="0">
        <animate attributeName="height"
                 calcMode="discrete"
                 values="{v_str}"
                 keyTimes="{kt_str}"
                 dur="7.5s"
                 repeatCount="indefinite" />
      </rect>
    </clipPath>'''
    content = re.sub(r'<clipPath id="asciiTypeClip">[\s\S]*?</clipPath>', new_clip, content)

    # Injeksi HUD dengan Font Raksasa & Spasi Padat
    hud_injection = f'''
  <!-- Terminal Session Header -->
  <text x="18" y="22" font-family="ui-monospace, monospace" font-size="10" fill="#58a6ff" letter-spacing="1.2">SYSTEM://AZVI.LAB <tspan fill="#58a6ff"><animate attributeName="opacity" values="1;0;1" dur="0.9s" repeatCount="indefinite">█</animate></tspan></text>
  <!-- /Terminal Session Header -->

  <!-- OPERATOR HUD (FONT BESAR, JELAS & PADAT) -->
  <g id="operator-hud" transform="translate(180, 26)">
    <rect width="265" height="294" rx="12" fill="#161b22" stroke="#30363d" stroke-width="1.5"/>

    <!-- Header Box Ribbon -->
    <rect width="265" height="34" rx="12" fill="#21262d"/>
    <rect y="22" width="265" height="12" fill="#21262d"/>
    
    <circle cx="16" cy="17" r="4.5" fill="#3fb950">
      <animate attributeName="opacity" values="1;0.3;1" dur="1.8s" repeatCount="indefinite"/>
    </circle>
    <text x="28" y="21" fill="#3fb950" font-family="ui-monospace, monospace" font-size="12" font-weight="bold" letter-spacing="1.2">OPERATOR</text>
    <text x="250" y="21" text-anchor="end" fill="#58a6ff" font-family="ui-monospace, monospace" font-size="11.5" font-weight="bold" letter-spacing="0.8">[ ONLINE ]</text>

    <!-- 1. IDENTITAS UTAMA (FONT 20px BOLD) -->
    <text x="16" y="65" fill="#ffffff" font-family="ui-monospace, monospace" font-size="19" font-weight="bold">Farhan Azvi</text>
    <text x="16" y="86" fill="#58a6ff" font-family="ui-monospace, monospace" font-size="13.5" font-weight="600">@Azvi27 <tspan fill="#8b949e">· Teknik Fisika UGM</tspan></text>

    <line x1="14" y1="102" x2="251" y2="102" stroke="#30363d" stroke-width="1.2"/>

    <!-- 2. LABORATORY (FONT 22px BOLD) -->
    <text x="16" y="122" fill="#8b949e" font-family="ui-monospace, monospace" font-size="11" font-weight="bold" letter-spacing="1">LABORATORY</text>
    <text x="250" y="122" text-anchor="end" fill="#39d353" font-family="ui-monospace, monospace" font-size="11" font-weight="bold">[ ACTIVE ]</text>

    <text x="16" y="148" fill="#3fb950" font-family="ui-monospace, monospace" font-size="22" font-weight="bold">Lab. SSTK</text>
    <text x="16" y="171" fill="#f0f6fc" font-family="ui-monospace, monospace" font-size="14" font-weight="600">Sensor &amp; Sistem Telekontrol</text>

    <line x1="14" y1="188" x2="251" y2="188" stroke="#30363d" stroke-width="1.2"/>

    <!-- 3. CURRENT ROLE & ACTIVITY (FONT 18px BOLD) -->
    <text x="16" y="208" fill="#8b949e" font-family="ui-monospace, monospace" font-size="11" font-weight="bold" letter-spacing="1">ROLE &amp; ASSIGNMENT</text>
    <text x="250" y="208" text-anchor="end" fill="#58a6ff" font-family="ui-monospace, monospace" font-size="11" font-weight="bold">STATUS</text>

    <text x="16" y="235" fill="#58a6ff" font-family="ui-monospace, monospace" font-size="18" font-weight="bold">Lab Assistant &amp; Intern</text>
    <text x="16" y="258" fill="#c9d1d9" font-family="ui-monospace, monospace" font-size="14" font-weight="500">Asisten Lab &amp; Magang SSTK</text>
    <text x="16" y="278" fill="#8b949e" font-family="ui-monospace, monospace" font-size="12">Universitas Gadjah Mada</text>
  </g>
  <!-- /OPERATOR HUD -->
'''
    content = re.sub(r'</svg>', f'{hud_injection}\n</svg>', content)
    with open("azvi-ascii.svg", "w", encoding="utf-8") as f:
        f.write(content)

# =============================================================
# 2. GENERATE BUILD CARD (COMPACT & BALANCED)
# =============================================================
def generate_build_card():
    sprite_path = "assets/Build_Capsem_Sprite.webp"
    sprite_b64 = ""
    if os.path.exists(sprite_path):
        with open(sprite_path, "rb") as f:
            sprite_b64 = base64.b64encode(f.read()).decode("utf-8")

    svg = f'''<svg width="{CARD_R_W}" height="{CARD_H}" viewBox="0 0 {CARD_R_W} {CARD_H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="chromeGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="35%" stop-color="#cbd5e1"/>
      <stop offset="70%" stop-color="#64748b"/>
      <stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>

    <pattern id="hazardPattern" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <rect width="6" height="12" fill="#000000"/>
      <rect x="6" width="6" height="12" fill="#dc2626"/>
    </pattern>

    <clipPath id="dynamoClip">
      <circle cx="70" cy="74" r="24"/>
    </clipPath>

    <clipPath id="slotAreaClip">
      <rect x="156" y="4" width="170" height="96" rx="6"/>
    </clipPath>
  </defs>

  <rect width="{CARD_R_W}" height="{CARD_H}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>

  <!-- Top Session Header -->
  <text x="18" y="22" font-family="ui-monospace, monospace" font-size="9" fill="#ff7b72" letter-spacing="1.2">SYSTEM://BUILD.DRIVER <tspan fill="#ff7b72"><animate attributeName="opacity" values="1;0;1" dur="0.9s" repeatCount="indefinite">█</animate></tspan></text>

  <!-- Bagian Atas: Sprite & Quotes Padat -->
  <g transform="translate(16, 32)">
    <image href="data:image/webp;base64,{sprite_b64}" width="88" height="88"/>

    <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif">
      <text x="96" y="15" fill="#58a6ff" font-size="11" font-weight="bold">さぁ、実験を始めようか？</text>
      <text x="96" y="30" fill="#c9d1d9" font-size="9.5" font-style="italic">Shall we begin the experiment?</text>
      <text x="96" y="44" fill="#8b949e" font-size="8.8">Nah, mari kita mulai eksperimennya!</text>

      <line x1="96" y1="52" x2="{CARD_R_W - 32}" y2="52" stroke="#21262d" stroke-width="1"/>

      <text x="96" y="68" fill="#ff7b72" font-size="11" font-weight="bold">勝利の法則は決まった！</text>
      <text x="96" y="83" fill="#c9d1d9" font-size="9.5" font-style="italic">The formula for victory is set!</text>
      <text x="96" y="97" fill="#8b949e" font-size="8.8">Hukum kemenangannya telah ditentukan!</text>
    </g>
  </g>

  <!-- Bagian Bawah: DX Driver Dirampingkan Rapi -->
  <g transform="translate(14, 142)">
    <rect width="{CARD_R_W - 28}" height="178" rx="10" fill="#070b14" stroke="#30363d" stroke-width="1.5">
      <animate attributeName="stroke" values="#30363d; #30363d; #ff7b72; #3fb950; #facc15; #30363d" keyTimes="0; 0.60; 0.64; 0.75; 0.90; 1" dur="12s" repeatCount="indefinite"/>
    </rect>

    <g>
      <rect x="0" y="56" width="8" height="60" rx="2" fill="#facc15" stroke="#ca8a04" stroke-width="1"/>
      <circle cx="4" cy="70" r="1.5" fill="#854d0e"/><circle cx="4" cy="86" r="1.5" fill="#854d0e"/><circle cx="4" cy="102" r="1.5" fill="#854d0e"/>
      <rect x="{CARD_R_W - 36}" y="56" width="8" height="60" rx="2" fill="#facc15" stroke="#ca8a04" stroke-width="1"/>
      <circle cx="{CARD_R_W - 32}" cy="70" r="1.5" fill="#854d0e"/><circle cx="{CARD_R_W - 32}" cy="86" r="1.5" fill="#854d0e"/><circle cx="{CARD_R_W - 32}" cy="102" r="1.5" fill="#854d0e"/>
    </g>

    <rect x="10" y="8" width="{CARD_R_W - 48}" height="18" rx="4" fill="#111827"/>
    <circle cx="20" cy="17" r="3" fill="#ef4444">
      <animate attributeName="fill" values="#ef4444;#3b82f6;#facc15;#3fb950;#ef4444" dur="4s" repeatCount="indefinite"/>
    </circle>

    <text x="28" y="20.5" fill="#ff7b72" font-family="ui-monospace, monospace" font-size="7.5" font-weight="bold" letter-spacing="0.8">
      <animate attributeName="opacity" values="1;1;0;0;0;0;1" keyTimes="0; 0.16; 0.17; 0.98; 0.99; 1; 1" dur="12s" repeatCount="indefinite"/>
      [ SHAKA-SHAKA ] &gt;&gt; &quot;RABBIT!&quot; 🐰
    </text>
    <text x="28" y="20.5" fill="#58a6ff" font-family="ui-monospace, monospace" font-size="7.5" font-weight="bold" letter-spacing="0.8">
      <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0; 0.165; 0.175; 0.33; 0.34; 1" dur="12s" repeatCount="indefinite"/>
      [ SHAKA-SHAKA ] &gt;&gt; &quot;TANK!&quot; 🛡️
    </text>
    <text x="28" y="20.5" fill="#facc15" font-family="ui-monospace, monospace" font-size="7.5" font-weight="bold" letter-spacing="0.8">
      <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0; 0.335; 0.345; 0.50; 0.51; 1" dur="12s" repeatCount="indefinite"/>
      [ DOCKED! ] &gt;&gt; &quot;BEST MATCH!&quot; ★
    </text>
    <text x="28" y="20.5" fill="#3fb950" font-family="ui-monospace, monospace" font-size="7.5" font-weight="bold" letter-spacing="0.8">
      <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0; 0.515; 0.525; 0.75; 0.76; 1" dur="12s" repeatCount="indefinite"/>
      [ CRANKING ] &gt;&gt; MOONSAULT! YEAAHH!
    </text>
    <text x="28" y="20.5" fill="#ffffff" font-family="ui-monospace, monospace" font-size="7.5" font-weight="bold" letter-spacing="0.8">
      <animate attributeName="opacity" values="0;0;1;1" keyTimes="0; 0.755; 0.765; 1" dur="12s" repeatCount="indefinite"/>
      [ DRIVER ] &gt;&gt; <tspan fill="#facc15">&quot;ARE YOU READY?!&quot;</tspan>
    </text>

    <text x="{CARD_R_W - 38}" y="20.5" text-anchor="end" font-family="ui-monospace, monospace" font-size="7.5" font-weight="bold">
      <animate attributeName="fill" values="#8b949e;#ff7b72;#58a6ff;#facc15;#3fb950" keyTimes="0; 0.16; 0.33; 0.50; 1" dur="12s" repeatCount="indefinite"/>
      100%
    </text>

    <!-- Dynamo & Crank Assembly -->
    <circle cx="66" cy="80" r="30" fill="#1e293b" stroke="url(#chromeGrad)" stroke-width="2.5"/>
    <circle cx="66" cy="80" r="24" fill="#060911"/>

    <g clip-path="url(#dynamoClip)" transform="translate(-4, 6)">
      <rect x="46" y="60" width="24" height="42" fill="#dc2626"><animate attributeName="opacity" values="0.15; 0.15; 0.15; 0.85; 0.85" keyTimes="0; 0.16; 0.33; 0.50; 1" dur="12s" repeatCount="indefinite"/></rect>
      <rect x="70" y="60" width="24" height="42" fill="#2563eb"><animate attributeName="opacity" values="0.15; 0.15; 0.15; 0.85; 0.85" keyTimes="0; 0.16; 0.33; 0.50; 1" dur="12s" repeatCount="indefinite"/></rect>
      <circle cx="70" cy="74" r="14" fill="#facc15" opacity="0.4"><animate attributeName="r" values="7; 7; 15; 20; 14" keyTimes="0; 0.50; 0.65; 0.78; 1" dur="12s" repeatCount="indefinite"/></circle>
    </g>

    <g>
      <animateTransform attributeName="transform" type="rotate" values="0 66 80; 0 66 80; 720 66 80; 2160 66 80; 2520 66 80" keyTimes="0; 0.50; 0.65; 0.88; 1" dur="12s" repeatCount="indefinite"/>
      <line x1="45" y1="80" x2="87" y2="80" stroke="#f8fafc" stroke-width="2" stroke-linecap="round"/>
      <line x1="56" y1="62" x2="76" y2="98" stroke="#f8fafc" stroke-width="2" stroke-linecap="round"/>
      <line x1="76" y1="62" x2="56" y2="98" stroke="#f8fafc" stroke-width="2" stroke-linecap="round"/>
      <circle cx="66" cy="80" r="8" fill="#1e293b" stroke="url(#chromeGrad)" stroke-width="1.8"/>
      <circle cx="66" cy="80" r="3" fill="#facc15"/>
    </g>

    <g>
      <animateTransform attributeName="transform" type="rotate" values="0 106 90; 0 106 90; -720 106 90; -1800 106 90; -1980 106 90" keyTimes="0; 0.50; 0.65; 0.88; 1" dur="12s" repeatCount="indefinite"/>
      <circle cx="106" cy="90" r="9.5" fill="#cbd5e1" stroke="#475569" stroke-width="1"/>
      <line x1="106" y1="79" x2="106" y2="101" stroke="#475569" stroke-width="2"/><line x1="95" y1="90" x2="117" y2="90" stroke="#475569" stroke-width="2"/><circle cx="106" cy="90" r="3" fill="#0f172a"/>
    </g>

    <g>
      <animateTransform attributeName="transform" type="rotate" values="0 123 102; 0 123 102; 960 123 102; 2400 123 102; 2640 123 102" keyTimes="0; 0.50; 0.65; 0.88; 1" dur="12s" repeatCount="indefinite"/>
      <circle cx="123" cy="102" r="7" fill="#94a3b8" stroke="#334155" stroke-width="1"/>
      <line x1="123" y1="94" x2="123" y2="110" stroke="#334155" stroke-width="1.8"/><line x1="115" y1="102" x2="131" y2="102" stroke="#334155" stroke-width="1.8"/><circle cx="123" cy="102" r="2" fill="#0f172a"/>
    </g>

    <g>
      <animateTransform attributeName="transform" type="rotate" values="0 66 80; 0 66 80; 360 66 80; 1080 66 80; 1080 66 80; 0 66 80" keyTimes="0; 0.50; 0.65; 0.85; 0.95; 1" dur="12s" repeatCount="indefinite"/>
      <path d="M 66 77 L 28 69 A 3 3 0 0 0 25 72 L 25 79 A 3 3 0 0 0 28 82 L 66 85 Z" fill="#111827" stroke="#475569" stroke-width="1"/>
      <rect x="9" y="65" width="20" height="14" rx="3" fill="#dc2626" stroke="#7f1d1d" stroke-width="1"/>
      <circle cx="66" cy="80" r="6" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.8"/>
    </g>

    <!-- Botol Fullbottle Ramping -->
    <g clip-path="url(#slotAreaClip)" transform="translate(-10, 0)">
      <g transform="translate(164, 30)">
        <g><animateTransform attributeName="transform" type="translate" values="0,-20; 0,-12; 0,-24; 0,-12; 0,-22; 0,-14; 0,-20; 0,-20; 0,0; 0,0; 0,-20" keyTimes="0; 0.04; 0.08; 0.12; 0.14; 0.16; 0.18; 0.33; 0.38; 0.95; 1" dur="12s" repeatCount="indefinite"/>
          <rect x="24" y="0" width="26" height="10" rx="2.5" fill="#dc2626" stroke="#991b1b" stroke-width="1"/>
          <rect x="32" y="2" width="10" height="6" rx="1" fill="#0d1117"/><text x="37" y="7" text-anchor="middle" font-family="ui-monospace, monospace" font-size="5" font-weight="bold" fill="#facc15">R/T</text>
          <path d="M 12 10 L 62 10 L 64 20 L 58 22 L 16 22 L 10 20 Z" fill="#1e293b" stroke="#0f172a" stroke-width="1"/>
          <path d="M 16 22 Q 14 38 19 46 Q 14 56 16 66 L 58 66 Q 60 56 55 46 Q 60 38 58 22 Z" fill="#2a080c" stroke="#ef4444" stroke-width="1.2"/>
          <path d="M 18 25 Q 16 38 21 46 Q 16 56 18 64 L 56 64 Q 58 56 53 46 Q 58 38 56 25 Z" fill="#dc2626" opacity="0.85"/>
          <circle cx="37" cy="42" r="4.5" fill="#f8fafc" stroke="#64748b" stroke-width="1">
            <animate attributeName="cy" values="32; 54; 30; 56; 32; 42; 42" keyTimes="0; 0.04; 0.08; 0.12; 0.16; 0.18; 1" dur="12s" repeatCount="indefinite"/>
          </circle>
          <text x="37" y="47" text-anchor="middle" font-size="10">🐰</text>
          <text x="37" y="60" text-anchor="middle" font-family="ui-monospace, monospace" font-size="7" font-weight="bold" fill="#ffffff" letter-spacing="1">RABBIT</text>
          <rect x="14" y="66" width="46" height="8" rx="2" fill="#1e293b" stroke="#0f172a" stroke-width="1"/>
        </g>
      </g>
      <g transform="translate(242, 30)">
        <g><animateTransform attributeName="transform" type="translate" values="0,-20; 0,-20; 0,-12; 0,-24; 0,-12; 0,-22; 0,-14; 0,-20; 0,0; 0,0; 0,-20" keyTimes="0; 0.17; 0.20; 0.23; 0.26; 0.29; 0.31; 0.34; 0.40; 0.95; 1" dur="12s" repeatCount="indefinite"/>
          <rect x="24" y="0" width="26" height="10" rx="2.5" fill="#2563eb" stroke="#1d4ed8" stroke-width="1"/>
          <rect x="32" y="2" width="10" height="6" rx="1" fill="#0d1117"/><text x="37" y="7" text-anchor="middle" font-family="ui-monospace, monospace" font-size="5" font-weight="bold" fill="#facc15">R/T</text>
          <path d="M 12 10 L 62 10 L 64 20 L 58 22 L 16 22 L 10 20 Z" fill="#1e293b" stroke="#0f172a" stroke-width="1"/>
          <path d="M 16 22 Q 14 38 19 46 Q 14 56 16 66 L 58 66 Q 60 56 55 46 Q 60 38 58 22 Z" fill="#091426" stroke="#3b82f6" stroke-width="1.2"/>
          <path d="M 18 25 Q 16 38 21 46 Q 16 56 18 64 L 56 64 Q 58 56 53 46 Q 58 38 56 25 Z" fill="#2563eb" opacity="0.85"/>
          <circle cx="37" cy="42" r="4.5" fill="#f8fafc" stroke="#64748b" stroke-width="1">
            <animate attributeName="cy" values="42; 42; 32; 54; 30; 56; 32; 42; 42" keyTimes="0; 0.17; 0.20; 0.23; 0.26; 0.29; 0.31; 0.34; 1" dur="12s" repeatCount="indefinite"/>
          </circle>
          <text x="37" y="47" text-anchor="middle" font-size="10">🛡️</text>
          <text x="37" y="60" text-anchor="middle" font-family="ui-monospace, monospace" font-size="7" font-weight="bold" fill="#ffffff" letter-spacing="1">TANK</text>
          <rect x="14" y="66" width="46" height="8" rx="2" fill="#1e293b" stroke="#0f172a" stroke-width="1"/>
        </g>
      </g>
    </g>

    <!-- Hazard Stripes & Banner Bawah -->
    <g transform="translate(150, 108)">
      <rect width="170" height="24" rx="4" fill="url(#hazardPattern)" stroke="#ef4444" stroke-width="1.5"/>
      <rect x="6" y="4" width="76" height="16" rx="3" fill="#000000" opacity="0.88"/>
      <text x="44" y="15.5" text-anchor="middle" font-family="ui-monospace, monospace" font-size="8" font-weight="bold" letter-spacing="1">
        <animate attributeName="fill" values="#8b949e; #8b949e; #facc15; #facc15; #3fb950; #facc15" keyTimes="0; 0.33; 0.38; 0.62; 0.75; 1" dur="12s" repeatCount="indefinite"/>BEST MATCH
      </text>
      <text x="124" y="16" text-anchor="middle" font-family="ui-monospace, monospace" font-size="8" font-weight="bold" letter-spacing="1">
        <animate attributeName="fill" values="#484f58; #484f58; #484f58; #ff7b72; #3fb950; #3fb950; #484f58" keyTimes="0; 0.33; 0.50; 0.62; 0.85; 0.95; 1" dur="12s" repeatCount="indefinite"/>MOONSAULT
      </text>
    </g>

    <path d="M 98 142 L 210 142 Q 224 142 224 136 Q 224 132 238 132 L 320 132" stroke="url(#chromeGrad)" stroke-width="3.5" stroke-linecap="round" fill="none"/>
    <path d="M 106 148 L 206 148 Q 218 148 218 143 Q 218 139 230 139 L 308 139" stroke="url(#chromeGrad)" stroke-width="2" stroke-linecap="round" fill="none"/>

    <g transform="translate(174, 163)">
      <text text-anchor="middle" font-family="ui-monospace, monospace" font-size="8.8" font-weight="bold" letter-spacing="1.5">
        <animate attributeName="fill" values="#484f58; #484f58; #484f58; #484f58; #facc15; #3fb950; #484f58" keyTimes="0; 0.33; 0.50; 0.72; 0.78; 0.96; 1" dur="12s" repeatCount="indefinite"/>
        [ DRIVER: &quot;ARE YOU READY?&quot; ]
      </text>
    </g>
  </g>
</svg>'''
    with open("assets/build-card.svg", "w", encoding="utf-8") as f:
        f.write(svg)

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

# =============================================================
# 4. UPDATE README CACHE BUSTER (v=65)
# =============================================================
def update_readme():
    content = f'''<div align="center">

<!-- DUAL BALANCED CARDS (PROFILE 455px, BUILD 375px -> TOTAL 830px) -->
<img src="./azvi-ascii.svg?v=65" width="{CARD_L_W}" alt="Azvi Portrait" /><img src="./assets/build-card.svg?v=65" width="{CARD_R_W}" alt="Kamen Rider Build" />

<!-- RABBIT-TANK GRADIENT DIVIDER -->
<br><br>
<img src="./assets/divider.svg?v=65" width="840" alt="Divider" />
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
<img src="./contrib-heatmap.svg?v=65" alt="Aggregated Heatmap" width="840" />

</div>
'''
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    patch_ascii_portrait()
    generate_build_card()
    generate_divider()
    update_readme()
    print("[✓] Layout diperbaiki: Font profil besar & jelas, rongga kosong hilang total!")
