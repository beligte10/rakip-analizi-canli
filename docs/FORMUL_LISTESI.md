# Ölçü Formül Listesi

Otomatik üretildi (2026-10-24): `data/catalog.json` (213 ölçü) + `docs/olcu_metadata.json` (161 ölçü) + `pipeline/measures.py` kodu.

- **Tanımlı (metadata)**: formül/tanım `olcu_metadata.json` içinden alındı.
- **Yalnız kod**: metadata kaydı yok; formülün tek kaynağı ölçü fonksiyonudur, kod alıntılanmıştır. Bu ölçülerin metadata kaydı eksiktir (bkz. denetim raporu).

## Ortak tanımlar

- **Krediler (net)**: Bilanço 'Krediler ve Alacaklar (Toplam)'; eski TMS 39 dönemlerinde 'Krediler'. Donuk alacaklar ve karşılıklar netleştirilmiş haliyle.
- **Toplam Brüt Krediler**: Krediler ve Alacaklar + Faktoring Alacakları + Kiralama İşlemlerinden Alacaklar + Donuk Alacaklar + Takipteki Krediler (NPL dahil). TP/YP kırılımı aynı kalemlerin TP/YP kolonlarıyla.
- **Toplam Canlı Krediler**: Krediler ve Alacaklar + Faktoring Alacakları + Kiralama İşlemlerinden Alacaklar (NPL hariç).
- **Toplam Kaynak**: Mevduat + Alınan Krediler + İhraç Edilen Menkul Kıymetler (Net). Para piyasalarına borçlar DAHİL DEĞİL.
- **Toplam Fonlama**: Mevduat + Alınan Krediler + Para Piyasalarına Borçlar + İhraç Edilen Menkul Kıymetler (Net).
- **Altındışı**: Kıymetli maden (altın) mevduatı düşülmüş tutar, ör. Altındışı Mevduat = Mevduat − Kıymetli Maden Mevduatı.
- **Menkul Kıymetler**: GUD Farkı K/Z Yansıtılan FV + GUD Farkı DKG Yansıtılan FV + İtfa Edilmiş Maliyetle Ölçülen FV + Türev FV + Satılmaya Hazır FV (eski) + Vadeye Kadar Elde Tutulacak (eski).
- **Faiz (Kar Payı) Getirili Aktifler (detaylı, 13 bileşen)**: TCMB Hesabı (TP+YP) + Bankalar + Para Piyasalarından Alacaklar + GUD K/Z FV + GUD DKG FV + İtfa Edilmiş Maliyet FV + Satılmaya Hazır (eski) + VKET (eski) + Türev FV + Riskten Korunma Türev FV + Toplam Brüt Krediler − |Beklenen Zarar Karşılıkları|.
- **Faiz (Kar Payı) Maliyetli Pasifler (detaylı, 9 bileşen)**: Vadeli Mevduat + Alınan Krediler + Para Piyasalarına Borçlar + İhraç Edilen MK (Net) + GUD K/Z Finansal Yükümlülükler + Türev Finansal Yükümlülükler + Faktoring Borçları + Kiralama Borçları + Sermaye Benzeri Krediler.
- **Maliyetli Pasif (basit, 5 bileşen)**: Mevduat (tamamı) + Alınan Krediler + Para Piyasalarına Borçlar + İhraç Edilen MK (Net) + Sermaye Benzeri Krediler. Yalnız "Faiz Maliyetli Pasiflerin Maliyeti" ve "Kaynağın Paçal Maliyeti" paydasında.
- **Düzeltilmiş Net Faiz Geliri**: Net Faiz (Kar Payı) Geliri + Ticari Kar/Zarar (Net).
- **TTM (son 12 ay)**: BDDK gelir tablosu YtD olduğundan: TTM(t) = YtD(t) + (Önceki yıl sonu − YtD(t − 12 ay)). 4. çeyrekte doğrudan yıllık tutar. Geçmiş dönem yoksa YtD × 12 / ay sayısı.
- **Ortalama bakiye**: (Bakiye(t) + Bakiye(t − 12 ay)) / 2. Bir yıl önceki dönem yoksa dönem sonu bakiye.
- **Grup 2 Krediler**: Yakın İzlemedeki krediler: 'Krediler ve Diğer Alacaklar' + 'Ödeme Planı Uzatılanlar' + 'Diğer' alt kalemleri.
- **Toplam Risk Tabanı**: Kredi Riskine Esas Tutar + Piyasa Riskine Esas Tutar + Operasyonel Riske Esas Tutar.

## Zaman yöntemi kısaltmaları

- `S`: Dönem sonu bakiye
- `Y`: Yılbaşından kümülatif (YtD)
- `TA`: Pay: son 12 ay (TTM) · Payda: 12 aylık ortalama bakiye
- `AA`: Pay ve payda: 12 aylık ortalama bakiye
- `TS`: Pay: son 12 ay (TTM) · Payda: dönem sonu bakiye
- `TT`: Pay ve payda: son 12 ay (TTM)
- `YY`: Pay ve payda: yılbaşından kümülatif (YtD), yıllıklandırılmaz
- `YA`: Pay: yılbaşından kümülatif (YtD) · Payda: 12 aylık ortalama bakiye
- `FARK`: İki yıllıklandırılmış oranın farkı (TTM / ortalama bakiye)
- `SS`: Dönem sonu bakiye / dönem sonu adet
- `TSA`: Pay: son 12 ay (TTM) · Payda: dönem sonu adet

## Grup (Rakip/Katılım vb.) toplulaştırma kuralı

- Büyüklük (TL/adet): üye değerlerinin **toplamı**.
- Stok rasyo: **ağırlıklı** (Σpay / Σpayda × 100).
- Akım/TTM rasyo: TTM pay toplamı / ortalama bakiye payda toplamı.
- Spread/fark ölçüleri: **basit ortalama**; SYR ve CET1 de basit ortalama.
- Şube/personel başına: Σtoplam / Σbölücü.
- Pay/payda tanımları: `pipeline/groups.py::RATIO_NUM_DEN`.


## Bilanço (115 ölçü)

### Toplam Aktifler  
`toplam_aktifler` · birim: TL · tip: buyukluk · stok · alt kategori: Aktifler
- **Formül:** Toplam Aktifler
- Tanım: Bankanın bilançosundaki tüm varlıkların toplamı; ölçek göstergesi.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor

### Krediler  
`krediler` · birim: TL · tip: buyukluk · stok · alt kategori: Aktifler
- **Formül:** Krediler (net)
- Tanım: Bilançodaki net krediler ve alacaklar.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Faktoring/leasing ve donuk alacaklar dahil değil; brüt tanım için Toplam Brüt Krediler.

### Grup 1 Krediler  
`grup_1_krediler` · birim: TL · tip: buyukluk · stok · alt kategori: Aktifler
- **Formül:** Krediler (net) − Donuk Alacaklar − Grup 2 Krediler
- Tanım: Standart nitelikli (Aşama 1) krediler.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço; Grup 1-2 Krediler tablosu
- Durum: Ham veriden hesaplanıyor

### Donuk Alacaklar  
`donuk_alacaklar` · birim: TL · tip: buyukluk · stok · alt kategori: Aktifler
- **Formül:** Donuk Alacaklar
- Tanım: Tahsili gecikmiş / takibe düşmüş (Aşama 3) krediler.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Düşük değer daha iyi (sıralama artan).

### Donuk Alacaklar (Satış ve Terkin Öncesi)  
`donuk_alacaklar_satis_terkin_oncesi` · birim: TL · tip: buyukluk · stok · alt kategori: Aktifler
- **Formül:** Donuk Alacaklar + |Aktiften Silinen (Sınırlı + Şüpheli + Zarar Niteliğinde)|
- Tanım: Dönem içinde satılan veya aktiften silinen tutarlar geri eklenmiş donuk alacaklar.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço; Donuk Alacak Hareket tablosu
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Silinen tutarlar YtD hareket tablosundan gelir.

### Grup 2 Krediler  
`grup_2_krediler` · birim: TL · tip: buyukluk · stok · alt kategori: Aktifler
- **Formül:** Grup 2 Krediler (Toplam)
- Tanım: Yakın izlemedeki (Aşama 2) krediler.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Grup 1-2 Krediler tablosu
- Durum: Ham veriden hesaplanıyor

### Tüketici Kredileri ve Bireysel Kredi Kartları  
`tuketici_kredileri` · birim: TL · tip: buyukluk · stok · alt kategori: Aktifler
- **Formül:** Tüketici ve Personel Kredileri + Kredi Kartları (Toplam)
- Tanım: Bireysel krediler ve bireysel kredi kartları toplamı (personel kredileri dahil).
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Tüketici Kredileri detay tablosu
- Durum: Ham veriden hesaplanıyor

### Bireysel Kredi Kartları  
`bireysel_kredi_kartlari` · birim: TL · tip: buyukluk · stok · alt kategori: Aktifler
- **Formül:** Bireysel KK (TP+YP) + Personel KK (TP+YP)
- Tanım: Bireysel ve personel kredi kartı bakiyeleri.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Tüketici Kredileri detay tablosu
- Durum: Ham veriden hesaplanıyor

### İhtiyaç Kredileri  
`ihtiyac_kredileri` · birim: TL · tip: buyukluk · stok · alt kategori: Aktifler
- **Formül:** Tüketici + Personel İhtiyaç Kredisi (TP + YP + Dövize Endeksli)
- Tanım: Genel ihtiyaç kredileri.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Tüketici Kredileri detay tablosu
- Durum: Ham veriden hesaplanıyor

### Konut Kredileri  
`konut_kredileri` · birim: TL · tip: buyukluk · stok · alt kategori: Aktifler
- **Formül:** Tüketici + Personel Konut Kredisi (TP + YP + Dövize Endeksli)
- Tanım: Konut kredileri.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Tüketici Kredileri detay tablosu
- Durum: Ham veriden hesaplanıyor

### Taşıt Kredileri  
`tasit_kredileri` · birim: TL · tip: buyukluk · stok · alt kategori: Aktifler
- **Formül:** Tüketici + Personel Taşıt Kredisi (TP + YP + Dövize Endeksli)
- Tanım: Taşıt kredileri.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Tüketici Kredileri detay tablosu
- Durum: Ham veriden hesaplanıyor

### Tüzel Krediler  
`tuzel_krediler` · birim: TL · tip: buyukluk · stok · alt kategori: Aktifler
- **Formül:** Krediler (net) − Tüketici Kredileri ve Bireysel KK
- Tanım: Bireysel olmayan (kurumsal/ticari/KOBİ) krediler.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço; Tüketici Kredileri detay tablosu
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Doğrudan raporlanmaz, farktan türetilir.

### TP Aktifler / Toplam Aktifler  
`tp_aktifler_ta` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** TP Toplam Aktifler / Toplam Aktifler
- Tanım: Aktiflerin Türk parası kısmının payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor

### Finansal Varlıklar (Net) / Toplam Aktifler  
`finansal_varliklar_net_ta` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** (Finansal Varlıklar (Net) + İtfa Edilmiş Maliyetle Ölçülen FV) / Toplam Aktifler
- Tanım: Finansal varlıkların aktif içindeki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor

### Menkul Kıymetler / Toplam Aktifler  
`menkul_kiymetler_ta` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** Menkul Kıymetler / Toplam Aktifler
- Tanım: Menkul kıymet portföyünün aktif içindeki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor

### Krediler / Toplam Aktifler  
`krediler_ta` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** Krediler (net) / Toplam Aktifler
- Tanım: Net kredilerin aktif içindeki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Brüt versiyonu: brut_krediler_ta.

