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
    total_str = data.get("total", "533 contributions in the last year")

    weeks = []
    current_week = []
    for d in days:
        dt = datetime.strptime(d["date"], "%Y-%m-%d")
        w_day = (dt.weekday() + 1) % 7  
        current_week.append((dt, w_day, d.get("level", 0)))
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
    
    # ANIMASI PING-PONG FILL & WIPE
    svg.append('''  <defs>
    <clipPath id="pingPongClip">
      <rect x="53" y="32" width="0" height="104">
        <animate attributeName="width"
                 values="0; 0; 760; 760; 0; 0"
                 keyTimes="0; 0.04; 0.46; 0.78; 0.94; 1"
                 dur="8s"
                 repeatCount="indefinite" />
      </rect>
    </clipPath>
  </defs>''')

    start_x = 55
    start_y = 35
    cell_size = 10.5
    cell_gap = 3.5

    # Label bulan dinamis dengan penanda tahun ('25 & '26)
    last_month = None
    for c_idx, w in enumerate(weeks):
        first_dt = w[0][0]
        m = first_dt.month
        y = first_dt.year
        if last_month is None or m != last_month:
            col = c_idx
            # Berikan ruang ekstra untuk Oct agar 'Sep '25' dan 'Oct' tidak berhimpitan
            if m == 10 and col == 2:
                col = 3
            x = start_x + (col * (cell_size + cell_gap))
            m_name = first_dt.strftime("%b")
            
            # Tampilkan tahun pada awal rentang, pergantian Januari, dan akhir rentang
            if c_idx == 0 or m == 1 or c_idx >= len(weeks) - 4:
                m_str = f"{m_name} <tspan fill='#8b949e' font-size='8.5'>'{str(y)[2:]}</tspan>"
            else:
                m_str = m_name
                
            svg.append(f'  <text x="{x:.1f}" y="22" fill="#8b949e" font-size="10" font-family="ui-monospace, monospace">{m_str}</text>')
            last_month = m

    svg.append('  <text x="24" y="58" fill="#8b949e" font-size="9" font-family="ui-monospace, monospace">Mon</text>')
    svg.append('  <text x="24" y="88" fill="#8b949e" font-size="9" font-family="ui-monospace, monospace">Wed</text>')
    svg.append('  <text x="24" y="118" fill="#8b949e" font-size="9" font-family="ui-monospace, monospace">Fri</text>')

    # 1. Base Grid
    svg.append('  <!-- BASE GRID -->')
    svg.append('  <g id="base-grid">')
    for c_idx, w in enumerate(weeks):
        x = start_x + (c_idx * (cell_size + cell_gap))
        for _, r_day, _ in w:
            y = start_y + (r_day * (cell_size + cell_gap))
            svg.append(f'    <rect x="{x:.1f}" y="{y:.1f}" width="{cell_size}" height="{cell_size}" rx="2" fill="#161b22" />')
    svg.append('  </g>')

    # 2. Active Grid dengan Halo Glow pada Level 4
    svg.append('  <!-- ACTIVE GRID -->')
    svg.append('  <g id="active-grid" clip-path="url(#pingPongClip)">')
    for c_idx, w in enumerate(weeks):
        x = start_x + (c_idx * (cell_size + cell_gap))
        for _, r_day, lvl in w:
            if lvl > 0:
                y = start_y + (r_day * (cell_size + cell_gap))
                # Halo glow lembut khusus level 4 (paling aktif)
                if lvl == 4:
                    svg.append(f'    <rect x="{x - 1.2:.1f}" y="{y - 1.2:.1f}" width="{cell_size + 2.4:.1f}" height="{cell_size + 2.4:.1f}" rx="3" fill="#39d353" opacity="0.32" />')
                color = COLOR_LEVELS[min(lvl, 4)]
                svg.append(f'    <rect x="{x:.1f}" y="{y:.1f}" width="{cell_size}" height="{cell_size}" rx="2" fill="{color}" />')
    svg.append('  </g>')

    d_start = datetime.strptime(days[0]["date"], "%Y-%m-%d").strftime("%b %Y") if days else ""
    d_end = datetime.strptime(days[-1]["date"], "%Y-%m-%d").strftime("%b %Y") if days else ""
    range_str = f" • <tspan fill='#8b949e'>({d_start} – {d_end})</tspan>" if d_start else ""
    svg.append(f'  <text x="55" y="172" fill="#c9d1d9" font-size="11" font-family="ui-monospace, monospace">{total_str}{range_str}</text>')
    svg.append('  <g transform="translate(680, 162)">')
    svg.append('    <text x="-32" y="10" fill="#8b949e" font-size="10" font-family="ui-monospace, monospace">Less</text>')
    for idx, c in enumerate(COLOR_LEVELS):
        svg.append(f'    <rect x="{idx * 14}" y="0" width="10.5" height="10.5" rx="2" fill="{c}" />')
    svg.append('    <text x="76" y="10" fill="#8b949e" font-size="10" font-family="ui-monospace, monospace">More</text>')
    svg.append('  </g>')

    svg.append('</svg>')

    with open("contrib-heatmap.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print("[✓] contrib-heatmap.svg berhasil di-render dengan aura glow level 4!")

if __name__ == "__main__":
    render()
