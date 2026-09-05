import os
import re
import base64

def get_target_dimensions():
    # Standar fallback jika tidak terbaca
    w, h = 420, 440
    if os.path.exists("azvi-ascii.svg"):
        with open("azvi-ascii.svg", "r", encoding="utf-8") as f:
            content = f.read()
            vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', content)
            if vb:
                w, h = int(vb.group(1)), int(vb.group(2))
            else:
                wm = re.search(r'width="(\d+)"', content)
                hm = re.search(r'height="(\d+)"', content)
                if wm and hm:
                    w, h = int(wm.group(1)), int(hm.group(2))
    return w, h

def generate_svg():
    width, height = get_target_dimensions()
    
    sprite_path = "assets/Build_Capsem_Sprite.webp"
    sprite_b64 = ""
    if os.path.exists(sprite_path):
        with open(sprite_path, "rb") as f:
            sprite_b64 = base64.b64encode(f.read()).decode("utf-8")

    cx = width / 2

    svg_content = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Window Frame -->
  <rect width="{width}" height="{height}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>
  
  <!-- Terminal Header -->
  <circle cx="28" cy="24" r="5.5" fill="#ff5f56"/>
  <circle cx="45" cy="24" r="5.5" fill="#ffbd2e"/>
  <circle cx="62" cy="24" r="5.5" fill="#27c93f"/>
  <text x="{width - 24}" y="28" fill="#8b949e" font-size="12" font-family="ui-monospace, SFMono-Regular, monospace" text-anchor="end">build.sh</text>
  <line x1="16" y1="44" x2="{width - 16}" y2="44" stroke="#21262d" stroke-width="1"/>

  <!-- Background Physics Watermark (Kiryu Sento Formula Effect) -->
  <g font-family="ui-monospace, monospace" font-size="10" fill="#58a6ff" opacity="0.08" select-none="true">
    <text x="24" y="78">∇ × E = -∂B/∂t</text>
    <text x="{width - 130}" y="82">iℏ(∂ψ/∂t) = Ĥψ</text>
    <text x="20" y="132">E² = (pc)² + (mc²)²</text>
    <text x="{width - 120}" y="136">∮ B·dl = μ₀I</text>
    <text x="24" y="236">S = k_B ln Ω</text>
    <text x="{width - 90}" y="236">F = ma</text>
    <text x="22" y="318">∇ · D = ρ</text>
    <text x="{width - 105}" y="318">λ = h / p</text>
  </g>

  <!-- Sprite Character -->
  <g transform="translate({cx - 50}, 52)">
    <image href="data:image/webp;base64,{sprite_b64}" width="100" height="100"/>
  </g>

  <!-- Quotes & Content -->
  <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif" text-anchor="middle">
    <!-- Quote 1 -->
    <text x="{cx}" y="174" fill="#58a6ff" font-size="14" font-weight="600">さぁ、実験を始めようか？</text>
    <text x="{cx}" y="194" fill="#c9d1d9" font-size="12" font-style="italic">Shall we begin the experiment?</text>
    <text x="{cx}" y="212" fill="#8b949e" font-size="11">Nah, mari kita mulai eksperimennya!</text>

    <!-- Line divider -->
    <line x1="70" y1="230" x2="{width - 70}" y2="230" stroke="#21262d" stroke-width="1"/>

    <!-- Quote 2 -->
    <text x="{cx}" y="258" fill="#f78166" font-size="14" font-weight="600">勝利の法則は決まった！</text>
    <text x="{cx}" y="278" fill="#c9d1d9" font-size="12" font-style="italic">The formula for victory is set!</text>
    <text x="{cx}" y="296" fill="#8b949e" font-size="11">Hukum kemenangannya telah ditentukan!</text>

    <!-- Best Match Tag -->
    <rect x="{cx - 160}" y="324" width="320" height="42" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1"/>
    <text x="{cx}" y="342" fill="#3fb950" font-size="11" font-weight="600" font-family="ui-monospace, monospace">Physics (Rabbit) × Code (Tank)</text>
    <text x="{cx}" y="356" fill="#e6edf3" font-size="11" font-weight="bold" font-family="ui-monospace, monospace">= BEST MATCH!</text>
  </g>

  <!-- Terminal Footer -->
  <text x="24" y="{height - 18}" fill="#484f58" font-size="11" font-family="ui-monospace, monospace">formula: verified // v1.0</text>
</svg>
'''
    with open("assets/build-card.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Sukses! assets/build-card.svg diperbarui dengan ukuran {width}x{height}")

if __name__ == "__main__":
    generate_svg()
