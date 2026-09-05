import os
import re
import base64

def patch_ascii_card_with_animation():
    """Menghapus header lama dan menyuntikkan animasi terminal typing ke azvi-ascii.svg"""
    if not os.path.exists("azvi-ascii.svg"):
        return 420, 480

    with open("azvi-ascii.svg", "r", encoding="utf-8") as f:
        content = f.read()

    # Bersihkan sisa tombol dan header
    content = re.sub(r'<circle[^>]*>', '', content)
    content = re.sub(r'<text[^>]*>portrait\.sh</text>', '', content)
    content = re.sub(r'<line[^>]*y1="4[04]"[^>]*/>', '', content)

    # Dapatkan dimensi
    w, h = 420, 480
    vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', content)
    if vb:
        w, h = int(vb.group(1)), int(vb.group(2))

    # Sisipkan CSS animasi terminal scan/typing jika belum ada
    if "<style>" not in content:
        anim_css = """
  <defs>
    <style>
      @keyframes terminalScan {
        0% { clip-path: inset(0 0 100% 0); opacity: 0.2; }
        15% { opacity: 1; }
        100% { clip-path: inset(0 0 0% 0); opacity: 1; }
      }
      .animated-ascii {
        animation: terminalScan 2.4s steps(45) forwards;
      }
    </style>
  </defs>"""
        content = content.replace("<svg", "<svg" + anim_css, 1)
        # Tambahkan class animated-ascii ke tag g utama pembungkus teks
        content = re.sub(r'<g([^>]*)font-family', r'<g\1class="animated-ascii" font-family', content, count=1)

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
  <defs>
    <!-- Gradien Perpaduan Merah (Rabbit) dan Biru (Tank) -->
    <linearGradient id="bestmatch-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ff334b" />
      <stop offset="50%" stop-color="#c054e8" />
      <stop offset="100%" stop-color="#2f81f7" />
    </linearGradient>
    <style>
      @keyframes pulseText {{
        0%, 100% {{ opacity: 0.85; }}
        50% {{ opacity: 1; transform: scale(1.02); }}
      }}
      .ready-callout {{
        animation: pulseText 2.5s infinite ease-in-out;
      }}
    </style>
  </defs>

  <!-- Card Frame -->
  <rect width="{width}" height="{height}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>

  <!-- SISI KIRI: Sprite Kamen Rider Build (Proporsional & Seimbang) -->
  <g transform="translate(18, 48)">
    <image href="data:image/webp;base64,{sprite_b64}" width="138" height="138"/>
  </g>

  <!-- SISI KANAN: Kutipan 3 Bahasa -->
  <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif">
    <!-- Quote 1 -->
    <text x="162" y="66" fill="#58a6ff" font-size="13.5" font-weight="600">さぁ、実験を始めようか？</text>
    <text x="162" y="86" fill="#c9d1d9" font-size="11.5" font-style="italic">Shall we begin the experiment?</text>
    <text x="162" y="104" fill="#8b949e" font-size="10.5">Nah, mari kita mulai eksperimennya!</text>

    <!-- Divider halus antar quote -->
    <line x1="162" y1="120" x2="{width - 24}" y2="120" stroke="#21262d" stroke-width="1"/>

    <!-- Quote 2 -->
    <text x="162" y="142" fill="#f78166" font-size="13.5" font-weight="600">勝利の法則は決まった！</text>
    <text x="162" y="162" fill="#c9d1d9" font-size="11.5" font-style="italic">The formula for victory is set!</text>
    <text x="162" y="180" fill="#8b949e" font-size="10.5">Hukum kemenangannya telah ditentukan!</text>
  </g>

  <!-- TRANSISI HENSHIN: Are You Ready? -->
  <g class="ready-callout" font-family="ui-monospace, 'Courier New', monospace" text-anchor="middle">
    <text x="{cx}" y="{height - 128}" fill="#d29922" font-size="11.5" font-weight="bold" letter-spacing="3">
      [ DRIVER: "ARE YOU READY?" ]
    </text>
  </g>

  <!-- BAGIAN BAWAH: Best Match Banner Bergaya Pixel Monospace -->
  <g transform="translate(20, {height - 116})">
    <rect width="{width - 40}" height="76" rx="6" fill="#161b22" stroke="#30363d" stroke-width="1.5"/>
    
    <!-- Rabbit (Merah) x Tank (Biru) -->
    <text x="{(width - 40) / 2}" y="30" text-anchor="middle" font-family="ui-monospace, monospace" font-size="12" font-weight="bold">
      <tspan fill="#ff4d4d">◆ Rabbit [Fisika]</tspan>
      <tspan fill="#8b949e"> × </tspan>
      <tspan fill="#388bfd">Tank [Kode] ◆</tspan>
    </text>

    <!-- BEST MATCH! dengan Gradasi Campuran Merah + Biru -->
    <text x="{(width - 40) / 2}" y="56" text-anchor="middle" font-family="ui-monospace, monospace" font-size="15" font-weight="900" letter-spacing="3" fill="url(#bestmatch-grad)">
      = BEST MATCH! =
    </text>
  </g>

  <!-- Terminal Footer Simetris -->
  <text x="24" y="{height - 18}" fill="#484f58" font-size="11" font-family="ui-monospace, monospace">kernel: best-match-v1.0 // formula: verified</text>
</svg>
'''
    with open("assets/build-card.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[✓] Kartu Build & ASCII berhasil diperbarui dengan efek animasi ({width}x{height})")

if __name__ == "__main__":
    w, h = patch_ascii_card_with_animation()
    generate_build_card(w, h)
