# REQS — Günlük İlerleme Raporu

**Tarih:** 2 Eylül 2026  
**Tez sahibi / ana sorumlu:** Sıla Temel  
**Proje:** Yazılım Projelerinde Gereksinim Önceliklendirmesi ve İzlenebilirlik İçin Karar Destek Sistemi (REQS)

## Günlük hedef

30 Ağustos–1 Eylül görevleri daha önce yapılmadığından önce literatür notları, kavramsal çerçeve, örnek gereksinim listesi ve veri taslağı tamamlandı. Ardından 2 Eylül sorumlulukları doğrultusunda PostgreSQL geliştirme ortamı ve SQLAlchemy veri katmanı hazırlandı.

## Tamamlanan işler

1. Başlangıç aşamasının ön literatür sentezi, kavramsal çerçevesi ve örnek gereksinim listesi tamamlandı. Nihai tez kaynakçası yalnızca indirilen/yasal tam metni doğrulanmış yayınlardan oluşturulacaktır.
2. Proje temeli oluşturuldu: Python paket yapısı, paket tanımı ve test çalışma düzeni eklendi.
3. PostgreSQL 16 geliştirme servisi `docker-compose.yml` içinde tanımlandı. Servis; kalıcı veri alanı, sağlık kontrolü ve yerel 5432 portu ile yapılandırıldı.
4. SQLAlchemy 2.0 veri modeli tamamlandı:
   - `Requirement`: benzersiz gereksinim anahtarı, başlık, açıklama, durum ve zaman damgaları.
   - `RequirementRelation`: gereksinimler arası yönlü izlenebilirlik bağlantısı; bağımlılık, ön koşul, ayrıntılandırma ve ilişki türleri.
   - `PriorityScore`: AHP, Wiegers ve Volere sonuçları için ham skor, 0–100 normalize skor ve yönteme özgü giriş verileri.
5. Veri bütünlüğü kuralları eklendi:
   - Aynı gereksinim anahtarı tekrar edemez.
   - Bir gereksinim kendisiyle ilişkilendirilemez.
   - Aynı kaynak–hedef–ilişki türü üçlüsü tekrar edemez.
   - Her gereksinimin her yöntem için yalnızca tek puan kaydı olur.
   - Normalize puan 0–100 aralığında tutulur.
6. Model testleri yazıldı ve başarıyla çalıştırıldı: **2/2 test geçti**.

## Teknik doğrulama

Testler geçici SQLite veritabanında yürütüldü; böylece model ilişkileri ve kısıtlar bağımsız olarak doğrulandı. PostgreSQL için çalışma ortamı hazırdır; yerel Docker hizmeti başlatıldığında aynı şema PostgreSQL üzerinde kullanılacaktır.

## Henüz tamamlanmayan / dış bağımlılıklar

- PostgreSQL konteyneri çalıştırılmadı; cihazda Docker’ın hazır ve çalışır olduğu ayrıca doğrulanmalıdır.
- Alembic migration altyapısı ve CRUD API uçları 3 Eylül görevlerine bırakıldı.
- Uzak GitHub deposu ya da erişim bilgisi çalışma alanında bulunmadığından dış GitHub yüklemesi yapılamadı. Yerel sürüm geçmişi oluşturulacaktır; uzak depo bağlandığında bu kayıtlar güvenle gönderilebilir.

## Sonraki günlük hedef — 3 Eylül

Sıla sorumluluğunda Alembic migration kurulumu ile gereksinim/ilişki/puanlama için temel CRUD uçlarının hazırlanması. Çıktı ölçütü: veritabanına bağlanan ve gereksinim oluşturma, listeleme, güncelleme, silme işlemlerini sunan API katmanı.
