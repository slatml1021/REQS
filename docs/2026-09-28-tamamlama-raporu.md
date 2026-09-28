# REQS Tamamlama Raporu

**Tarih:** 28 Eylül 2026  
**Çalışma:** TÜBİTAK 2209-A REQS prototipinin tamamlanması

## Tamamlanan sistem kapsamı

- Gereksinim kayıtları, benzersiz anahtarlar, durum bilgisi ve MySQL/SQLAlchemy kalıcılığı.
- AHP ikili karşılaştırmaları, Saaty özdeğer öncelik vektörü, tutarlılık oranı ve ortak 0-100 sonuç kaydı.
- Wiegers fayda, ceza, maliyet ve risk ağırlıklandırması ile toplu puanlama ve normalize karşılaştırma.
- Volere kriter ağırlığı ve 0-10 puanlama akışı.
- İlişki CRUD'u, otomatik izlenebilirlik matrisi, ağ görünümü, ileri-geri sorgular ve transitive etki analizi.
- Başlangıç çalışma alanı, puanlama, matris, ağ, etki analizi ve sonuç ekranlarını bağlayan responsive Bootstrap arayüzü.
- Güncel puanları ve izlenebilirlik matrisini içeren Türkçe karakter uyumlu PDF dışa aktarma.

## Doğrulama

- Otomatik test paketi: **24/24 geçti**.
- PDF çıktısı A4 olarak render edildi; başlık, tablolar ve Türkçe karakterler görsel olarak kontrol edildi.
- WeasyPrint'in yerel sistem bağımlılığı sorunu, taşınabilir ReportLab üreticisi kullanılarak giderildi.

## Akademik kapsam notu

Uygulama, başvurudaki yöntemlerin işlevsel prototipidir; elde edilen puanlar kullanıcı girdilerine dayalı karar desteği sağlar. Bir yöntemin üstünlüğü veya kullanıcı memnuniyeti hakkında ampirik iddia için ayrı vaka çalışması ve katılımcı değerlendirmesi gerekir.

## GitHub durumu

Değişiklikler yerel Git geçmişine kaydedilecektir. Uzak GitHub deposu tanımlı olmadığı için gönderim yapılamaz; depo adresi sağlandığında `main` dalı gönderilebilir.
