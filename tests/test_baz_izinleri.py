"""Reel TL / USD para bazı izinleri (baz_reel, baz_usd): rol bazında açılır.

Varsayılan: Analist, Veri Yöneticisi ve Admin'de açık; Görüntüleyici ve özel rollerde kapalı.
Eski roles.json (izinler henüz bilinmiyor) yüklenince hazır rollere bir kez eklenir."""
import json

import roles as R


def _eski_roles_json(path):
    """baz izinlerinin henüz tanınmadığı döneme ait roles.json."""
    bilinen = [k for k in R.IZIN_ANAHTARLARI if not k.startswith('baz_')]
    path.write_text(json.dumps({
        'bilinen_izinler': bilinen,
        'roles': [
            {'id': 'goruntuleyici', 'ad': 'Görüntüleyici', 'izinler': list(R.EKRAN_IZINLERI), 'asistan_gunluk': 0},
            {'id': 'analist', 'ad': 'Analist', 'izinler': ['asistan'] + list(R.EKRAN_IZINLERI), 'asistan_gunluk': 50},
            {'id': 'ozel_rol', 'ad': 'Özel', 'izinler': ['asistan'] + list(R.EKRAN_IZINLERI), 'asistan_gunluk': 5},
        ],
    }), encoding='utf-8')


def test_baz_izinleri_tanimli_ve_ekran_izni_degil():
    assert {'baz_tl', 'baz_reel', 'baz_usd', 'buyume_ortalama'} <= set(R.IZIN_ANAHTARLARI)
    assert not {'baz_tl', 'baz_reel', 'baz_usd', 'buyume_ortalama'} & set(R.EKRAN_IZINLERI)   # özellik izni: yetki yükseltmede sayılır


def test_hazir_roller_varsayilani(tmp_path):
    yol = tmp_path / 'roles.json'
    R.ensure_roles_file(yol)
    izin = {r['id']: set(r['izinler']) for r in R.list_roles(yol)}
    assert not {'baz_tl', 'baz_reel', 'baz_usd', 'buyume_ortalama'} & izin['goruntuleyici']
    for rol in ('analist', 'veri_yoneticisi', R.ADMIN_ROL):
        assert {'baz_tl', 'baz_reel', 'baz_usd', 'buyume_ortalama'} <= izin[rol]


def test_eski_roles_json_goc_hazir_rollere_eklenir_ozel_role_eklenmez(tmp_path):
    yol = tmp_path / 'roles.json'
    _eski_roles_json(yol)
    izin = {r['id']: set(r['izinler']) for r in R.list_roles(yol)}
    assert {'baz_tl', 'baz_reel', 'baz_usd'} <= izin['analist']
    assert not {'baz_tl', 'baz_reel', 'baz_usd'} & izin['goruntuleyici']
    assert not {'baz_tl', 'baz_reel', 'baz_usd'} & izin['ozel_rol']          # özel rol: admin panelden açılır


def test_admin_kapattigi_baz_izni_geri_gelmez(tmp_path):
    yol = tmp_path / 'roles.json'
    R.ensure_roles_file(yol)
    mevcut = R.get_role(yol, 'analist')
    R.update_role(yol, 'analist', mevcut['ad'], [k for k in mevcut['izinler'] if k != 'baz_usd'], mevcut['asistan_gunluk'])
    assert 'baz_usd' not in R.get_role(yol, 'analist')['izinler']
    assert 'baz_reel' in R.get_role(yol, 'analist')['izinler']
