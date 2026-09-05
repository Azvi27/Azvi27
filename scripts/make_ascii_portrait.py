import os
from PIL import Image

# Kerapatan karakter dari gelap ke terang
ASCII_CHARS = [" ", ".", ":", "-", "=", "+", "*", "#", "%", "@"]


def image_to_ascii(image_path, width=48):
  if not os.path.exists(image_path):
    raise FileNotFoundError(f"File foto {image_path} tidak ditemukan!")

  img = Image.open(image_path).convert("L")  # Ubah ke Grayscale
  aspect_ratio = img.height / img.width
  # Karakter font monospace biasanya 2x lebih tinggi daripada lebar, kalikan 0.55
  height = int(width * aspect_ratio * 0.55)
  img = img.resize((width, height))

  pixels = img.getdata()
  characters = [ASCII_CHARS[pixel * len(ASCII_CHARS) // 256] for pixel in pixels]
  lines = [
      "".join(characters[i : i + width]) for i in range(0, len(characters), width)
  ]
  return lines


def generate_ascii_svg():
  # Cari avatar.jpg atau avatar.png
  img_path = (
      "assets/avatar.jpg"
      if os.path.exists("assets/avatar.jpg")
      else "assets/avatar.png"
  )
  lines = image_to_ascii(img_path, width=46)

  y_start = 65
  line_height = 8.5
  text_elements = []

  for idx, line in enumerate(lines[:31]):  # Batasi agar pas di tinggi 340px
    delay = 0.05 + (idx * 0.03)
    # Sanitasi karakter XML
    safe_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text_elements.append(
        f'<text x="25" y="{y_start + (idx * line_height):.1f}"'
        f' style="animation-delay: {delay:.2f}s;">{safe_line}</text>'
    )

  svg_content = f"""<svg width="350" height="340" viewBox="0 0 350 340" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    text {{
      fill: #8b949e;
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      font-size: 7.8px;
      letter-spacing: 1.5px;
      opacity: 0;
      animation: scanline 0.25s ease forwards;
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
  </style>

  <!-- Window Frame -->
  <rect width="350" height="340" rx="8" fill="#0d1117" stroke="#21262d" stroke-width="1"/>

  <!-- macOS Window Controls -->
  <circle cx="24" cy="24" r="5" fill="#ff5f56"/>
  <circle cx="40" cy="24" r="5" fill="#ffbd2e"/>
  <circle cx="56" cy="24" r="5" fill="#27c93f"/>
  <text x="325" y="28" class="title" text-anchor="end">portrait.sh</text>

  <line x1="15" y1="44" x2="335" y2="44" stroke="#21262d" stroke-width="1"/>

  <!-- ASCII Art Matrix -->
  {''.join(text_elements)}
</svg>
"""

  with open("azvi-ascii.svg", "w") as f:
    f.write(svg_content)
  print("Berhasil membuat file azvi-ascii.svg")


if __name__ == "__main__":
  generate_ascii_svg()
