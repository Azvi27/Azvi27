import os
import re
import base64

def clean_ascii_card():
    if not os.path.exists("azvi-ascii.svg"):
        return 420, 480
    
    with open("azvi-ascii.svg", "r", encoding="utf-8") as f:
        content = f.read()

    content = re.sub(r'<circle[^>]*>', '', content)
    content = re.sub(r'<text[^>]*>portrait\.sh</text>', '', content)
    content = re.sub(r'<line[^>]*y1="4[04]"[^>]*/>', '', content)

    w, h = 420, 480
    vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', content)
    if vb:
        w, h = int(vb.group(1)), int(vb.group(2))

    with open("azvi-ascii.svg", "w", encoding="utf-8") as f:
        f.write(content)
    return w, h

def generate_build_card(width, height):
    sprite_path = "assets/Build_Capsem_Sprite.webp"
    sprite_b64 = ""
    if os.path.exists(sprite_path):
        with open(sprite_path, "rb") as f:
            sprite_b64 = base64.b64encode(f.read()).decode("utf-8")

    cx = width / 2

    svg_content = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Card Frame -->
  <rect width="{width}" height="{height}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>

  <!-- SISI KIRI: Sprite Build -->
  <g transform="translate(20, 52)">
    <image href="data:image/webp;base64,{sprite_b64}" width="132" height="132"/>
  </g>

  <!-- SISI KANAN: Quotes 3 Bahasa -->
  <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif">
    <!-- Quote 1 -->
    <text x="164" y="70" fill="#58a6ff" font-size="13.5" font-weight="600">さぁ、実験を始めようか？</text>
    <text x="164" y="90" fill="#c9d1d9" font-size="11.5" font-style="italic">Shall we begin the experiment?</text>
    <text x="164" y="108" fill="#8b949e" font-size="10.5">Nah, mari kita mulai eksperimennya!</text>

    <!-- Divider halus -->
    <line x1="164" y1="126" x2="{width - 24}" y2="126" stroke="#21262d" stroke-width="1"/>

    <!-- Quote 2 -->
    <text x="164" y="150" fill="#ff7b72" font-size="13.5" font-weight="600">勝利の法則は決まった！</text>
    <text x="164" y="170" fill="#c9d1d9" font-size="11.5" font-style="italic">The formula for victory is set!</text>
    <text x="164" y="188" fill="#8b949e" font-size="10.5">Hukum kemenangannya telah ditentukan!</text>
  </g>

  <!-- KOTAK STATUS: Minimalist Console Style -->
  <g transform="translate(24, {height - 96})">
    <rect width="{width - 48}" height="64" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1"/>
    
    <!-- "Are you ready?" -->
    <text x="{(width - 48) / 2}" y="26" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11.5" fill="#8b949e" letter-spacing="1.5">
      &gt; &quot;Are you ready?&quot;
    </text>

    <!-- Rabbit × Tank ➔ Best Match -->
    <text x="{(width - 48) / 2}" y="47" text-anchor="middle" font-family="ui-monospace, monospace" font-size="12" font-weight="bold">
      <tspan fill="#ff7b72">Rabbit</tspan>
      <tspan fill="#484f58"> × </tspan>
      <tspan fill="#58a6ff">Tank</tspan>
      <tspan fill="#484f58"> ➔ </tspan>
      <tspan fill="#3fb950">Best Match</tspan>
    </text>
  </g>
</svg>
'''
    with open("assets/build-card.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
    print("[✓] assets/build-card.svg berhasil diperbarui (desain minimalis tanpa kernel)")

if __name__ == "__main__":
    w, h = clean_ascii_card()
    generate_build_card(w, h)