### Grup 1 Krediler / Toplam Krediler  
`grup_1_krediler_toplam` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** Grup 1 Krediler / Toplam Brüt Krediler
- Tanım: Standart nitelikli kredilerin toplam krediler içindeki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço; Grup 1-2 Krediler
- Durum: Ham veriden hesaplanıyor

### Donuk Alacaklar / Toplam Krediler (NPL Rasyosu)  
`npl_rasyosu` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** Donuk Alacaklar / Krediler (net)
- Tanım: Takipteki kredi oranı (NPL).
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Payda net krediler; düşük değer daha iyi.

### NPL Rasyosu (Satış ve Terkin Öncesi)  
`npl_rasyosu_satis_terkin_oncesi` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** (Donuk Alacaklar + |Aktiften Silinen|) / (Krediler (net) + |Aktiften Silinen|)
- Tanım: Satış ve aktiften silme etkisi arındırılmış NPL oranı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço; Donuk Alacak Hareket tablosu
- Durum: Ham veriden hesaplanıyor

### Net NPL Formasyon Rasyosu  
`npl_formasyonu` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** (Σ Dönem İçi İntikal + Diğer Giriş + Σ Dönem İçi Tahsilat + Diğer Çıkış) / Ortalama Toplam Brüt Krediler
- Tanım: Dönemde oluşan net yeni NPL'in kredilere oranı.
- Zaman yöntemi: Pay: yılbaşından kümülatif (YtD) · Payda: 12 aylık ortalama bakiye
- Kaynak tablo: Donuk Alacak Hareket tablosu; Bilanço
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Tahsilatlar ham veride negatif. Pay YtD, yıllıklandırılmaz.

### Donuk Alacaklar Dönemiçi Tahsilat / Ortalama Krediler  
`donuk_tahsilat_ort_krediler` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** −(Σ Dönem İçi Tahsilat + Diğer Çıkış) / Ortalama Toplam Brüt Krediler
- Tanım: Dönem içinde donuk alacaklardan yapılan tahsilatın kredilere oranı.
- Zaman yöntemi: Pay: yılbaşından kümülatif (YtD) · Payda: 12 aylık ortalama bakiye
- Kaynak tablo: Donuk Alacak Hareket tablosu; Bilanço
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Pozitif gösterim için işaret çevrilir.

### Donuk Alacaklar Dönemiçi İntikal / Ortalama Krediler  
`donuk_intikal_ort_krediler` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** (Σ Dönem İçi İntikal + Diğer Giriş) / Ortalama Toplam Brüt Krediler
- Tanım: Dönem içinde donuk alacağa geçen tutarın kredilere oranı.
- Zaman yöntemi: Pay: yılbaşından kümülatif (YtD) · Payda: 12 aylık ortalama bakiye
- Kaynak tablo: Donuk Alacak Hareket tablosu; Bilanço
- Durum: Ham veriden hesaplanıyor

### Grup 2 Krediler / Toplam Krediler  
`grup_2_krediler_toplam` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** Grup 2 Krediler / (Krediler (net) − Kiralama İşlemlerinden Alacaklar)
- Tanım: Yakın izlemedeki kredilerin toplam kredilere oranı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Grup 1-2 Krediler; Bilanço
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: ⚠ Diğer "…/Toplam Krediler" oranlarından farklı payda (brüt değil).

### Grup 2 Krediler / Çekirdek Sermaye  
`grup_2_krediler_cekirdek_sermaye` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** Grup 2 Krediler / Çekirdek Sermaye Toplamı
- Tanım: Aşama 2 kredilerin çekirdek sermayeye oranı; sermaye üzerindeki potansiyel risk baskısı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Grup 1-2 Krediler; Sermaye Yeterliliği tablosu
- Durum: Ham veriden hesaplanıyor

### Tüketici Kredileri / Toplam Krediler  
`tuketici_toplam` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** Tüketici Kredileri ve Bireysel KK / Toplam Brüt Krediler
- Tanım: Bireysel kredilerin toplam kredi içindeki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Tüketici Kredileri detay; Bilanço
- Durum: Ham veriden hesaplanıyor

### Grup 2 Tüketici Kredileri / Tüketici Kredileri  
`grup_2_tuketici_tuketici` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** Grup 2 Tüketici Kredileri / Tüketici Kredileri (KK hariç)
- Tanım: Bireysel kredilerde Aşama 2 oranı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Grup 1-2 Krediler; Tüketici Kredileri detay
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Payda kredi kartlarını içermez, KMH dahildir.

### Bireysel Kredi Kartları / Toplam Krediler  
`bkk_toplam` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** Bireysel Kredi Kartları / Toplam Brüt Krediler
- Tanım: Bireysel kredi kartlarının toplam kredi içindeki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Tüketici Kredileri detay; Bilanço
- Durum: Ham veriden hesaplanıyor

### İhtiyaç Kredileri / Toplam Krediler  
`ihtiyac_toplam` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** İhtiyaç Kredileri / Toplam Brüt Krediler
- Tanım: İhtiyaç kredilerinin toplam kredi içindeki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Tüketici Kredileri detay; Bilanço
- Durum: Ham veriden hesaplanıyor

### Konut Kredileri / Tüketici Kredileri  
`konut_tuketici` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** Konut Kredileri / Tüketici Kredileri ve Bireysel KK
- Tanım: Konut kredilerinin bireysel krediler içindeki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Tüketici Kredileri detay
- Durum: Ham veriden hesaplanıyor

### Konut Kredileri / TP Pasifler  
`konut_tp_pasifler` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** Konut Kredileri / (TP Toplam Pasifler − TP Özkaynaklar)
- Tanım: Konut kredilerinin TP yabancı kaynaklara oranı (vade uyumsuzluğu göstergesi).
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Tüketici Kredileri detay; Bilanço
- Durum: Ham veriden hesaplanıyor

### Taşıt Kredileri / Tüketici Kredileri  
`tasit_tuketici` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** Taşıt Kredileri / Tüketici Kredileri ve Bireysel KK
- Tanım: Taşıt kredilerinin bireysel krediler içindeki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Tüketici Kredileri detay
- Durum: Ham veriden hesaplanıyor

### Tüzel Krediler / Toplam Krediler  
`tuzel_toplam` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** Tüzel Krediler / Toplam Brüt Krediler
- Tanım: Tüzel kredilerin toplam kredi içindeki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço; Tüketici Kredileri detay
- Durum: Ham veriden hesaplanıyor

### Grup 2 Tüzel Krediler / Tüzel Krediler  
`grup_2_tuzel_tuzel` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** (Grup 2 Toplam − Grup 2 Kredi Kartları − Grup 2 Tüketici − Grup 2 Mali Kesim) / Tüzel Krediler
- Tanım: Tüzel kredilerde Aşama 2 oranı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Grup 1-2 Krediler; Bilanço
- Durum: Ham veriden hesaplanıyor

### Dış Ticaret Kredileri / Toplam Krediler  
`dis_ticaret_toplam` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** (İhracat + İthalat Kredileri; Standart + Grup 2) / Toplam Brüt Krediler
- Tanım: İhracat ve ithalat kredilerinin toplam kredi içindeki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Grup 1-2 Krediler; Bilanço
- Durum: Ham veriden hesaplanıyor

### Mali Kesime Verilen Krediler / Toplam Krediler  
`mali_kesim_toplam` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** Mali Kesime Verilen Krediler (Standart Nitelikli) / Toplam Brüt Krediler
- Tanım: Finansal kuruluşlara verilen kredilerin payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Grup 1-2 Krediler; Bilanço
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Pay yalnız Grup 1 (Standart) kısmı içerir.

### TP Krediler / Toplam Krediler  
`tp_krediler_toplam` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** TP Toplam Brüt Krediler / Toplam Brüt Krediler
- Tanım: TL kredilerin toplam kredi içindeki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor

### USD Cinsi Krediler / YP Krediler  
`usd_yp_krediler` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** USD Cinsi Krediler / YP Krediler Toplamı
- Tanım: YP krediler içinde USD cinsinin payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Kur Riski tablosu
- Durum: Ham veriden hesaplanıyor

### EURO Cinsi Krediler / YP Krediler  
`euro_yp_krediler` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** EUR Cinsi Krediler / YP Krediler Toplamı
- Tanım: YP krediler içinde EUR cinsinin payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Kur Riski tablosu
- Durum: Ham veriden hesaplanıyor

### Ortaklık Yatırımları / Toplam Aktifler  
`ortaklik_yatirimlari_ta` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** Ortaklık Yatırımları / Toplam Aktifler
- Tanım: İştirak/bağlı ortaklık yatırımlarının aktif içindeki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor

### Diğer Aktifler / Toplam Aktifler  
`diger_aktifler_ta` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** (Maddi Duran V. + Maddi Olmayan Duran V. + Yatırım Amaçlı Gayrimenkuller + Diğer Aktifler + Vergi Varlığı) / Toplam Aktifler
- Tanım: Faiz getirmeyen diğer aktiflerin payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor

### Faiz (Kar Payı) Getirili Aktifler / Toplam Aktifler  
`faiz_getirili_ta` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** Faiz Getirili Aktifler (detaylı) / Toplam Aktifler
- Tanım: Faiz/kâr payı getiren aktiflerin toplam aktife oranı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço; TCMB tablosu
- Durum: Ham veriden hesaplanıyor

### Faiz (Kar Payı) Getirili Aktifler / Maliyetli Pasifler  
`faiz_getirili_maliyetli` · birim: kat · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** Faiz Getirili Aktifler (detaylı) / Faiz Maliyetli Pasifler (detaylı)
- Tanım: Getirili aktiflerin maliyetli pasifleri kaç kat karşıladığı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço; TCMB tablosu
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Birim: kat.

### YP Aktifler / YP Pasifler  
`yp_aktifler_toplam_pasifler` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** YP Toplam Aktifler / YP Toplam Pasifler
- Tanım: YP aktiflerin YP pasifleri karşılama oranı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Ad "YP Pasifler" diyor; id'deki "toplam_pasifler" eski tanımdan kalma.

### Ortalama Faiz (Kar Payı) Getirili Aktifler / Ortalama Özkaynaklar  
`faiz_getirili_ozkaynak` · birim: kat · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** Ort. Faiz Getirili Aktifler (detaylı) / Ort. Özkaynaklar
- Tanım: Getirili aktiflerin özkaynağa oranı (kaldıraç).
- Zaman yöntemi: Pay ve payda: 12 aylık ortalama bakiye
- Kaynak tablo: Bilanço; TCMB tablosu
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Birim: kat.

### Yabancı Para Net Genel Pozisyonu / Toplam Özkaynaklar  
`yp_net_pozisyon_ozkaynak` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** (YP Net Bilanço Pozisyonu + YP Net Nazım Hesap Pozisyonu) / Toplam Özkaynaklar (Ana + Katkı Sermaye)
- Tanım: Açık/fazla döviz pozisyonunun yasal özkaynağa oranı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Kur Riski tablosu; Özkaynak Kalemleri tablosu
- Durum: Ham veriden hesaplanıyor

### NPL Karşılama Oranı  
`npl_karsilama_orani` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** |Beklenen Zarar Karşılıkları| / Donuk Alacaklar
- Tanım: Donuk alacakların ayrılan karşılıkla ne ölçüde karşılandığı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Karşılık toplam BZK (Aşama 1-2-3 birlikte) olabilir; teyit edilmeli.

### Mevduat  
`mevduat` · birim: TL · tip: buyukluk · stok · alt kategori: Pasifler
- **Formül:** Mevduat
- Tanım: Toplam mevduat (katılım bankalarında toplanan fonlar).
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor

