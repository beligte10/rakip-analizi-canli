"""
pipeline.veri_duzeltmeleri
===========================
Ham BDDK verisindeki bilinen tutarsızlıklar için belgelenmiş, tek yerde toplanmış
düzeltmeler. LookupContext veriyi indekslemeden önce uygular — yükleme, yeniden
hesaplama ve izleme yollarının hepsi aynı değeri görür.

Her kayıt `beklenen` (düzeltme öncesi ham değer) taşır: ham dosya ileride
düzeltilirse ya da yeniden yüklenirse kayıt kendiliğinden devre dışı kalır
(değer beklenenle uyuşmuyorsa dokunulmaz).
"""
from __future__ import annotations
from typing import Dict, List

DUZELTMELER: List[Dict] = [
    {
        'banka': 'Halk Bank', 'tarih': '2025-03-31', 'tablo': 'Gelir Tablosu',
        'kalem': 'Net Dönem Karı / Zararı', 'para_birimi': 'Toplam',
        'beklenen': 6_405_000_000.0, 'deger': 7_050_953_000.0,
        'karar': '2026-10-01 (kullanıcı)',
        'neden': (
            "Halk Eylül 2025'te iştirak/bağlı ortaklık muhasebesini TMS 28 özkaynak yöntemine "
            "çevirip geçmiş dönemleri yeniden düzenledi. 31.03.2025 ham dosyasında gelir tablosu "
            "yeniden düzenlenmiş net kârı (6.405 mn), bilanço satırı ve özkaynak ise raporlananı "
            "(7.051 mn; özkaynak 158,2 mlr) taşıyor. Aynı dönemde iki tabanı karıştırmamak ve Power "
            "BI raporuyla uyumlu kalmak için raporlanan net kâr kullanılır (Mart 2026 ROAE %15,40, "
            "çeyreklik değişim +90 bps = PDF). Kaynak: Halk 31.03.2026 BDR, yeniden düzenleme notu."
        ),
    },
    {
        'banka': 'Enpara', 'tarih': '2025-09-30', 'tablo': 'Şube-Personel',
        'kalem': 'Şube Sayısı', 'para_birimi': 'Toplam',
        'beklenen': 1.0, 'deger': 0.0,
        'karar': '2026-10-01 (kullanıcı)',
        'neden': (
            "Enpara şubesiz bir dijital bankadır; diğer tüm dönemlerde şube sayısı 0. "
            "30.09.2025 ham dosyasındaki 1 değeri hatalı olduğundan 0'a çekilir; aksi halde "
            "'şube başına' ölçüler bu tek dönemde (ör. şube başına krediler 141,9 mn) "
            "anlamsız değerler üretir."
        ),
    },
    {
        'banka': 'TEB', 'tarih': '2025-03-31', 'tablo': 'Gelir Tablosu',
        'kalem': 'Verilen Ücret Ve Komisyonlar', 'para_birimi': 'Toplam',
        'beklenen': 3200999999.9999995, 'deger': 3280756000.0,
        'karar': '2026-10-01 (BDR doğrulaması)',
        'neden': ("31.03.2025 BDR'si (teb-solo.pdf, bin TL) kar/zarar tablosuyla karşılaştırıldı: ham dosyada Verilen Ücret ve Komisyonlar 3.201 mn yazılmış (BDR 3.280,8); Net Ücret, Faaliyet Brüt Kârı ve Diğer Faaliyet Giderleri bu hatadan etkilenmiş. Power BI raporu BDR değerlerini gösterir."),
    },
    {
        'banka': 'TEB', 'tarih': '2025-03-31', 'tablo': 'Gelir Tablosu',
        'kalem': 'Net Ücret Ve Komisyon Gelirleri/Giderleri', 'para_birimi': 'Toplam',
        'beklenen': 3427000000.0, 'deger': 3347353000.0,
        'karar': '2026-10-01 (BDR doğrulaması)',
        'neden': ("31.03.2025 BDR'si (teb-solo.pdf, bin TL) kar/zarar tablosuyla karşılaştırıldı: ham dosyada Verilen Ücret ve Komisyonlar 3.201 mn yazılmış (BDR 3.280,8); Net Ücret, Faaliyet Brüt Kârı ve Diğer Faaliyet Giderleri bu hatadan etkilenmiş. Power BI raporu BDR değerlerini gösterir."),
    },
    {
        'banka': 'TEB', 'tarih': '2025-03-31', 'tablo': 'Gelir Tablosu',
        'kalem': 'Faaliyet Gelirleri/Giderleri Toplamı', 'para_birimi': 'Toplam',
        'beklenen': 13287000000.000002, 'deger': 13207384000.0,
        'karar': '2026-10-01 (BDR doğrulaması)',
        'neden': ("31.03.2025 BDR'si (teb-solo.pdf, bin TL) kar/zarar tablosuyla karşılaştırıldı: ham dosyada Verilen Ücret ve Komisyonlar 3.201 mn yazılmış (BDR 3.280,8); Net Ücret, Faaliyet Brüt Kârı ve Diğer Faaliyet Giderleri bu hatadan etkilenmiş. Power BI raporu BDR değerlerini gösterir."),
    },
    {
        'banka': 'TEB', 'tarih': '2025-03-31', 'tablo': 'Gelir Tablosu',
        'kalem': 'Diğer Faaliyet Giderleri (-)', 'para_birimi': 'Toplam',
        'beklenen': 3990000000.0000005, 'deger': 3908977000.0,
        'karar': '2026-10-01 (BDR doğrulaması)',
        'neden': ("31.03.2025 BDR'si (teb-solo.pdf, bin TL) kar/zarar tablosuyla karşılaştırıldı: ham dosyada Verilen Ücret ve Komisyonlar 3.201 mn yazılmış (BDR 3.280,8); Net Ücret, Faaliyet Brüt Kârı ve Diğer Faaliyet Giderleri bu hatadan etkilenmiş. Power BI raporu BDR değerlerini gösterir."),
    },
    {
        'banka': 'TEB', 'tarih': '2024-06-30', 'tablo': 'Gelir Tablosu',
        'kalem': 'Alınan Ücret Ve Komisyonlar', 'para_birimi': 'Toplam',
        'beklenen': 8387936000.0, 'deger': 8398325000.0,
        'karar': '2026-10-01 (BDR doğrulaması)',
        'neden': ("30.06.2024 BDR'si (teb-solo-3.pdf, bin TL) kar/zarar tablosuyla karşılaştırıldı: ham dosyada Alınan Ücret ve Komisyonlar, Net Ücret, Faaliyet Brüt Kârı ve Personel Giderleri BDR'den tam 10,389 mn düşük. Power BI raporu BDR değerlerini gösterir."),
    },
    {
        'banka': 'TEB', 'tarih': '2024-06-30', 'tablo': 'Gelir Tablosu',
        'kalem': 'Net Ücret Ve Komisyon Gelirleri/Giderleri', 'para_birimi': 'Toplam',
        'beklenen': 4096506000.0, 'deger': 4106895000.0,
        'karar': '2026-10-01 (BDR doğrulaması)',
        'neden': ("30.06.2024 BDR'si (teb-solo-3.pdf, bin TL) kar/zarar tablosuyla karşılaştırıldı: ham dosyada Alınan Ücret ve Komisyonlar, Net Ücret, Faaliyet Brüt Kârı ve Personel Giderleri BDR'den tam 10,389 mn düşük. Power BI raporu BDR değerlerini gösterir."),
    },
    {
        'banka': 'TEB', 'tarih': '2024-06-30', 'tablo': 'Gelir Tablosu',
        'kalem': 'Faaliyet Gelirleri/Giderleri Toplamı', 'para_birimi': 'Toplam',
        'beklenen': 15147639999.999998, 'deger': 15158029000.0,
        'karar': '2026-10-01 (BDR doğrulaması)',
        'neden': ("30.06.2024 BDR'si (teb-solo-3.pdf, bin TL) kar/zarar tablosuyla karşılaştırıldı: ham dosyada Alınan Ücret ve Komisyonlar, Net Ücret, Faaliyet Brüt Kârı ve Personel Giderleri BDR'den tam 10,389 mn düşük. Power BI raporu BDR değerlerini gösterir."),
    },
    {
        'banka': 'TEB', 'tarih': '2024-06-30', 'tablo': 'Gelir Tablosu',
        'kalem': 'Personel Giderleri (-)', 'para_birimi': 'Toplam',
        'beklenen': 5746019000.0, 'deger': 5756408000.0,
        'karar': '2026-10-01 (BDR doğrulaması)',
        'neden': ("30.06.2024 BDR'si (teb-solo-3.pdf, bin TL) kar/zarar tablosuyla karşılaştırıldı: ham dosyada Alınan Ücret ve Komisyonlar, Net Ücret, Faaliyet Brüt Kârı ve Personel Giderleri BDR'den tam 10,389 mn düşük. Power BI raporu BDR değerlerini gösterir."),
    },
    {
        'banka': 'TEB', 'tarih': '2024-09-30', 'tablo': 'Toplam Donuk Alacaklara İlişkin Bilgiler',
        'kalem': 'Donuk Alacaklar (Zarar Niteliğinde, Dönem İçi İntikal)', 'para_birimi': 'Toplam',
        'beklenen': 228196000.0, 'deger': 73115000.0,
        'karar': '2026-10-01 (BDR doğrulaması)',
        'neden': ("2024-09 BDR'si (teb-solo*.pdf / teb-solo.docx) 'Toplam donuk alacak hareketleri' tablosundaki V. Grup 'Dönem İçinde İntikal' 73.115 mn; ham dosyada 228.196 mn (BDR'deki 'Diğer'/'Kur farkı' satırı intikale eklenmiş, tablonun dönem sonu bakiyesi BDR değerini tutmuyor). Power BI raporu BDR değerini gösterir (NPL formasyonu/donuk intikal PDF ile eşleşir)."),
    },
    {
        'banka': 'TEB', 'tarih': '2024-12-31', 'tablo': 'Toplam Donuk Alacaklara İlişkin Bilgiler',
        'kalem': 'Donuk Alacaklar (Zarar Niteliğinde, Dönem İçi İntikal)', 'para_birimi': 'Toplam',
        'beklenen': 347118000.0, 'deger': 117006000.0,
        'karar': '2026-10-01 (BDR doğrulaması)',
        'neden': ("2024-12 BDR'si (teb-solo*.pdf / teb-solo.docx) 'Toplam donuk alacak hareketleri' tablosundaki V. Grup 'Dönem İçinde İntikal' 117.006 mn; ham dosyada 347.118 mn (BDR'deki 'Diğer'/'Kur farkı' satırı intikale eklenmiş, tablonun dönem sonu bakiyesi BDR değerini tutmuyor). Power BI raporu BDR değerini gösterir (NPL formasyonu/donuk intikal PDF ile eşleşir)."),
    },
    {
        'banka': 'TEB', 'tarih': '2025-03-31', 'tablo': 'Toplam Donuk Alacaklara İlişkin Bilgiler',
        'kalem': 'Donuk Alacaklar (Zarar Niteliğinde, Dönem İçi İntikal)', 'para_birimi': 'Toplam',
        'beklenen': 337914000.0, 'deger': 173151000.0,
        'karar': '2026-10-01 (BDR doğrulaması)',
        'neden': ("2025-03 BDR'si (teb-solo*.pdf / teb-solo.docx) 'Toplam donuk alacak hareketleri' tablosundaki V. Grup 'Dönem İçinde İntikal' 173.151 mn; ham dosyada 337.914 mn (BDR'deki 'Diğer'/'Kur farkı' satırı intikale eklenmiş, tablonun dönem sonu bakiyesi BDR değerini tutmuyor). Power BI raporu BDR değerini gösterir (NPL formasyonu/donuk intikal PDF ile eşleşir)."),
    },
    {
        'banka': 'Denizbank', 'tarih': '2024-09-30', 'tablo': 'Toplam Donuk Alacaklara İlişkin Bilgiler',
        'kalem': 'Donuk Alacaklar (Zarar Niteliğinde, Dönem İçi İntikal)', 'para_birimi': 'Toplam',
        'beklenen': 4354716000.0, 'deger': 4053399000.0,
        'karar': '2026-10-01 (BDR doğrulaması)',
        'neden': ("2024-09 BDR'si (denizbank-solo*.pdf) 'Toplam donuk alacak hareketleri' tablosundaki V. Grup 'Dönem İçinde İntikal' 4,053.399 mn; ham dosyada 4,354.716 mn (BDR'deki 'Diğer'/'Kur farkı' satırı intikale eklenmiş, tablonun dönem sonu bakiyesi BDR değerini tutmuyor). Power BI raporu BDR değerini gösterir (NPL formasyonu/donuk intikal PDF ile eşleşir)."),
    },
    {
        'banka': 'Denizbank', 'tarih': '2024-12-31', 'tablo': 'Toplam Donuk Alacaklara İlişkin Bilgiler',
        'kalem': 'Donuk Alacaklar (Zarar Niteliğinde, Dönem İçi İntikal)', 'para_birimi': 'Toplam',
        'beklenen': 6969089000.0, 'deger': 6667772000.0,
        'karar': '2026-10-01 (BDR doğrulaması)',
        'neden': ("2024-12 BDR'si (denizbank-solo*.pdf) 'Toplam donuk alacak hareketleri' tablosundaki V. Grup 'Dönem İçinde İntikal' 6,667.772 mn; ham dosyada 6,969.089 mn (BDR'deki 'Diğer'/'Kur farkı' satırı intikale eklenmiş, tablonun dönem sonu bakiyesi BDR değerini tutmuyor). Power BI raporu BDR değerini gösterir (NPL formasyonu/donuk intikal PDF ile eşleşir)."),
    },
    {
        'banka': 'Denizbank', 'tarih': '2025-12-31', 'tablo': 'Şube-Personel',
        'kalem': 'Şube Sayısı', 'para_birimi': 'Toplam',
        'beklenen': 574.0, 'deger': 576.0,
        'karar': '2026-10-01 (kullanıcı + BDR)',
        'neden': ("Denizbank 30.06.2026 BDR'sinin karşılaştırma sütunu (31.12.2025): şube sayısı 576, personel sayısı 11.972; "
                  "ham dosyada 574 ve 11.910 yazıyordu. Kullanıcı da 31 Aralık personel sayısını 11.972 olarak teyit etti."),
    },
    {
        'banka': 'Denizbank', 'tarih': '2025-12-31', 'tablo': 'Şube-Personel',
        'kalem': 'Personel Sayısı', 'para_birimi': 'Toplam',
        'beklenen': 11910.0, 'deger': 11972.0,
        'karar': '2026-10-01 (kullanıcı + BDR)',
        'neden': ("Denizbank 30.06.2026 BDR'sinin karşılaştırma sütunu (31.12.2025): şube sayısı 576, personel sayısı 11.972; "
                  "ham dosyada 574 ve 11.910 yazıyordu. Kullanıcı da 31 Aralık personel sayısını 11.972 olarak teyit etti."),
    },
    {
        'banka': 'Akbank', 'tarih': '2016-09-30', 'tablo': 'Şube-Personel',
        'kalem': 'Personel Sayısı', 'para_birimi': 'Toplam',
        'beklenen': 13.744, 'deger': 13744.0,
        'karar': '2026-10-21 (veri taraması, kullanıcı onayı)',
        'neden': ("2016-09 ham dosyasında binlik ayracı ondalık okunmuş (13.744 yerine 13,744); komşu çeyreklerle ve diğer bankalarla tutarlı değer ×1000. "
                  "Etkisi: 2017-09 personel YoY'si ≈ +%100.000 görünüyordu."),
    },
    {
        'banka': 'Burgan Bank', 'tarih': '2016-09-30', 'tablo': 'Şube-Personel',
        'kalem': 'Personel Sayısı', 'para_birimi': 'Toplam',
        'beklenen': 1.007, 'deger': 1007.0,
        'karar': '2026-10-21 (veri taraması, kullanıcı onayı)',
        'neden': ("2016-09 ham dosyasında binlik ayracı ondalık okunmuş (1.007 yerine 1,007); komşu çeyreklerle ve diğer bankalarla tutarlı değer ×1000. "
                  "Etkisi: 2017-09 personel YoY'si ≈ +%100.000 görünüyordu."),
    },
    {
        'banka': 'Fibabanka', 'tarih': '2016-09-30', 'tablo': 'Şube-Personel',
        'kalem': 'Personel Sayısı', 'para_birimi': 'Toplam',
        'beklenen': 1.496, 'deger': 1496.0,
        'karar': '2026-10-21 (veri taraması, kullanıcı onayı)',
        'neden': ("2016-09 ham dosyasında binlik ayracı ondalık okunmuş (1.496 yerine 1,496); komşu çeyreklerle ve diğer bankalarla tutarlı değer ×1000. "
                  "Etkisi: 2017-09 personel YoY'si ≈ +%100.000 görünüyordu."),
    },
    {
        'banka': 'Garanti Bankası', 'tarih': '2016-09-30', 'tablo': 'Şube-Personel',
        'kalem': 'Personel Sayısı', 'para_birimi': 'Toplam',
        'beklenen': 19.904, 'deger': 19904.0,
        'karar': '2026-10-21 (veri taraması, kullanıcı onayı)',
        'neden': ("2016-09 ham dosyasında binlik ayracı ondalık okunmuş (19.904 yerine 19,904); komşu çeyreklerle ve diğer bankalarla tutarlı değer ×1000. "
                  "Etkisi: 2017-09 personel YoY'si ≈ +%100.000 görünüyordu."),
    },
    {
        'banka': 'HSBC', 'tarih': '2016-09-30', 'tablo': 'Şube-Personel',
        'kalem': 'Personel Sayısı', 'para_birimi': 'Toplam',
        'beklenen': 3.968, 'deger': 3968.0,
        'karar': '2026-10-21 (veri taraması, kullanıcı onayı)',
        'neden': ("2016-09 ham dosyasında binlik ayracı ondalık okunmuş (3.968 yerine 3,968); komşu çeyreklerle ve diğer bankalarla tutarlı değer ×1000. "
                  "Etkisi: 2017-09 personel YoY'si ≈ +%100.000 görünüyordu."),
    },
    {
        'banka': 'Halk Bank', 'tarih': '2016-09-30', 'tablo': 'Şube-Personel',
        'kalem': 'Personel Sayısı', 'para_birimi': 'Toplam',
        'beklenen': 16.843, 'deger': 16843.0,
        'karar': '2026-10-21 (veri taraması, kullanıcı onayı)',
        'neden': ("2016-09 ham dosyasında binlik ayracı ondalık okunmuş (16.843 yerine 16,843); komşu çeyreklerle ve diğer bankalarla tutarlı değer ×1000. "
                  "Etkisi: 2017-09 personel YoY'si ≈ +%100.000 görünüyordu."),
    },
    {
        'banka': 'Vakıfbank', 'tarih': '2016-09-30', 'tablo': 'Şube-Personel',
        'kalem': 'Personel Sayısı', 'para_birimi': 'Toplam',
        'beklenen': 15.51, 'deger': 15510.0,
        'karar': '2026-10-21 (veri taraması, kullanıcı onayı)',
        'neden': ("2016-09 ham dosyasında binlik ayracı ondalık okunmuş (15.510 yerine 15,510); komşu çeyreklerle ve diğer bankalarla tutarlı değer ×1000. "
                  "Etkisi: 2017-09 personel YoY'si ≈ +%100.000 görünüyordu."),
    },
    {
        'banka': 'Yapı Kredi', 'tarih': '2016-09-30', 'tablo': 'Şube-Personel',
        'kalem': 'Personel Sayısı', 'para_birimi': 'Toplam',
        'beklenen': 18.545, 'deger': 18545.0,
        'karar': '2026-10-21 (veri taraması, kullanıcı onayı)',
        'neden': ("2016-09 ham dosyasında binlik ayracı ondalık okunmuş (18.545 yerine 18,545); komşu çeyreklerle ve diğer bankalarla tutarlı değer ×1000. "
                  "Etkisi: 2017-09 personel YoY'si ≈ +%100.000 görünüyordu."),
    },
    {
        'banka': 'Şekerbank', 'tarih': '2016-09-30', 'tablo': 'Şube-Personel',
        'kalem': 'Personel Sayısı', 'para_birimi': 'Toplam',
        'beklenen': 3.546, 'deger': 3546.0,
        'karar': '2026-10-21 (veri taraması, kullanıcı onayı)',
        'neden': ("2016-09 ham dosyasında binlik ayracı ondalık okunmuş (3.546 yerine 3,546); komşu çeyreklerle ve diğer bankalarla tutarlı değer ×1000. "
                  "Etkisi: 2017-09 personel YoY'si ≈ +%100.000 görünüyordu."),
    },
    {
        'banka': 'Halk Bank', 'tarih': '2025-03-31', 'tablo': 'Şube-Personel',
        'kalem': 'Personel Sayısı', 'para_birimi': 'Toplam',
        'beklenen': 27000.0, 'deger': 22162.0,
        'karar': '2026-10-21 (veri taraması, kullanıcı onayı)',
        'neden': ("Ham dosyada 27.000 (yuvarlak, komşu çeyrekler ≈22.200); Power BI modelinde 22.162. "
                  "Mart YoY'sini (+%21,7 / −%16,4) bozuyordu. 2025-09 (28.000) hâlâ açık: BDR PDF'i bekleniyor."),
    },
]
