import json
from datetime import datetime

# Palet warna GitHub Dark Mode asli
PALETTE = [
    "#161b22",  # 0: Kosong
    "#0e4429",  # 1: Sedikit
    "#006d32",  # 2: Sedang
    "#26a641",  # 3: Banyak
    "#39d353"   # 4: Sangat banyak
]

def generate_svg():
    with open("data/contributions.json", "r") as f:
        data = json.load(f)

    rows = 7
    box_size = 10
    gap = 3
    start_x = 40
    start_y = 42

    svg_rects = []
    month_labels = []
    last_month = None

    for i, item in enumerate(data):
        col = i // rows
        row = i % rows

        x = start_x + col * (box_size + gap)
        y = start_y + row * (box_size + gap)

        lvl = item.get("level", 0)
        color = PALETTE[lvl] if lvl < len(PALETTE) else PALETTE[-1]

        # Efek animasi diagonal halus
        delay = (col * 0.012) + (row * 0.02)

        rect = (
            f'<rect class="box" x="{x}" y="{y}" width="{box_size}" height="{box_size}" '
            f'rx="2" fill="{color}" style="animation-delay: {delay:.3f}s;" />'
        )
        svg_rects.append(rect)

        # Label Bulan: pasang nama bulan pada kolom pertama kemunculannya di baris 0
        if row == 0:
            dt = datetime.strptime(item["date"], "%Y-%m-%d")
            m_name = dt.strftime("%b")
            if m_name != last_month:
                month_labels.append(f'<text x="{x}" y="30" class="meta-text">{m_name}</text>')
                last_month = m_name

    svg_content = f"""<svg width="860" height="185" viewBox="0 0 860 185" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .box {{
      opacity: 0;
      transform: translateY(-4px);
      animation: reveal 0.3s ease forwards;
    }}
    @keyframes reveal {{
      to {{
        opacity: 1;
        transform: translateY(0);
      }}
    }}
    .prompt {{
      fill: #58a6ff;
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      font-size: 13px;
      font-weight: 600;
    }}
    .meta-text {{
      fill: #7d8590;
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      font-size: 10px;
    }}
    .footer-stat {{
      fill: #e6edf3;
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      font-size: 12px;
      font-weight: 500;
    }}
  </style>

  <!-- Background Terminal Box -->
  <rect width="860" height="185" rx="8" fill="#0d1117" stroke="#30363d" stroke-width="1"/>

  <!-- Bulan -->
  {''.join(month_labels)}

  <!-- Hari -->
  <text x="12" y="62" class="meta-text">Mon</text>
  <text x="12" y="88" class="meta-text">Wed</text>
  <text x="12" y="114" class="meta-text">Fri</text>

  <!-- Heatmap Boxes -->
  {''.join(svg_rects)}

  <!-- Footer Stat -->
  <text x="40" y="163" class="footer-stat">298 contributions in the last year</text>

  <!-- Legenda -->
  <text x="695" y="163" class="meta-text">Less</text>
  <rect x="730" y="153" width="10" height="10" rx="2" fill="#161b22"/>
  <rect x="743" y="153" width="10" height="10" rx="2" fill="#0e4429"/>
  <rect x="756" y="153" width="10" height="10" rx="2" fill="#006d32"/>
  <rect x="769" y="153" width="10" height="10" rx="2" fill="#26a641"/>
  <rect x="782" y="153" width="10" height="10" rx="2" fill="#39d353"/>
  <text x="798" y="163" class="meta-text">More</text>
</svg>
"""
    with open("contrib-heatmap.svg", "w") as f:
        f.write(svg_content)
    print("Berhasil me-render contrib-heatmap.svg terbaru!")

if __name__ == "__main__":
    generate_svg()
