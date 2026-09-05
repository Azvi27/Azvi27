import json, os
from datetime import datetime

COLOR_LEVELS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

def render():
    if not os.path.exists("data/contributions.json"):
        print("data/contributions.json tidak ditemukan.")
        return

    with open("data/contributions.json") as f:
        data = json.load(f)

    days = data.get("days", [])
    total_str = data.get("total", "454 contributions in the last year")

    weeks = []
    current_week = []
    for d in days:
        dt = datetime.strptime(d["date"], "%Y-%m-%d")
        w_day = (dt.weekday() + 1) % 7 
        current_week.append((w_day, d.get("level", 0)))
        if w_day == 6:
            weeks.append(current_week)
            current_week = []
    if current_week:
        weeks.append(current_week)

    width = 840
    height = 195

    svg = []
    svg.append(f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">')
    svg.append(f'  <rect width="{width}" height="{height}" rx="12" fill="#0d1117" stroke="#30363d" stroke-width="1"/>')
    
    # CSS & ANIMASI RADAR SWEEP
    svg.append('''  <defs>
    <linearGradient id="radarSweep" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#3fb950" stop-opacity="0" />
      <stop offset="70%" stop-color="#3fb950" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#3fb950" stop-opacity="0.35" />
    </linearGradient>
    <clipPath id="gridClip">
      <rect x="52" y="30" width="765" height="110" rx="4" />
    </clipPath>
    <style>
      @keyframes sweepScan {
        0% { transform: translateX(-150px); }
        50% { transform: translateX(850px); }
        100% { transform: translateX(850px); }
      }
      .radar-scanner {
        animation: sweepScan 5s ease-in-out infinite;
      }
    </style>
  </defs>''')

    # Month Labels
    months = ["Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"]
    for i, m in enumerate(months):
        x = 55 + (i * 64)
        svg.append(f'  <text x="{x}" y="22" fill="#8b949e" font-size="10" font-family="ui-monospace, monospace">{m}</text>')

    # Day of week labels
    svg.append('  <text x="24" y="58" fill="#8b949e" font-size="9" font-family="ui-monospace, monospace">Mon</text>')
    svg.append('  <text x="24" y="88" fill="#8b949e" font-size="9" font-family="ui-monospace, monospace">Wed</text>')
    svg.append('  <text x="24" y="118" fill="#8b949e" font-size="9" font-family="ui-monospace, monospace">Fri</text>')

    # GRID KONTRIBUSI
    svg.append('  <g id="heatmap-grid">')
    start_x = 55
    start_y = 35
    cell_size = 10.5
    cell_gap = 3.5

    for c_idx, w in enumerate(weeks):
        x = start_x + (c_idx * (cell_size + cell_gap))
        for r_day, lvl in w:
            y = start_y + (r_day * (cell_size + cell_gap))
            color = COLOR_LEVELS[min(lvl, 4)]
            svg.append(f'    <rect x="{x:.1f}" y="{y:.1f}" width="{cell_size}" height="{cell_size}" rx="2" fill="{color}" />')
    svg.append('  </g>')

    # ELEMEN RADAR SWEEP (Oscilloscope Line)
    svg.append('''  <g clip-path="url(#gridClip)">
    <g class="radar-scanner">
      <rect x="0" y="30" width="100" height="110" fill="url(#radarSweep)" />
      <line x1="100" y1="30" x2="100" y2="140" stroke="#3fb950" stroke-width="1.5" opacity="0.8" />
    </g>
  </g>''')

    # FOOTER: Total & Legend
    svg.append(f'  <text x="55" y="172" fill="#c9d1d9" font-size="11" font-family="ui-monospace, monospace">{total_str}</text>')
    svg.append('  <g transform="translate(680, 162)">')
    svg.append('    <text x="-32" y="10" fill="#8b949e" font-size="10" font-family="ui-monospace, monospace">Less</text>')
    for idx, c in enumerate(COLOR_LEVELS):
        svg.append(f'    <rect x="{idx * 14}" y="0" width="10.5" height="10.5" rx="2" fill="{c}" />')
    svg.append('    <text x="76" y="10" fill="#8b949e" font-size="10" font-family="ui-monospace, monospace">More</text>')
    svg.append('  </g>')

    svg.append('</svg>')

    with open("contrib-heatmap.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print("[✓] contrib-heatmap.svg berhasil di-render dengan animasi radar sweep!")

if __name__ == "__main__":
    render()
