#!/usr/bin/env python3
"""data/computed.json içindeki LCR, LCR (YP) ve Basel kaldıraç grup değerlerini (aktif ağırlıklı ortalama) tam yeniden hesaplama beklemeden yazar.

Yalnız `group_data[AKTIF_AGIRLIKLI ölçüler]` değişir. Canlıda veri yüklemesi/yeniden hesaplama aynı sonucu pipeline'dan üretir (groups.py).
Kullanım: python3 scripts/grup_lcr_yaz.py
"""
import json
import os
import shutil
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK))

from pipeline import groups as G  # noqa: E402
from pipeline import rekabet_olculer as R  # noqa: E402

yol = KOK / 'data' / 'computed.json'
d = json.loads(yol.read_text(encoding='utf-8'))
kat = json.loads((KOK / 'data' / 'catalog.json').read_text(encoding='utf-8'))
uyeler = (kat.get('groups') or {}).get('members') or {}
gercek = {b['banka_adi'] for b in kat.get('banks', [])}
bd = d['bank_data']


def _v(x):
    return x.get('value') if isinstance(x, dict) else x


# bank_data değerleri düz sayı; first_date_map toplam_aktifler'in ilk dolu tarihi
ta = bd.get('toplam_aktifler', {})
ilk = {b: (min((t for t, v in ta.get(b, {}).items() if _v(v) is not None), default=None)) for b in gercek}
tarihler = sorted({t for mid in R.AKTIF_AGIRLIKLI for ser in bd.get(mid, {}).values() for t in ser})
yazilan = 0
for mid in sorted(R.AKTIF_AGIRLIKLI):
    gd = {}
    for ad, uye in uyeler.items():
        if not uye:
            continue
        ser = {}
        for t in tarihler:
            v = G._agg_aktif_agirlikli(bd, mid, uye, t, ilk)
            if v is not None:
                ser[t] = {'value': v}
        if ser:
            gd[ad] = ser
            yazilan += len(ser)
    d['group_data'][mid] = gd
shutil.copy2(yol, yol.with_name('computed.json.bak_lcr'))
gecici = yol.with_suffix('.json.tmp')
with open(gecici, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, separators=(',', ':'))
    f.flush()
    os.fsync(f.fileno())
os.replace(gecici, yol)
print(f'{yazilan} grup×tarih LCR değeri yazıldı')
