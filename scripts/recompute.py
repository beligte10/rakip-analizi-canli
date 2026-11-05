"""
scripts/recompute.py
=====================
Yeniden hesaplama scripti — data/raw'dan parquet'i yükler, baseline JSON'unu
overlay eder, computed.json üretir (bank_data + group_data).

Kullanım:
    python scripts/recompute.py                                    # data/computed.json üret
    python scripts/recompute.py --base data/v29_baseline.json
    python scripts/recompute.py --skip-groups                      # sadece banka değerleri, group_data yazma

Ne zaman çağırılır:
- Yeni measure / grup eklediğinde (bu durumda measures.py + groups.py güncellenir)
- Pipeline bug fix sonrası
- Yeni çeyrek raw verisi geldikten sonra (önce init_data.py, sonra bu)

UYARI: Bu script bank_data / group_data / composition_data / currency_data / catalog /
timestamp üretir. Canlı data/computed.json içindeki meta alanını ÜRETMEZ (yalnızca
meta.compositions'ı catalog'dan tazeler). Bu yüzden canlı dosyanın üzerine yazmayı varsayılan
olarak REDDEDER; yeniden hesaplama için admin panelindeki "recompute" uç
noktasını (app.py) kullanın. Başka bir yola yazmak için --out verin; canlı
dosyayı bilerek (diğer alanlar korunarak) güncellemek için --force kullanın.

NOT: Grup aggregate hesabı (build_group_data) admin panelin kullandığı
app.py ile AYNI, TEK fonksiyon — bu script de artık admin endpoint'leriyle
birebir aynı sonucu üretir.
"""
import argparse
import sys
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from pipeline import LookupContext, compute_all, build_group_data
from pipeline.composition import build_composition_payload


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data-dir', type=Path, default=REPO_ROOT / 'data')
    ap.add_argument('--base', type=Path,
                    help='Baseline JSON (örn. v29 export). Belirtilmezse '
                         'data/computed.json varsa onu kullanır.')
    ap.add_argument('--out', type=Path,
                    help='Çıktı yolu (varsayılan: data/computed.json)')
    ap.add_argument('--skip-groups', action='store_true',
                    help='build_group_data() çağrısını atla, sadece bank_data üret (debug için).')
    ap.add_argument('--bank', help='Sadece tek banka için hesapla (debug)')
    ap.add_argument('--date', help='Sadece tek tarih için hesapla (debug)')
    ap.add_argument('--force', action='store_true',
                    help='Canlı computed.json üzerine yaz; mevcut dosyadaki diğer alanlar (meta, '
                         'composition_data, currency_data ...) korunur.')
    ap.add_argument('-v', '--verbose', action='store_true')
    args = ap.parse_args()

    parquet_path = args.data_dir / 'veriler.parquet'
    catalog_path = args.data_dir / 'catalog.json'
    out_path = args.out or (args.data_dir / 'computed.json')

    live_path = args.data_dir / 'computed.json'
    if out_path.resolve() == live_path.resolve() and not args.force:
        sys.exit(f"❌ {live_path} canlı dosyadır; bu script meta alanını üretmez."
                 " Admin panelindeki recompute'u kullanın, başka bir --out verin "
                 "ya da bilerek --force ile çalıştırın.")

    if not parquet_path.exists():
        print(f"❌ {parquet_path} yok. Önce scripts/init_data.py çalıştır.")
        sys.exit(1)

    if not catalog_path.exists():
        print(f"❌ {catalog_path} yok.")
        sys.exit(1)

    with open(catalog_path) as f:
        catalog = json.load(f)

    # Baseline yükle
    base_data = {}
    if args.base and args.base.exists():
        print(f"📥 Baseline yükleniyor: {args.base}")
        with open(args.base) as f:
            base = json.load(f)
        base_data = base.get('bank_data', base)
    elif out_path.exists():
        print(f"📥 Mevcut çıktıyı baseline olarak kullan: {out_path}")
        with open(out_path) as f:
            base = json.load(f)
        base_data = base.get('bank_data', base)
    else:
        print("⚠ Baseline yok — sadece raw'dan hesaplanacak (passthrough kalemler boş kalır)")

    # LookupContext kur
    print(f"📊 Parquet yükleniyor: {parquet_path}")
    BANK_TURU = {b['banka_adi']: b['tur'] for b in catalog['banks']}
    ctx = LookupContext.from_parquet(parquet_path, BANK_TURU)

    banks = [args.bank] if args.bank else None
    dates = [args.date] if args.date else None

    print(f"🚀 compute_all çalıştırılıyor...")
    out = compute_all(
        ctx, base_data, catalog,
        banks=banks, dates=dates,
        verbose=args.verbose,
    )

    group_data = {}
    if not args.skip_groups:
        print(f"🚀 build_group_data çalıştırılıyor...")
        group_data = build_group_data(out, catalog, ctx)

    composition_data, currency_data = {}, {}
    if not args.skip_groups and not (args.bank or args.date):
        print(f"🚀 build_composition_payload çalıştırılıyor...")
        composition_data, currency_data = build_composition_payload(ctx, catalog)

    # Çıktı baseline yapısında: {'bank_data': out, 'group_data': ..., 'catalog': catalog['measures']}
    output = {
        'catalog': catalog['measures'],
        'bank_data': out,
        'group_data': group_data,
        **({'composition_data': composition_data, 'currency_data': currency_data} if composition_data else {}),
        'timestamp': __import__('datetime').datetime.now().isoformat(),
    }

    if out_path.exists():   # --force: üretilmeyen alanları koru
        with open(out_path, encoding='utf-8') as f:
            onceki = json.load(f)
        output = {**{k: v for k, v in onceki.items() if k not in output}, **output}

    if composition_data and catalog.get('compositions') and isinstance(output.get('meta'), dict):
        output['meta'] = {**output['meta'], 'compositions': catalog['compositions']}   # app.py::_rebuild_dynamic_meta ile aynı: kaynak catalog

    print(f"💾 Yazılıyor: {out_path}")
    with open(out_path, 'w') as f:
        json.dump(output, f, ensure_ascii=False, separators=(',', ':'))   # app.py::_write_computed ile aynı kompakt biçim (indent dosyayı ~%75 şişiriyordu)

    try:    # Rekabet ölçülerinde boş hücre nedenleri ("Tanımsız" / "Veri yok" etiketleri) — app.py ile aynı çıktı
        from pipeline.bos_nedenleri import uret
        bos = uret(ctx, catalog, out)
        with open(args.data_dir / 'bos_nedenleri.json', 'w', encoding='utf-8') as f:
            json.dump(bos, f, ensure_ascii=False, separators=(',', ':'))
    except Exception as e:  # noqa: BLE001
        print(f"⚠️  bos_nedenleri.json üretilemedi: {e}")

    print(f"✅ Bitti. {sum(len(v) for v in out.values())} (measure, banka) çifti")


if __name__ == '__main__':
    main()
