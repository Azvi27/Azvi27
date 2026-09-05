import os
from PIL import Image, ImageEnhance, ImageOps

# Karakter kerapatan cahaya pada terminal gelap:
# Spasi ' ' dikhususkan HANYA untuk background transparan.
# Area tubuh (rambut, kemeja, kulit) selalu memiliki karakter agar siluet tidak bolong.
ASCII_RAMP = [".", ":", "-", "=", "+", "*", "#", "%", "@"]


def image_to_ascii(image_path, target_width=70):
  if not os.path.exists(image_path):
    raise FileNotFoundError(f"File {image_path} tidak ditemukan!")

  img = Image.open(image_path).convert("RGBA")

  # 1. Potong otomatis seluruh ruang kosong transparan di pinggir foto
  bbox = img.getbbox()
  if bbox:
    img = img.crop(bbox)

  # 2. Sesuaikan proporsi font terminal (tinggi karakter ~1.8x lebarnya)
  aspect_ratio = img.height / img.width
  target_height = int(target_width * aspect_ratio * 0.55)

  img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

  r, g, b, a = img.split()
  rgb = Image.merge("RGB", (r, g, b))

  # 3. Optimalkan kontras wajah dan ketajaman garis kacamata/kabel
  gray = rgb.convert("L")
  gray = ImageOps.autocontrast(gray, cutoff=2)
  gray = ImageEnhance.Sharpness(gray).enhance(2.0)
  gray = ImageEnhance.Contrast(gray).enhance(1.4)

  pixels = list(gray.getdata())
  alphas = list(a.getdata())

  lines = []
  for row in range(target_height):
    line_chars = []
    for col in range(target_width):
      idx = row * target_width + col
      # Background transparan = Spasi murni
      if alphas[idx] < 50:
        line_chars.append(" ")
      else:
        # Tubuh manusia: skala nilai 0-255 ke indeks 0 s/d 8
        val = pixels[idx]
        char_idx = int((val / 255.0) * (len(ASCII_RAMP) - 1))
        line_chars.append(ASCII_RAMP[char_idx])
    lines.append("".join(line_chars))

  return lines


def generate_ascii_svg():
  img_path = (
      "assets/avatar.png"
      if os.path.exists("assets/avatar.png")
      else "assets/avatar.jpg"
  )
  target_width = 72
  lines = image_to_ascii(img_path, target_width=target_width)

  # Penataan vertikal dan horizontal agar simetris di tengah jendela
  y_start = 64
  line_height = 5.6
  max_lines = 46

  text_elements = []
  for idx, line in enumerate(lines[:max_lines]):
    delay = 0.03 + (idx * 0.015)
    safe_line = (
        line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )
    text_elements.append(
        f'<text x="22" y="{y_start + (idx * line_height):.1f}"'
        f' style="animation-delay: {delay:.2f}s;">{safe_line}</text>'
    )

  svg_content = f"""<svg width="350" height="340" viewBox="0 0 350 340" fill="none" xmlns="http://www.w3.org/2000/svg" xml:space="preserve">
  <style>
    text {{
      fill: #c9d1d9;
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      font-size: 5.1px;
      white-space: pre;
      opacity: 0;
      animation: scanline 0.25s ease forwards;
    }}
    @keyframes scanline {{
      to {{
        opacity: 1;
      }}
    }}
    .title {{
      font-size: 12px;
      font-weight: bold;
      fill: #8b949e;
      white-space: normal;
      opacity: 1;
      animation: none;
    }}
    .subtext {{
      font-size: 9px;
      fill: #484f58;
      white-space: normal;
      opacity: 1;
      animation: none;
    }}
  </style>

  <!-- Frame Window -->
  <rect width="350" height="340" rx="8" fill="#0d1117" stroke="#21262d" stroke-width="1"/>

  <!-- macOS Dots -->
  <circle cx="24" cy="24" r="5" fill="#ff5f56"/>
  <circle cx="40" cy="24" r="5" fill="#ffbd2e"/>
  <circle cx="56" cy="24" r="5" fill="#27c93f"/>
  <text x="325" y="28" class="title" text-anchor="end">portrait.sh</text>

  <line x1="15" y1="44" x2="335" y2="44" stroke="#21262d" stroke-width="1"/>

  <!-- Matriks ASCII -->
  {''.join(text_elements)}

  <text x="22" y="328" class="subtext">rendered: azvi-terminal-v1.0</text>
</svg>
"""

  with open("azvi-ascii.svg", "w") as f:
    f.write(svg_content)
  print("Berhasil membuat file azvi-ascii.svg dengan white-space preserved!")


if __name__ == "__main__":
  generate_ascii_svg()
