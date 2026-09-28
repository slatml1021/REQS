# REQS — Gereksinim Önceliklendirme ve İzlenebilirlik Sistemi

TÜBİTAK 2209-A bitirme tezi kapsamında geliştirilen karar destek sistemi.

## Kapsam

- AHP (Saaty özdeğer yöntemi ve tutarlılık oranı), Wiegers ve Volere önceliklendirmesi
- Otomatik izlenebilirlik matrisi, ilişki ağı ve ileri-geri değişiklik etki analizi
- Responsive çalışma alanı, sonuç ekranı ve PDF dışa aktarma

## Çalıştırma

1. PostgreSQL'i başlatın: `docker compose up -d db`
2. Ortam değişkenini ayarlayın: `DATABASE_URL=postgresql+psycopg://reqs:reqs@localhost:5432/reqs`
3. Bağımlılıkları kurun: `python -m pip install -e '.[dev]'`
4. Uygulamayı başlatın: `uvicorn app.main:app --reload`

Varsayılan bağlantı adresi yerel PostgreSQL'dir. Testler, harici bir veritabanına ihtiyaç duymamak için geçici SQLite veritabanı kullanır.

## MySQL uyumluluk profili

2209-A başvurusunda yer alan MySQL seçeneği için ikinci servis de tanımlıdır. PostgreSQL ana geliştirme veritabanı olarak kalır; MySQL aynı migration zincirini doğrulamak için ayrı çalıştırılır.

```bash
docker compose up -d mysql
DATABASE_URL=mysql+pymysql://reqs:reqs@localhost:3307/reqs alembic upgrade head
```

Ayrıntılı akış için [kullanım kılavuzuna](docs/KULLANIM_KILAVUZU.md) bakın.