### Toplam Kaynak  
`toplam_kaynak` · birim: TL · tip: buyukluk · stok · alt kategori: Pasifler
- **Formül:** Toplam Kaynak
- Tanım: Mevduat ve piyasa borçlanmasından oluşan ana fon kaynağı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Para piyasalarına borçlar hariç; dahil tanım: Toplam Fonlama.

### Kıymetli Maden Mevduatı  
`kiymetli_maden_mevduati` · birim: TL · tip: buyukluk · stok · alt kategori: Pasifler
- **Formül:** Kıymetli Maden Depo Hesabı
- Tanım: Altın ve diğer kıymetli maden cinsinden mevduat.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Mevduat / Katılım Fonu detay tablosu
- Durum: Ham veriden hesaplanıyor

### Vadesiz Mevduat  
`vadesiz_mevduat` · birim: TL · tip: buyukluk · stok · alt kategori: Pasifler
- **Formül:** Vadesiz Mevduat
- Tanım: Vadesiz (özel cari) mevduat.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Mevduat / Katılım Fonu detay tablosu
- Durum: Ham veriden hesaplanıyor

### Vadeli Mevduat  
`vadeli_mevduat` · birim: TL · tip: buyukluk · stok · alt kategori: Pasifler
- **Formül:** Mevduat − Vadesiz Mevduat
- Tanım: Vadeli mevduat / katılma hesapları.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço; Mevduat detay
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Farktan türetilir.

### Resmi Kurumlar Mevduatı  
`resmi_kurumlar_mevduat` · birim: TL · tip: buyukluk · stok · alt kategori: Pasifler
- **Formül:** Resmi Kuruluşlar Mevduatı
- Tanım: Resmi kuruluşlardan toplanan mevduat.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Mevduat / Katılım Fonu detay tablosu
- Durum: Ham veriden hesaplanıyor

### Özkaynaklar  
`ozkaynaklar` · birim: TL · tip: buyukluk · stok · alt kategori: Pasifler
- **Formül:** Özkaynaklar
- Tanım: Bilanço özkaynakları.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Yasal özkaynaktan farklı; bkz. toplam_ozkaynaklar_regulasyon.

### Alınan Krediler ve İ.E.M.K / Toplam Kaynak  
`alinan_krediler_iemk_toplam_kaynak` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** (Alınan Krediler + İhraç Edilen MK) / Toplam Kaynak
- Tanım: Borçlanma ve ihraçların toplam kaynak içindeki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor

### TP Alınan Krediler ve İ.E.M.K / Toplam Alınan Krediler ve İ.E.M.K  
`tp_alinan_toplam_alinan` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** TP (Alınan Krediler + İhraç Edilen MK) / (Alınan Krediler + İhraç Edilen MK)
- Tanım: Borçlanma ve ihraçların TL kısmının payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor

### Krediler / Mevduat  
`krediler_mevduat` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** Krediler (net) / Mevduat
- Tanım: Kredi/mevduat oranı (LDR).
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor

### Tüzel Krediler / Tüzel Mevduat  
`tuzel_krediler_tuzel_mevduat` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** Tüzel Krediler / Tüzel Mevduat
- Tanım: Tüzel kredilerin tüzel mevduatla fonlanma oranı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço; Mevduat detay
- Durum: Ham veriden hesaplanıyor

### Krediler / Altındışı Mevduat  
`krediler_altindisi_mevduat` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** Krediler (net) / (Mevduat − Kıymetli Maden Mevduatı)
- Tanım: Altın mevduatı hariç kredi/mevduat oranı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço; Mevduat detay
- Durum: Ham veriden hesaplanıyor

### Krediler / Toplam Kaynak  
`krediler_toplam_kaynak` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** Toplam Brüt Krediler / Toplam Kaynak
- Tanım: Kredilerin toplam kaynakla fonlanma oranı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor

### TP Krediler / TP Kaynak  
`tp_krediler_tp_kaynak` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** TP Krediler (net) / TP (Mevduat + Alınan Krediler + İhraç Edilen MK)
- Tanım: TL kredilerin TL kaynaklarla fonlanma oranı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Pay net krediler (brüt değil).

### YP Krediler / YP Altındışı Kaynak  
`yp_krediler_yp_altindisi_kaynak` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** YP Krediler (net) / (YP Kaynak − Kıymetli Maden Mevduatı)
- Tanım: YP kredilerin altın hariç YP kaynaklarla fonlanma oranı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço; Mevduat detay
- Durum: Ham veriden hesaplanıyor

### Vadesiz Mevduat / Toplam Mevduat  
`vadesiz_mevduat_toplam_mevduat` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** Vadesiz Mevduat / Mevduat
- Tanım: Vadesiz mevduat payı (düşük maliyetli fon).
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço; Mevduat detay
- Durum: Ham veriden hesaplanıyor

### Kıymetli Maden Mevduatı / Toplam Mevduat  
`kiymetli_maden_toplam_mevduat` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** Kıymetli Maden Mevduatı / Mevduat
- Tanım: Altın mevduatının mevduat içindeki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço; Mevduat detay
- Durum: Ham veriden hesaplanıyor

### Vadesiz Mevduat / Toplam Kaynak  
`vadesiz_mevduat_toplam_kaynak` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** Vadesiz Mevduat / Toplam Kaynak
- Tanım: Vadesiz mevduatın toplam kaynak içindeki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço; Mevduat detay
- Durum: Ham veriden hesaplanıyor

### TP Mevduat / Toplam Mevduat  
`tp_mevduat_toplam_mevduat` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** TP Mevduat / Mevduat
- Tanım: TL mevduatın payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor

### YP Mevduat / Toplam Mevduat  
`yp_mevduat_toplam_mevduat` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül (yalnız kod, metadata yok):**
```python
def m_yp_mevduat_toplam_mevduat(ctx, b, t):
    """YP Mevduat (kıymetli maden dahil) / Toplam Mevduat. 100 − TP payı
    olarak DEĞİL doğrudan hesaplanır: bazı eski dönemlerde ham veride
    TP + YP ≠ Toplam. PBI kalemlerinden (YP Mevduat / Toplam Mevduat)
    hesaplanan oranla 2019+ 641/643 aynı (2026-09-24)."""
    return safe_ratio(ctx.bilanco(b, t, 'Mevduat', 'YP'), ctx.bilanco(b, t, 'Mevduat'))
```

### TP Vadeli Mevduat / TP Mevduat  
`tp_vadeli_tp_mevduat` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül (yalnız kod, metadata yok):**
```python
def m_tp_vadeli_tp_mevduat(ctx, b, t):
    return safe_ratio(*mevduat_vade_bolumu(ctx, b, t, 'TP', True))
```

### TP Vadesiz Mevduat / TP Mevduat  
`tp_vadesiz_tp_mevduat` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül (yalnız kod, metadata yok):**
```python
def m_tp_vadesiz_tp_mevduat(ctx, b, t):
    return safe_ratio(*mevduat_vade_bolumu(ctx, b, t, 'TP', False))
```

### YP Vadeli Mevduat / YP Mevduat (KM Hariç)  
`yp_vadeli_yp_mevduat` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül (yalnız kod, metadata yok):**
```python
def m_yp_vadeli_yp_mevduat(ctx, b, t):
    return safe_ratio(*mevduat_vade_bolumu(ctx, b, t, 'YP', True))
```

### YP Vadesiz Mevduat / YP Mevduat (KM Hariç)  
`yp_vadesiz_yp_mevduat` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül (yalnız kod, metadata yok):**
```python
def m_yp_vadesiz_yp_mevduat(ctx, b, t):
    return safe_ratio(*mevduat_vade_bolumu(ctx, b, t, 'YP', False))
```

### TP Mevduat / Altındışı Mevduat  
`tp_mevduat_altindisi_mevduat` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** TP Mevduat / (Mevduat − Kıymetli Maden Mevduatı)
- Tanım: TL mevduatın altın hariç mevduat içindeki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço; Mevduat detay
- Durum: Ham veriden hesaplanıyor

### TP Kaynak / Toplam Kaynak  
`tp_kaynak_toplam_kaynak` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** TP (Mevduat + Alınan Krediler + İhraç Edilen MK) / Toplam Kaynak
- Tanım: TL kaynakların payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor

### Toplam Kaynak / Toplam Pasifler  
`toplam_kaynak_toplam_pasifler` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** Toplam Kaynak / Toplam Pasifler
- Tanım: Toplam kaynağın pasif içindeki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor

### TP Pasifler / Toplam Pasifler (Özkaynaklar Hariç)  
`tp_pasifler_toplam_pasifler_ozkaynak_haric` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** TP Toplam Pasifler / (Toplam Pasifler − Özkaynaklar)
- Tanım: TL pasiflerin yabancı kaynaklara oranı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: ⚠ Pay özkaynak DAHİL, payda HARİÇ; %100'ü aşabilir.

### Sermaye Benzeri Krediler / Toplam Pasifler  
`sermaye_benzeri_pasifler` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** Sermaye Benzeri Krediler / Toplam Pasifler
- Tanım: Sermaye benzeri borçların pasif içindeki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor

### Para Piyasasına Borçlar / Toplam Pasifler  
`ppborclari_pasifler` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** Para Piyasalarına Borçlar / Toplam Pasifler
- Tanım: Para piyasası borçlarının pasif içindeki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor

### Faiz (Kar Payı) Maliyetli Pasifler / Toplam Pasifler  
`maliyetli_pasifler_toplam_pasifler` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** Faiz Maliyetli Pasifler (detaylı) / Toplam Pasifler
- Tanım: Faiz/kâr payı maliyeti olan pasiflerin payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço; Mevduat detay
- Durum: Ham veriden hesaplanıyor

### Serbest Sermaye / Toplam Aktifler  
`serbest_sermaye_ta` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** (Özkaynaklar − Ortaklık Yatırımları − Maddi Duran V. − Maddi Olmayan Duran V.) / Toplam Aktifler
- Tanım: Duran varlıklara bağlanmamış özkaynağın aktife oranı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor

### Sermaye Yeterlilik Rasyosu (SYR)  
`syr` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** BDDK raporlanan Sermaye Yeterlilik Rasyosu (%)
- Tanım: Sermaye yeterlilik rasyosu.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Sermaye oranları tablosu
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Hesaplanmaz, raporlanan oran alınır.

### Çekirdek Sermaye Yeterliliği Oranı  
`cekirdek_syr` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** BDDK raporlanan Çekirdek Sermaye Yeterliliği Oranı (%)
- Tanım: Çekirdek sermaye (CET1) yeterlilik oranı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Sermaye oranları tablosu
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Hesaplanmaz, raporlanan oran alınır.

### Gayrinakdi Krediler (Garanti ve Kefaletler)  
`gayrinakdi_krediler` · birim: TL · tip: buyukluk · stok · alt kategori: Bilanço Dışı
- **Formül:** Garanti ve Kefaletler, Toplam
- Tanım: Teminat mektupları, akreditifler vb. garanti ve kefaletler.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Nazım Hesaplar (Bilanço Dışı)
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Toplam satırı negatifse alt kalemlerin toplamı kullanılır.

### Toplam Brüt Krediler  
`toplam_brut_krediler` · birim: TL · tip: buyukluk · stok · alt kategori: Aktifler
- **Formül:** Toplam Brüt Krediler
- Tanım: NPL, faktoring ve leasing dahil brüt kredi stoku.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor

