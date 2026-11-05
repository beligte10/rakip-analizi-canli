# Oturum Özeti — 21.10.2026

Bu belge, 21 Ekim 2026'daki Claude Code oturumunda yapılanları ve nasıl yapıldıklarını anlatır. İki ana iş vardı: (1) rekabet analizi verisinin taranması ve düzeltilmesi, (2) Anlık Görünüm arayüzünün (`frontend/index_v30.html`) yeniden düzenlenmesi.

Hiçbir değişiklik commit'lenmedi (`Rakip Analizi/.git` var, `git commit` çalıştırılmadı).

---

## 1. Veri tarafı

### 1.1 Çıkış sorusu
"Personel sayısı YoY ile bps neden tutmuyor?" Cevap iki parçalı:

- **Tanım farkı (hata değil):** Adet sütunundaki bps, bankanın 27 banka toplamındaki **pay** değişimidir (varsayılan çeyreklik, `msDeltaBps`). YoY % bankanın kendi yıllık büyümesidir. "Personel Sayısı Değişimi (YoY)" ölçüsünde bps, YoY oranının çeyrekten çeyreğe farkıdır (`measureQoQDelta`). Şube & Personel kategorisinde ise mutlak fark gösterilir (`miktarDelta`).
- **Veri hatası:** Garanti 2026-03 personeli 23.376 idi (komşu çeyrekler ≈20.300); bu tek değer Mart YoY'sini ve Haziran pay bps'ini (−129) bozuyordu.

### 1.2 Tarama yöntemi
Araçlar: rekabet analizi MCP sunucusu (Power BI modeli), `data/veriler.parquet` (ham BDDK), `data/computed.json` (dashboard çıktısı), `datatable_1.xlsx` (Power BI dışa aktarımı). Betikler oturumun geçici (scratchpad) klasöründe yazıldı, projeye eklenmedi.

