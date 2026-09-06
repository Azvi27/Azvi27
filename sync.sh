#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

# 1. Pastikan virtual environment aktif
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

echo "=========================================="
echo " [1/5] Mengambil data GitLab Lab SSTK 1 & 2"
echo "=========================================="
python scripts/fetch_local_gitlab.py

echo "=========================================="
echo " [2/5] Mengambil data GitHub & GitLab Cloud"
echo "=========================================="
python scripts/fetch_contributions.py

echo "=========================================="
echo " [3/5] Merender Heatmap SVG"
echo "=========================================="
python scripts/render_heatmap_svg.py

echo "=========================================="
echo " [4/5] Menaikkan Versi Cache di README.md"
echo "=========================================="
python3 -c "import re; f=open('README.md','r+'); c=f.read(); f.seek(0); f.write(re.sub(r'\?v=\d+', lambda m: f'?v={int(m.group(0)[3:])+1}', c)); f.truncate()"

echo "=========================================="
echo " [5/5] Commit dan Push ke GitHub"
echo "=========================================="
git add data/ contrib-heatmap.svg README.md
git commit -m "chore: sync contributions [$(date +'%Y-%m-%d %H:%M')]"
git push origin main

echo ""
echo "[✓] Selesai! Buka https://github.com/Azvi27 dan tekan Ctrl+Shift+R."