### Toplam Canlı Krediler  
`toplam_canli_krediler` · birim: TL · tip: buyukluk · stok · alt kategori: Aktifler
- **Formül:** Toplam Canlı Krediler
- Tanım: Donuk ve takipteki alacaklar hariç brüt krediler.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor

### Toplam Fonlama  
`toplam_fonlama` · birim: TL · tip: buyukluk · stok · alt kategori: Pasifler
- **Formül:** Toplam Fonlama
- Tanım: Para piyasası borçları dahil toplam fonlama.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor

### Toplam Kredi Kartları  
`toplam_kredi_kartlari` · birim: TL · tip: buyukluk · stok · alt kategori: Aktifler
- **Formül:** Kredi Kartları Standart Nitelikli (Toplam) + Bireysel KK TP + Bireysel KK TP
- Tanım: Kredi kartı kaynaklı toplam alacak (PBI tanımı).
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Grup 1-2 Krediler; Tüketici Kredileri detay
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: ⚠ PBI DAX'ına birebir sadık: Bireysel KK TP iki kez toplanıyor, YP hiç yok. Kaynak formülde kopyala-yapıştır hatası olabilir; teyit edilmeli.

### Toplam Mevduat (KM Hariç)  
`toplam_mevduat_km_haric` · birim: TL · tip: buyukluk · stok · alt kategori: Pasifler
- **Formül:** Mevduat − Kıymetli Maden Mevduatı
- Tanım: Kıymetli maden hariç mevduat.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço; Mevduat detay
- Durum: Ham veriden hesaplanıyor

### Toplam Özkaynaklar (Ana Sermaye+ Katkı Sermaye)  
`toplam_ozkaynaklar_regulasyon` · birim: TL · tip: buyukluk · stok · alt kategori: Pasifler
- **Formül:** Toplam Özkaynaklar (Ana Sermaye + Katkı Sermaye)
- Tanım: Sermaye yeterliliği hesabındaki yasal özkaynak.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Özkaynak Kalemleri tablosu
- Durum: Ham veriden hesaplanıyor

### Toplam Pasifler  
`toplam_pasifler` · birim: TL · tip: buyukluk · stok · alt kategori: Pasifler
- **Formül:** Toplam Pasifler
- Tanım: Bilanço pasif toplamı (= Toplam Aktifler).
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor

### Toplam Pasifler (Özkaynak Hariç)  
`toplam_pasifler_ozkaynak_haric` · birim: TL · tip: buyukluk · stok · alt kategori: Pasifler
- **Formül:** Toplam Pasifler − Özkaynaklar
- Tanım: Yabancı kaynaklar toplamı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor

