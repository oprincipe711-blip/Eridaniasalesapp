# Crea le due versioni dell'app a partire da src/app.html
import pathlib, sys
root = pathlib.Path(__file__).resolve().parent.parent
src = (root/'src/app.html').read_text(encoding='utf-8')
lib = (root/'tools/xlsx.full.min.js').read_text(encoding='utf-8').replace('</script','<\\/script')
sample = (root/'tools/sample.json').read_text(encoding='utf-8').replace('</','<\\/')
with_sample = src.replace('/*__SAMPLE__*/', 'const SAMPLE=' + sample + ';')
# 1) versione per il PC: un solo file, funziona anche offline
local = with_sample.replace('<!--XLSX-->', '<script>' + lib + '</script>')
head = ('<!doctype html>\n<html lang="it">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<style>*,*::before,*::after{box-sizing:border-box}body{margin:0}[hidden]{display:none!important}</style>\n')
t_end = local.index('</style>') + len('</style>')
local = head + local[:t_end] + '\n</head>\n<body>\n' + local[t_end:] + '\n</body>\n</html>\n'
(root/'Calendario_Promo.html').write_text(local, encoding='utf-8')
# 2) sito per GitHub Pages (cartella docs): senza dati di esempio, libreria in un file a parte
docs = root/'docs'; (docs/'data').mkdir(parents=True, exist_ok=True)
site = src.replace('/*__SAMPLE__*/', '').replace('<!--XLSX-->', '<script src="xlsx.full.min.js"></script>')
pwa = ('<link rel="manifest" href="manifest.webmanifest">\n<link rel="apple-touch-icon" href="icon-180.png">\n'
       '<link rel="icon" href="icon-192.png">\n<meta name="theme-color" content="#2c43b0">\n'
       '<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-title" content="Promo">\n')
t_end = site.index('</style>') + len('</style>')
site = head + pwa + site[:t_end] + '\n</head>\n<body>\n' + site[t_end:] + '\n</body>\n</html>\n'
(docs/'index.html').write_text(site, encoding='utf-8')
(docs/'xlsx.full.min.js').write_text((root/'tools/xlsx.full.min.js').read_text(encoding='utf-8'), encoding='utf-8')
(docs/'.nojekyll').write_text('')
(docs/'manifest.webmanifest').write_text('{"name":"Calendario Promo","short_name":"Promo","start_url":"./","display":"standalone",'
  '"background_color":"#f3f5f8","theme_color":"#2c43b0","icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png"},'
  '{"src":"icon-512.png","sizes":"512x512","type":"image/png"}]}\n')
try:
    from PIL import Image, ImageDraw
    for sz in (180, 192, 512):
        im = Image.new('RGB', (sz, sz), '#2c43b0'); dr = ImageDraw.Draw(im); u = sz/16
        dr.rounded_rectangle([3*u, 3.5*u, 13*u, 13*u], radius=u, fill='#ffffff')
        dr.rectangle([3*u, 3.5*u, 13*u, 6*u], fill='#cfd6f5')
        for x in (5.5, 10.5): dr.rounded_rectangle([(x-.4)*u, 2.5*u, (x+.4)*u, 4.8*u], radius=.3*u, fill='#ffffff')
        for i, (x0, x1, y, c) in enumerate([(4, 9, 7.6, '#cc3f55'), (6.5, 12, 9.4, '#2f6fd6'), (4, 10.5, 11.2, '#d97c0f')]):
            dr.rounded_rectangle([x0*u, y*u, x1*u, (y+1.1)*u], radius=.4*u, fill=c)
        im.save(docs/f'icon-{sz}.png')
except ImportError:
    pass
# 3) versione anteprima online (libreria da CDN)
out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else root/'build/artifact.html'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(with_sample.replace('<!--XLSX-->', '<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>'), encoding='utf-8')
print('ok')
