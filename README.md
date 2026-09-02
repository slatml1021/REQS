# REQS — Gereksinim Önceliklendirme ve İzlenebilirlik Sistemi

TÜBİTAK 2209-A bitirme tezi kapsamında geliştirilen karar destek sistemi.

## Bugünkü ilerleme (2 Eylül 2026)

- PostgreSQL için yerel geliştirme ortamı `docker compose` ile tanımlandı.
- SQLAlchemy veri modeli oluşturuldu: gereksinimler, gereksinim ilişkileri ve üç önceliklendirme yönteminin puanları.
- Veri bütünlüğü için benzersiz kimlikler, ilişki türleri ve puan kısıtları eklendi.

## Çalıştırma

1. PostgreSQL'i başlatın: `docker compose up -d db`
2. Ortam değişkenini ayarlayın: `DATABASE_URL=postgresql+psycopg://reqs:reqs@localhost:5432/reqs`
3. Bağımlılıkları kurun: `python -m pip install -e '.[dev]'`

Varsayılan bağlantı adresi yerel PostgreSQL'dir. Testler, harici bir veritabanına ihtiyaç duymamak için geçici SQLite veritabanı kullanır.
