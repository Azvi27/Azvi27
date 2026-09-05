from datetime import datetime
import json

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]


def generate_svg():
  with open("data/contributions.json", "r") as f:
    payload = json.load(f)

  days = payload["days"]
  total_str = payload.get("total", "299 contributions in the last year")

  box_size = 10
  gap = 3
  start_x = 42
  start_y = 38

  # Hari pertama dalam kalender
  first_date = datetime.strptime(days[0]["date"], "%Y-%m-%d")
  # Hari dalam seminggu untuk item pertama (0: Senin, 6: Minggu)
  # GitHub memulai grid dari Sunday (0 di US calendar)
  # Di Python: weekday() -> Monday=0, Sunday=6.
  # Konversi ke Sunday=0: (weekday + 1) % 7
  start_day_offset = (first_date.weekday() + 1) % 7

  svg_rects = []
  month_positions = {}

  for idx, item in enumerate(days):
    grid_index = idx + start_day_offset
    col = grid_index // 7
    row = grid_index % 7

    x = start_x + col * (box_size + gap)
    y = start_y + row * (box_size + gap)

    lvl = item.get("level", 0)
    color = PALETTE[lvl] if lvl < len(PALETTE) else PALETTE[-1]

    delay = (col * 0.01) + (row * 0.015)
    rect = (
        f'<rect class="box" x="{x}" y="{y}" width="{box_size}"'
        f' height="{box_size}" rx="2" fill="{color}" style="animation-delay:'
        f' {delay:.3f}s;" />'
    )
    svg_rects.append(rect)

    # Catat posisi label bulan jika tanggal adalah awal bulan (1 s/d 7)
    dt = datetime.strptime(item["date"], "%Y-%m-%d")
    month_name = dt.strftime("%b")
    if dt.day <= 7 and month_name not in month_positions:
      month_positions[month_name] = x

  # Buat elemen SVG label bulan
  month_labels = [
      f'<text x="{pos}" y="24" class="label">{m}</text>'
      for m, pos in month_positions.items()
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
      fill: #7d8590;
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      font-size: 11px;
    }}
    .footer {{
      fill: #c9d1d9;
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      font-size: 12px;
    }}
  </style>

  <rect width="860" height="175" rx="8" fill="#0d1117" stroke="#21262d" stroke-width="1"/>

  <!-- Bulan -->
  {''.join(month_labels)}

  <!-- Hari (Minggu=0, Senin=1, Rabu=3, Jumat=5) -->
  <text x="14" y="58" class="label">Mon</text>
  <text x="14" y="84" class="label">Wed</text>
  <text x="14" y="110" class="label">Fri</text>

  <!-- Kotak Grid -->
  {''.join(svg_rects)}

  <!-- Footer -->
  <text x="42" y="154" class="footer">{total_str}</text>

  <!-- Legenda -->
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
  print("contrib-heatmap.svg berhasil di-render ulang!")


if __name__ == "__main__":
  generate_svg()
