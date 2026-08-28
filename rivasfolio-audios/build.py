#!/usr/bin/env python3
"""
Generador de páginas + QR para RivasFolio — Audios personalizados.

Uso:
    python3 build.py
        -> genera public/<slug>/index.html para cada fila de data/friends.csv

    python3 build.py --qr https://tudominio.com
        -> genera las páginas Y los códigos QR (uno por amigo) en qrcodes/,
           apuntando a https://tudominio.com/<slug>/

Vuelve a correr este script cada vez que edites data/friends.csv.
"""

import csv
import os
import sys
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(ROOT, "data", "friends.csv")
TEMPLATE_PATH = os.path.join(ROOT, "template.html")
PUBLIC_DIR = os.path.join(ROOT, "public")
QR_DIR = os.path.join(ROOT, "qrcodes")


def load_friends():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader if row.get("slug", "").strip()]
    return rows


def build_pages(friends):
    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        template = f.read()

    count = 0
    for row in friends:
        slug = row["slug"].strip()
        name = row["name"].strip()
        audio_file = row["audio_filename"].strip()
        message = (row.get("message") or "").strip()

        page_dir = os.path.join(PUBLIC_DIR, slug)
        os.makedirs(page_dir, exist_ok=True)

        html = template
        html = html.replace("{{NAME}}", name)
        html = html.replace("{{AUDIO_FILE}}", audio_file)
        html = html.replace("{{ASSET_PATH}}", "../")
        html = html.replace("{{MESSAGE}}", message)
        html = html.replace("{{MESSAGE_HIDDEN}}", "" if message else "hidden")

        with open(os.path.join(page_dir, "index.html"), "w", encoding="utf-8") as out:
            out.write(html)

        count += 1

    print(f"✓ {count} páginas generadas en public/")

    missing = []
    audio_dir = os.path.join(PUBLIC_DIR, "assets", "audio")
    for row in friends:
        audio_path = os.path.join(audio_dir, row["audio_filename"].strip())
        if not os.path.isfile(audio_path):
            missing.append(row["audio_filename"].strip())
    if missing:
        print(f"\n⚠ Faltan {len(missing)} archivos de audio en public/assets/audio/:")
        for m in missing[:10]:
            print(f"   - {m}")
        if len(missing) > 10:
            print(f"   ... y {len(missing) - 10} más")


def build_qr(friends, base_url):
    try:
        import qrcode
    except ImportError:
        print("Falta la librería 'qrcode'. Instálala con:")
        print("   pip install qrcode[pil]")
        sys.exit(1)

    base_url = base_url.rstrip("/")
    os.makedirs(QR_DIR, exist_ok=True)

    for row in friends:
        slug = row["slug"].strip()
        name = row["name"].strip()
        url = f"{base_url}/{slug}/"

        img = qrcode.make(url)
        safe_name = slug
        img.save(os.path.join(QR_DIR, f"{safe_name}.png"))

    print(f"✓ {len(friends)} códigos QR generados en qrcodes/ (dominio: {base_url})")


def main():
    friends = load_friends()
    if not friends:
        print("No hay filas en data/friends.csv")
        return

    build_pages(friends)

    if "--qr" in sys.argv:
        idx = sys.argv.index("--qr")
        if idx + 1 >= len(sys.argv):
            print("Uso: python3 build.py --qr https://tudominio.com")
            sys.exit(1)
        base_url = sys.argv[idx + 1]
        build_qr(friends, base_url)


if __name__ == "__main__":
    main()
