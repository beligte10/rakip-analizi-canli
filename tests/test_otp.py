"""E-posta OTP (otp.py + /api/login akışı). Gerçek e-posta atılmaz: otp.posta_gonder sahteyle değiştirilir."""
import re

import pytest
from fastapi import HTTPException
from starlette.requests import Request

import app as A
import otp
import users as U

EPOSTA = 'uye@kuveytturk.com.tr'
PAROLA = 'parola12345'


@pytest.fixture
def giden(monkeypatch):
    """Gönderilen e-postaları toplar; her testte durum sıfırlanır."""
    otp.sifirla()
    kutu = []
    monkeypatch.setattr(otp, 'posta_gonder', lambda alici, konu, govde: kutu.append((alici, konu, govde)))
    yield kutu
    otp.sifirla()


def _kod(kutu, i=-1):
    return re.search(r'kodunuz: (\d{6})', kutu[i][2]).group(1)


# ---------------------------------------------------------------- otp.py
def test_kod_gonderilir_dogrulanir_ve_tek_kullanimliktir(giden):
    ok, _ = otp.kod_iste(EPOSTA)
    assert ok and len(giden) == 1 and giden[0][0] == EPOSTA
    kod = _kod(giden)
    assert otp.kod_dogrula(EPOSTA, kod) == (True, '')
    assert otp.kod_dogrula(EPOSTA, kod)[0] is False        # ikinci kullanım reddedilir


def test_yanlis_kod_5_denemeden_sonra_iptal_olur(giden):
    otp.kod_iste(EPOSTA)
    kod = _kod(giden)
    yanlis = '000000' if kod != '000000' else '111111'
    for _ in range(5):
        assert otp.kod_dogrula(EPOSTA, yanlis) == (False, 'Kod hatalı')
    assert otp.kod_dogrula(EPOSTA, kod)[0] is False        # doğru kod bile artık geçmez
    assert 'Yeni kod' in otp.kod_dogrula(EPOSTA, kod)[1]


def test_kodun_suresi_dolar(giden, monkeypatch):
    otp.kod_iste(EPOSTA)
    kod = _kod(giden)
    gercek = otp.time.time
    monkeypatch.setattr(otp.time, 'time', lambda: gercek() + otp.GECERLILIK_SN + 5)
    assert otp.kod_dogrula(EPOSTA, kod) == (False, 'Kodun süresi doldu. Yeni kod isteyin')


def test_yeniden_gonderme_bekleme_ve_pencere_siniri(giden, monkeypatch):
    t0 = otp.time.time()
    monkeypatch.setattr(otp.time, 'time', lambda: t0)
    assert otp.kod_iste(EPOSTA)[0]
    ok, mesaj = otp.kod_iste(EPOSTA)                        # hemen tekrar: bekleme
    assert not ok and 'saniye' in mesaj
    for k in (1, 2):                                        # beklemeler geçilince 2. ve 3. kod gider
        monkeypatch.setattr(otp.time, 'time', lambda k=k: t0 + k * (otp.YENIDEN_BEKLEME_SN + 1))
        assert otp.kod_iste(EPOSTA)[0]
    monkeypatch.setattr(otp.time, 'time', lambda: t0 + 3 * (otp.YENIDEN_BEKLEME_SN + 1))
    ok, mesaj = otp.kod_iste(EPOSTA)                        # 15 dk içinde 4. kod: reddedilir
    assert not ok and 'Çok fazla' in mesaj and len(giden) == 3


def test_gonderim_hatasinda_kod_saklanmaz(monkeypatch):
    otp.sifirla()

    def patla(*a):
        raise OSError('smtp kapalı')
    monkeypatch.setattr(otp, 'posta_gonder', patla)
    with pytest.raises(OSError):
        otp.kod_iste(EPOSTA)
    assert otp.kod_dogrula(EPOSTA, '123456')[0] is False and not otp.bekleyen_kod_var(EPOSTA)
    otp.sifirla()


def test_maskele_ve_muaf():
    assert otp.maskele('faruk.kezer@kuveytturk.com.tr') == 'f*********r@kuveytturk.com.tr'
    assert otp.muaf('localtest@admin.local') and not otp.muaf(EPOSTA)


