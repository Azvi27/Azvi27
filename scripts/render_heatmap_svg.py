from datetime import datetime
import json

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]


def generate_svg():
  with open("data/contributions.json", "r") as f:
    payload = json.load(f)

  days = payload["days"]
  total_str = payload.get("total", "300 contributions in the last year")

  # Ukuran grid proporsional untuk lebar 860px
  box_size = 11
  gap = 4
  start_x = 35
  start_y = 35

  first_date = datetime.strptime(days[0]["date"], "%Y-%m-%d")
  start_day_offset = (first_date.weekday() + 1) % 7

  svg_rects = []
  month_positions = {}
  max_x = start_x

  for idx, item in enumerate(days):
    grid_index = idx + start_day_offset
    col = grid_index // 7
    row = grid_index % 7

    x = start_x + col * (box_size + gap)
    y = start_y + row * (box_size + gap)
    if x > max_x:
      max_x = x

    lvl = item.get("level", 0)
    color = PALETTE[lvl] if lvl < len(PALETTE) else PALETTE[-1]

    delay = (col * 0.008) + (row * 0.015)
    rect = (
        f'<rect class="box" x="{x}" y="{y}" width="{box_size}"'
        f' height="{box_size}" rx="2" fill="{color}" style="animation-delay:'
        f' {delay:.3f}s;" />'
    )
    svg_rects.append(rect)

    # Catat posisi teks nama bulan
    dt = datetime.strptime(item["date"], "%Y-%m-%d")
    month_name = dt.strftime("%b")
    if dt.day <= 7 and month_name not in month_positions:
      month_positions[month_name] = x

  # Posisi ujung kanan grid visual yang presisi
  grid_right = max_x + box_size

  # Posisi vertikal footer dan legenda (rapat dan presisi di bawah grid)
  footer_y = start_y + (7 * (box_size + gap)) + 14  # ~154px
  legend_box_y = footer_y - 9  # ~145px
  svg_height = footer_y + 20  # ~174px

  # Label bulan
  month_labels = [
      f'<text x="{pos}" y="22" class="label">{m}</text>'
      for m, pos in month_positions.items()
  ]

# Koordinat kotak legenda dengan jarak aman agar tidak menabrak teks
    b4 = grid_right - 48 - box_size
    b3 = b4 - 13
    b2 = b3 - 13
    b1 = b2 - 13
    b0 = b1 - 13
    less_x = b0 - 8

    svg_content = f"""<svg width="860" height="{svg_height}" viewBox="0 0 860 {svg_height}" fill="none" xmlns="http://www.w3.org/2000/svg">
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

  <rect width="860" height="{svg_height}" rx="8" fill="#0d1117" stroke="#21262d" stroke-width="1"/>

  <!-- Bulan -->
  {''.join(month_labels)}

  <!-- Hari -->
  <text x="12" y="60" class="label">Mon</text>
  <text x="12" y="90" class="label">Wed</text>
  <text x="12" y="120" class="label">Fri</text>

  <!-- Kotak Grid -->
  {''.join(svg_rects)}

  <!-- Footer Info -->
  <text x="{start_x}" y="{footer_y}" class="footer">{total_str}</text>

  <!-- Legenda Less ... More -->
  <text x="{less_x}" y="{footer_y}" class="label" text-anchor="end">Less</text>
  <rect x="{b0}" y="{legend_box_y}" width="10" height="10" rx="2" fill="#161b22"/>
  <rect x="{b1}" y="{legend_box_y}" width="10" height="10" rx="2" fill="#0e4429"/>
  <rect x="{b2}" y="{legend_box_y}" width="10" height="10" rx="2" fill="#006d32"/>
  <rect x="{b3}" y="{legend_box_y}" width="10" height="10" rx="2" fill="#26a641"/>
  <rect x="{b4}" y="{legend_box_y}" width="10" height="10" rx="2" fill="#39d353"/>
  <text x="{grid_right}" y="{footer_y}" class="label" text-anchor="end">More</text>
</svg>
"""
