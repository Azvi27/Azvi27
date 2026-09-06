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
                [('linux', 'Linux', 70), ('ubuntu', 'Ubuntu', 78), ('debian', 'Debian', 78)]
            ]
        },
        {
            'title': 'MOD 02 // IoT, EMBEDDED &amp; TELECONTROL',
            'color': '#3fb950',
            'box': (426, 52, 394, 142),
            'rows': [
                [('espressif', 'ESP32', 74), ('raspberrypi', 'Raspberry Pi 3B', 124), ('arduino', 'Arduino Uno', 108)],
                [('arduino_ide', 'Arduino IDE', 104), ('mqtt', 'EMQX (MQTT)', 110), ('modbus', 'Modbus', 80), ('lorawan', 'LoRaWAN', 88)]
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
                [('mariadb', 'MariaDB', 84), ('dbeaver', 'DBeaver', 88)]
            ]
        },
        {
            'title': 'MOD 05 // DEVOPS &amp; CLOUD',
            'color': '#79c0ff',
            'box': (562, 206, 258, 136),
            'rows': [
                [('gitlab', 'GitLab', 78), ('github', 'GitHub', 78)],
                [('cloudflare', 'Cloudflare', 98), ('cpanel', 'cPanel', 78)]
            ]
        }
    ]

    svg_elements = []
    for cat in categories:
        bx, by, bw, bh = cat['box']
        svg_elements.append(f'''
  <!-- {cat["title"]} -->
  <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/>
  <circle cx="{bx + 16}" cy="{by + 16}" r="3.5" fill="{cat["color"]}"/>
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
  <!-- Frame -->
  <rect width="840" height="360" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>
  
  <!-- Header Bar -->
  <rect width="840" height="38" rx="16" fill="#161b22"/>
  <rect y="24" width="840" height="14" fill="#161b22"/>
  
  <circle cx="22" cy="19" r="4" fill="#3fb950">
    <animate attributeName="opacity" values="1;0.3;1" dur="1.8s" repeatCount="indefinite"/>
  </circle>
  <text x="34" y="23" fill="#3fb950" font-family="ui-monospace, SFMono-Regular, monospace" font-size="12" font-weight="700" letter-spacing="1.2">SYSTEM://EQUIPMENT.MATRIX // RESEARCH &amp; TECH_STACK</text>
  <text x="818" y="23" text-anchor="end" fill="#58a6ff" font-family="ui-monospace, SFMono-Regular, monospace" font-size="11" font-weight="700">[ 24 PRODUCTION TOOLS LOADED ]</text>

{''.join(svg_elements)}</svg>'''

    with open("assets/tech-stack.svg", "w", encoding="utf-8") as f:
        f.write(svg_full)
    print("[✓] assets/tech-stack.svg berhasil dibuat (840px Cyber Equipment Matrix)!")

if __name__ == "__main__":
    generate_tech_card()
