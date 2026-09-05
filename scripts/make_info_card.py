def generate_info_card():
  # Daftar baris informasi (Label, Nilai, Warna Label)
  lines = [
      ("user", "mkfazvi@azvi-vivobook", "#58a6ff"),
      ("os", "Ubuntu 24.04 LTS x86_64", "#3fb950"),
      ("host", "VivoBook ASUSLaptop K3402ZA", "#3fb950"),
      ("role", "Engineering Physics Student & Dev", "#e3b341"),
      ("focus", "AI, IoT & Full-Stack Development", "#f0883e"),
      ("stack", "Go, Python, React, Docker, OpenCV", "#d29922"),
      ("tools", "KiCad, DBeaver, Portainer, Linux", "#bc8cff"),
      ("uptime", "4th year of non-stop engineering", "#58a6ff"),
  ]

  y_start = 75
  line_height = 24
  svg_lines = []

  for idx, (label, val, color) in enumerate(lines):
    delay = 0.1 + (idx * 0.08)
    svg_lines.append(f"""
    <g class="line" style="animation-delay: {delay:.2f}s;">
      <text x="30" y="{y_start + (idx * line_height)}" class="label" fill="{color}">{label}</text>
      <text x="95" y="{y_start + (idx * line_height)}" class="sep" fill="#6e7681">~</text>
      <text x="115" y="{y_start + (idx * line_height)}" class="val" fill="#c9d1d9">{val}</text>
    </g>""")

  # Color palette blocks khas Neofetch
  palette_y = y_start + (len(lines) * line_height) + 15
  colors = [
      "#ff7b72",
      "#3fb950",
      "#d29922",
      "#58a6ff",
      "#bc8cff",
      "#39c5cf",
      "#b1bac4",
  ]
  palette_rects = "".join([
      f'<rect x="{30 + (i * 22)}" y="{palette_y}" width="16" height="12"'
      f' rx="2" fill="{c}"/>'
      for i, c in enumerate(colors)
  ])

  svg_content = f"""<svg width="490" height="340" viewBox="0 0 490 340" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .line {{
      opacity: 0;
      transform: translateY(4px);
      animation: fadeIn 0.3s ease forwards;
    }}
    @keyframes fadeIn {{
      to {{
        opacity: 1;
        transform: translateY(0);
      }}
    }}
    .title {{
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      font-size: 12px;
      font-weight: bold;
      fill: #8b949e;
    }}
    .label {{
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      font-size: 12px;
      font-weight: 600;
    }}
    .sep {{
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      font-size: 12px;
    }}
    .val {{
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      font-size: 12px;
    }}
  </style>

  <!-- Background Box -->
  <rect width="490" height="340" rx="8" fill="#0d1117" stroke="#21262d" stroke-width="1"/>

  <!-- macOS / Terminal Window Dots -->
  <circle cx="28" cy="24" r="5" fill="#ff5f56"/>
  <circle cx="44" cy="24" r="5" fill="#ffbd2e"/>
  <circle cx="60" cy="24" r="5" fill="#27c93f"/>
  <text x="460" y="28" class="title" text-anchor="end">neofetch</text>

  <line x1="20" y1="44" x2="470" y2="44" stroke="#21262d" stroke-width="1"/>

  <!-- Content Rows -->
  {''.join(svg_lines)}

  <!-- Neofetch Color Dots -->
  {palette_rects}
</svg>
"""

  with open("info-card.svg", "w") as f:
    f.write(svg_content)
  print("Berhasil membuat file info-card.svg")


if __name__ == "__main__":
  generate_info_card()
