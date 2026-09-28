# REQS Tamamlama Raporu

**İlk kayıt:** 28 Eylül 2026
**Teknik revizyon:** 29 Eylül 2026
**Çalışma:** TÜBİTAK 2209-A REQS prototipinin tamamlanması

## Tamamlanan sistem kapsamı

- Gereksinim kayıtları, benzersiz anahtarlar, durum bilgisi ve PostgreSQL/SQLAlchemy kalıcılığı.
- AHP ikili karşılaştırmaları, Saaty özdeğer öncelik vektörü, tutarlılık oranı ve ortak 0-100 sonuç kaydı.
- Wiegers fayda, ceza, maliyet ve risk ağırlıklandırması ile toplu puanlama ve normalize karşılaştırma.
- Volere kriter ağırlığı ve 0-10 puanlama akışı.
- İlişki CRUD'u, otomatik izlenebilirlik matrisi, ağ görünümü, ileri-geri sorgular ve transitive etki analizi.
- Başlangıç çalışma alanı, puanlama, matris, ağ, etki analizi ve sonuç ekranlarını bağlayan responsive Bootstrap arayüzü.
- Güncel puanları, yöntem özetlerini, SVG grafiği, izlenebilirlik matrisini ve etki listesini içeren Türkçe karakter uyumlu WeasyPrint PDF dışa aktarma.

## Doğrulama

- Otomatik test paketi: **29/29 geçti**; 1 üçüncü taraf kullanım uyarısı, hata yok.
- PDF çıktısı WeasyPrint 66.0 ile 4 A4 sayfa olarak üretildi; başlık, tablolar, grafik, matris, etki listesi ve Türkçe karakterler görsel olarak kontrol edildi.
- Yerel dosya paylaşımındaki test kilidi, uygulama klasörünü bağlamayan ayrı Docker test hizmetiyle giderildi. PDF üretim teknolojisi WeasyPrint olarak korunmuştur.

## Akademik kapsam notu

Uygulama, başvurudaki yöntemlerin işlevsel prototipidir; elde edilen puanlar kullanıcı girdilerine dayalı karar desteği sağlar. Bir yöntemin üstünlüğü veya kullanıcı memnuniyeti hakkında ampirik iddia için ayrı vaka çalışması ve katılımcı değerlendirmesi gerekir.

## GitHub durumu

Değişiklikler yerel Git geçmişine kaydedilecektir. Uzak GitHub deposu tanımlı olmadığı için gönderim yapılamaz; depo adresi sağlandığında seçilen uzak dal gönderilebilir.
