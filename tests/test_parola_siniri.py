"""72 bayttan uzun parola bcrypt'te 500 yerine anlamlı hata verir (2026-11-05)."""
import users as U


def test_cok_uzun_parola_kayitta_reddedilir(tmp_path):
    U.ensure_users_file(tmp_path / 'users.json')
    ok, mesaj = U.create_signup(tmp_path / 'users.json', 'Test', 'a@kuveytturk.com.tr', 'ş' * 40)   # 80 bayt
    assert not ok and 'bayt' in mesaj and '{' not in mesaj


def test_normal_parola_kabul_edilir(tmp_path):
    U.ensure_users_file(tmp_path / 'users.json')
    ok, _ = U.create_signup(tmp_path / 'users.json', 'Test', 'b@kuveytturk.com.tr', 'Guvenli-Parola1')
    assert ok


def test_herkese_acik_kayit_admin_local_kabul_etmez(tmp_path):
    U.ensure_users_file(tmp_path / 'users.json')
    ok, mesaj = U.create_signup(tmp_path / 'users.json', 'Kok', 'kok@admin.local', 'Guvenli-Parola1')
    assert not ok and 'kuveytturk.com.tr' in mesaj
