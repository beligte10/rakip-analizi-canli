"""Regresyon: /admin/import-data yetki kapısı ve /admin/upload-zip raw yedeği.

HTTP katmanı olmadan uç fonksiyonlar doğrudan çağrılır (bağımlılıklar atlanır).
Denetim bulguları: (1) "Kullanıcılar ve roller" izni olan ama tam admin olmayan
biri import ile kendine Admin rolü verebiliyordu; (2) upload-zip pipeline'dan
önce data/raw'ı yedeksiz siliyordu."""
import io
import json
import zipfile

import pytest
from fastapi import HTTPException, UploadFile

import app as A
import roles as R
import users as U
from pipeline import ingest as ingest_mod


@pytest.fixture
def ortam(tmp_path, monkeypatch):
    d = tmp_path / 'data'
    d.mkdir()
    yollar = {
        'DATA_DIR': d, 'DATA_RAW': d / 'raw', 'DATA_BACKUPS': d / 'backups',
        'DATA_USERS': d / 'users.json', 'DATA_ROLES': d / 'roles.json',
        'DATA_COMPUTED': d / 'computed.json', 'DATA_PARQUET': d / 'veriler.parquet',
        'DATA_HISTORY': d / 'upload_history.json', 'DATA_BOARD': d / 'board.json',
        'DATA_CATALOG': d / 'catalog.json', 'DATA_BOS_NEDEN': d / 'bos_nedenleri.json',
    }
    for ad, yol in yollar.items():
        monkeypatch.setattr(A, ad, yol)
    monkeypatch.setattr(A, 'EXPORT_DATA_FILES', [
        ('computed.json', yollar['DATA_COMPUTED']),
        ('veriler.parquet', yollar['DATA_PARQUET']),
        ('upload_history.json', yollar['DATA_HISTORY']),
        ('board.json', yollar['DATA_BOARD']),
    ])
    yollar['DATA_RAW'].mkdir()
    U.ensure_users_file(yollar['DATA_USERS'])
    R.ensure_roles_file(yollar['DATA_ROLES'])
    return yollar


def _uye(yollar, email, rol):
    ok, err = U.admin_create_user(yollar['DATA_USERS'], email.split('@')[0], email, 'parola12345', 'test')
    assert ok, err
    uid = next(u['id'] for u in U.list_users(yollar['DATA_USERS']) if u['email'] == email)
    assert U.set_role(yollar['DATA_USERS'], uid, rol)
    return email


def _zip(dosyalar: dict) -> UploadFile:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as zf:
        for ad, icerik in dosyalar.items():
            zf.writestr(ad, icerik)
    buf.seek(0)
    return UploadFile(filename='paket.zip', file=buf)


def _import_paketi(**ekstra) -> UploadFile:
    d = {
        'manifest.json': json.dumps({'exported_at': 'x'}),
        'computed.json': json.dumps({'bank_data': {'toplam_aktifler': {'Kuveyt Türk': {'2025-12-31': 1}}}}),
    }
    d.update(ekstra)
    return _zip(d)


def _kotu_users_json() -> str:
    return json.dumps({'users': [{'id': 99, 'name': 'Saldirgan', 'email': 'x@kuveytturk.com.tr',
                                  'password_hash': 'h', 'status': 'approved', 'role': R.ADMIN_ROL}]})


# ----------------------------------------------------------------- import-data
def test_import_kullanici_yonetici_users_json_iceri_alamaz(ortam):
    """admin_kullanicilar + admin_veri izni olan ama Admin olmayan üye 403 alır; users.json değişmez."""
    R.create_role(ortam['DATA_ROLES'], 'Kullanıcı Yöneticisi', ['admin_kullanicilar', 'admin_veri'], 0)
    kimlik = _uye(ortam, 'yonetici@kuveytturk.com.tr', 'kullanici_yoneticisi')
    onceki = ortam['DATA_USERS'].read_text(encoding='utf-8')

    paket = _import_paketi(**{'users.json': _kotu_users_json()})
    with pytest.raises(HTTPException) as e:
        A.admin_import_data(file=paket, include_users=True, user=kimlik)

    assert e.value.status_code == 403
    assert ortam['DATA_USERS'].read_text(encoding='utf-8') == onceki
    assert not ortam['DATA_COMPUTED'].exists()      # hiçbir şey yazılmadı


def test_import_tam_admin_users_json_iceri_alabilir(ortam):
    kimlik = _uye(ortam, 'admin2@kuveytturk.com.tr', R.ADMIN_ROL)
    paket = _import_paketi(**{'users.json': _kotu_users_json()})

    sonuc = A.admin_import_data(file=paket, include_users=True, user=kimlik)

    assert 'users.json' in sonuc['applied_files']
    assert json.loads(ortam['DATA_USERS'].read_text(encoding='utf-8'))['users'][0]['email'] == 'x@kuveytturk.com.tr'


