"""Yönetici işlemleri denetim günlüğü (2026-11-05): `data/denetim.jsonl`, satır başına bir JSON, yalnız eklenir.

Kim (kimlik), ne zaman, hangi ucu (yöntem + yol), sonuç kodu ve IP. İstek gövdesi (parola, veri) ASLA yazılmaz.
Dosya dönmez; büyürse dışarıdan döndürülür (logrotate). Yazma hatası isteği bozmaz (yalnız uyarı günlüğü).
"""
import json
import logging
import threading
from datetime import datetime
from pathlib import Path

_log = logging.getLogger('denetim')
_kilit = threading.Lock()
IZLENEN_YONTEMLER = ('POST', 'PUT', 'DELETE', 'PATCH')


def izlenir_mi(yontem: str, yol: str) -> bool:
    """Yalnız yönetici yazma uçları: /api/admin/* ve /admin/* (durum değiştiren yöntemler)."""
    return yontem in IZLENEN_YONTEMLER and (yol.startswith('/api/admin/') or yol.startswith('/admin/'))


def kaydet(dosya: Path, kimlik: str, yontem: str, yol: str, durum: int, ip: str = '') -> None:
    satir = {'zaman': datetime.now().isoformat(timespec='seconds'), 'kimlik': kimlik, 'yontem': yontem,
             'yol': yol, 'durum': durum, 'ip': ip}
    try:
        with _kilit, open(dosya, 'a', encoding='utf-8') as f:
            f.write(json.dumps(satir, ensure_ascii=False) + '\n')
    except OSError as e:   # günlük yazılamıyor diye yönetici işlemi düşmez
        _log.warning('denetim günlüğü yazılamadı: %s', e)
