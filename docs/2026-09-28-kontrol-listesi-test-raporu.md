# REQS ana kontrol listesi - test raporu

**Tarih:** 28 Eylül 2026  
**Kapsam:** Sıla Temel için paylaşılan ana kontrol listesi  
**Sonuç:** Çekirdek karar destek API'leri çalışıyor; ancak listeyi eksiksiz tamamlanmış saydırmayacak işlevsel ve akademik açıklar var.

## Çalıştırılan doğrulamalar

| Kontrol | Sonuç |
| --- | --- |
| Tüm pytest paketi | **28 geçti**, 1 üçüncü taraf kullanım uyarısı; başarısız test yok |
| Yeni uçtan uca kabul senaryosu | 5 gereksinimde AHP, Wiegers, Volere, ortak 0-100 sonuçlar, ilişki matrisi, ileri/geri iz, iki yönlü etki, dinamik ilişki silme ve PDF yanıtı geçti |
| AHP tutarsızlık senaryosu | Tutarsız üçlü karşılaştırmada `CR > 0,10` ve uyarı sonucu geçti |
| Girdi sınırları | Volere'de beşinci kriter ve Wiegers'te 1-9 dışı puan reddedildi |
| 100 gereksinimli matris | 100 satır/sütunlu matris başarıyla üretildi; test üst sınırı olan 5 saniyenin altında kaldı |
| PostgreSQL 16 | Sağlıklı; Alembic `20260928_02 (head)` |
| MySQL 8.4 uyumluluk profili | Sağlıklı; Alembic `20260928_02 (head)` |
| Yerel web ve OpenAPI | `http://127.0.0.1:8000/` ve `/openapi.json` HTTP 200 |
| PDF görsel denetimi | A4, Türkçe karakterler, başlık/tarih, öncelik tablosu ve matris okunaklı; geçici test dosyası ve test kayıtları sonradan silindi |

Yeni kabul senaryoları [`tests/test_acceptance_scenario.py`](../tests/test_acceptance_scenario.py) içindedir. Testler kalıcı PostgreSQL/MySQL kayıtlarına dokunmamak için geçici SQLite veritabanında çalışır; iki gerçek veritabanının migration başları ayrıca yukarıda doğrulanmıştır.

## Ana ürün kabul kriterleri

| Kriter | Durum | Kanıt / sınır |
| --- | --- | --- |
| AHP, Wiegers, Volere tek sistemde | Geçti | Üç yöntem aynı kabul senaryosunda çalıştı. |
| Sonuçların ortak 0-100 formatı | Geçti | 15 sonuçta tüm skorlar `0 <= skor <= 100`. |
| Gereksinim CRUD ve benzersiz anahtar | Geçti | Oluşturma, listeleme, ayrıntı, güncelleme, silme ve yinelenen anahtar reddi testli. |
| İlişki oluşturma/listeleme/silme ve bütünlük | Kısmi | Yinelenen ve öz-ilişki reddi, oluşturma/silme çalışıyor. **İlişki güncelleme endpoint'i yok.** |
| Bağımlılık, ön koşul, üst-alt ve benzerlik ilişkileri | Kısmi | `depends_on`, `prerequisite_of`, `refines`, `related_to` mevcut. Açık `conflicts_with`/çelişki türü yok. |
| Dinamik izlenebilirlik matrisi | Geçti | İlişki silindikten sonra hücrenin boşaldığı test edildi. |
| İleri ve geri izlenebilirlik | Geçti | Yön ve hedef/kaynak doğruluğu kabul senaryosunda test edildi. |
| Etki analizi | Kısmi | NetworkX ile doğrudan/dolaylı, ileri/geri etki listeleniyor. Ancak gereksinim `PATCH` işleminden sonra **otomatik** uyarı tetiklenmiyor; kullanıcı analiz ekranından sorgu başlatıyor. |
| AHP, Wiegers, Volere veri giriş ekranları | Kısmi | Üç puanlama ekranı ve API bağlantıları var. Ana çalışma alanındaki **“Gereksinim ekle”** düğmesi formu açmıyor; Bootstrap JavaScript yüklenmediği için tarayıcı testi başarısız. |
| Sıralı sonuç, çubuk ve pasta grafik | Kısmi | Sonuç API'si ve Chart.js bar/doughnut kodu mevcut; boş veriyle canlı ekranda grafik oluşmaz. Dolu canlı veriyle tarayıcı görsel testi henüz yapılmadı. |
| Tablo ve interaktif ağ | Kısmi | Matris endpoint'i ve vis-network entegrasyonu test/kod denetiminden geçti. Dolu canlı veriyle düğüm etkileşimi tarayıcıda henüz doğrulanmadı. |
| PDF raporu | Kısmi | İndirilebilir, okunaklı ve öncelik tablosu/matrisi var. **Grafikler** ve yöntemlerin kısa açıklamaları rapora aktarılmıyor. WeasyPrint yerine 2209-A başvurusunda bulunan ReportLab kullanılıyor. |
| 5-10 gereksinimli vaka | Geçti | Beş gereksinimli uçtan uca senaryo geçti. |
| 100 gereksinimli matris gözlemi | Geçti | 100 gereksinimlik matris başarıyla üretildi. |
| Büyük AHP için gruplama/hiyerarşik AHP | Doğrulanamadı | Böyle bir seçenek ya da değerlendirme kaydı bulunmuyor. |
| Büyük matris filtreleme/modüler görünüm | Doğrulanamadı | Filtreleme/modüler görünüm uygulanmamış. |