def test_import_users_olmadan_izinli_uye_veriyi_alir_users_degismez(ortam):
    R.create_role(ortam['DATA_ROLES'], 'Veri Sorumlusu', ['admin_veri'], 0)
    kimlik = _uye(ortam, 'veri@kuveytturk.com.tr', 'veri_sorumlusu')
    onceki = ortam['DATA_USERS'].read_text(encoding='utf-8')

    sonuc = A.admin_import_data(
        file=_import_paketi(**{'users.json': _kotu_users_json()}), include_users=False, user=kimlik)

    assert sonuc['applied_files'] == ['computed.json']
    assert ortam['DATA_USERS'].read_text(encoding='utf-8') == onceki


def test_import_bozuk_manifest_400_doner(ortam):
    kimlik = _uye(ortam, 'admin3@kuveytturk.com.tr', R.ADMIN_ROL)
    paket = _import_paketi(**{'manifest.json': '{bozuk'})
    with pytest.raises(HTTPException) as e:
        A.admin_import_data(file=paket, include_users=False, user=kimlik)
    assert e.value.status_code == 400


@pytest.mark.parametrize('ekstra', [
    {'computed.json': json.dumps([1, 2, 3])},                              # nesne değil → eskiden AttributeError (500)
    {'computed.json': json.dumps({'bank_data': [1]})},                     # bank_data nesne değil
    {'computed.json': b'\xff\xfe{bozuk'},                                  # UTF-8 değil → eskiden UnicodeDecodeError (500)
    {'manifest.json': json.dumps([1])},                                    # manifest nesne değil
])
def test_import_bozuk_icerik_500_degil_400(ortam, ekstra):
    kimlik = _uye(ortam, 'admin4@kuveytturk.com.tr', R.ADMIN_ROL)
    with pytest.raises(HTTPException) as e:
        A.admin_import_data(file=_import_paketi(**ekstra), include_users=False, user=kimlik)
    assert e.value.status_code == 400


def test_import_bozuk_users_json_hesaplari_bozmaz(ortam):
    """Bozuk users.json yazılsaydı kimse giriş yapamazdı: doğrulama yazmadan ÖNCE reddeder, mevcut dosya aynen kalır."""
    kimlik = _uye(ortam, 'admin5@kuveytturk.com.tr', R.ADMIN_ROL)
    onceki = ortam['DATA_USERS'].read_text(encoding='utf-8')
    for kotu in ('{bozuk', json.dumps({'users': 'liste degil'}), json.dumps([1])):
        with pytest.raises(HTTPException) as e:
            A.admin_import_data(file=_import_paketi(**{'users.json': kotu}), include_users=True, user=kimlik)
        assert e.value.status_code == 400
    assert ortam['DATA_USERS'].read_text(encoding='utf-8') == onceki


# ----------------------------------------------------------------- upload-zip
@pytest.fixture
def zip_ortam(ortam):
    banka = 'Kuveyt Türk'
    ortam['DATA_CATALOG'].write_text(json.dumps({'banks': [{'banka_adi': banka, 'tur': 'Katılım'}]}),
                                     encoding='utf-8')
    eski = ortam['DATA_RAW'] / banka
    eski.mkdir()
    (eski / 'eski - 31.12.2024.xlsx').write_bytes(b'ESKI-VERI')
    return ortam, banka


def _banka_zip(banka):
    return _zip({f'{banka}/{banka} - 31.03.2025.xlsx': b'YENI-VERI'})


def test_upload_zip_pipeline_hatasinda_raw_geri_yuklenir(zip_ortam, monkeypatch):
    ortam, banka = zip_ortam

    def patla(*a, **k):
        raise RuntimeError('pipeline patladı')
    monkeypatch.setattr(ingest_mod, 'rebuild_parquet', patla)

    with pytest.raises(HTTPException) as e:
        A.admin_upload_zip(file=_banka_zip(banka), force=False, user='admin')

    assert e.value.status_code == 500
    geri = ortam['DATA_RAW'] / banka
    assert [p.name for p in geri.iterdir()] == ['eski - 31.12.2024.xlsx']
    assert (geri / 'eski - 31.12.2024.xlsx').read_bytes() == b'ESKI-VERI'
    assert not list(ortam['DATA_BACKUPS'].glob('raw_*'))       # yedek klasörü geri alındı


def test_upload_zip_basarida_raw_yedegi_tutulur(zip_ortam, monkeypatch):
    ortam, banka = zip_ortam
    monkeypatch.setattr(ingest_mod, 'rebuild_parquet', lambda *a, **k: None)
    monkeypatch.setattr(A, '_run_pipeline_and_save', lambda *a, **k: {
        'bank_data': {}, 'regresyon': {}, 'timestamp': '2025-01-01T00:00:00'})

    A.admin_upload_zip(file=_banka_zip(banka), force=False, user='admin')

    yeni = ortam['DATA_RAW'] / banka
    assert [p.read_bytes() for p in yeni.iterdir()] == [b'YENI-VERI']
    yedekler = list(ortam['DATA_BACKUPS'].glob('raw_*'))
    assert len(yedekler) == 1
    assert (yedekler[0] / banka / 'eski - 31.12.2024.xlsx').read_bytes() == b'ESKI-VERI'


