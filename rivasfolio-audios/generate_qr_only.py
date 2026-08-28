#!/usr/bin/env python3
"""
Genera códigos QR para cada amigo apuntando a su URL en Netlify.
Extrae el nombre real directamente del archivo index.html de cada amigo.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(ROOT, "public")
QR_DIR = os.path.join(ROOT, "qrcodes")


def get_friend_folders():
    folders = []
    for item in sorted(os.listdir(PUBLIC_DIR)):
        item_path = os.path.join(PUBLIC_DIR, item)
        if os.path.isdir(item_path) and item.startswith("amigo-"):
            index_path = os.path.join(item_path, "index.html")
            name = item
            if os.path.isfile(index_path):
                with open(index_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    match = re.search(r'<h1 class="name">([^<]+)</h1>', content)
                    if match:
                        name = match.group(1).strip()
            folders.append((item, name))
    return folders


def main():
    try:
        import qrcode
    except ImportError:
        print("Falta la librería 'qrcode'.")
        sys.exit(1)

    os.makedirs(QR_DIR, exist_ok=True)
    friends = get_friend_folders()

    print(f"Generando {len(friends)} códigos QR...\n")

    for slug, name in friends:
        url = f"https://mensajeparaellos.netlify.app/rivasfolio-audios/public/{slug}/index.html"
        
        # Generar QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        file_path = os.path.join(QR_DIR, f"{slug}.png")
        img.save(file_path)
        print(f"✓ {slug}.png ({name}) -> {url}")

    print(f"\n✅ ¡Listo! Se generaron {len(friends)} códigos QR en la carpeta 'qrcodes/'.")


if __name__ == "__main__":
    main()
