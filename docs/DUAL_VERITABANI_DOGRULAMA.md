# Çift Veritabanı Doğrulaması

Tarih: 28 Eylül 2026

Bu kayıt, REQS projesinde PostgreSQL'in ana veritabanı olarak korunduğunu ve 2209-A başvurusunda belirtilen MySQL seçeneğinin ayrı bir uyumluluk profili olarak doğrulandığını gösterir. MySQL, PostgreSQL'in yerini almaz.

| Profil | Adres | Rol | Migration sonucu |
| --- | --- | --- | --- |
| PostgreSQL 16 | `localhost:5432/reqs` | Varsayılan uygulama veritabanı | `20260928_02 (head)` |
| MySQL 8.4 | `localhost:3307/reqs` | Uyumluluk/doğrulama profili | `20260928_02 (head)` |

## Temiz kurulum doğrulaması

MySQL'de ayrıca boş `reqs_migration_check` veritabanı oluşturuldu. Alembic zinciri bu veritabanında sırasıyla aşağıdaki revizyonları başarıyla uyguladı:

1. `20260903_01` — başlangıç REQS şeması
2. `20260905_01` — kalıcı AHP ikili karşılaştırmaları
3. `20260928_02` — önceliklendirme ve izlenebilirlik sorgu indeksleri

Son durum `20260928_02 (head)` olarak doğrulandı. Aynı doğrulama turunda uygulama testleri `24 passed` sonucu verdi.

## Kullanım ilkesi

- Uygulama `DATABASE_URL` verilmediğinde PostgreSQL'e bağlanır.
- MySQL yalnızca `DATABASE_URL=mysql+pymysql://reqs:reqs@localhost:3307/reqs` açıkça verildiğinde seçilir.
- Her iki ortam aynı Alembic migration zincirini kullanır.
