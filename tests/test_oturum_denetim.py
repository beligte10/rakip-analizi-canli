"""Oturum iptali (şifre/rol/durum değişince eski oturumlar düşer) ve yönetici denetim günlüğü (2026-11-05)."""
import json

import audit
import users as U


def _uye(tmp_path, email='ali@kuveytturk.com.tr'):
    p = tmp_path / 'users.json'
    U.ensure_users_file(p)
    ok, err = U.create_signup(p, 'Ali', email, 'parola12345')
    assert ok, err
    uid = U.list_users(p)[-1]['id']
    U.set_status(p, uid, 'approved', 'admin')
    return p, uid


def _surum(p, uid):
    return U.get_user_by_id(p, uid)['oturum_surumu']


def test_sifre_sifirlama_ve_degistirme_oturumu_iptal_eder(tmp_path):
    p, uid = _uye(tmp_path)
    v0 = _surum(p, uid)
    assert U.admin_reset_password(p, uid, 'yeni-parola-1')[0]
    assert _surum(p, uid) == v0 + 1
    assert U.change_password(p, uid, 'yeni-parola-1', 'baska-parola-2')[0]
    assert _surum(p, uid) == v0 + 2


def test_durum_ve_rol_degisimi_iptal_eder_ayni_deger_etmez(tmp_path):
    p, uid = _uye(tmp_path)
    v0 = _surum(p, uid)
    U.set_status(p, uid, 'approved', 'admin')           # değişmedi
    assert _surum(p, uid) == v0
    U.set_status(p, uid, 'rejected', 'admin')           # reddedildi
    assert _surum(p, uid) == v0 + 1


def test_denetim_yalniz_admin_yazma_uclarini_izler():
    assert audit.izlenir_mi('POST', '/api/admin/users/3/approve')
    assert audit.izlenir_mi('DELETE', '/api/admin/roles/x')
    assert audit.izlenir_mi('POST', '/admin/upload-zip')
    assert not audit.izlenir_mi('GET', '/api/admin/users')
    assert not audit.izlenir_mi('POST', '/api/login')


def test_denetim_satiri_yazilir_govde_yok(tmp_path):
    f = tmp_path / 'denetim.jsonl'
    audit.kaydet(f, 'root@kuveytturk.com.tr', 'POST', '/api/admin/users/3/reset-password', 200, '10.0.0.1')
    audit.kaydet(f, 'root@kuveytturk.com.tr', 'DELETE', '/api/admin/roles/x', 403)
    satirlar = [json.loads(s) for s in f.read_text(encoding='utf-8').splitlines()]
    assert [s['durum'] for s in satirlar] == [200, 403]
    assert set(satirlar[0]) == {'zaman', 'kimlik', 'yontem', 'yol', 'durum', 'ip'}


def test_denetim_yazilamazsa_istek_dusmez(tmp_path):
    audit.kaydet(tmp_path / 'yok' / 'denetim.jsonl', 'x', 'POST', '/admin/rebuild', 200)   # dizin yok → OSError yutulur