## Akademik, ekip ve teslim maddeleri

| Kriter | Durum | Kanıt / sınır |
| --- | --- | --- |
| Tam metin kaynak arşivi | Kısmi | `literature/full_text/` altında **15** açılabilir PDF kayıtlı. |
| 15 Wiegers + 15 Volere / toplam 30 güçlü kaynak | Başarısız | Mevcut arşiv 15 PDF; `ana-makale-listesi.md` yalnızca **6** kaynağın kesin ana makale olduğunu belirtiyor. Yöntem bazında 15'er kaynak ve 30 kaynaklık nihai tarama yok. |
| Her kaynak için yöntem/formül/avantaj/sınırlılık notu | Kısmi | Kaynak kayıt ve başlangıç sentezi var; bütün 15 PDF için ayrı tam analiz notu yok. |
| Kullanıcı testi ve geri bildirim | Yapılmadı | Gerçek katılımcı ve geri bildirim kaydı olmadan bu madde tamamlandı denemez. |
| Test senaryolarında en az %90 başarı | Kısmi | Uygulanan otomatik testlerin tamamı geçti (28/28). Kontrol listesindeki tüm kabul maddeleri geçmediği için proje geneli için %90 kabul iddiası yapılamaz. |
| GitHub, dallanma, PR ve ekip incelemesi | Yapılmadı | Yerel Git kaydı var; uzak GitHub deposu tanımlı değil, bu nedenle ekip erişimi/PR akışı doğrulanamadı. |
| 29-30 Eylül nihai rapor, sunum, danışman onayı | Bekliyor | Test edilmedi; tarihe göre sonraki teslim adımları. |

## Net hüküm

Çekirdek API ve veritabanı altyapısı testten geçti; PostgreSQL ana veritabanı, MySQL ise aynı şema için doğrulanmış uyumluluk profili olarak çalışıyor. Buna karşılık proje **henüz kontrol listesinin tamamını karşılamıyor**. Öncelik sırasıyla düzeltilmesi gerekenler:

1. Ana ekrandaki gereksinim ekleme akışını çalışır hale getirmek ve ilişki güncelleme işlevini eklemek.
2. Değişiklik sonrasında otomatik etki uyarısını, ilişki türü eksiklerini ve canlı ağ/grafik görsel testlerini tamamlamak.
3. PDF'e yöntem özeti ve grafikler eklemek; uzun veri seti sayfa düzenini yeniden denetlemek.
4. 30 doğrulanmış, yöntemle ilişkili tam metin kaynağa ulaşmak ve kullanıcı testi/geri bildirimini gerçek katılımcılarla kaydetmek.
