"""
otp.py
======
E-posta ile giriş doğrulama kodu (OTP, 2026-10-25).

- KT_OTP=true ile açılır (varsayılan KAPALI: sistem bugünkü gibi çalışır). Açıkken şifresi doğru olan üye,
  oturum açılmadan önce e-postasına gelen 6 haneli kodu girer.
- SMTP ayarları ortam değişkenlerinden: KT_SMTP_HOST, KT_SMTP_PORT (587), KT_SMTP_USER, KT_SMTP_PASS,
  KT_MAIL_FROM (varsayılan KT_SMTP_USER), KT_SMTP_SECURITY ('starttls' | 'ssl' | 'none', varsayılan starttls).
- Kodlar yalnız BELLEKTE tutulur (uygulama tek worker, bkz. app.py'nin tek-worker notu); yeniden başlatmada bekleyen
  kodlar düşer, kullanıcı yeni kod ister. Düz metin tutulmaz: tuzlu SHA-256 özeti saklanır.
- Kod 10 dk geçerli, tek kullanımlık, 5 yanlış denemede iptal. Yeniden gönderme 60 sn bekleme + 15 dk'da en çok 3 kod.
- Kök admin hesabı (…@admin.local) gerçek bir posta kutusu olmadığı için OTP dışıdır (kilitlenme olmasın).
"""
from __future__ import annotations

import hashlib
import hmac
import os
import secrets
import smtplib
import threading
import time
from email.message import EmailMessage
from typing import Dict, Tuple

KOD_HANE = 6
GECERLILIK_SN = 600          # 10 dk
EN_COK_DENEME = 5
YENIDEN_BEKLEME_SN = 60
PENCERE_SN = 900             # 15 dk
PENCERE_EN_COK = 3
MUAF_ALAN_ADLARI = ('admin.local',)

_lock = threading.Lock()
_kodlar: Dict[str, dict] = {}       # e-posta → {'ozet', 'tuz', 'bitis', 'deneme'}
_gonderimler: Dict[str, list] = {}  # e-posta → gönderim zamanları (hız sınırı)


def etkin() -> bool:
    return os.environ.get('KT_OTP', '').strip().lower() in ('1', 'true', 'yes', 'on')


def muaf(email: str) -> bool:
    alan = (email or '').strip().lower().rsplit('@', 1)[-1]
    return alan in MUAF_ALAN_ADLARI


def smtp_hazir() -> bool:
    return bool(os.environ.get('KT_SMTP_HOST', '').strip())


def maskele(email: str) -> str:
    yerel, _, alan = (email or '').partition('@')
    if len(yerel) <= 2:
        return (yerel[:1] + '*') + '@' + alan
    return yerel[0] + '*' * (len(yerel) - 2) + yerel[-1] + '@' + alan


def _ozet(kod: str, tuz: str) -> str:
    return hashlib.sha256((tuz + ':' + kod).encode('utf-8')).hexdigest()


def posta_gonder(alici: str, konu: str, govde: str) -> None:
    """SMTP ile tek e-posta. Testlerde bu fonksiyon sahteyle değiştirilir. Hata olursa istisna fırlatır."""
    host = os.environ['KT_SMTP_HOST'].strip()
    port = int(os.environ.get('KT_SMTP_PORT', '587') or 587)
    kullanici = os.environ.get('KT_SMTP_USER', '').strip()
    parola = os.environ.get('KT_SMTP_PASS', '')
    gonderen = os.environ.get('KT_MAIL_FROM', '').strip() or kullanici
    guvenlik = os.environ.get('KT_SMTP_SECURITY', 'starttls').strip().lower()
    if not gonderen:
        raise RuntimeError('KT_MAIL_FROM (ya da KT_SMTP_USER) tanımlı değil')
    msg = EmailMessage()
    msg['From'], msg['To'], msg['Subject'] = gonderen, alici, konu
    msg.set_content(govde)
    if guvenlik == 'ssl':
        sunucu = smtplib.SMTP_SSL(host, port, timeout=10)
    else:
        sunucu = smtplib.SMTP(host, port, timeout=10)
    with sunucu as s:
        if guvenlik == 'starttls':
            s.starttls()
        if kullanici:
            s.login(kullanici, parola)
        s.send_message(msg)


def kod_iste(email: str) -> Tuple[bool, str]:
    """Yeni kod üretir ve e-postayı yollar. Dönüş: (başarılı, hata_mesajı). Hız sınırları burada uygulanır.
    SMTP hatasında kod silinir ve istisna yukarı fırlar (çağıran loglar, kullanıcıya genel mesaj verir)."""
    email = (email or '').strip().lower()
    simdi = time.time()
    with _lock:
        zamanlar = [t for t in _gonderimler.get(email, []) if simdi - t < PENCERE_SN]
        if zamanlar and simdi - zamanlar[-1] < YENIDEN_BEKLEME_SN:
            kalan = int(YENIDEN_BEKLEME_SN - (simdi - zamanlar[-1])) + 1
            return False, f'Yeni kod için {kalan} saniye bekleyin'
        if len(zamanlar) >= PENCERE_EN_COK:
            return False, 'Çok fazla kod istendi. Lütfen birkaç dakika sonra tekrar deneyin'
        kod = ''.join(str(secrets.randbelow(10)) for _ in range(KOD_HANE))
        tuz = secrets.token_hex(8)
        _kodlar[email] = {'ozet': _ozet(kod, tuz), 'tuz': tuz, 'bitis': simdi + GECERLILIK_SN, 'deneme': 0}
        zamanlar.append(simdi)
        _gonderimler[email] = zamanlar
    govde = (f'Kuveyt Türk Rakip Analizi doğrulama kodunuz: {kod}\n\n'
             f'Kod {GECERLILIK_SN // 60} dakika geçerlidir ve tek kullanımlıktır. '
             f'Bu girişi siz yapmadıysanız bu e-postayı yok sayın ve şifrenizi değiştirin.')
    try:
        posta_gonder(email, 'Kuveyt Türk Rakip Analizi — doğrulama kodu', govde)
    except Exception:
        with _lock:
            _kodlar.pop(email, None)
        raise
    return True, ''


def bekleyen_kod_var(email: str) -> bool:
    """Süresi dolmamış, deneme hakkı kalmış bir kod var mı (şifre adımı hız sınırına takılınca eski kodla devam edilebilsin)."""
    email = (email or '').strip().lower()
    with _lock:
        k = _kodlar.get(email)
        return bool(k) and time.time() <= k['bitis'] and k['deneme'] <= EN_COK_DENEME


def kod_dogrula(email: str, kod: str) -> Tuple[bool, str]:
    """Kodu doğrular. Başarıda kod silinir (tek kullanımlık). Dönüş: (başarılı, hata_mesajı)."""
    email = (email or '').strip().lower()
    kod = (kod or '').strip()
    simdi = time.time()
    with _lock:
        kayit = _kodlar.get(email)
        if not kayit or simdi > kayit['bitis']:
            _kodlar.pop(email, None)
            return False, 'Kodun süresi doldu. Yeni kod isteyin'
        kayit['deneme'] += 1
        if kayit['deneme'] > EN_COK_DENEME:
            _kodlar.pop(email, None)
            return False, 'Çok fazla yanlış deneme. Yeni kod isteyin'
        if not hmac.compare_digest(_ozet(kod, kayit['tuz']), kayit['ozet']):
            return False, 'Kod hatalı'
        _kodlar.pop(email, None)
        return True, ''


def sifirla() -> None:
    """Testler için: bellekteki tüm durumu temizler."""
    with _lock:
        _kodlar.clear()
        _gonderimler.clear()
