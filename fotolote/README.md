# fotolote

Edição de fotos em lote por linha de comando (Python + Pillow). Nunca altera os originais: tudo vai para uma pasta de saída.

```bash
pip install -r requirements.txt

# redimensionar tudo para no máximo 1600px e converter para WebP
python -m fotolote ~/fotos -o ~/fotos_web --max-lado 1600 --formato webp --qualidade 82

# usando um preset, incluindo subpastas, em paralelo
python -m fotolote ~/fotos -o ~/saida -p presets/instagram.json -r

# ver o que seria feito, sem gravar
python -m fotolote ~/fotos -o ~/saida -p presets/web.json --dry-run
```

## Operações rápidas
`--max-lado`, `--largura/--altura --fit contain|cover|exact`, `--corte 16:9`, `--girar`, `--brilho`, `--contraste`, `--saturacao`, `--nitidez`, `--auto-contraste`, `--pb`, `--sepia`, `--marca "© Nome"`.

Saída: `--formato jpg|png|webp|tiff`, `--qualidade`, `--sufixo`, `--renomear 'viagem_{n:03d}'`, `--manter-exif` (por padrão o EXIF, inclusive GPS, é removido). A orientação EXIF é sempre aplicada antes de editar.

## Presets (JSON)
Lista ordenada de operações; a ordem importa. Operações disponíveis: `resize, crop_ratio, rotate, flip, brightness, contrast, saturation, sharpness, autocontrast, grayscale, sepia, blur, border, watermark`. Veja `presets/`. Flags da CLI são aplicadas depois do preset.

## Testes
`python -m unittest discover -s tests -t .`
