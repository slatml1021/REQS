# REQS — Günlük İlerleme Raporu

**Tarih:** 4 Eylül 2026  
**Sorumlu:** Sıla Temel  
**Planlanan görev:** AHP ikili karşılaştırma ekranı tasarımı

## Tamamlanan işler

1. AHP ikili karşılaştırma ekranı eklendi: `/ahp/comparisons`.
2. Ekran, veritabanındaki iki gereksinimi seçerek karşılaştırmaya hazırlar.
3. Saaty ölçeği için 9, 7, 5, 3, 1 ve ters değerler (1/3, 1/5, 1/7, 1/9) seçilebilir biçimde tasarlandı.
4. En az iki gereksinim bulunmadığında kullanıcıyı yönlendiren boş durum mesajı eklendi.
5. Ekran, responsive Bootstrap bileşenleri ve erişilebilir form etiketleriyle oluşturuldu.

## Doğrulama

- API, model ve AHP ekran testleri: **5/5 geçti**.
- Ekran testi, iki örnek gereksinim oluşturup bunların seçim alanlarında görünmesini doğrular.

## Kapsam notu

Karşılaştırmayı kalıcı olarak kaydetme düğmesi bu aşamada bilinçli olarak pasiftir. 5 Eylül görevinde AHP verisini API katmanına bağlama ve kayıt işlemi eklenecektir.

## GitHub durumu

Değişiklikler yerel Git geçmişine kaydedilecektir. Uzak GitHub deposu tanımlı olmadığı için bu çalışmada dış yükleme yapılamamıştır.
