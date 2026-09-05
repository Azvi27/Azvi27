import os
from PIL import Image, ImageEnhance

# Karakter dari tipis ke padat untuk terminal gelap:
# Bagian bayangan/gelap = karakter tipis
# Bagian terang (kulit, kacamata, highlight) = karakter padat (@, %, #)
ASCII_CHARS = [" ", ".", ":", "-", "=", "+", "*", "#", "%", "@"]


def image_to_ascii(image_path, width=72):
  if not os.path.exists(image_path):
    raise FileNotFoundError(f"File {image_path} tidak ditemukan!")

  img = Image.open(image_path).convert("RGBA")

  # Rasio aspek font terminal (tinggi karakter ~1.9x lebarnya)
  aspect_ratio = img.height / img.width
  height = int(width * aspect_ratio * 0.52)

  img = img.resize((width, height), Image.Resampling.LANCZOS)

  # Pisahkan channel RGB dan Alpha
  r, g, b, a = img.split()
  rgb_img = Image.merge("RGB", (r, g, b))

  # Naikkan kontras agar garis kacamata, senyum, dan kabel menonjol tajam
  gray = rgb_img.convert("L")
  enhancer = ImageEnhance.Contrast(gray)
  enhanced = enhancer.enhance(1.7)

  pixels = list(enhanced.getdata())
  alphas = list(a.getdata())

  lines = []
  for row in range(height):
    line_chars = []
    for col in range(width):
      idx = row * width + col
      # Jika piksel transparan (latar belakang), ganti dengan spasi kosong
      if alphas[idx] < 60:
        line_chars.append(" ")
      else:
        val = pixels[idx]
        char_idx = val * len(ASCII_CHARS) // 256
        if char_idx >= len(ASCII_CHARS):
          char_idx = len(ASCII_CHARS) - 1
        line_chars.append(ASCII_CHARS[char_idx])
    lines.append("".join(line_chars))

  return lines


def generate_ascii_svg():
  img_path = (
      "assets/avatar.png"
      if os.path.exists("assets/avatar.png")
      else "assets/avatar.jpg"
  )
  lines = image_to_ascii(img_path, width=72)

  y_start = 62
  line_height = 5.4
  text_elements = []

  # Batasi baris agar pas di kartu terminal tinggi 340px
  for idx, line in enumerate(lines[:49]):
    delay = 0.04 + (idx * 0.015)
    safe_line = (
        line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )
    text_elements.append(
        f'<text x="16" y="{y_start + (idx * line_height):.1f}" '
        f'style="animation-delay: {delay:.2f}s;">{safe_line}</text>'
    )

  svg_content = f"""<svg width="350" height="340" viewBox="0 0 350 340" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    text {{
      fill: #8b949e;
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      font-size: 4.6px;
      letter-spacing: 0.5px;
      opacity: 0;
      animation: scanline 0.22s ease forwards;
    }}
    @keyframes scanline {{
      to {{
        opacity: 1;
      }}
    }}
    .title {{
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      font-size: 12px;
      font-weight: bold;
      fill: #8b949e;
      opacity: 1;
      animation: none;
    }}
    .subtext {{
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      font-size: 9px;
      fill: #484f58;
      opacity: 1;
      animation: none;
    }}
  </style>

  <!-- Frame Terminal -->
  <rect width="350" height="340" rx="8" fill="#0d1117" stroke="#21262d" stroke-width="1"/>

  <!-- Window Dots -->
  <circle cx="24" cy="24" r="5" fill="#ff5f56"/>
  <circle cx="40" cy="24" r="5" fill="#ffbd2e"/>
  <circle cx="56" cy="24" r="5" fill="#27c93f"/>
  <text x="325" y="28" class="title" text-anchor="end">portrait.sh</text>

  <line x1="15" y1="44" x2="335" y2="44" stroke="#21262d" stroke-width="1"/>

  <!-- Matriks Karakter ASCII -->
  {''.join(text_elements)}

  <!-- Footer Info Mirip Avi -->
  <text x="18" y="328" class="subtext">rendered: azvi-terminal-v1.0</text>
</svg>
"""

  with open("azvi-ascii.svg", "w") as f:
    f.write(svg_content)
  print("Berhasil membuat file azvi-ascii.svg tanpa noise latar belakang!")


if __name__ == "__main__":
  generate_ascii_svg()
