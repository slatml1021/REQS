# REQS — Günlük İlerleme Raporu

**Tarih:** 12 Eylül 2026  
**Sorumlu:** Sıla Temel  
**Planlanan görev:** Volere kriter/puanlama ekranının API ile entegrasyonu

## Tamamlanan işler

1. Volere puanlama API’si eklendi: `PUT /api/v1/volere/scores`.
2. Kriter adları, yüzde ağırlıkları ve 0–10 puanları API tarafından doğrulanıyor.
3. Kriter ağırlıklarının toplamının tam olarak %100 olması zorunlu kılındı.
4. Ağırlıklı toplam ham skor (0–10) ve normalize skor (0–100) hesaplanıyor.
5. Aynı gereksinim için Volere sonucu tekrar gönderildiğinde önceki kayıt güncelleniyor.
6. Volere ekranındaki kaydetme düğmesi API’ye bağlandı; kullanıcı hesaplanan normalize skoru ekranda görüyor.

## Doğrulama

- API ve ekran testleri: **10/10 geçti**.
- Testler, ağırlıklı skor hesaplamasını, güncelleme davranışını ve %100 olmayan ağırlıkların reddedilmesini doğrular.

## Sonraki görev

13 Eylül’de Volere birim testleri ve hata düzeltmeleri ortak yürütülecek. Sıla tarafında Volere ekranı ve API akışı bu testlere hazırdır.

## GitHub durumu

Değişiklikler yerel Git geçmişine kaydedilecektir. Uzak GitHub deposu tanımlı olmadığı için bu çalışmada dış yükleme yapılamamıştır.