Yapılan kontroller:
1. Kapsam: banka × dönem, eksik dönem, kopya satır, NaN.
2. 213 ölçünün tüm banka serilerinde otomatik anomali taraması: tek çeyrek sıçrayıp geri dönme, 1000 kat ölçek hatası, ≥4 çeyrek aynı değer (donmuş veri), komşular arasında sıfır.
3. Bilanço denkliği: Toplam Aktifler = Toplam Pasifler (1.184 banka-dönemin hepsinde tuttu).
4. Dashboard ↔ `datatable_1.xlsx` karşılaştırması (`pipeline/datatable.py`'nin kendi eşleme fonksiyonlarıyla).
5. Dashboard ↔ MCP karşılaştırması, grup havuzlaması (Kuveyt Türk, Katılım, Rakip) yeniden hesabı.
6. bps/YoY kodunun okunması (`index_v30.html`, `pipeline/rekabet_olculer.py`, `pipeline/measures.py`).

### 1.3 Bulgular (özet)
Ayrıntılar `Rakip Analizi Veri Tarama Raporu.md` ve `.html` dosyalarında (proje klasörünün bir üstünde, `~/Desktop/v3/`).

| # | Önem | Bulgu | Durum |
|---|---|---|---|
| P1 | Kritik | 2016-09 personel sayısı 9 bankada binlik ayracı ondalık okunmuş (13,744 → 13.744) | **Düzeltildi** |
| P2 | Kritik | Garanti 2026-03 = 23.376 | BDR bekliyor |
| P3 | Kritik | Halk 2025-03 = 27.000 (Power BI'da 22.162) ve 2025-09 = 28.000 | 2025-03 **düzeltildi**, 2025-09 açık |
| P4 | Yüksek | ING Bank 2.416, 13 çeyrek boyunca aynı | Açık |
| P5 | Yüksek | Sıfır girilmiş eksik değerler (Kuveyt Türk 2014-03/2015-03, Şekerbank 2014-09, Ziraat Katılım 2018-09, Vakıf Katılım 2019-06/09) | Açık |
| P6–P7 | Orta | Yeni banka sıfırları (Enpara, Dünya, TOM), Şekerbank her Aralık +%13 sıçrama | Doğrulanmalı |
| K1 | Yüksek | "Rakip" grubu dashboard'da 5 banka, MCP'de 3 banka | Açık |
| K2–K5 | Orta | Denizbank düzeltmesinin MCP'ye yansımaması, MCP'nin eksiği 0 göstermesi, MCP `report_page`'in YoY ölçülerde boş dönmesi, datatable'ın 2026-03'te bitmesi | Açık |
| — | Orta | 68 tek çeyreklik sıçrama (kredi kartları, serbest karşılık, resmi kurumlar mevduatı vb.) | Doğrulanmalı |

### 1.4 Uygulanan veri düzeltmeleri
`pipeline/veri_duzeltmeleri.py` içine 10 kayıt eklendi (dosya 17'den 27 kayda çıktı): 9 banka için 2016-09 `Personel Sayısı` ×1000 ve Halk Bank 2025-03 `Personel Sayısı` 27.000 → 22.162. Her kayıt `beklenen` değeri taşır; ham dosya düzelirse kayıt kendiliğinden devre dışı kalır (`pipeline/lookup.py::_veri_duzeltmeleri_uygula`). `karar` alanı `2026-10-21 (veri taraması, kullanıcı onayı)`.

Yeniden hesaplama (`scripts/recompute.py`) sonrası etki:
- 2017-09 YoY: Akbank %1,12, Garanti −%3,98, Halk %4,6 (önceden ≈ +%100.000).
- Halk YoY: 2025-03 −%0,1, 2026-03 +%1,8 (önceden +%21,7 ve −%16,4).
- Mevduat grubu YoY (2026-03): −%1,94 → +%0,71.
- Personel başına ölçüler (örn. Akbank personel başına krediler 2016-09) normale döndü.
- Yan etki yok: diğer ölçülerde yalnızca ondalık gürültü (1e-15 düzeyi).

### 1.5 Önemli uyarı: `scripts/recompute.py` güncel değil
Script çalıştırıldığında `computed.json`'dan `meta`, `composition_data` ve `currency_data` alanlarını atıyor (yalnızca `bank_data`, `group_data`, `catalog`, `timestamp` yazıyor). Bu yüzden:
1. Önceki dosya yedeklendi (scratchpad'e).
2. Yeni `bank_data` ve `group_data`, eski dosyadaki diğer alanlarla **birleştirildi**.
3. `tests/test_regression_spotcheck.py::test_date_coverage_meta_mevcut` ile doğrulandı.

Scripti ileride doğrudan çalıştırmayın; admin panelindeki "recompute" uç noktası (`app.py`) kullanılmalı ya da script düzeltilmeli.

### 1.6 Hâlâ açık veri işleri
Garanti 2026-03, Halk 2025-09, ING donmuş seri, sıfır girilen dönemler (kaynak BDR PDF'lerinden doğrulanmalı); zaman serisi koruma testi (mevcut `tests/test_data_quality.py` yalnızca dosya sağlığına bakıyor); "Rakip" grup tanımının tek yerde belirlenmesi; MCP tarafı düzeltmeleri.

---

## 2. Arayüz tarafı (`frontend/index_v30.html`)

Kronolojik, her madde kullanıcının isteğiyle birlikte.

### 2.1 Tek ekran düzeni: kutuların yeri değişmesin
**İstek:** Tek sayfa görünümde kutular her ekran boyutunda aynı yerde kalsın; boşluklar ve hizalama ekrana göre dinamik uyum sağlasın.

**Sorun (mevcut kod):** 1800 mantıksal pikselden geniş ekranda 3 sütunlu farklı yerleşim (`fit-genis`), sol liste ekran yüksekliğine göre 1–3 sütuna bölünüyor, ölçekleme yalnızca büyütme yönündeydi.

**Yapılan:**
- Sabit ızgara: `grid-template-areas` her ekranda aynı. `fit-genis` bloğu ve `data-cols` kuralları kaldırıldı.
- Ölçek: `zoom = clamp(0.6, 3, min(innerWidth/1440, innerHeight/820))`, 0,02 adımla yuvarlanır. Hem büyütür hem küçültür; en/boy oranı farklıysa artan alan sütunlara fr oranıyla dağılır.
- Boşluk/dolgu mantıksal genişliğe göre: `--fit-gap` (8–18 px), `--fit-pad` (6–14 px); alt kartların ızgara boşlukları bunlardan türer.
- `tamEkranMi`: eşik 901×520 (önceden 1100×640).

### 2.2 Yapı: referans görsele göre
**İstek:** Gönderilen referans görsele göre: solda tam yükseklikte liste, sağda üst üste YtD grafiği / Banka Grupları / Rakip Bankalar; kaydırma yok.

**Yapılan:**
- `grid-template-areas: "rank ust" "rank alt1" "rank alt2"`, sütunlar `1fr 1.25fr`, satırlar `minmax(0,1fr) auto auto`.
- Alt kartlara `min-height` oranı: `alt1` fit-h × 0,17, `alt2` fit-h × 0,22 (kart içeriği boşta kalmasın diye dikey ortalandı).
- Sol liste her zaman tek sütun; satır 16 px'in altına düşecek kadar kısa mantıksal alanda iki sütun (kaydırma yerine).
- Deneme notu: `minmax(min-content, …fr)` ile satır boyutlandırma YtD kartını çökertti, geri alındı.

### 2.3 Sıralama kartı
- Bankalar 1–27 numaralandı (`.bank-row-sira`, önceden yalnız PDF'te görünürdü).
- "Kuveyt Türk sırası: 10 / 27" alt şeridi arayüzden gizlendi (PDF'te kalır).
- Satır yüksekliği kesirli hesaplanıyor: liste kartın altına kadar iniyor.
- Az satırlı filtrelerde (Rakip Bankalar, Katılım) `ROW_MAX = 36`: satırlar uzamaz, altta boşluk kalır.
- Ad sütunu numaraya yer açacak şekilde genişletildi (`--fit-ad`: 122–176 px).

### 2.4 Başlık
**Tek ekran açıkken tek başlık** (`DateSelectorBar`): Yıl, Çeyrek, görünüm düğmeleri, sağda STRATEJİ logosu ve hamburger. Eski yeşil şerit, KT logosu ve ölçü adı kaldırıldı.
**Tek ekran kapalıyken eski iki başlık**: yeşil üst şerit (KT logosu, "Rakip Analizi", ortada ölçü adı · dönem, STRATEJİ + hamburger) ve altında tarih satırı. `TopBar`, `tekEkranUi[0]`'a göre hangisini kuracağına karar verir; STRATEJİ + hamburger tek bir `sagKume` öğesi olarak iki yerden birine yerleşir.
- **Çeyrek seçici:** 4'lü buton şeridi yerine `QuarterDropdown` (yıl seçici gibi açılır/kapanır, verisi olmayan çeyrek soluk ve tıklanamaz).
- **Simgeler:** Anında Görünüm / Trend / Kompozisyon simgeleri 15 → 13 px.
- **Mobil (≤900 px):** STRATEJİ + hamburger, Yıl/Çeyrek ile aynı satırda sağa yaslı; görünüm düğmeleri alt satırda (CSS `order`).

### 2.5 Asistan düğmesi
Geçirdiği hâller: yüzen sağ alt → üst şeritte → yüzen → USD'nin yanında → (son durum) **Tek ekran AÇIK iken USD seçicisinin hemen yanında, KAPALI iken sağ altta yüzer**.
- `ChatPanel` içindeki efekt (400 ms aralıkla ve `resize`'da) `.baz-sec` (yoksa ölçü kutusu) konumunu ölçer; `left/top` satır içi stil olarak yazılır.
- Çapa yoksa ya da ekran <901 px ise varsayılan sağ alt konum.
- **Taşma düzeltmesi:** "Önceki ölçü" dolunca satır genişleyip USD ve Asistan'ı ekran dışına itiyordu. Çözüm: ölçü alanı ve ⇄ düğmesi daralır (`flex: 1 1 0`, `min-width: 0`), kontrol çubuğunun sağında 118 px yer ayrılır (`html body.tek-ekran .control-bar`; mevcut ≤1200 px kuralının özgüllüğünü aşmak için `html body` öneki gerekti), ≤1250 px'te "Önceki: ad" yalnız simge olur.

### 2.6 Varsayılanlar ve tarih aralığı
- **Tek ekran varsayılan açık:** Depolama anahtarı `kt_tek_ekran_v2`; eski sürümde "kapalı" saklanmış tercihler yok sayılır. Tercih yalnızca `'0'` ise kapalı.
- **2021 başlangıcı yalnız Rekabet Analizi ölçülerinde:** `olcuVeriTarihleri` içinde `kategori === 'Rekabet Analizi'` ise tarihler `REKABET_BASLANGIC = '2021-01-01'` ve sonrası. Diğer ölçüler tüm aralıkta. 2020 ve öncesi veri silinmedi; YoY/YtD/CAGR tarih aritmetiğiyle (`yoyTarih`, `ytdTarih`) eski tabanı okur. (İlk uygulama tüm ölçülere genel filtreydi, sonra bu kategori bazlı hâle getirildi.)

### 2.7 "Ölçü Oluştur" kısayolu
Aktif ölçünün kategorisi **"Özel Ölçülerim"** iken, rolde `olcu_olustur` izni varsa, görünüm düğmelerinin soluna "Ölçü Oluştur" düğmesi eklenir (telefonda üstte tam genişlik). Hamburger menüdeki düğme duruyor. Yeni hiç özel ölçüsü olmayan kullanıcıda kategori görünmediği için buton da görünmez.

---

## 3. Doğrulama yöntemi

Gerçek sunucu (`:7860`) giriş gerektirdiği için doğrulamalar kimliksiz bir **önizleme sunucusuyla** yapıldı (oturumun geçici klasöründe, projeye eklenmedi):
- `scripts/duzen_denetimi.py`'deki sahte uç noktaların (`/api/me`, `/api/my/measures`, …) aynısı + `/api/data` için `data/computed.json`.
- Test için sunucu `?tek0` parametresiyle tarayıcı depolamasını ayarlayabiliyor ve bir ölçüyü geçici olarak "Özel Ölçülerim" kategorisine alabiliyordu.

Doğrulama araçları:
1. Gömülü tarayıcı paneli + JavaScript ile `getBoundingClientRect` ölçümleri (taşma, çakışma, ekran dışı kontrolü) — 960, 1100, 1280, 1440, 1600, 1920, 2400 genişlikleri.
2. Başsız Chrome (`--headless=new --screenshot`) ile gerçek ekran görüntüsü (gömülü panel küçük olduğu için gözle kontrol için bu yol kullanıldı).
3. `pytest`: `tests/test_duzen_mobil.py` (mobil/tablet düzen denetimi, ~2,5 dk), `tests/test_i18n.py`, `tests/test_custom_measures_js.py` — son durumda **34 geçti**. Veri tarafında `test_data_quality`, `test_computed_guards`, `test_rekabet_olculer`, `test_regression_spotcheck`, `test_group_aggregation` — **93 geçti**.

Sınırlar: gerçek `:7860` sunucusunda giriş yapılmadı; telefon boyutunda (375 px) yalnızca ölçüm yapıldı, her değişiklik için ayrı görüntü alınmadı; Kompozisyon ve dışa aktarma ekranları ayrı ayrı gözle incelenmedi.

---

## 4. Değişen / eklenen dosyalar

| Dosya | Değişiklik |
|---|---|
| `Rakip Analizi/frontend/index_v30.html` | Tüm arayüz değişiklikleri (bölüm 2) |
| `Rakip Analizi/pipeline/veri_duzeltmeleri.py` | +10 düzeltme kaydı |
| `Rakip Analizi/data/computed.json` | Yeniden hesaplandı (`bank_data`, `group_data`, `timestamp`) |
| `Rakip Analizi Veri Tarama Raporu.md` | Veri bulguları raporu (`~/Desktop/v3/`) |
| `Rakip Analizi Veri Tarama Raporu.html` | Aynı rapor, tek sayfalık sabit yerleşimli HTML |
| `Rakip Analizi/docs/OTURUM_OZETI_2026-10-21.md` | Bu belge |

Not: `Rakip Analizi/data/` altında ayrıca `computed.json.bak` ve `computed_backup_2026-08-11.json` gibi eski yedekler zaten vardı; bu oturumda yeni yedek dosyası bırakılmadı, yeniden hesaplama öncesi kopya geçici klasörde duruyor.

---

## 5. Bilinmesi gerekenler

- **Geri alma:** Veri düzeltmeleri `veri_duzeltmeleri.py`'den kayıtları silerek ve `computed.json`'u yeniden üreterek geri alınır. Arayüz için `git diff frontend/index_v30.html` ile değişiklikler görülebilir (commit yok).
- **Güvenlik notu:** `start.sh` içinde yönetici parolası ve API anahtarları (OpenRouter, EVDS, TÜİK) düz metin yazılı. `.gitignore`'da olduğundan emin olunmalı; anahtarların yenilenmesi düşünülmeli. Bu oturumda `start.sh` yalnızca sunucuyu başlatmak için çalıştırıldı, içeriği değiştirilmedi.
- **Sunucu:** Oturumda `bash start.sh` ile başlatılan sunucu arka planda `127.0.0.1:7860`'ta çalışır durumda kalmış olabilir; durdurmak için `pkill -f "python3 app.py"`.
- **Kalıcı çözüm eksikleri:** Veri tarafında zaman serisi koruma testi ve `recompute.py`'nin güncellenmesi yapılmadı (bölüm 1.5–1.6).

---

## 6. Ajan incelemesi ve dalga önerileri (22.10.2026) — ONAY BEKLİYOR

Oturumun sonunda dört ajan kuruldu. Üçü salt okunur analiz yaptı, dördüncü (Yönetici) bu üç raporu birleştirip öncelik verdi. **Hiçbir öneri uygulanmadı; kullanıcı onayı bekleniyor.** Ajanlar yalnızca öneri üretti, proje dosyalarına dokunmadı.

### 6.1 Ajanlar ve görevleri
| Ajan | Görev | Çıktı |
|---|---|---|
| Uzman Denetçi | Sistem eksikleri ve riskleri: veri hattı, test, güvenlik, operasyon, mimari, belge | Bulgu listesi (13 başlık) |
| Ölçü Denetçisi | 213 ölçünün formül, birim, taban dönem, grup hesabı, catalog tutarlılığı | 21 bulgu |
| Arayüz Geliştirici | Arayüz inceleme (ekran görüntüleri dahil), geliştirme önerileri, kod yazmadan | 14 öneri |
| Yönetici | Üç raporu birleştirir, çakışmaları ayıklar, kritik iddiaları doğrular, dalga planı yapar | Birleşik iş planı |

Yöntem notu: ajanlar `general-purpose` tipinde, arka planda ve salt okunur çalıştırıldı. Raporlar dosyaya çıkarılıp (`scratchpad/yonetici/`) Yönetici'ye okutuldu; Yönetici arayüz raporunu ayrıştıramadığı için o 14 öneri plana oturum yürütücüsü tarafından eklendi.

### 6.2 Yönetici özeti
En büyük üç risk:
1. **Eksik veri `0` olarak taşınıyor** (`pipeline/lookup.py:213-217`): doğrulandı. Kuveyt Türk `tp_aktifler_ta` 66,55 → 0,0 → 62,35; Katılım grubu personel gideri YoY'si 2017-12'de −94, 2018-12'de +2186.
2. **Ekranda yanlış sayı üreten formüller:** NPL intikal/tahsilat şişmesi, reel OPEX/net kâr için yanlış TÜFE (2024-12'de çeyrek sonu 44,4 vs YtD ortalama 58,5), `krediler` tanım kırılması (2018-03).
3. **Operasyonel tuzaklar:** `scripts/recompute.py` canlı `computed.json`'u bozar, `start.sh`'te düz metin sırlar, veri yüklemede anlamsal doğrulama yok.

Sıra: Dalga 0 → Dalga 1 (ölçü ve arayüz paralel) → Dalga 2 → Dalga 3. Ölçü değişikliklerinden sonra `computed.json` yönetici paneli (admin recompute) ile yeniden üretilir, `recompute.py` ile değil.

### 6.3 Dalga 0: hızlı ve düşük riskli
1. `recompute.py`'yi güvenli hâle getir (hata fırlatsın, docstring düzelsin). S
2. Sırları yenile, `start.sh`'i depodan uzak tut. S–M, **karar gerek**
3. Bilgi kartı ve belge düzeltmeleri (kodu tanımlayan, tanımı değiştirmeyen). S
4. Trendde baz ≤ 0 koruması; akım ölçülerde QoQ'yu çeyreklik farka çevir. S
5. Ölü kod, hata mesajında `textContent`, `HEALTHCHECK $PORT`, `rebuild_parquet` atomik yazım. S

### 6.4 Dalga 1A: ölçü doğruluğu (P0/P1)
6. Eksik veri `None` olsun (önce hızlı yama, sonra `_lookup` varsayılanı). M–L
7. Sıfır personel gideri `None` ve grup YoY koruması (`rekabet_olculer.py:285-299`). S–M
8. Reel büyüme ölçülerinde doğru TÜFE (YtD ortalama endeks oranı). Sonuç değişir (KT reel OPEX 2024-12: 34,9 → 22,9). S
9. NPL intikal/tahsilat "Diğer Giriş/Çıkış" şişmesi. S, **karar gerek**
10. `finansal_varliklar_net_ta` eski kalemler. S
11. `grup_2_krediler_cekirdek_sermaye` paydası sıfır üyeler (`groups.py:815-831`). S
12. Reel/USD bazında beş TTM ölçü için doğru endeks (`index_v30.html:4850-4863`). S
13. Pazar payı: işaretli/kısmi evrenli üç ölçü. S–M, **karar gerek**

### 6.5 Dalga 1B: arayüz (paralel; kararları bozmaz)
14. Pazar payı çubuk-rakam çakışması, pozitiflere "+" işareti. S
15. Düşük kontrastlı gri metinler (83 yerde, `#94a3b8` → `#64748b`). S
16. Hata/yükleme ekranı: "Yükleniyor", doğru Türkçe, "Yeniden dene". S
17. Asistan konumu: 400 ms aralık yerine `ResizeObserver`. S–M
18. Klavye erişimi (banka satırları) ve genel `:focus-visible`. S–M
19. Kompozisyon/Trend'de çeyrek seçici tutarsızlığı. S
20. YtD grafiği boşluğunun kök nedeni (ölçüm CSS `zoom`'u hesaba katmıyor, `measureBarsArea`). M

### 6.6 Dalga 2: karar gerektiren işler
21. `krediler` tek tanım (2018 kırılması). 22. Rakip grubu tek tanım (dashboard 5, katalog bayrakları 5 farklı, MCP 3). 23. İki NPL karşılama ölçüsü, özdeş ölçüler. 24. Akım rasyolarda yıllıklandırma tutarlılığı. 25. Yeni bankalarda ilk çeyrek eşiği. 26. Veri yüklemede anlamsal doğrulama modülü (L). 27. Açık veri kalemleri (Garanti 2026-03, Halk 2025-09, ING). 28. Parquet/users/roles/catalog için rotasyonlu yedek ve felaket kurtarma.

### 6.7 Dalga 3: iyileştirmeler
CDN SRI/self-host, tek süreç koruması, logging, memoizasyon, ekran okuyucu desteği, zoom sınırları, tablet düzeni, belge birleştirme, ölçü katalogunda `sort_direction` ve ad/birim tutarlılığı.

### 6.8 Kullanıcıdan istenen kararlar (ve önerilen cevaplar)
| Karar | Öneri |
|---|---|
| Sırlar döndürülsün mü? | Evet |
| Rakip grubu hangisi? | Tek kaynak `catalog groups.members`; seti kullanıcı belirlesin |
| NPL intikal/tahsilat: PBI DAX mı, "Dönem İçi" mi? | Dönem İçi |
| `krediler` | 2013'e kadar brüt tanım |
| SYR/CET1 grup değeri | Basit ortalama kalsın (kasıtlı tasarım, kartta belirt) |
| Pazar payı: `net_ticari_kar`, `tufex_tamponu`, `serbest_karsilik` | Kapat |
| Yeni bankalarda ilk 4 çeyrek oran ölçüleri | `None` (PBI paritesi bozulur, kabul) |
| Garanti 2026-03, Halk 2025-09, ING için BDR PDF | Verilirse düzeltme, yoksa "doğrulanamadı" |

### 6.9 Önerilmeyenler / sonraya bırakılanlar
`app.py` bölme ve arayüz derleme adımı (büyük risk; ayrıca commit'lenmemiş çok değişiklik var, önce commit önerilir), SSO/MFA ve oturum iptali, CI ve uçtan uca testler, `_lookup` varsayılanının tam sürümü (Dalga 1 yamasından sonra ayrı iş), 5 noktalı ortalama bakiye, üçüncü taraf LLM'in hukuki onayı.

### 6.10 Yöneticinin doğruladığı ve düzelttiği iddialar
- **Doğrulandı:** `_lookup` eksikte `0.0` döndürüyor; KT 2017-12 personel gideri ham veride 0; Katılım grubu personel başına personel gideri YoY'si −94,34 / +2186,28; Akbank 2025-12 intikal/tahsilat 7,96/5,31; TÜFE farkları (44,38 vs 58,51; 30,89 vs 34,88); `recompute.py` çıktısında `meta`/`composition_data`/`currency_data` yok; `catalog.json` Rakip bayrakları ile `groups.members` çelişiyor; `app.py` 3.302 satır, frontend 11.830 satır.
- **Düzeltildi:** SYR/CET1'in basit ortalaması hata değil, belgelenmiş tasarım (MCP talimatı da yazıyor); P1 yerine P2. NPL intikal/tahsilat için "PBI birebir" iddiası kodla çelişiyor, bu yüzden karar gerekiyor. Uzman Denetçi raporundaki "150K satırlık app.py" ifadesi yanlıştı.
- **Doğrulanmadı:** `finansal_varliklar_net_ta` 2018-03 çukuru, `krediler` 2018 oranları, `avg_balance` etkileri, Enpara/TOM uç değerleri; hiçbir test çalıştırılmadı.

### 6.11 Durum
Kullanıcıya iki seçenek sunuldu: "Dalga 0 + Dalga 1" (önerilen) veya "Sadece Dalga 0". **Henüz cevap gelmedi, hiçbir dalga uygulanmadı.** Onaydan sonra Ölçü Denetçisi (`pipeline/*.py`, catalog, docs) ve Arayüz Geliştirici (`frontend/index_v30.html`) farklı dosyalarda paralel çalışacak; yalnızca Ölçü tarafı `computed.json` üretecek.
