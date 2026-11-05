"""Rekabet ölçüleri ayrı kategori değil, asıl kategorilerinde `rekabet: true` işaretiyle durur (2026-11-04)."""
import json
from pathlib import Path

from pipeline.rekabet_olculer import IDS, KATALOG

KOK = Path(__file__).resolve().parent.parent


def _seed():
    return json.loads((KOK / 'catalog.seed.json').read_text(encoding='utf-8'))['measures']


def test_rekabet_analizi_kategorisi_kalmadi():
    assert not [m for m in _seed() if m['kategori'] == 'Rekabet Analizi']
    assert not [m for m in _seed() if m.get('alt_kategori') in ('Zorunlu Karşılık ve Marj', 'Kâr Tamponu')]


def test_rekabet_isareti_tam_ve_yalniz_katalog_olculerinde():
    isaretli = {m['id'] for m in _seed() if m.get('rekabet')}
    assert isaretli == set(IDS) and len(IDS) == 39


def test_kategori_dagilimi():
    from collections import Counter
    c = Counter((m['kategori'], m.get('alt_kategori')) for m in _seed() if m.get('rekabet'))
    assert c == {('Gelir Tablosu', None): 18, ('Şube & Personel', None): 5,
                 ('Bilanço', 'Aktifler'): 8, ('Bilanço', 'Pasifler'): 8}
    assert all(m['kategori'] == k['kategori'] for m in _seed() for k in KATALOG if m['id'] == k['id'])
