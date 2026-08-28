# RivasFolio — Audios personalizados con QR

Sistema para generar 38 páginas privadas (una por amigo/a), cada una con
su audio personalizado, y un código QR único que lleva directo a esa página.

## Qué hay en esta carpeta

```
rivasfolio-audios/
├── build.py              ← el script que genera todo (no lo edites)
├── template.html          ← la plantilla visual (no la edites, salvo que quieras cambiar textos)
├── data/
│   └── friends.csv        ← AQUÍ editas los nombres y archivos de audio
├── public/                ← esto es lo que subes a tu hosting (se genera solo)
│   ├── assets/
│   │   ├── style.css
│   │   ├── script.js
│   │   └── audio/         ← AQUÍ pones tus 38 archivos .mp3
│   └── <slug>/index.html  ← una carpeta por amigo (se genera solo)
└── qrcodes/                ← los 38 QR en PNG (se genera solo, con --qr)
```

## Paso 1 — Completa la lista de amigos

Abre `data/friends.csv` (con Excel, Google Sheets o Numbers) y reemplaza
las filas de ejemplo. Columnas:

- `slug`: parte de la URL, sin espacios ni acentos (ej. `ana-perez`). Debe ser único.
- `name`: el nombre que se muestra en la página (ej. `Ana Pérez`).
- `audio_filename`: el nombre exacto del archivo de audio que vas a poner en `public/assets/audio/` (ej. `ana.mp3`).
- `message` (opcional): un mensaje corto de texto debajo del reproductor. Déjalo vacío si no quieres nada ahí.

Guárdalo como CSV (no como .xlsx).

## Paso 2 — Coloca los audios

Pon tus 38 archivos de audio dentro de `public/assets/audio/`, con el
mismo nombre que pusiste en la columna `audio_filename` del CSV.

Formatos recomendados: `.mp3` (el más compatible) o `.m4a`. Evita archivos
muy pesados — si puedes, expórtalos a un bitrate razonable (128–192 kbps)
para que carguen rápido en el celular de tus amigos.

## Paso 3 — Genera las páginas

Con Python instalado, desde esta carpeta:

```bash
python3 build.py
```

Esto crea `public/<slug>/index.html` para cada amigo. Si corriste esto antes
de tener todos los audios, el script te avisa cuáles faltan.

## Paso 4 — Sube `public/` a un hosting

El contenido de la carpeta `public/` debe subirse tal cual, como la RAÍZ
del sitio (no como subcarpeta), para que las URLs queden así:
`https://tudominio.com/ana-perez/`

Opciones gratis y sencillas:
- **Netlify Drop** (netlify.com/drop): arrastras la carpeta `public/` y listo, te da una URL.
- **GitHub Pages**: subes el contenido de `public/` a un repo y activas Pages.
- **Vercel**: similar a Netlify.
- O tu hosting/dominio propio si ya tienes uno (súbelo por FTP/cPanel).

Una vez publicado, anota la URL base (ej. `https://rivasfolio-audios.netlify.app`).

## Paso 5 — Genera los QR con tu dominio real

Vuelve a correr el script, ahora pasándole la URL donde publicaste el sitio:

```bash
python3 build.py --qr https://tu-url-real.com
```

Esto crea `qrcodes/<slug>.png` — un PNG por amigo, listo para imprimir o
enviar. Cada QR apunta directo a `https://tu-url-real.com/<slug>/`.

⚠️ Como cada URL es solo el slug (no lleva contraseña), la privacidad depende
de que el link/QR no se comparta ni sea fácil de adivinar — por eso conviene
usar slugs que no sean obvios (evita `amigo-01`, mejor algo como iniciales +
un código, ej. `ap-7x2q`) si quieres que sea difícil de encontrar sin el QR.

## Si quieres cambiar algo del diseño

- Colores y tipografía: `public/assets/style.css` (variables al inicio del archivo).
- Textos fijos ("Un audio para ti", etc.): `template.html`.
- Después de editar `template.html` o el CSS, vuelve a correr `python3 build.py`
  para que se reflejen los cambios en las 38 páginas.

## Reimprimir / actualizar

Cada vez que cambies el CSV, el mensaje de alguien, o agregues un audio nuevo,
solo corre `python3 build.py` de nuevo (y `--qr` si cambió algún slug o el dominio).