def test_upload_zip_dogrulama_hatasinda_raw_dokunulmaz(zip_ortam):
    ortam, banka = zip_ortam
    with pytest.raises(HTTPException) as e:
        A.admin_upload_zip(file=_zip({'Bilinmeyen Banka/x - 31.03.2025.xlsx': b'x'}), force=False, user='admin')
    assert e.value.status_code == 400
    assert (ortam['DATA_RAW'] / banka / 'eski - 31.12.2024.xlsx').read_bytes() == b'ESKI-VERI'
    assert not list(ortam['DATA_BACKUPS'].glob('raw_*'))


# ------------------------------------------------- export yetkisi ve geri alma açıkları (2. tur)
def test_export_kullanici_yonetici_users_json_indiremez(ortam):
    """Parola hash'leri yalnız tam admin'e: 'Kullanıcılar ve roller' izni olan üye include_users ile 403 alır."""
    ortam['DATA_COMPUTED'].write_text(json.dumps({'bank_data': {'x': {}}}), encoding='utf-8')
    R.create_role(ortam['DATA_ROLES'], 'Kullanıcı Yöneticisi', ['admin_kullanicilar', 'admin_veri'], 0)
    kimlik = _uye(ortam, 'yonetici2@kuveytturk.com.tr', 'kullanici_yoneticisi')
    with pytest.raises(HTTPException) as e:
        A.admin_export_data(include_users=True, admin_user=kimlik)
    assert e.value.status_code == 403
    # users.json olmadan export serbest
    A.admin_export_data(include_users=False, admin_user=kimlik)


def test_export_tam_admin_users_json_indirebilir(ortam):
    ortam['DATA_COMPUTED'].write_text(json.dumps({'bank_data': {'x': {}}}), encoding='utf-8')
    kimlik = _uye(ortam, 'admin4@kuveytturk.com.tr', R.ADMIN_ROL)
    yanit = A.admin_export_data(include_users=True, admin_user=kimlik)
    with zipfile.ZipFile(io.BytesIO(yanit.body)) as zf:
        assert {'users.json', 'roles.json', 'computed.json'} <= set(zf.namelist())


def test_upload_zip_pipeline_hatasinda_parquet_da_geri_alinir(zip_ortam, monkeypatch):
    ortam, banka = zip_ortam
    ortam['DATA_PARQUET'].write_bytes(b'ESKI-PARQUET')
    ortam['DATA_BOS_NEDEN'].write_text('{"eski": true}', encoding='utf-8')

    def yarim_yaz_ve_patla(*a, **k):
        ortam['DATA_PARQUET'].write_bytes(b'YENI-PARQUET')      # pipeline parquet'i yazdı...
        raise RuntimeError('regresyon kilidi')                  # ...sonra hata (ör. 409)
    monkeypatch.setattr(ingest_mod, 'rebuild_parquet', yarim_yaz_ve_patla)

    with pytest.raises(HTTPException):
        A.admin_upload_zip(file=_banka_zip(banka), force=False, user='admin')

    assert ortam['DATA_PARQUET'].read_bytes() == b'ESKI-PARQUET'
    assert json.loads(ortam['DATA_BOS_NEDEN'].read_text(encoding='utf-8')) == {'eski': True}
    assert (ortam['DATA_RAW'] / banka / 'eski - 31.12.2024.xlsx').read_bytes() == b'ESKI-VERI'


def test_upload_zip_tasima_yarida_kalirsa_orijinaller_silinmez(zip_ortam, monkeypatch):
    """Eski klasörleri yedeğe taşırken 2. taşıma patlarsa: henüz taşınmamış orijinal de, taşınan da korunur."""
    ortam, banka = zip_ortam
    katalog = json.loads(ortam['DATA_CATALOG'].read_text(encoding='utf-8'))
    katalog['banks'].append({'banka_adi': 'Akbank', 'tur': 'Mevduat'})
    ortam['DATA_CATALOG'].write_text(json.dumps(katalog), encoding='utf-8')
    (ortam['DATA_RAW'] / 'Akbank').mkdir()
    (ortam['DATA_RAW'] / 'Akbank' / 'ak - 31.12.2024.xlsx').write_bytes(b'AKBANK-ESKI')

    gercek, sayac = A.shutil.move, {'n': 0}

    def ikinci_tasimada_patla(src, dst, *a, **k):
        sayac['n'] += 1
        if sayac['n'] == 2:
            raise OSError('disk hatası')
        return gercek(src, dst, *a, **k)
    monkeypatch.setattr(A.shutil, 'move', ikinci_tasimada_patla)

    with pytest.raises(HTTPException) as e:
        A.admin_upload_zip(file=_banka_zip(banka), force=False, user='admin')

    assert e.value.status_code == 500
    assert (ortam['DATA_RAW'] / banka / 'eski - 31.12.2024.xlsx').read_bytes() == b'ESKI-VERI'
    assert (ortam['DATA_RAW'] / 'Akbank' / 'ak - 31.12.2024.xlsx').read_bytes() == b'AKBANK-ESKI'
