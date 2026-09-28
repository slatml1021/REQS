# Test sonuçları

**Tarih:** 29 Eylül 2026
**Kapsam:** REQS uygulaması, örnek vaka ve iki veritabanı uyumluluk profili

## Otomatik test özeti

| Doğrulama | Sonuç | Kanıt |
| --- | --- | --- |
| Birim ve entegrasyon testleri | **29 geçti** | Ayrı Docker test hizmetinde `pytest -q`; 1 üçüncü taraf kullanım uyarısı, hata yok |
| Gereksinim CRUD ve benzersiz anahtar | Geçti | Entegrasyon testleri |
| AHP hesaplama ve tutarsızlık uyarısı | Geçti | AHP kabul ve sınır senaryoları |
| Wiegers hesaplama ve giriş sınırları | Geçti | API testleri |
| Volere kriter, ağırlık ve skor doğrulaması | Geçti | API testleri |
| İlişki ekleme, güncelleme, silme; yönlü/yönsüz matris | Geçti | İlişki ve izlenebilirlik testleri |
| İleri/geri izlenebilirlik ve NetworkX etki analizi | Geçti | Kabul senaryosu |
| 100 gereksinimli matris | Geçti | Kabul senaryosunda 5 saniye sınırı altında |
| PDF üretimi | Geçti | HTTP PDF yanıtı ve `%PDF` imzası |

Testler, kalıcı vaka verisini değiştirmemek için SQLite tabanlı geçici test veritabanında çalışır. Docker test hizmeti ana uygulama hizmetindeki macOS dosya paylaşım kilidinden bağımsızdır.

## Ortam doğrulamaları

| Ortam | Durum |
| --- | --- |
| PostgreSQL 16 | Ana geliştirme profili; Alembic baş sürümü `20260928_03` |
| MySQL 8.4 | Uyumluluk profili; aynı Alembic baş sürümü `20260928_03` |
| Vaka verisi | 10 gereksinim, 10 ilişki, üç yöntemin toplam 30 puan kaydı |
| PDF dosyası | `reports/reqs-vaka-raporu.pdf`, WeasyPrint 66.0, 4 A4 sayfa |

## Kapsam dışı veya insan kanıtı gerektiren sonuçlar

Otomatik test başarısı, kullanılabilirlik veya kullanıcı memnuniyeti kanıtı değildir. [Kullanıcı testi formu](KULLANICI_TESTI_FORMU.md) gerçek katılımcılarla doldurulmadan kullanıcı testi sonucu raporlanmayacaktır. Aynı şekilde, GitHub uzak deposu tanımlı olmadığı için uzak yedekleme, PR ve ekip kod incelemesi bu raporda doğrulanmış değildir.