### Toplam Risk Ağırlıklı Varlıklar (RAV)  
`rav` · birim: TL · tip: buyukluk · stok · alt kategori: Pasifler
- **Formül:** Kredi Riskine Esas Tutar: Toplam
- Tanım: Kredi riskine esas tutar.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Sermaye Yeterliliği tablosu
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: ⚠ Ad "Toplam RAV" olsa da yalnız kredi riskini içerir (PBI DAX'ına sadık). Piyasa + operasyonel dahil tutar: toplam_risk_tabani.

### Ortalama RAV / Ortalama Özkaynaklar  
`ort_rav_ort_ozkaynak` · birim: kat · tip: rasyo · stok · alt kategori: Pasifler
- **Formül (yalnız kod, metadata yok):**
```python
def m_ort_rav_ort_ozkaynak(ctx, b, t):
    """PBI [Ortalama RAV / Ortalama Özkaynaklar] (kat) — ortalama RAV
    (m_rav) / ortalama Özkaynaklar. PBI datatable'ıyla son 5 çeyrekte
    130/135, KT birebir (2025-12: 4,99 kat)."""
    return safe_ratio(_avg(ctx, b, t, lambda bb, tt: m_rav(ctx, bb, tt)),
                      _avg(ctx, b, t, lambda bb, tt: ctx.bilanco(bb, tt, 'Özkaynaklar')),
                      scale=1.0)
```

### Toplam Risk  
`toplam_risk_tabani` · birim: TL · tip: buyukluk · stok · alt kategori: Pasifler
- **Formül:** Toplam Risk Tabanı
- Tanım: Sermaye yeterliliği paydası olan toplam risk tabanı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Sermaye Yeterliliği; TCMB tablosu
- Durum: Ham veriden hesaplanıyor

### Kredi Riski/ Toplam Risk Tabanı  
`kredi_riski_toplam_risk` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** Kredi Riskine Esas Tutar / Toplam Risk Tabanı
- Tanım: Kredi riskinin risk tabanındaki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Sermaye Yeterliliği; TCMB tablosu
- Durum: Ham veriden hesaplanıyor

### Piyasa Riski/ Toplam Risk Tabanı  
`piyasa_riski_toplam_risk` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** Piyasa Riskine Esas Tutar / Toplam Risk Tabanı
- Tanım: Piyasa riskinin risk tabanındaki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Sermaye Yeterliliği; TCMB tablosu
- Durum: Ham veriden hesaplanıyor

### Operasyonel Riski/ Toplam Risk Tabanı  
`operasyonel_risk_toplam_risk` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** Operasyonel Riske Esas Tutar / Toplam Risk Tabanı
- Tanım: Operasyonel riskin risk tabanındaki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Sermaye Yeterliliği; TCMB tablosu
- Durum: Ham veriden hesaplanıyor

### Brüt Krediler/ Toplam Aktifler  
`brut_krediler_ta` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** Toplam Brüt Krediler / Toplam Aktifler
- Tanım: Brüt kredilerin aktif içindeki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor

### Alınan Krediler/ Toplam Pasifler  
`alinan_krediler_toplam_pasifler` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** Alınan Krediler / Toplam Pasifler
- Tanım: Alınan kredilerin pasif içindeki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor

### Bankalar/ Toplam Aktifler  
`bankalar_toplam_aktifler` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** Bankalar / Toplam Aktifler
- Tanım: Bankalardan alacakların aktif içindeki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor

### Birikimli Vadeli Mevduat/ Toplam Vadeli Mevduat  
`birikimli_vadeli_mevduat_toplam_vadeli` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** Birikimli Vadeli Mevduat / Vadeli Mevduat
- Tanım: Birikimli vadeli mevduatın vadeli mevduat içindeki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Mevduat Vade Yapısı (katılımda Katılma Hesapları) tablosu
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Katılım bankalarında "Birikimli Katılma Hesabı" kullanılır.

### Resmi Kurumlar Mevduatı/ Toplam Mevduat  
`resmi_kurumlar_mevduat_toplam_mevduat` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** Resmi Kuruluşlar Mevduatı / Mevduat
- Tanım: Resmi kurum mevduatının payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço; Mevduat detay
- Durum: Ham veriden hesaplanıyor

### Toplam Fonlama/ Faiz (Kar Payı) Maliyetli Pasifler  
`toplam_fonlama_faiz_maliyetli_pasif` · birim: kat · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** Toplam Fonlama / Faiz Maliyetli Pasifler (detaylı)
- Tanım: Toplam fonlamanın maliyetli pasiflere oranı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço; Mevduat detay
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Birim: kat.

### Tüzel Mevduat / Toplam Mevduat  
`tuzel_mevduat_toplam_mevduat` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** Tüzel Mevduat / Mevduat
- Tanım: Tüzel mevduatın payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço; Mevduat detay
- Durum: Ham veriden hesaplanıyor

### Nakit Değerler / Toplam Aktifler  
`nakit_degerler_ta` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** Nakit Değerler ve Merkez Bankası / Toplam Aktifler
- Tanım: Nakit ve merkez bankası bakiyelerinin aktif içindeki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor

### 1 Aya Kadar Vadeli Mevduat/ Toplam Vadeli Mevduat  
`vadeli_1ay_toplam_vadeli` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** Vadeli Mevduat (1 Aya Kadar) / Vadeli Mevduat
- Tanım: 1 aya kadar vadeli mevduatın payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Mevduat Vade Yapısı tablosu
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: ⚠ Katılım bankalarında vade dilimleri farklı olduğundan 0 döner.

### 1-3 Ay Vadeli Mevduat/ Toplam Vadeli Mevduat  
`vadeli_1_3ay_toplam_vadeli` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** Vadeli Mevduat (1-3 Ay) / Vadeli Mevduat
- Tanım: 1-3 ay vadeli mevduatın payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Mevduat Vade Yapısı tablosu
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: ⚠ Katılım bankalarında 0 döner.

### 3-6 Ay Vadeli Mevduat/ Toplam Vadeli Mevduat  
`vadeli_3_6ay_toplam_vadeli` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** Vadeli Mevduat (3-6 Ay) / Vadeli Mevduat
- Tanım: 3-6 ay vadeli mevduatın payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Mevduat Vade Yapısı tablosu
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: ⚠ Katılım bankalarında 0 döner.

### 6-12 Ay Vadeli Mevduat/ Toplam Vadeli Mevduat  
`vadeli_6_12ay_toplam_vadeli` · birim: % · tip: rasyo · stok · alt kategori: Pasifler
- **Formül:** Vadeli Mevduat (6 Ay-1 Yıl) / Vadeli Mevduat
- Tanım: 6-12 ay vadeli mevduatın payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Mevduat Vade Yapısı tablosu
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: ⚠ Katılım bankalarında 0 döner.

### YP Krediler/ Toplam Krediler  
`yp_krediler_toplam_krediler` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** YP Toplam Brüt Krediler / Toplam Brüt Krediler
- Tanım: Yabancı para kredilerin toplam kredi içindeki payı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Bilanço
- Durum: Ham veriden hesaplanıyor

### Likidite Açığı, Vadesiz / Toplam Aktifler  
`likidite_acigi_vadesiz_ta` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** Likidite Açığı (Vadesiz) / Toplam Aktifler
- Tanım: Kalan vadeye göre vadesiz dilimdeki likidite açığının aktife oranı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Kalan Vade (Likidite) tablosu; Bilanço
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Negatif = açık.

### Likidite Açığı, 1 Aya Kadar / Toplam Aktifler  
`likidite_acigi_1ay_ta` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** Likidite Açığı (1 Aya Kadar) / Toplam Aktifler
- Tanım: 1 aya kadar vade dilimindeki likidite açığının aktife oranı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Kalan Vade (Likidite) tablosu; Bilanço
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Negatif = açık.

### Likidite Açığı, 1-3 Ay / Toplam Aktifler  
`likidite_acigi_1_3ay_ta` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** Likidite Açığı (1-3 Ay) / Toplam Aktifler
- Tanım: 1-3 ay vade dilimindeki likidite açığının aktife oranı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Kalan Vade (Likidite) tablosu; Bilanço
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Negatif = açık.

### Likidite Açığı, 3-12 Ay / Toplam Aktifler  
`likidite_acigi_3_12ay_ta` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** Likidite Açığı (3-12 Ay) / Toplam Aktifler
- Tanım: 3-12 ay vade dilimindeki likidite açığının aktife oranı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Kalan Vade (Likidite) tablosu; Bilanço
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Negatif = açık.

### Likidite Açığı, 1-5 Yıl / Toplam Aktifler  
`likidite_acigi_1_5yil_ta` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** Likidite Açığı (1-5 Yıl) / Toplam Aktifler
- Tanım: 1-5 yıl vade dilimindeki likidite açığının aktife oranı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Kalan Vade (Likidite) tablosu; Bilanço
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Negatif = açık.

### Likidite Açığı, 5 Yıl ve Üzeri / Toplam Aktifler  
`likidite_acigi_5yil_uzeri_ta` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** Likidite Açığı (5 Yıl ve Üzeri) / Toplam Aktifler
- Tanım: 5 yıl üzeri vade dilimindeki likidite fazlası/açığının aktife oranı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Kalan Vade (Likidite) tablosu; Bilanço
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Negatif = açık.

### Likidite Açığı, Dağıtılamayan / Toplam Aktifler  
`likidite_acigi_dagitilamayan_ta` · birim: % · tip: rasyo · stok · alt kategori: Aktifler
- **Formül:** Likidite Açığı (Dağıtılamayan) / Toplam Aktifler
- Tanım: Vadeye dağıtılamayan kalemlerin net pozisyonunun aktife oranı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Kalan Vade (Likidite) tablosu; Bilanço
- Durum: Ham veriden hesaplanıyor


## Gelir Tablosu (48 ölçü)

### Net Dönem Karı (Zararı)  
`net_donem_kari` · birim: TL · tip: buyukluk · akim
- **Formül:** Net Dönem Karı / Zararı
- Tanım: Vergi sonrası net dönem kârı.
- Zaman yöntemi: Yılbaşından kümülatif (YtD)
- Kaynak tablo: Gelir Tablosu
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Ara çeyreklerde yılbaşından kümülatif; çeyrekler arası kıyasta dikkat.

### Brüt Faaliyet Karı / Zararı  
`brut_faaliyet_kari` · birim: TL · tip: buyukluk · akim
- **Formül:** Net Faaliyet Karı / Zararı
- Tanım: Karşılık ve giderler sonrası faaliyet kârı.
- Zaman yöntemi: Yılbaşından kümülatif (YtD)
- Kaynak tablo: Gelir Tablosu
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Ad "brüt" diyor, kaynak kalem "Net Faaliyet Karı".

### Faiz (Kar Payı) Gelirleri  
`faiz_gelirleri` · birim: TL · tip: buyukluk · akim
- **Formül:** Faiz Gelirleri
- Tanım: Faiz / kâr payı gelirleri.
- Zaman yöntemi: Yılbaşından kümülatif (YtD)
- Kaynak tablo: Gelir Tablosu
- Durum: Ham veriden hesaplanıyor

### Faiz (Kar Payı) Giderleri  
`faiz_giderleri` · birim: TL · tip: buyukluk · akim
- **Formül:** Faiz Giderleri
- Tanım: Faiz / kâr payı giderleri.
- Zaman yöntemi: Yılbaşından kümülatif (YtD)
- Kaynak tablo: Gelir Tablosu
- Durum: Ham veriden hesaplanıyor

### Net Faiz (Kar Payı) Geliri (Gideri)  
`net_faiz_geliri` · birim: TL · tip: buyukluk · akim
- **Formül:** Net Faiz Geliri / Gideri
- Tanım: Net faiz / kâr payı geliri.
- Zaman yöntemi: Yılbaşından kümülatif (YtD)
- Kaynak tablo: Gelir Tablosu
- Durum: Ham veriden hesaplanıyor

### Alınan Ücret ve Komisyonlar  
`alinan_ucret_komisyonlar` · birim: TL · tip: buyukluk · akim
- **Formül:** Alınan Ücret ve Komisyonlar
- Tanım: Alınan ücret ve komisyonlar.
- Zaman yöntemi: Yılbaşından kümülatif (YtD)
- Kaynak tablo: Gelir Tablosu
- Durum: Ham veriden hesaplanıyor

### G.Nakdi Kredilerden Alınan Ücret ve Komisyonlar  
`gnakdi_alinan_ucret_komisyonlar` · birim: TL · tip: buyukluk · akim
- **Formül:** Gayri Nakdi Kredilerden (alınan ücret ve komisyon alt kalemi)
- Tanım: Gayrinakdi kredilerden alınan komisyonlar.
- Zaman yöntemi: Yılbaşından kümülatif (YtD)
- Kaynak tablo: Gelir Tablosu
- Durum: Ham veriden hesaplanıyor

### Verilen Ücret ve Komisyonlar  
`verilen_ucret_komisyonlar` · birim: TL · tip: buyukluk · akim
- **Formül:** Verilen Ücret ve Komisyonlar
- Tanım: Ödenen ücret ve komisyonlar.
- Zaman yöntemi: Yılbaşından kümülatif (YtD)
- Kaynak tablo: Gelir Tablosu
- Durum: Ham veriden hesaplanıyor

### Net Ücret ve Komisyonlar  
`net_ucret_komisyonlar` · birim: TL · tip: buyukluk · akim
- **Formül:** Net Ücret ve Komisyon Gelirleri / Giderleri
- Tanım: Net ücret ve komisyon geliri.
- Zaman yöntemi: Yılbaşından kümülatif (YtD)
- Kaynak tablo: Gelir Tablosu
- Durum: Ham veriden hesaplanıyor

### Diğer Faaliyet Giderleri (Operasyonel Giderler)  
`diger_faaliyet_giderleri` · birim: TL · tip: buyukluk · akim
- **Formül:** Diğer Faaliyet Giderleri (−)
- Tanım: Personel dışı faaliyet giderleri.
- Zaman yöntemi: Yılbaşından kümülatif (YtD)
- Kaynak tablo: Gelir Tablosu
- Durum: Ham veriden hesaplanıyor

### Net Ticari Kar (Zarar)  
`net_ticari_kar` · birim: TL · tip: buyukluk · akim
- **Formül:** Ticari Kar / Zarar (Net)
- Tanım: Sermaye piyasası, türev ve kambiyo işlemleri net sonucu.
- Zaman yöntemi: Yılbaşından kümülatif (YtD)
- Kaynak tablo: Gelir Tablosu
- Durum: Ham veriden hesaplanıyor

### Reklam Giderleri  
`reklam_giderleri` · birim: TL · tip: buyukluk · akim
- **Formül:** Reklam ve İlan Giderleri
- Tanım: Reklam ve ilan giderleri.
- Zaman yöntemi: Yılbaşından kümülatif (YtD)
- Kaynak tablo: Faaliyet Giderleri detay dipnotu
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Sıralama azalan (en çok harcayan üstte).

### Personel Giderleri  
`personel_giderleri` · birim: TL · tip: buyukluk · akim
- **Formül:** Personel Giderleri (−)
- Tanım: Personel giderleri.
- Zaman yöntemi: Yılbaşından kümülatif (YtD)
- Kaynak tablo: Gelir Tablosu
- Durum: Ham veriden hesaplanıyor

### Karşılık Giderleri  
`karsilik_giderleri` · birim: TL · tip: buyukluk · akim
- **Formül:** Kredi ve Diğer Alacaklar Değer Düşüş Karşılığı (−)
- Tanım: Kredi ve diğer alacaklar için ayrılan beklenen zarar karşılığı gideri.
- Zaman yöntemi: Yılbaşından kümülatif (YtD)
- Kaynak tablo: Gelir Tablosu
- Durum: Ham veriden hesaplanıyor

### Ortalama Aktif Karlılığı (ROAA)  
`roaa` · birim: % · tip: rasyo · akim
- **Formül:** TTM Net Dönem Karı / Ortalama Toplam Aktifler
- Tanım: Ortalama aktif kârlılığı.
- Zaman yöntemi: Pay: son 12 ay (TTM) · Payda: 12 aylık ortalama bakiye
- Kaynak tablo: Gelir Tablosu; Bilanço
- Durum: Ham veriden hesaplanıyor

### Ortalama Özkaynak Karlılığı (ROAE)  
`roae` · birim: % · tip: rasyo · akim
- **Formül:** TTM Net Dönem Karı / Ortalama Özkaynaklar
- Tanım: Ortalama özkaynak kârlılığı.
- Zaman yöntemi: Pay: son 12 ay (TTM) · Payda: 12 aylık ortalama bakiye
- Kaynak tablo: Gelir Tablosu; Bilanço
- Durum: Ham veriden hesaplanıyor

### RORWA  
`rorwa` · birim: % · tip: rasyo · akim
- **Formül:** TTM Net Dönem Karı / Ortalama RAV
- Tanım: Risk ağırlıklı varlık kârlılığı.
- Zaman yöntemi: Pay: son 12 ay (TTM) · Payda: 12 aylık ortalama bakiye
- Kaynak tablo: Gelir Tablosu; Sermaye Yeterliliği
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: RAV yalnız kredi riski (bkz. rav notu).

### Net Faiz (Kar Payı) Geliri / Ortalama RAV  
`net_faiz_ort_rav` · birim: % · tip: rasyo · akim
- **Formül:** TTM Net Faiz Geliri / Ortalama RAV
- Tanım: Risk ağırlıklı varlık başına net faiz geliri.
- Zaman yöntemi: Pay: son 12 ay (TTM) · Payda: 12 aylık ortalama bakiye
- Kaynak tablo: Gelir Tablosu; Sermaye Yeterliliği
- Durum: Ham veriden hesaplanıyor

### Faiz (Kar Payı) Getirili Aktiflerin Getirisi  
`faiz_getirili_aktif_getirisi` · birim: % · tip: rasyo · akim
- **Formül:** TTM Faiz Gelirleri / Ort. Faiz Getirili Aktifler (detaylı)
- Tanım: Getirili aktiflerin ortalama getirisi.
- Zaman yöntemi: Pay: son 12 ay (TTM) · Payda: 12 aylık ortalama bakiye
- Kaynak tablo: Gelir Tablosu; Bilanço; TCMB tablosu
- Durum: Ham veriden hesaplanıyor

### Faiz (Kar Payı) Gideri / Faiz (Kar Payı) Geliri  
`faiz_gideri_faiz_geliri` · birim: % · tip: rasyo · akim
- **Formül:** TTM Faiz Giderleri / TTM Faiz Gelirleri
- Tanım: Faiz gelirinin ne kadarının faiz giderine gittiği.
- Zaman yöntemi: Pay ve payda: son 12 ay (TTM)
- Kaynak tablo: Gelir Tablosu
- Durum: Ham veriden hesaplanıyor

### Faaliyet Giderleri / Ortalama Aktifler  
`faaliyet_gid_ort_aktif` · birim: % · tip: rasyo · akim
- **Formül:** TTM Diğer Faaliyet Giderleri / Ortalama Toplam Aktifler
- Tanım: Operasyonel verimlilik: aktif başına faaliyet gideri.
- Zaman yöntemi: Pay: son 12 ay (TTM) · Payda: 12 aylık ortalama bakiye
- Kaynak tablo: Gelir Tablosu; Bilanço
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Personel giderleri dahil değil.

### Faiz (Kar Payı) Maliyetli Pasiflerin Maliyeti  
`faiz_maliyetli_pasif_maliyeti` · birim: % · tip: rasyo · akim
- **Formül:** TTM Faiz Giderleri / Ortalama Maliyetli Pasif (basit, 5 bileşen)
- Tanım: Maliyetli pasiflerin ortalama maliyeti.
- Zaman yöntemi: Pay: son 12 ay (TTM) · Payda: 12 aylık ortalama bakiye
- Kaynak tablo: Gelir Tablosu; Bilanço
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Spread hesabında 9 bileşenli detaylı payda kullanılır; bu ölçüde değil.

### Net Faiz (Kar Payı) Marjı (NIM)  
`nim` · birim: % · tip: rasyo · akim
- **Formül:** TTM Net Faiz Geliri / Ortalama Toplam Aktifler
- Tanım: Net faiz marjı.
- Zaman yöntemi: Pay: son 12 ay (TTM) · Payda: 12 aylık ortalama bakiye
- Kaynak tablo: Gelir Tablosu; Bilanço
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Payda toplam aktif (getirili aktif değil).

### Düzeltilmiş Net Faiz (Kar Payı) Marjı (NIM)  
`nim_duzeltilmis` · birim: % · tip: rasyo · akim
- **Formül:** TTM Düzeltilmiş Net Faiz Geliri / Ort. Faiz Getirili Aktifler (detaylı)
- Tanım: Ticari kâr/zarar etkisiyle düzeltilmiş net faiz marjı.
- Zaman yöntemi: Pay: son 12 ay (TTM) · Payda: 12 aylık ortalama bakiye
- Kaynak tablo: Gelir Tablosu; Bilanço; TCMB tablosu
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Payda NIM'den farklı (getirili aktif).

### BZK Sonrası Düzeltilmiş Net Faiz (Kar Payı) Marjı (NIM)  
`nim_bzk_sonrasi` · birim: % · tip: rasyo · akim
- **Formül:** TTM (Düzeltilmiş Net Faiz Geliri − Karşılık Giderleri) / Ort. Faiz Getirili Aktifler (detaylı)
- Tanım: Karşılık giderleri sonrası düzeltilmiş net faiz marjı.
- Zaman yöntemi: Pay: son 12 ay (TTM) · Payda: 12 aylık ortalama bakiye
- Kaynak tablo: Gelir Tablosu; Bilanço; TCMB tablosu
- Durum: Ham veriden hesaplanıyor

### Gayrinakdi Kredi Komisyonları / Gayrinakdi Krediler  
`gayrinakdi_komisyon_gayrinakdi` · birim: % · tip: rasyo · akim
- **Formül:** TTM G.Nakdi Kredilerden Alınan Komisyon / Gayrinakdi Krediler (dönem sonu)
- Tanım: Gayrinakdi kredilerin komisyon getirisi.
- Zaman yöntemi: Pay: son 12 ay (TTM) · Payda: dönem sonu bakiye
- Kaynak tablo: Gelir Tablosu; Nazım Hesaplar
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Payda ortalama değil, dönem sonu.

### Komisyon Giderleri / Komisyon Gelirleri  
`komisyon_gid_gel` · birim: % · tip: rasyo · akim
- **Formül:** TTM Verilen Ücret ve Komisyonlar / TTM Alınan Ücret ve Komisyonlar
- Tanım: Komisyon gelirinin ne kadarının komisyon giderine gittiği.
- Zaman yöntemi: Pay ve payda: son 12 ay (TTM)
- Kaynak tablo: Gelir Tablosu
- Durum: Ham veriden hesaplanıyor

### Net Ücret ve Komisyonlar / Ortalama Aktifler  
`net_ucret_ort_aktif` · birim: % · tip: rasyo · akim
- **Formül:** TTM Net Ücret ve Komisyonlar / Ortalama Toplam Aktifler
- Tanım: Aktif başına net ücret-komisyon geliri.
- Zaman yöntemi: Pay: son 12 ay (TTM) · Payda: 12 aylık ortalama bakiye
- Kaynak tablo: Gelir Tablosu; Bilanço
- Durum: Ham veriden hesaplanıyor

### Net Ücret ve Komisyonlar / Operasyonel Giderler  
`net_ucret_operasyonel` · birim: % · tip: rasyo · akim
- **Formül:** TTM Net Ücret ve Komisyonlar / TTM Diğer Faaliyet Giderleri
- Tanım: Net komisyon gelirinin faaliyet giderlerini karşılama oranı.
- Zaman yöntemi: Pay ve payda: son 12 ay (TTM)
- Kaynak tablo: Gelir Tablosu
- Durum: Ham veriden hesaplanıyor

### Reklam Giderleri / Ortalama Aktifler  
`reklam_ort_aktif` · birim: % · tip: rasyo · akim
- **Formül:** TTM Reklam Giderleri / Ortalama Toplam Aktifler
- Tanım: Aktif başına reklam harcaması.
- Zaman yöntemi: Pay: son 12 ay (TTM) · Payda: 12 aylık ortalama bakiye
- Kaynak tablo: Faaliyet Giderleri dipnotu; Bilanço
- Durum: Ham veriden hesaplanıyor

### Reklam Giderleri / Net Dönem Kar/Zararı  
`reklam_net_kar` · birim: % · tip: rasyo · akim
- **Formül:** TTM Reklam Giderleri / TTM Net Dönem Karı
- Tanım: Reklam giderinin net kâra oranı.
- Zaman yöntemi: Pay ve payda: son 12 ay (TTM)
- Kaynak tablo: Faaliyet Giderleri dipnotu; Gelir Tablosu
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Zarar eden bankada negatif/anlamsız.

### Personel Giderleri / Ortalama Aktifler  
`personel_ort_aktif` · birim: % · tip: rasyo · akim
- **Formül:** TTM Personel Giderleri / Ortalama Toplam Aktifler
- Tanım: Aktif başına personel gideri.
- Zaman yöntemi: Pay: son 12 ay (TTM) · Payda: 12 aylık ortalama bakiye
- Kaynak tablo: Gelir Tablosu; Bilanço
- Durum: Ham veriden hesaplanıyor

### Personel Giderleri / Net Dönem Kar/Zararı  
`personel_net_kar` · birim: % · tip: rasyo · akim
- **Formül:** TTM Personel Giderleri / TTM Net Dönem Karı
- Tanım: Personel giderinin net kâra oranı.
- Zaman yöntemi: Pay ve payda: son 12 ay (TTM)
- Kaynak tablo: Gelir Tablosu
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Zarar eden bankada negatif/anlamsız.

### Maliyet / Gelir Rasyosu  
`maliyet_gelir` · birim: % · tip: rasyo · akim
- **Formül:** (Diğer Faaliyet Giderleri + Personel Giderleri) / Faaliyet Gelirleri-Giderleri Toplamı
- Tanım: Maliyet/gelir (verimlilik) oranı.
- Zaman yöntemi: Pay ve payda: yılbaşından kümülatif (YtD), yıllıklandırılmaz
- Kaynak tablo: Gelir Tablosu
- Durum: Ham veriden hesaplanıyor

### Düzeltilmiş Maliyet / Gelir Rasyosu  
`maliyet_gelir_duzeltilmis` · birim: % · tip: rasyo · akim
- **Formül:** Formül belgelenmemiş — PBI baseline değeri kopyalanıyor
- Tanım: Düzeltilmiş maliyet/gelir oranı (PBI özel).
- Zaman yöntemi: —
- Kaynak tablo: PBI baseline
- Durum: PBI baseline (kopya)
- ⚠ Not: ⚠ Ham veriden hesaplanmıyor; yeni dönemlerde güncellenmeyebilir. DAX tanımı temin edilmeli.

### OPEX Büyümesi (YoY)  
`opex_yoy_buyumesi` · birim: % · tip: rasyo · akim
- **Formül (yalnız kod, metadata yok):**
```python
def m_opex_yoy_buyumesi(ctx, b, t):
    return safe_ratio(*opex_yoy_num_den(ctx, b, t))
```

### Reel OPEX Büyümesi (TÜFE'ye Göre)  
`reel_opex_buyumesi` · birim: % · tip: rasyo · akim
- **Formül (yalnız kod, metadata yok):**
```python
def m_reel_opex_buyumesi(ctx, b, t):
    from .makro import tufe_ytd_yillik
    return reel_buyume(m_opex_yoy_buyumesi(ctx, b, t), tufe_ytd_yillik(t))
```

### Faaliyet Gelirleri Büyümesi (YoY)  
`gelir_yoy_buyumesi` · birim: % · tip: rasyo · akim
- **Formül (yalnız kod, metadata yok):**
```python
def m_gelir_yoy_buyumesi(ctx, b, t):
    return safe_ratio(*gelir_yoy_num_den(ctx, b, t))
```

### Makas: Gelir Büyümesi − OPEX Büyümesi (puan)  
`opex_gelir_makasi` · birim: % · tip: rasyo · akim
- **Formül (yalnız kod, metadata yok):**
```python
def m_opex_gelir_makasi(ctx, b, t):
    """Makas (puan) = Faaliyet gelirleri büyümesi − OPEX büyümesi (YoY, YtD). Pozitif =
    gelir giderden hızlı büyüyor (operasyonel kaldıraç); negatif = gider gelirin önünde."""
    g, o = m_gelir_yoy_buyumesi(ctx, b, t), m_opex_yoy_buyumesi(ctx, b, t)
    return None if g is None or o is None else g - o
```

### Kredi Riski Maliyeti (Cost of Risk)  
`cost_of_risk` · birim: % · tip: rasyo · akim
- **Formül:** TTM Karşılık Giderleri / Ortalama Krediler (net)
- Tanım: Kredi riski maliyeti.
- Zaman yöntemi: Pay: son 12 ay (TTM) · Payda: 12 aylık ortalama bakiye
- Kaynak tablo: Gelir Tablosu; Bilanço
- Durum: Ham veriden hesaplanıyor

### Kredi Mevduat Spread'i  
`kredi_mevduat_spread` · birim: % · tip: rasyo · akim
- **Formül:** Kredilerin Paçal Getirisi − (TTM Mevduata Verilen Faizler / Ortalama Mevduat)
- Tanım: Kredi getirisi ile mevduat maliyeti arasındaki fark.
- Zaman yöntemi: İki yıllıklandırılmış oranın farkı (TTM / ortalama bakiye)
- Kaynak tablo: Gelir Tablosu; Bilanço
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Puan cinsinden fark.

### Spread  
`spread` · birim: % · tip: rasyo · akim
- **Formül:** Faiz Getirili Aktiflerin Getirisi − (TTM Faiz Giderleri / Ort. Faiz Maliyetli Pasifler (detaylı))
- Tanım: Getirili aktif getirisi ile maliyetli pasif maliyeti farkı.
- Zaman yöntemi: İki yıllıklandırılmış oranın farkı (TTM / ortalama bakiye)
- Kaynak tablo: Gelir Tablosu; Bilanço; TCMB tablosu
- Durum: Ham veri — en iyi tahmin
- ⚠ Not: ⚠ En iyi tahmin; PBI ile ±0,5 puan içinde uyum %78.

### TP Kredi Mevduat Spread'i  
`tp_spread` · birim: % · tip: rasyo · akim
- **Formül:** Henüz hesaplanmıyor
- Tanım: TL kredi-mevduat spread'i.
- Zaman yöntemi: —
- Kaynak tablo: —
- Durum: Hesaplanmıyor (placeholder)
- ⚠ Not: ⚠ Placeholder: değer boş döner.

### YP Kredi Mevduat Spread'i  
`yp_spread` · birim: % · tip: rasyo · akim
- **Formül:** Henüz hesaplanmıyor
- Tanım: YP kredi-mevduat spread'i.
- Zaman yöntemi: —
- Kaynak tablo: —
- Durum: Hesaplanmıyor (placeholder)
- ⚠ Not: ⚠ Placeholder: değer boş döner.

### TP Getirili Aktif – Maliyetli Pasif Spread'i  
`tp_getirili_maliyetli_spread` · birim: % · tip: rasyo · akim
- **Formül (yalnız kod, metadata yok):**
```python
def m_tp_getirili_maliyetli_spread(ctx, b, t): return _getirili_maliyetli_spread_pb(ctx, b, t, 'TP')
```

### YP Getirili Aktif – Maliyetli Pasif Spread'i  
`yp_getirili_maliyetli_spread` · birim: % · tip: rasyo · akim
- **Formül (yalnız kod, metadata yok):**
```python
def m_yp_getirili_maliyetli_spread(ctx, b, t): return _getirili_maliyetli_spread_pb(ctx, b, t, 'YP')
```

### Kredilerin Paçal Getirisi  
`kredi_pacal_getiri` · birim: % · tip: rasyo · akim
- **Formül:** TTM Kredilerden Alınan Faizler / Ortalama Krediler (net)
- Tanım: Kredilerin ortalama getirisi.
- Zaman yöntemi: Pay: son 12 ay (TTM) · Payda: 12 aylık ortalama bakiye
- Kaynak tablo: Gelir Tablosu; Bilanço
- Durum: Ham veriden hesaplanıyor

### Kaynağın Paçal Maliyeti  
`kaynak_pacal_maliyet` · birim: % · tip: rasyo · akim
- **Formül:** = Faiz Maliyetli Pasiflerin Maliyeti
- Tanım: Kaynakların ortalama maliyeti.
- Zaman yöntemi: Pay: son 12 ay (TTM) · Payda: 12 aylık ortalama bakiye
- Kaynak tablo: Gelir Tablosu; Bilanço
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: faiz_maliyetli_pasif_maliyeti ile birebir aynı değer.


## Şube & Personel (11 ölçü)

### Şube Sayısı  
`sube_sayisi` · birim: adet · tip: buyukluk · stok
- **Formül:** Şube Sayısı
- Tanım: Yurt içi + yurt dışı şube sayısı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Şube & Personel (faaliyet raporu bilgisi)
- Durum: Ham veriden hesaplanıyor

### Şube Başına Krediler  
`sube_basina_krediler` · birim: bin_TL · tip: rasyo · stok
- **Formül:** Krediler (net) / Şube Sayısı / 1000
- Tanım: Şube başına kredi hacmi.
- Zaman yöntemi: Dönem sonu bakiye / dönem sonu adet
- Kaynak tablo: Bilanço; Şube & Personel
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Şubesiz bankalar (Enpara, TOM Bank, Hayat Finans) listede gösterilmez.

### Şube Başına Mevduat  
`sube_basina_mevduat` · birim: bin_TL · tip: rasyo · stok
- **Formül:** Mevduat / Şube Sayısı / 1000
- Tanım: Şube başına mevduat hacmi.
- Zaman yöntemi: Dönem sonu bakiye / dönem sonu adet
- Kaynak tablo: Bilanço; Şube & Personel
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Şubesiz bankalar gösterilmez.

### Şube Başına Net Kar  
`sube_basina_net_kar` · birim: bin_TL · tip: rasyo · akim
- **Formül:** TTM Net Dönem Karı / Şube Sayısı / 1000
- Tanım: Şube başına yıllık net kâr.
- Zaman yöntemi: Pay: son 12 ay (TTM) · Payda: dönem sonu adet
- Kaynak tablo: Gelir Tablosu; Şube & Personel
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Şubesiz bankalar gösterilmez.

### Personel Sayısı  
`personel_sayisi` · birim: adet · tip: buyukluk · stok
- **Formül:** Personel Sayısı
- Tanım: Toplam personel sayısı.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Şube & Personel
- Durum: Ham veriden hesaplanıyor

### Şube Başına Personel  
`sube_basina_personel` · birim: adet · tip: rasyo · stok
- **Formül:** Personel Sayısı / Şube Sayısı
- Tanım: Şube başına çalışan.
- Zaman yöntemi: Dönem sonu bakiye
- Kaynak tablo: Şube & Personel
- Durum: Ham veriden hesaplanıyor
- ⚠ Not: Şubesiz bankalar gösterilmez.

### Personel Başına Krediler  
`personel_basina_krediler` · birim: bin_TL · tip: rasyo · stok
- **Formül:** Krediler (net) / Personel Sayısı / 1000
- Tanım: Çalışan başına kredi hacmi.
- Zaman yöntemi: Dönem sonu bakiye / dönem sonu adet
- Kaynak tablo: Bilanço; Şube & Personel
- Durum: Ham veriden hesaplanıyor

### Personel Başına Mevduat  
`personel_basina_mevduat` · birim: bin_TL · tip: rasyo · stok
- **Formül:** Mevduat / Personel Sayısı / 1000
- Tanım: Çalışan başına mevduat hacmi.
- Zaman yöntemi: Dönem sonu bakiye / dönem sonu adet
- Kaynak tablo: Bilanço; Şube & Personel
- Durum: Ham veriden hesaplanıyor

### Personel Başına Net Kar  
`personel_basina_net_kar` · birim: bin_TL · tip: rasyo · akim
- **Formül:** TTM Net Dönem Karı / Personel Sayısı / 1000
- Tanım: Çalışan başına yıllık net kâr.
- Zaman yöntemi: Pay: son 12 ay (TTM) · Payda: dönem sonu adet
- Kaynak tablo: Gelir Tablosu; Şube & Personel
- Durum: Ham veriden hesaplanıyor

### Personel Başına Personel Gideri  
`personel_basina_personel_gideri` · birim: bin_TL · tip: rasyo · akim
- **Formül:** TTM Personel Giderleri / Personel Sayısı / 1000
- Tanım: Çalışan başına yıllık personel gideri.
- Zaman yöntemi: Pay: son 12 ay (TTM) · Payda: dönem sonu adet
- Kaynak tablo: Gelir Tablosu; Şube & Personel
- Durum: Ham veriden hesaplanıyor

### İnsan Sermayesi Yatırım Getirisi  
`insan_sermayesi_yatirim_getirisi` · birim: kat · tip: rasyo · akim
- **Formül (yalnız kod, metadata yok):**
```python
def m_insan_sermayesi_yatirim_getirisi(ctx, b, t):
    """İnsan Sermayesi Yatırım Getirisi = Dönem Net Kârı / Personel Giderleri ('kat').

    1 TL personel giderine karşılık kaç TL net kâr: 1,2 = 1,2 katı. Yüzdeye
    ÇEVRİLMEZ (scale=1). Pay ve payda yılbaşından kümülatif (YtD) — kardeş ölçü
    personel_net_kar'ın (Personel Giderleri / Net Dönem Kârı) tersi; yıllıklandırılmaz."""
    return safe_ratio(ctx.gelir(b, t, 'Net Dönem Karı / Zararı'),
                      ctx.gelir(b, t, 'Personel Giderleri (-)'), scale=1.0)
```


## Rekabet Analizi ölçüleri (39 ölçü; 2026-11-04'ten beri asıl kategorilerinde, `rekabet: true`)

> "alt kategori" satırları eski Rekabet Analizi gruplamasını gösterir; seçicide ölçü Bilanço/Gelir Tablosu/Şube & Personel altındadır.

### Zorunlu Karşılıklardan Alınan Faiz (Kar Payı) Gelirleri  
`zorunlu_karsilik_geliri` · birim: TL · tip: buyukluk · akim · alt kategori: Zorunlu Karşılık ve Marj
- **Formül (yalnız kod, metadata yok):**
```python
def m_zorunlu_karsilik_geliri(ctx, b, t):
    return _zk_geliri(ctx, b, t)
```

### Zorunlu Karşılık Gelirleri / Faiz (Kar Payı) Gelirleri  
`zk_faiz_gelirleri_orani` · birim: % · tip: rasyo · akim · alt kategori: Zorunlu Karşılık ve Marj
- **Formül (yalnız kod, metadata yok):**
```python
mid: (lambda fn, sc: (lambda ctx, b, t: safe_ratio(*fn(ctx, b, t), scale=sc)))(fn, RATIO_SCALE.get(mid, 100.0))
```

### Ortalama TCMB Hesabı / Ortalama Faiz (Kar Payı) Getirili Aktifler  
`tcmb_hesabi_getirili_aktif` · birim: % · tip: rasyo · stok · alt kategori: Zorunlu Karşılık ve Marj
- **Formül (yalnız kod, metadata yok):**
```python
mid: (lambda fn, sc: (lambda ctx, b, t: safe_ratio(*fn(ctx, b, t), scale=sc)))(fn, RATIO_SCALE.get(mid, 100.0))
```

### Örtük TCMB Getirisi (ZK Geliri / Ortalama TCMB Hesabı)  
`ortuk_tcmb_getirisi` · birim: % · tip: rasyo · akim · alt kategori: Zorunlu Karşılık ve Marj
- **Formül (yalnız kod, metadata yok):**
```python
mid: (lambda fn, sc: (lambda ctx, b, t: safe_ratio(*fn(ctx, b, t), scale=sc)))(fn, RATIO_SCALE.get(mid, 100.0))
```

### ZK Hariç Faiz (Kar Payı) Getirili Aktif Getirisi  
`zk_haric_getirili_aktif_getirisi` · birim: % · tip: rasyo · akim · alt kategori: Zorunlu Karşılık ve Marj
- **Formül (yalnız kod, metadata yok):**
```python
mid: (lambda fn, sc: (lambda ctx, b, t: safe_ratio(*fn(ctx, b, t), scale=sc)))(fn, RATIO_SCALE.get(mid, 100.0))
```

### Zorunlu Karşılık Sürüklemesi (puan)  
`zk_surukleme` · birim: % · tip: rasyo · akim · alt kategori: Zorunlu Karşılık ve Marj
- **Formül (yalnız kod, metadata yok):**
```python
def m_zk_surukleme(ctx, b, t):
    """Sürükleme (puan) = ZK hariç getiri − getiri'nin negatifi ters: getiri − ZK hariç getiri (≤ 0 beklenir).
    Doküman: −(getiri_zk − getiri) × 10.000 bps; burada yüzde puan (−2,46 = −246 bps)."""
    g = _bir(nd_getiri)(ctx, b, t)
    gz = _bir(nd_zk_haric_getiri)(ctx, b, t)
    return None if g is None or gz is None else g - gz
```

### Net Faiz (Kar Payı) Marjı (Getirili Aktif Bazlı)  
`nim_getirili_aktif` · birim: % · tip: rasyo · akim · alt kategori: Zorunlu Karşılık ve Marj
- **Formül (yalnız kod, metadata yok):**
```python
mid: (lambda fn, sc: (lambda ctx, b, t: safe_ratio(*fn(ctx, b, t), scale=sc)))(fn, RATIO_SCALE.get(mid, 100.0))
```

### Swap Düzeltilmiş Net Faiz (Kar Payı) Marjı (Getirili Aktif Bazlı)  
`nim_swap_duzeltilmis` · birim: % · tip: rasyo · akim · alt kategori: Zorunlu Karşılık ve Marj
- **Formül (yalnız kod, metadata yok):**
```python
mid: (lambda fn, sc: (lambda ctx, b, t: safe_ratio(*fn(ctx, b, t), scale=sc)))(fn, RATIO_SCALE.get(mid, 100.0))
```

### Donuk Alacak Tahsilatı / İntikali  
`donuk_tahsilat_intikal` · birim: % · tip: rasyo · akim · alt kategori: Donuk Alacak ve Karşılıklar
- **Formül (yalnız kod, metadata yok):**
```python
mid: (lambda fn, sc: (lambda ctx, b, t: safe_ratio(*fn(ctx, b, t), scale=sc)))(fn, RATIO_SCALE.get(mid, 100.0))
```

### Donuk Alacak Portföy Temizliği ((Terkin + Satış) / Dönem Başı Donuk)  
`donuk_portfoy_temizligi` · birim: % · tip: rasyo · akim · alt kategori: Donuk Alacak ve Karşılıklar
- **Formül (yalnız kod, metadata yok):**
```python
mid: (lambda fn, sc: (lambda ctx, b, t: safe_ratio(*fn(ctx, b, t), scale=sc)))(fn, RATIO_SCALE.get(mid, 100.0))
```

### Donuk Alacak Net Oluşumu (İntikal − Tahsilat)  
`donuk_net_olusum` · birim: TL · tip: buyukluk · akim · alt kategori: Donuk Alacak ve Karşılıklar
- **Formül (yalnız kod, metadata yok):**
```python
def m_donuk_net_olusum(ctx, b, t):
    return _intikal(ctx, b, t) - _tahsilat(ctx, b, t)
```

### NPL 3. Aşama Karşılama Oranı  
`npl_3_asama_karsilama` · birim: % · tip: rasyo · stok · alt kategori: Donuk Alacak ve Karşılıklar
- **Formül (yalnız kod, metadata yok):**
```python
mid: (lambda fn, sc: (lambda ctx, b, t: safe_ratio(*fn(ctx, b, t), scale=sc)))(fn, RATIO_SCALE.get(mid, 100.0))
```

### Grup 2 Krediler 2. Aşama Karşılama Oranı  
`grup_2_karsilama` · birim: % · tip: rasyo · stok · alt kategori: Donuk Alacak ve Karşılıklar
- **Formül (yalnız kod, metadata yok):**
```python
mid: (lambda fn, sc: (lambda ctx, b, t: safe_ratio(*fn(ctx, b, t), scale=sc)))(fn, RATIO_SCALE.get(mid, 100.0))
```

### Faaliyet Gelirleri  
`faaliyet_gelirleri` · birim: TL · tip: buyukluk · akim · alt kategori: Gider ve Verimlilik
- **Formül (yalnız kod, metadata yok):**
```python
def m_faaliyet_gelirleri(ctx, b, t):
    return _gelir_toplami(ctx, b, t)
```

### Net Ücret ve Komisyonlar / Faaliyet Gelirleri  
`net_ucret_faaliyet_gelirleri` · birim: % · tip: rasyo · akim · alt kategori: Gider ve Verimlilik
- **Formül (yalnız kod, metadata yok):**
```python
mid: (lambda fn, sc: (lambda ctx, b, t: safe_ratio(*fn(ctx, b, t), scale=sc)))(fn, RATIO_SCALE.get(mid, 100.0))
```

### Personel Başına OPEX  
`personel_basina_opex` · birim: bin_TL · tip: rasyo · akim · alt kategori: Gider ve Verimlilik
- **Formül (yalnız kod, metadata yok):**
```python
mid: (lambda fn, sc: (lambda ctx, b, t: safe_ratio(*fn(ctx, b, t), scale=sc)))(fn, RATIO_SCALE.get(mid, 100.0))
```

### Şube Başına OPEX  
`sube_basina_opex` · birim: bin_TL · tip: rasyo · akim · alt kategori: Gider ve Verimlilik
- **Formül (yalnız kod, metadata yok):**
```python
mid: (lambda fn, sc: (lambda ctx, b, t: safe_ratio(*fn(ctx, b, t), scale=sc)))(fn, RATIO_SCALE.get(mid, 100.0))
```

### Personel Sayısı Değişimi (YoY)  
`personel_sayisi_yoy` · birim: % · tip: rasyo · stok · alt kategori: Gider ve Verimlilik
- **Formül (yalnız kod, metadata yok):**
```python
mid: (lambda fn, sc: (lambda ctx, b, t: safe_ratio(*fn(ctx, b, t), scale=sc)))(fn, RATIO_SCALE.get(mid, 100.0))
```

### Personel Başına Personel Gideri Büyümesi (YoY)  
`personel_basina_personel_gideri_yoy` · birim: % · tip: rasyo · akim · alt kategori: Gider ve Verimlilik
- **Formül (yalnız kod, metadata yok):**
```python
def m_personel_basina_personel_gideri_yoy(ctx, b, t):
    return _kisi_basi_yoy(ctx, b, t, lambda c, bb, tt: c.gelir(bb, tt, 'Personel Giderleri (-)'))
```

### Personel Başına OPEX Büyümesi (YoY)  
`personel_basina_opex_yoy` · birim: % · tip: rasyo · akim · alt kategori: Gider ve Verimlilik
- **Formül (yalnız kod, metadata yok):**
```python
def m_personel_basina_opex_yoy(ctx, b, t):
    return _kisi_basi_yoy(ctx, b, t, _opex)
```

### Vergi Öncesi Kar (Sürdürülen Faaliyetler)  
`vergi_oncesi_kar` · birim: TL · tip: buyukluk · akim · alt kategori: Kârlılık Bileşimi
- **Formül (yalnız kod, metadata yok):**
```python
def m_vergi_oncesi_kar(ctx, b, t):
    return _vok(ctx, b, t)
```

### Efektif Vergi Oranı  
`efektif_vergi_orani` · birim: % · tip: rasyo · akim · alt kategori: Kârlılık Bileşimi
- **Formül (yalnız kod, metadata yok):**
```python
mid: (lambda fn, sc: (lambda ctx, b, t: safe_ratio(*fn(ctx, b, t), scale=sc)))(fn, RATIO_SCALE.get(mid, 100.0))
```

### Özkaynak Yöntemi İştirak Kârı / Vergi Öncesi Kar  
`istirak_kari_vergi_oncesi_kar` · birim: % · tip: rasyo · akim · alt kategori: Kârlılık Bileşimi
- **Formül (yalnız kod, metadata yok):**
```python
mid: (lambda fn, sc: (lambda ctx, b, t: safe_ratio(*fn(ctx, b, t), scale=sc)))(fn, RATIO_SCALE.get(mid, 100.0))
```

### Net Dönem Kârı Büyümesi (YoY)  
`net_kar_yoy_buyumesi` · birim: % · tip: rasyo · akim · alt kategori: Kârlılık Bileşimi
- **Formül (yalnız kod, metadata yok):**
```python
mid: (lambda fn, sc: (lambda ctx, b, t: safe_ratio(*fn(ctx, b, t), scale=sc)))(fn, RATIO_SCALE.get(mid, 100.0))
```

### Reel Net Dönem Kârı Büyümesi (TÜFE'ye Göre)  
`reel_net_kar_buyumesi` · birim: % · tip: rasyo · akim · alt kategori: Kârlılık Bileşimi
- **Formül (yalnız kod, metadata yok):**
```python
def m_reel_net_kar_buyumesi(ctx, b, t):
    return _reel(m_net_kar_yoy_buyumesi(ctx, b, t), t)
```

### Türev Finansal İşlemlerden Kar/Zarar  
`turev_kar_zarar` · birim: TL · tip: buyukluk · akim · alt kategori: Kârlılık Bileşimi
- **Formül (yalnız kod, metadata yok):**
```python
def m_turev_kar_zarar(ctx, b, t):
    return _turev_kz(ctx, b, t)
```

### Kambiyo İşlemleri Kâr/Zararı  
`kambiyo_kar_zarar` · birim: TL · tip: buyukluk · akim · alt kategori: Kârlılık Bileşimi
- **Formül (yalnız kod, metadata yok):**
```python
def m_kambiyo_kar_zarar(ctx, b, t):
    return _kambiyo_kz(ctx, b, t)
```

### YP Toplam Fonlama / Toplam Fonlama  
`yp_toplam_fonlama_payi` · birim: % · tip: rasyo · stok · alt kategori: Döviz, Altın ve Fonlama
- **Formül (yalnız kod, metadata yok):**
```python
mid: (lambda fn, sc: (lambda ctx, b, t: safe_ratio(*fn(ctx, b, t), scale=sc)))(fn, RATIO_SCALE.get(mid, 100.0))
```

### Toplam Brüt Krediler / Toplam Fonlama  
`krediler_toplam_fonlama` · birim: % · tip: rasyo · stok · alt kategori: Döviz, Altın ve Fonlama
- **Formül (yalnız kod, metadata yok):**
```python
mid: (lambda fn, sc: (lambda ctx, b, t: safe_ratio(*fn(ctx, b, t), scale=sc)))(fn, RATIO_SCALE.get(mid, 100.0))
```

### Altın Hesapları Vadesiz Payı (Altın Hesapları İçinde)  
`altin_vadesiz_payi` · birim: % · tip: rasyo · stok · alt kategori: Döviz, Altın ve Fonlama
- **Formül (yalnız kod, metadata yok):**
```python
mid: (lambda fn, sc: (lambda ctx, b, t: safe_ratio(*fn(ctx, b, t), scale=sc)))(fn, RATIO_SCALE.get(mid, 100.0))
```

### YP Fonlama Fazlası / Toplam Aktifler  
`yp_fonlama_fazlasi_aktif` · birim: % · tip: rasyo · stok · alt kategori: Döviz, Altın ve Fonlama
- **Formül (yalnız kod, metadata yok):**
```python
mid: (lambda fn, sc: (lambda ctx, b, t: safe_ratio(*fn(ctx, b, t), scale=sc)))(fn, RATIO_SCALE.get(mid, 100.0))
```

### RAV Yoğunluğu (Toplam RAV / Toplam Aktifler)  
`rav_yogunlugu` · birim: % · tip: rasyo · stok · alt kategori: Sermaye ve Likidite
- **Formül (yalnız kod, metadata yok):**
```python
mid: (lambda fn, sc: (lambda ctx, b, t: safe_ratio(*fn(ctx, b, t), scale=sc)))(fn, RATIO_SCALE.get(mid, 100.0))
```

### Basit Kaldıraç (Özkaynaklar / Toplam Aktifler)  
`basit_kaldirac` · birim: % · tip: rasyo · stok · alt kategori: Sermaye ve Likidite
- **Formül (yalnız kod, metadata yok):**
```python
mid: (lambda fn, sc: (lambda ctx, b, t: safe_ratio(*fn(ctx, b, t), scale=sc)))(fn, RATIO_SCALE.get(mid, 100.0))
```

### Basel III Kaldıraç Oranı  
`basel_kaldirac_orani` · birim: % · tip: rasyo · stok · alt kategori: Sermaye ve Likidite
- **Formül (yalnız kod, metadata yok):**
```python
return lambda ctx, b, t: manuel_veri.deger(mid, b, t)
```

### Likidite Karşılama Oranı (LCR)  
`lcr` · birim: % · tip: rasyo · stok · alt kategori: Sermaye ve Likidite
- **Formül (yalnız kod, metadata yok):**
```python
return lambda ctx, b, t: manuel_veri.deger(mid, b, t)
```

### Likidite Karşılama Oranı (LCR, YP)  
`lcr_yp` · birim: % · tip: rasyo · stok · alt kategori: Sermaye ve Likidite
- **Formül (yalnız kod, metadata yok):**
```python
return lambda ctx, b, t: manuel_veri.deger(mid, b, t)
```

### Serbest Karşılık Bakiyesi  
`serbest_karsilik` · birim: TL · tip: buyukluk · stok · alt kategori: Kâr Tamponu
- **Formül (yalnız kod, metadata yok):**
```python
return lambda ctx, b, t: manuel_veri.deger(mid, b, t)
```

### TÜFEX Tamponu  
`tufex_tamponu` · birim: TL · tip: buyukluk · akim · alt kategori: Kâr Tamponu
- **Formül (yalnız kod, metadata yok):**
```python
return lambda ctx, b, t: manuel_veri.deger(mid, b, t)
```

### Kâr Tamponu (Serbest Karşılık + TÜFEX) / Net Dönem Kârı  
`kar_tamponu_net_kar` · birim: % · tip: rasyo · akim · alt kategori: Kâr Tamponu
- **Formül (yalnız kod, metadata yok):**
```python
mid: (lambda fn, sc: (lambda ctx, b, t: safe_ratio(*fn(ctx, b, t), scale=sc)))(fn, RATIO_SCALE.get(mid, 100.0))
```
