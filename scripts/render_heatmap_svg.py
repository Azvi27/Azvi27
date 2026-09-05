import json

# Palet warna khas heatmap hijau GitHub (level 0 sampai 4)
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

def generate_svg():
    with open("data/contributions.json", "r") as f:
        data = json.load(f)

    # Konfigurasi grid 53 minggu x 7 hari
    rows = 7
    box_size = 11
    gap = 4
    start_x = 25
    start_y = 40

    svg_rects = []

    for i, item in enumerate(data):
        col = i // rows
        row = i % rows

        x = start_x + col * (box_size + gap)
        y = start_y + row * (box_size + gap)

        lvl = item.get("level", 0)
        color = PALETTE[lvl] if lvl < len(PALETTE) else PALETTE[-1]

        # Efek animasi drop-in beruntun secara diagonal
        delay = (col * 0.015) + (row * 0.03)

        rect = (
            f'<rect class="box" x="{x}" y="{y}" width="{box_size}" height="{box_size}" '
            f'rx="2" fill="{color}" style="animation-delay: {delay:.3f}s;" />'
        )
        svg_rects.append(rect)

    svg_content = f"""<svg width="860" height="160" viewBox="0 0 860 160" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .box {{
      opacity: 0;
      transform: translateY(-6px);
      animation: dropIn 0.35s ease forwards;
    }}
    @keyframes dropIn {{
      to {{
        opacity: 1;
        transform: translateY(0);
      }}
    }}
    .title {{
      fill: #58a6ff;
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
      font-size: 13px;
      font-weight: 600;
    }}
    .legend-text {{
      fill: #8b949e;
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
      font-size: 11px;
    }}
  </style>
  <rect width="860" height="160" rx="8" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>
  <text x="25" y="26" class="title">Azvi27@github:~$ ./contributions --last-year</text>
  {''.join(svg_rects)}

  <!-- Legenda Less -> More -->
  <text x="690" y="148" class="legend-text">Less</text>
  <rect x="725" y="139" width="10" height="10" rx="2" fill="#161b22"/>
  <rect x="739" y="139" width="10" height="10" rx="2" fill="#0e4429"/>
  <rect x="753" y="139" width="10" height="10" rx="2" fill="#006d32"/>
  <rect x="767" y="139" width="10" height="10" rx="2" fill="#26a641"/>
  <rect x="781" y="139" width="10" height="10" rx="2" fill="#39d353"/>
  <text x="797" y="148" class="legend-text">More</text>
</svg>
"""
    with open("contrib-heatmap.svg", "w") as f:
        f.write(svg_content)
    print("Berhasil membuat file contrib-heatmap.svg")

if __name__ == "__main__":
    generate_svg()
