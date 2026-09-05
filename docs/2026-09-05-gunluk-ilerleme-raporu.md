# REQS — Günlük İlerleme Raporu

**Tarih:** 5 Eylül 2026  
**Sorumlu:** Sıla Temel  
**Planlanan görev:** AHP ikili karşılaştırma ekranının API ile entegrasyonu

## Tamamlanan işler

1. AHP ikili karşılaştırmaları için kalıcı veri modeli eklendi.
   - Her gereksinim çifti tek kayıt olarak saklanır.
   - Karşılaştırma yönü ters seçilse de değer otomatik tersine çevrilerek yinelenen çift oluşması önlenir.
2. AHP API uçları eklendi.
   - `PUT /api/v1/ahp/comparisons`: karşılaştırma kaydını oluşturur veya günceller.
   - `GET /api/v1/ahp/comparisons`: mevcut karşılaştırmaları listeler.
3. Saaty ölçeğinin tam giriş kümesi desteklendi: 1–9 ve 1/2–1/9.
4. AHP ekranındaki kaydetme düğmesi etkinleştirildi; kullanıcı seçimi API’ye gönderilir ve sonuç ekranda bildirilir.
5. Aynı gereksinimin kendisiyle karşılaştırılması ve eksik gereksinim kimlikleri için koruma eklendi.
6. Alembic migration ile AHP karşılaştırma tablosu PostgreSQL şemasına eklendi.

## Doğrulama

- Model, CRUD, ekran ve AHP kayıt akışı testleri: **7/7 geçti**.
- PostgreSQL migration SQL’i üretildi; `ahp_comparisons` tablosunun oluştuğu doğrulandı.

## Sonraki görev

6 Eylül’de Sıla’nın görevi AHP ekranı/entegrasyon testleri ve karşılıklı kod incelemesidir. AHP hesaplama algoritması Dilara sorumluluğunda olduğundan Sıla tarafında API–arayüz veri akışı, hata durumları ve test senaryoları ele alınacaktır.

## GitHub durumu

Değişiklikler yerel Git geçmişine kaydedilecektir. Uzak GitHub deposu tanımlı olmadığı için bu çalışmada dış yükleme yapılamamıştır.
