"""Generate responsive WebP assets without altering the original project figures."""
from pathlib import Path
import yaml
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / 'assets/images'
out.mkdir(parents=True, exist_ok=True)
metadata = {}
sources = sorted((ROOT / 'img').rglob('*.png'))
sources.append(ROOT / 'img/FB_IMG_1790760243979.jpg')
for source in sources:
    key = '/' + source.relative_to(ROOT).as_posix()
    with Image.open(source) as original:
        original = original.convert('RGB') if original.mode not in ('RGB', 'RGBA') else original.copy()
        variants = []
        # Compact plates and high-DPI phones should not jump straight to 960px.
        for width in sorted({min(original.width, w) for w in (160, 320, 480, 640, 768, 960, 1600)}):
            resized = original.copy()
            resized.thumbnail((width, round(original.height * width / original.width)))
            target = out / f'{source.stem}-{width}.webp'
            resized.save(target, 'WEBP', quality=88, method=6)
            variants.append({'url': '/' + target.relative_to(ROOT).as_posix(), 'width': resized.width})
        metadata[key] = {'width': original.width, 'height': original.height, 'src': variants[-1]['url'], 'srcset': ', '.join(f"{v['url']} {v['width']}w" for v in variants)}
(ROOT / '_data/images.yml').write_text(yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False), encoding='utf-8')
print(f'Optimized {len(metadata)} images; original files preserved.')
