from datetime import datetime
import json

# Warna resmi GitHub Dark Mode
PALETTE = [
    "#161b22",  # Level 0 (gelap kosong)
    "#0e4429",  # Level 1
    "#006d32",  # Level 2
    "#26a641",  # Level 3
    "#39d353",  # Level 4
]


def generate_svg():
  with open("data/contributions.json", "r") as f:
    raw = json.load(f)

  data = raw.get("days", raw) if isinstance(raw, dict) else raw
  total_stat = raw.get("total", "298") if isinstance(raw, dict) else "298"

  box_size = 10
  gap = 3
  start_x = 42
  start_y = 38

  svg_rects = []
  month_labels = {}

  for i, item in enumerate(data):
    col = i // 7
    row = i % 7

    x = start_x + col * (box_size + gap)
    y = start_y + row * (box_size + gap)

    lvl = item.get("level", 0)
    color = PALETTE[lvl] if lvl < len(PALETTE) else PALETTE[-1]

    # Staggered animation
    delay = (col * 0.01) + (row * 0.015)

    rect = (
        f'<rect class="box" x="{x}" y="{y}" width="{box_size}"'
        f' height="{box_size}" rx="2" fill="{color}" style="animation-delay:'
        f' {delay:.3f}s;" />'
    )
    svg_rects.append(rect)

    # Petakan bulan: ambil hanya saat tanggal <= 7 agar tercatat sekali di awal bulan
    dt = datetime.strptime(item["date"], "%Y-%m-%d")
    m_name = dt.strftime("%b")
    if dt.day <= 7 and m_name not in month_labels:
      month_labels[m_name] = x

  # Buat elemen SVG untuk label bulan
  months_svg = [
      f'<text x="{pos}" y="24" class="label">{name}</text>'
      for name, pos in month_labels.items()
  ]

  svg_content = f"""<svg width="860" height="175" viewBox="0 0 860 175" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .box {{
      opacity: 0;
      transform: translateY(-4px);
      animation: dropIn 0.3s ease forwards;
    }}
    @keyframes dropIn {{
      to {{
        opacity: 1;
        transform: translateY(0);
      }}
    }}
    .label {{
      fill: #8b949e;
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      font-size: 11px;
    }}
    .footer {{
      fill: #c9d1d9;
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      font-size: 12px;
    }}
  </style>

  <!-- Latar Belakang Kartu Kontribusi -->
  <rect width="860" height="175" rx="8" fill="#0d1117" stroke="#21262d" stroke-width="1"/>

  <!-- Nama Bulan -->
  {''.join(months_svg)}

  <!-- Nama Hari -->
  <text x="14" y="58" class="label">Mon</text>
  <text x="14" y="84" class="label">Wed</text>
  <text x="14" y="110" class="label">Fri</text>

  <!-- Kotak Grid -->
  {''.join(svg_rects)}

  <!-- Footer -->
  <text x="42" y="154" class="footer">{total_stat} contributions in the last year</text>

  <!-- Legend -->
  <text x="690" y="154" class="label">Less</text>
  <rect x="726" y="145" width="10" height="10" rx="2" fill="#161b22"/>
  <rect x="739" y="145" width="10" height="10" rx="2" fill="#0e4429"/>
  <rect x="752" y="145" width="10" height="10" rx="2" fill="#006d32"/>
  <rect x="765" y="145" width="10" height="10" rx="2" fill="#26a641"/>
  <rect x="778" y="145" width="10" height="10" rx="2" fill="#39d353"/>
  <text x="795" y="154" class="label">More</text>
</svg>
"""

  with open("contrib-heatmap.svg", "w") as f:
    f.write(svg_content)
  print("contrib-heatmap.svg berhasil diperbaiki!")


if __name__ == "__main__":
  generate_svg()
