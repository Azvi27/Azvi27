import re

def fix_animation():
    with open("azvi-ascii.svg", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Hapus garis laser biru dan animasi bergeraknya
    content = re.sub(r'<line[^>]*stroke="#58a6ff"[^>]*/>', '', content)
    content = re.sub(r'<animateTransform[^>]*type="translate"[^>]*/>', '', content)
    content = re.sub(r'<g>\s*</g>', '', content) # Bersihkan grup kosong sisanya

    # 2. Buat animasi ketikan bertahap (Discrete Stepped Reveal)
    # Ini membuat masking turun secara patah-patah per baris (bukan mulus seperti scanner)
    N_STEPS = 38
    max_h = 450
    
    val_list = ["0"]
    kt_list = ["0"]
    
    for i in range(1, N_STEPS + 1):
        h_val = int((i / N_STEPS) * max_h)
        t_val = 0.04 + (i / N_STEPS) * 0.45 # Mengetik dari 4% s/d 49% durasi
        val_list.append(str(h_val))
        kt_list.append(f"{t_val:.3f}")
        
    # Tambahkan durasi diam (hold) dan reset
    val_list.extend([str(max_h), "0", "0"])
    kt_list.extend(["0.88", "0.94", "1"])
    
    v_str = "; ".join(val_list)
    k_str = "; ".join(kt_list)

    new_clip = f'''<clipPath id="asciiTypeClip">
      <rect x="0" y="24" width="420" height="0">
        <animate attributeName="height"
                 calcMode="discrete"
                 values="{v_str}"
                 keyTimes="{k_str}"
                 dur="7.5s"
                 repeatCount="indefinite" />
      </rect>
    </clipPath>'''

    # Ganti clipPath lama dengan yang baru
    content = re.sub(r'<clipPath id="asciiTypeClip">.*?</clipPath>', new_clip, content, flags=re.DOTALL)

    with open("azvi-ascii.svg", "w", encoding="utf-8") as f:
        f.write(content)
    print("[1/2] azvi-ascii.svg diperbarui: Garis biru hilang, efek ketikan per baris aktif.")

def update_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
    # Naikkan versi cache agar GitHub memuat animasi baru
    content = re.sub(r'\?v=\d+', '?v=19', content)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("[2/2] README.md diperbarui dengan cache-buster ?v=19.")

if __name__ == "__main__":
    fix_animation()