# ---------------------------------------------------------------- /api/login akışı
@pytest.fixture
def ortam(tmp_path, monkeypatch, giden):
    yol = tmp_path / 'users.json'
    U.ensure_users_file(yol)
    monkeypatch.setattr(A, 'DATA_USERS', yol)
    ok, err = U.admin_create_user(yol, 'Uye', EPOSTA, PAROLA, 'test')
    assert ok, err
    monkeypatch.setenv('KT_SMTP_HOST', 'smtp.test')
    A._login_attempts.clear()
    return yol


def _istek():
    return Request({'type': 'http', 'headers': [], 'client': ('127.0.0.1', 5000), 'session': {}})


def _giris(istek, eposta=EPOSTA, parola=PAROLA):
    return A.api_login(A.LoginPayload(email=eposta, password=parola), istek)


def test_otp_kapaliyken_giris_eskisi_gibi(ortam, monkeypatch):
    monkeypatch.delenv('KT_OTP', raising=False)
    istek = _istek()
    assert _giris(istek)['status'] == 'ok'
    assert istek.session.get('user_id')


def test_otp_acikken_oturum_kod_girilene_kadar_acilmaz(ortam, giden, monkeypatch):
    monkeypatch.setenv('KT_OTP', 'true')
    istek = _istek()
    sonuc = _giris(istek)
    assert sonuc['status'] == 'otp' and sonuc['email'].endswith('@kuveytturk.com.tr') and '*' in sonuc['email']
    assert 'user_id' not in istek.session and istek.session.get('otp_bekleyen')   # şifre doğru ama oturum kapalı
    with pytest.raises(HTTPException) as e:
        A.api_login_otp(A.OtpPayload(code='000000'), istek)
    assert e.value.status_code == 401 and 'user_id' not in istek.session
    sonuc = A.api_login_otp(A.OtpPayload(code=_kod(giden)), istek)
    assert sonuc['status'] == 'ok' and istek.session.get('user_id') and 'otp_bekleyen' not in istek.session


def test_kod_olmadan_otp_ucu_oturum_acamaz(ortam, monkeypatch):
    monkeypatch.setenv('KT_OTP', 'true')
    with pytest.raises(HTTPException) as e:
        A.api_login_otp(A.OtpPayload(code='123456'), _istek())
    assert e.value.status_code == 401


def test_yanlis_sifrede_kod_gonderilmez(ortam, giden, monkeypatch):
    monkeypatch.setenv('KT_OTP', 'true')
    with pytest.raises(HTTPException) as e:
        _giris(_istek(), parola='yanlis-parola-1')
    assert e.value.status_code == 401 and giden == []


def test_admin_local_otp_disinda(tmp_path, monkeypatch, giden):
    yol = tmp_path / 'users.json'
    U.ensure_users_file(yol)
    monkeypatch.setattr(A, 'DATA_USERS', yol)
    ok, err = U.admin_create_user(yol, 'Kok', 'kok@admin.local', PAROLA, 'test')
    assert ok, err
    monkeypatch.setenv('KT_OTP', 'true')
    istek = _istek()
    assert _giris(istek, 'kok@admin.local')['status'] == 'ok' and giden == []


def test_smtp_tanimli_degilse_giris_503_ve_oturum_acilmaz(ortam, monkeypatch):
    monkeypatch.setenv('KT_OTP', 'true')
    monkeypatch.delenv('KT_SMTP_HOST')
    istek = _istek()
    with pytest.raises(HTTPException) as e:
        _giris(istek)
    assert e.value.status_code == 503 and 'user_id' not in istek.session and 'otp_bekleyen' not in istek.session


def test_ikinci_sifre_adiminda_onceki_kodla_devam_edilir(ortam, giden, monkeypatch):
    """Şifre adımı 60 sn beklemesine takılırsa kullanıcı hata görmez, ilk kodla devam eder."""
    monkeypatch.setenv('KT_OTP', 'true')
    _giris(_istek())
    A._login_attempts.clear()
    istek2 = _istek()
    assert _giris(istek2)['status'] == 'otp' and len(giden) == 1
    assert A.api_login_otp(A.OtpPayload(code=_kod(giden)), istek2)['status'] == 'ok'
