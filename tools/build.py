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
# 2) versione anteprima online (libreria da CDN)
out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else root/'build/artifact.html'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(with_sample.replace('<!--XLSX-->', '<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>'), encoding='utf-8')
print('ok')
