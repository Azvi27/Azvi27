import os, re, subprocess
import xml.etree.ElementTree as ET

CARD_W = 420
CARD_H = 480

def get_valid_source_svg():
    """Mencari commit git yang menyimpan potret meja lab asli dan berstatus XML valid"""
    res = subprocess.run(["git", "log", "--format=%H", "--", "azvi-ascii.svg"], capture_output=True, text=True)
    commits = [c.strip() for c in res.stdout.strip().split() if c.strip()]
    
    for c in commits:
        show = subprocess.run(["git", "show", f"{c}:azvi-ascii.svg"], capture_output=True, text=True)
        content = show.stdout
        if "*+%*====" in content and "viewBox" in content:
            try:
                ET.fromstring(content)
                print(f"[✓] Ditemukan basis SVG valid dari commit: {c[:7]}")
                return content
            except ET.ParseError:
                continue
    return None

def patch_ascii_portrait():
    content = get_valid_source_svg()
    if not content:
        print("[!] Gagal menemukan basis commit yang valid.")
        return

    # 1. HAPUS TOTAL blok garis laser biru beserta animasi pembungkusnya
    content = re.sub(r'<g>\s*<animateTransform[\s\S]*?<line[^>]*stroke="#58a6ff"[^>]*/>\s*</g>', '', content)
    content = re.sub(r'<line[^>]*stroke="#58a6ff"[^>]*/>', '', content)
    content = re.sub(r'<text[^>]*>rendered:[^<]*</text>', '', content)

    # 2. Susun nilai tangga ketikan diskrit (36 baris teks)
    heights = [0]
    times = [0.0]
    for i in range(1, 37):
        h = int(30 + (i / 36) * 420)
        t = round(0.04 + (i / 36) * 0.50, 3)
        heights.append(h)
        times.append(t)
    
    # Diam tampil utuh sampai 92% siklus, lalu reset
    heights.extend([460, 0])
    times.extend([0.92, 1.0])

    v_str = "; ".join(str(h) for h in heights)
    kt_str = "; ".join(str(t) for t in times)

    new_clip = f'''<clipPath id="asciiTypeClip">
      <rect x="0" y="24" width="{CARD_W}" height="0">
        <animate attributeName="height"
                 calcMode="discrete"
                 values="{v_str}"
                 keyTimes="{kt_str}"
                 dur="7.5s"
                 repeatCount="indefinite" />
      </rect>
    </clipPath>'''

    # Ganti clipPath lama dengan animasi ketikan baru
    content = re.sub(r'<clipPath id="asciiTypeClip">[\s\S]*?</clipPath>', new_clip, content)

    # 3. Validasi keabsahan XML sebelum ditulis ke disk
    try:
        ET.fromstring(content)
        with open("azvi-ascii.svg", "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[1/2] azvi-ascii.svg 100% VALID XML. Garis biru hilang & animasi ketikan aktif ({CARD_W}x{CARD_H}).")
    except ET.ParseError as err:
        print(f"[!] Gagal: Masih ada tag tidak seimbang: {err}")

def update_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
    # Naikkan penanda versi cache ke ?v=21
    content = re.sub(r'\?v=\d+', '?v=21', content)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("[2/2] README.md diperbarui dengan cache-buster ?v=21.")

if __name__ == "__main__":
    patch_ascii_portrait()
    update_readme()
