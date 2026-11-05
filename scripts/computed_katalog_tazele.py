#!/usr/bin/env python3
"""data/computed.json içindeki `catalog` kopyasını catalog.seed.json ölçü tanımlarıyla eşitler (yalnız katalog alanı; değerlere dokunmaz).

Kategori/alt kategori/`rekabet` gibi katalog değişikliklerinin tam veri hesaplaması beklemeden yansıması için.
Önce data/computed.json.bak_katalog yedeği alınır; yazım atomiktir.
Kullanım: python3 scripts/computed_katalog_tazele.py
"""
import json
import os
import shutil
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
yol = KOK / 'data' / 'computed.json'
seed = {m['id']: m for m in json.loads((KOK / 'catalog.seed.json').read_text(encoding='utf-8'))['measures']}
d = json.loads(yol.read_text(encoding='utf-8'))
eski = d.get('catalog') or []
yeni = [seed.get(m['id'], m) for m in eski]
degisen = sum(1 for a, b in zip(eski, yeni) if a != b)

# Kompozisyon bileşen renkleri (meta.compositions): seed'deki renklerle eşitle (palet değişince)
tohum_komp = json.loads((KOK / 'catalog.seed.json').read_text(encoding='utf-8')).get('compositions') or {}
for kid, kmeta in (d.get('meta', {}).get('compositions') or {}).items():
    for alan in ('components', 'currency_alt'):
        renk = {x['id']: x.get('color') for x in (tohum_komp.get(kid, {}).get(alan) or [])}
        for x in kmeta.get(alan) or []:
            if renk.get(x['id']) and x.get('color') != renk[x['id']]:
                x['color'] = renk[x['id']]
                degisen += 1
if degisen:
    shutil.copy2(yol, yol.with_name('computed.json.bak_katalog'))
    d['catalog'] = yeni
    gecici = yol.with_suffix('.json.tmp')
    gecici.write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')
    os.replace(gecici, yol)
print(f'{degisen} ölçü tanımı güncellendi (toplam {len(yeni)})')
