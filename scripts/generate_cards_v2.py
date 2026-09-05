import os
import re
import base64

def clean_ascii_card():
    """Menghapus titik merah/kuning/hijau dan header dari azvi-ascii.svg"""
    if not os.path.exists("azvi-ascii.svg"):
        return 420, 480
    
    with open("azvi-ascii.svg", "r", encoding="utf-8") as f:
        content = f.read()

    # Hapus lingkaran titik merah kuning hijau
    content = re.sub(r'<circle[^>]*>', '', content)
    # Hapus teks header portrait.sh
    content = re.sub(r'<text[^>]*>portrait\.sh</text>', '', content)
    # Hapus garis divider header atas jika ada
    content = re.sub(r'<line[^>]*y1="44"[^>]*/>', '', content)
    content = re.sub(r'<line[^>]*y1="40"[^>]*/>', '', content)

    with open("azvi-ascii.svg", "w", encoding="utf-8") as f:
        f.write(content)

    # Ambil ukuran viewBox/height agar build-card.svg sama persis
    w, h = 420, 480
    vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', content)
    if vb:
        w, h = int(vb.group(1)), int(vb.group(2))
    else:
        hm = re.search(r'height="(\d+)"', content)
        wm = re.search(r'width="(\d+)"', content)
        if hm and wm:
            w, h = int(wm.group(1)), int(hm.group(2))
    return w, h

def generate_build_card(width, height):
    sprite_path = "assets/Build_Capsem_Sprite.webp"
    sprite_b64 = ""
    if os.path.exists(sprite_path):
        with open(sprite_path, "rb") as f:
            sprite_b64 = base64.b64encode(f.read()).decode("utf-8")

    svg_content = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Gradien Perpaduan Merah (Rabbit) dan Biru (Tank) -->
    <linearGradient id="bestmatch-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ff334b" />
      <stop offset="50%" stop-color="#c054e8" />
      <stop offset="100%" stop-color="#2f81f7" />
    </linearGradient>
  </defs>

  <!-- Card Frame (Sama persis dengan card ASCII) -->
  <rect width="{width}" height="{height}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>

  <!-- SISI KIRI: Sprite Kamen Rider Build -->
  <g transform="translate(18, 55)">
    <image href="data:image/webp;base64,{sprite_b64}" width="125" height="125"/>
  </g>

  <!-- SISI KANAN: Kutipan 3 Bahasa (Jepang, Inggris, Indonesia) -->
  <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif">
    <!-- Quote 1 -->
    <text x="152" y="68" fill="#58a6ff" font-size="13.5" font-weight="600">さぁ、実験を始めようか？</text>
    <text x="152" y="88" fill="#c9d1d9" font-size="11.5" font-style="italic">Shall we begin the experiment?</text>
    <text x="152" y="106" fill="#8b949e" font-size="10.5">Nah, mari kita mulai eksperimennya!</text>

    <!-- Divider halus antar quote -->
    <line x1="152" y1="124" x2="{width - 24}" y2="124" stroke="#21262d" stroke-width="1"/>

    <!-- Quote 2 -->
    <text x="152" y="148" fill="#f78166" font-size="13.5" font-weight="600">勝利の法則は決まった！</text>
    <text x="152" y="168" fill="#c9d1d9" font-size="11.5" font-style="italic">The formula for victory is set!</text>
    <text x="152" y="186" fill="#8b949e" font-size="10.5">Hukum kemenangannya telah ditentukan!</text>
  </g>

  <!-- BAGIAN BAWAH: Best Match Banner Bergaya Pixel Monospace -->
  <g transform="translate(20, {height - 110})">
    <!-- Pixel Box Container -->
    <rect width="{width - 40}" height="76" rx="6" fill="#161b22" stroke="#30363d" stroke-width="1.5"/>
    
    <!-- Rabbit (Merah) x Tank (Biru) -->
    <text x="{(width - 40) / 2}" y="32" text-anchor="middle" font-family="ui-monospace, 'Courier New', monospace" font-size="12" font-weight="bold">
      <tspan fill="#ff4d4d">◆ Rabbit [Fisika]</tspan>
      <tspan fill="#8b949e"> × </tspan>
      <tspan fill="#388bfd">Tank [Kode] ◆</tspan>
    </text>

    <!-- BEST MATCH! dengan Gradasi Campuran Merah + Biru -->
    <text x="{(width - 40) / 2}" y="58" text-anchor="middle" font-family="ui-monospace, 'Courier New', monospace" font-size="15" font-weight="900" letter-spacing="3" fill="url(#bestmatch-grad)">
      = BEST MATCH! =
    </text>
  </g>
</svg>
'''
    with open("assets/build-card.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[✓] Sukses! azvi-ascii.svg dibersihkan dan assets/build-card.svg disinkronkan ({width}x{height})")

if __name__ == "__main__":
    w, h = clean_ascii_card()
    generate_build_card(w, h)
