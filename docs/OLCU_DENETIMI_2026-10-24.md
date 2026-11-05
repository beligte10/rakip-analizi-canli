# Ölçü Denetimi — 2026-10-24

Kapsam: `data/computed.json` (213 ölçü, 27 banka) yerel taraması + test koşusu. Kaynak formüller: [FORMUL_LISTESI.md](FORMUL_LISTESI.md).
Tarama otomatiktir (istatistiksel eşikler); "olası neden" satırları doğrulanmış kök neden değil, **hipotezdir**.

## Test sonucu
`pytest tests/`: **443 geçti, 86 atlandı, 0 başarısız** (3 dk). Atlananlar:
- 82: `data/veriler.parquet` / PBI referans JSON bu makinede yok (`test_baseline_promoted.py`) — PBI ile karşılaştırma doğrulaması **yapılamadı**.
- 1: `pipeline/pdf_ingest.py` depoda yok.
- `data/raw/` boş: ham veriye bağlı testler de atlanır, yani ölçülerin ham veriden yeniden üretimi bu makinede doğrulanmadı.

## Tutarlılık
| Kaynak | Ölçü sayısı |
|---|---|
| `data/catalog.json` | 213 |
| `computed.json` bank_data | 213 |
| `MEASURE_FUNCS` | 213 |
| `docs/olcu_metadata.json` | **161** |
| `docs/MEASURES.md` | 128 (eski) |

- 52 ölçünün metadata kaydı yok (39'u Rekabet Analizi). Formülü yalnız kodda; 47'sinin docstring'i de yok.
- Bu 52 ölçü için `FORMUL_LISTESI.md` kod alıntısı verir.

## Veri kalitesi bulguları (önem sırasıyla)

**A. Muhtemel hesap/veri hatası**
1. `yp_vadeli_yp_mevduat` / `yp_vadesiz_yp_mevduat`: 15 hücre |%|>1000; ör. Kuveyt Türk 2015-06-30 vadeli −%1530,5, vadesiz +%1630,5. İki pay %100'ü vermeli; vadeli > payda olunca vadesiz negatif/aşırı çıkıyor. *Olası neden:* eski dönemde vadeli bakiye ile KM-hariç YP mevduat paydasının kapsam uyuşmazlığı.
2. `tp_vadeli_tp_mevduat` / `tp_vadesiz_tp_mevduat`: Enpara 2025-03-31 %13.022.679 / −%13.022.579. *Olası neden:* payda ≈ 0.
3. `npl_karsilama_orani`: 21 hücre >%1000, Ziraat Katılım 2015-03-31 %859.600. Tanım ayrıca belirsiz (metadata notu: "BZK Aşama 1-2-3 olabilir; teyit edilmeli").
4. `efektif_vergi_orani`: Hayat Finans 2023-09-30 −%277.090 (15 aşırı aykırı hücre). Vergi öncesi kâr ≈ 0 iken oran anlamsız.
5. Negatif stok bakiyeleri: `tuzel_krediler` TOM Bank 2024-12-31 −92,5 mn TL (2 hücre); `grup_1_krediler` ve `toplam_canli_krediler` Emlak Katılım 2018-12-31 −188,3 mn TL.
6. Pay >%100 olamaz: `faiz_getirili_ta` (maks %101,5), `tuketici_toplam` (%111,6).
7. `grup_2_krediler_cekirdek_sermaye`: Odeabank 2020-06-30 %2537,6. `yp_net_pozisyon_ozkaynak`: TOM Bank 2024-06-30 %683,5 (bu oran için >%100 mümkün, ama aykırı).

**B. Düşük payda (yeni/küçük banka) kaynaklı, anlamsız oranlar**
- Hayat Finans 2023-09-30: `krediler_mevduat` %24.312,7 (aynı değer `krediler_toplam_kaynak`, `krediler_toplam_fonlama`, `krediler_altindisi_mevduat`'ta), `tp_krediler_tp_kaynak` %65.776,6.
- `tuzel_krediler_tuzel_mevduat`: **88** hücre >%1000.
- `personel_net_kar`: 29, `net_kar_yoy_buyumesi`: 29, `reel_net_kar_buyumesi`: 19 hücre >%1000 (küçük/negatif baz).
- Öneri: payda eşiği (ör. min. mevduat/kâr) altında `None` dön ve "uygulanamaz" göster; grup ve sıralamadan hariç tut.

**C. 0 ile "veri yok" ayrımı**
Tam 0 oranı yüksek: `istirak_kari_vergi_oncesi_kar` %72, `tufex_tamponu` %63, `serbest_karsilik` %54, `birikimli_vadeli_mevduat_toplam_vadeli` %46, `kar_tamponu_net_kar` %38. Banka bu kalemi gerçekten raporlamamış olabilir (0) ya da veri yok (None).

**D. Tanım çelişkileri (kod/belge)**
- NPL paydası: `npl_rasyosu` metadata = Donuk / Krediler **(net)**; ad "Toplam Krediler"; sektör standardı **brüt**.
- `toplam_kaynak`: `MEASURES.md` formülü para piyasası borçlarını **içeriyor**, `olcu_metadata.json` ortak tanımı **hariç** tutuyor.
- `kaynak_pacal_maliyet` ve `faiz_maliyetli_pasif_maliyeti` metadata'da birebir aynı (mükerrer).
- `tp_spread`, `yp_spread`: placeholder.
- Hâlâ PBI baseline'ından kopyalanan ölçüler (NIM ailesi, spread, `maliyet_gelir_duzeltilmis`) — bir dönem geride kalır.

## Kapsam dışı / doğrulanamayanlar
- PBI/BDR referansına karşı eşleşme (referans dosyaları yok).
- Ham veriden yeniden hesaplama (`data/raw` boş).
- Bu bulguların hangileri gerçek hata, hangileri ham veri kaynaklı: Strateji ekibiyle teyit gerekir.
