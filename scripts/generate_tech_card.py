import os, json

def generate_tech_card():
    icons_path = "data/icons_b64.json"
    if not os.path.exists(icons_path):
        print("[!] data/icons_b64.json tidak ditemukan!")
        return

    with open(icons_path, "r", encoding="utf-8") as f:
        icons = json.load(f)

    categories = [
        {
            'title': 'MOD 01 // INFRASTRUCTURE &amp; HOMELAB',
            'color': '#58a6ff',
            'box': (20, 52, 394, 142),
            'rows': [
                [('proxmox', 'Proxmox VE', 106), ('docker', 'Docker', 76), ('portainer', 'Portainer', 92), ('tailscale', 'Tailscale', 86)],
                [('minio', 'MinIO', 76), ('ubuntu', 'Ubuntu', 78), ('debian', 'Debian', 78)]
            ]
        },
        {
            'title': 'MOD 02 // IoT, EMBEDDED &amp; TELECONTROL',
            'color': '#3fb950',
            'box': (426, 52, 394, 142),
            'rows': [
                [('espressif', 'ESP32', 74), ('raspberrypi', 'Raspberry Pi', 110), ('arduino', 'Arduino Uno', 108)],
                [('mqtt', 'EMQX (MQTT)', 110), ('modbus', 'Modbus', 80), ('lorawan', 'LoRaWAN', 88)]
            ]
        },
        {
            'title': 'MOD 03 // FRAMEWORKS',
            'color': '#bc8cff',
            'box': (20, 206, 258, 136),
            'rows': [
                [('laravel', 'Laravel', 84), ('go', 'Goravel (Go)', 110)],
                [('django', 'Django', 76), ('react', 'React', 70), ('vuedotjs', 'Vue.js', 74)]
            ]
        },
        {
            'title': 'MOD 04 // DATABASES &amp; STORAGE',
            'color': '#f0883e',
            'box': (290, 206, 260, 136),
            'rows': [
                [('postgresql', 'PostgreSQL', 106), ('mysql', 'MySQL', 74)],
                [('mariadb', 'MariaDB', 84), ('dbeaver', 'DBeaver', 86)]
            ]
        },
        {
            'title': 'MOD 05 // DEVOPS &amp; CLOUD',
            'color': '#79c0ff',
            'box': (562, 206, 258, 136),
            'rows': [
                [('gitlab', 'GitLab', 78), ('github', 'GitHub', 78)],
                [('cloudflare', 'Cloudflare', 96), ('cpanel', 'cPanel', 78)]
            ]
        }
    ]

    scan_configs = [
        ("#30363d; #58a6ff; #30363d; #30363d", "0; 0.10; 0.20; 1", "3.5; 5; 3.5; 3.5", "0; 0.10; 0.20; 1"),
        ("#30363d; #30363d; #3fb950; #30363d; #30363d", "0; 0.20; 0.30; 0.40; 1", "3.5; 3.5; 5; 3.5; 3.5", "0; 0.20; 0.30; 0.40; 1"),
        ("#30363d; #30363d; #bc8cff; #30363d; #30363d", "0; 0.40; 0.50; 0.60; 1", "3.5; 3.5; 5; 3.5; 3.5", "0; 0.40; 0.50; 0.60; 1"),
        ("#30363d; #30363d; #f0883e; #30363d; #30363d", "0; 0.60; 0.70; 0.80; 1", "3.5; 3.5; 5; 3.5; 3.5", "0; 0.60; 0.70; 0.80; 1"),
        ("#30363d; #30363d; #79c0ff; #30363d", "0; 0.80; 0.90; 1", "3.5; 3.5; 5; 3.5", "0; 0.80; 0.90; 1"),
    ]

    svg_elements = []
    for cat_idx, cat in enumerate(categories):
        bx, by, bw, bh = cat['box']
        s_val, s_kt, r_val, r_kt = scan_configs[cat_idx]
        svg_elements.append(f'''
  <!-- {cat["title"]} -->
  <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2">
    <animate attributeName="stroke" values="{s_val}" keyTimes="{s_kt}" dur="12s" repeatCount="indefinite"/>
  </rect>
  <circle cx="{bx + 16}" cy="{by + 16}" r="3.5" fill="{cat["color"]}">
    <animate attributeName="r" values="{r_val}" keyTimes="{r_kt}" dur="12s" repeatCount="indefinite"/>
  </circle>
  <text x="{bx + 26}" y="{by + 20}" fill="#8b949e" font-family="ui-monospace, SFMono-Regular, monospace" font-size="10" font-weight="bold" letter-spacing="1.2">{cat["title"]}</text>
  <line x1="{bx + 12}" y1="{by + 28}" x2="{bx + bw - 12}" y2="{by + 28}" stroke="#21262d" stroke-width="1"/>
''')
        start_y = by + 40
        for r_idx, row in enumerate(cat['rows']):
            row_y = start_y + (r_idx * 38)
            cur_x = bx + 12
            for key, name, pill_w in row:
                b64 = icons.get(key, '')
                svg_elements.append(f'''  <g transform="translate({cur_x}, {row_y})">
    <rect width="{pill_w}" height="28" rx="6" fill="#0d1117" stroke="#30363d" stroke-width="1"/>
    <image href="data:image/svg+xml;base64,{b64}" x="7" y="6" width="16" height="16"/>
    <text x="29" y="18" fill="#e6edf3" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="600">{name}</text>
  </g>
''')
                cur_x += pill_w + 6

    svg_full = f'''<svg width="840" height="360" viewBox="0 0 840 360" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="matrixScanGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#3fb950" stop-opacity="0"/>
      <stop offset="25%" stop-color="#58a6ff" stop-opacity="0.5"/>
      <stop offset="50%" stop-color="#3fb950" stop-opacity="0.85"/>
      <stop offset="75%" stop-color="#58a6ff" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#3fb950" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <!-- Frame -->
  <rect width="840" height="360" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>
  
  <!-- Header Bar -->
  <rect width="840" height="38" rx="16" fill="#161b22"/>
  <rect y="24" width="840" height="14" fill="#161b22"/>
  
  <circle cx="22" cy="19" r="4" fill="#3fb950">
    <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
  </circle>
  <text x="34" y="23" fill="#3fb950" font-family="ui-monospace, SFMono-Regular, monospace" font-size="12" font-weight="700" letter-spacing="1.2">SYSTEM://TECH.MATRIX // LAB &amp; PROJECT EXPERIENCE <tspan fill="#3fb950"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite">█</animate></tspan></text>
  
  <!-- Cycling Status Indicator (12s Loop) -->
  <g font-family="ui-monospace, SFMono-Regular, monospace" font-size="11" font-weight="700">
    <text x="818" y="23" text-anchor="end" fill="#58a6ff">
      <animate attributeName="opacity" values="1;1;0;0;0;0;1" keyTimes="0; 0.24; 0.25; 0.99; 0.995; 1; 1" dur="12s" repeatCount="indefinite"/>
      [ 26 TOOLS USED ]
    </text>
    <text x="818" y="23" text-anchor="end" fill="#3fb950">
      <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0; 0.245; 0.255; 0.49; 0.50; 1" dur="12s" repeatCount="indefinite"/>
      [ LAB &amp; PERSONAL PROJECTS ]
    </text>
    <text x="818" y="23" text-anchor="end" fill="#facc15">
      <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0; 0.495; 0.505; 0.74; 0.75; 1" dur="12s" repeatCount="indefinite"/>
      [ HANDS-ON EXPERIENCE ]
    </text>
    <text x="818" y="23" text-anchor="end" fill="#bc8cff">
      <animate attributeName="opacity" values="0;0;1;1" keyTimes="0; 0.745; 0.755; 1" dur="12s" repeatCount="indefinite"/>
      [ ACTIVELY USED ]
    </text>
  </g>

  <!-- Matrix Diagnostic Radar Sweep Beam -->
  <line x1="20" y1="52" x2="820" y2="52" stroke="url(#matrixScanGrad)" stroke-width="1.8" pointer-events="none">
    <animate attributeName="y1" values="52; 342; 52" keyTimes="0; 0.5; 1" dur="12s" repeatCount="indefinite"/>
    <animate attributeName="y2" values="52; 342; 52" keyTimes="0; 0.5; 1" dur="12s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.3; 0.8; 0.3" keyTimes="0; 0.5; 1" dur="12s" repeatCount="indefinite"/>
  </line>

{''.join(svg_elements)}</svg>'''

    with open("assets/tech-stack.svg", "w", encoding="utf-8") as f:
        f.write(svg_full)
    print("[✓] assets/tech-stack.svg berhasil dibuat (840px Cyber Equipment Matrix)!")

if __name__ == "__main__":
    generate_tech_card()
