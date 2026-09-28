# REQS Görev Uygunluk Denetimi

**Denetim tarihi:** 28 Eylül 2026  
**Esas belge:** Dilara Sıla Görev Dağılımı ve Yoğunlaştırılmış Uygulama Planı

## Teknoloji yığını

| Planlanan teknoloji | Uygulamadaki durum |
| --- | --- |
| Python 3, FastAPI | Uygun |
| PostgreSQL, SQLAlchemy, Alembic | Uygun; PostgreSQL 16 ana Docker servisi ve migration zinciri aktif |
| MySQL | 2209-A başvurusundaki araştırma olanağı seçeneği olarak ayrı uyumluluk profili eklendi. PostgreSQL'in yerine geçmez. |
| NumPy ile AHP | Uygun; Saaty özdeğer ve CR hesaplaması |
| NetworkX | Uygun; değişiklik etki analizi yönlü çoklu ilişki grafiği üzerinden yürür |
| Jinja2, Bootstrap | Uygun |
| Chart.js | Uygun; sonuç ekranında çubuk ve doughnut grafik |
| vis-network.js | Uygun; izlenebilirlik ağı interaktif düğüm-bağlantı görünümü |
| WeasyPrint | Yerel macOS bağımlılığı nedeniyle çalışmadı. 2209-A başvurusunun araştırma olanakları bölümünde belirtilen **ReportLab** ile PDF üretimi yapılıyor. Bu, başvuruda yer alan izinli araç değişikliğidir. |
| pytest, Git/GitHub | pytest uygundur; Git yerelde aktiftir. GitHub uzak deposu henüz tanımlı değildir. |

## Genel ve modül bazlı sahiplik

| Modül | Belgedeki ana sahip | Durum ve atıf kuralı |
| --- | --- | --- |
| AHP algoritması ve CR | Dilara | Çalışan uygulama var. Akademik raporda Dilara ana sahip olarak yazılmalı; Sıla katkısı ekran, entegrasyon ve testtir. |
| Wiegers algoritması | Sıla | Çalışan toplu puanlama, formül doğrulama ve testler var. |
| Volere algoritması | Dilara | Çalışan puanlama akışı var. Sıla katkısı ekran, API entegrasyonu ve testtir. |
| Üç yöntemin entegrasyonu | Ortak | Ortak sonuç API'si, normalize 0-100 görünümü ve Chart.js grafikleri var. |
| İlişki modeli ve matris ekranı | Dilara | İlişki CRUD'u ve matris ekranı var; akademik sahiplik Dilara'da kalır. |
| Matris backend'i ve ağ görselleştirmesi | Sıla | Otomatik matris, NetworkX destekli etki sorgusu ve vis-network görünümü var. |
| Etki analizi algoritması | Dilara | NetworkX tabanlı algoritma uygulamada mevcut; raporda Dilara ana sahip olarak atfedilmelidir. |
| Etki uyarı arayüzü | Sıla | Etki analizi ekranı, seviye ve ilişki yolu ile uyarı sunar. |
| Veritabanı ve CRUD | Sıla | PostgreSQL şeması, CRUD ve 28 Eylül indeksleri var. |
| Genel UI ve Chart.js | Dilara | Bootstrap çalışma alanı ve Chart.js görselleri var; raporda Dilara ana sahip olarak atfedilmelidir. |
| PDF raporlama | Sıla | Türkçe PDF üretimi, sonuç/matris tablosu ve görsel render kontrolü var. |

## Günlük checklist durumu

| Tarih aralığı | Sıla görevi | Durum |
| --- | --- | --- |
| 30 Ağustos - 1 Eylül | Wiegers/Volere literatürü, çerçeve, gereksinim listesi, şema | Kaynak arşivi, kavramsal çıktı ve şema mevcut. Kaynakların akademik uygunluk denetimi ayrı tutulur. |
| 2 - 3 Eylül | PostgreSQL, SQLAlchemy, Alembic, CRUD | Tamamlandı. |
| 4 - 7 Eylül | AHP ekranı, API entegrasyonu, ekran testleri | Tamamlandı. AHP algoritması Dilara sahipliğiyle atfedilir. |
| 8 - 10 Eylül | Wiegers algoritması, formül doğrulama, birim test | Tamamlandı. |
| 11 - 13 Eylül | Volere ekranı, API entegrasyonu ve test | Tamamlandı. |
| 14 Eylül | Normalize skor karşılaştırılabilirlik testi | Tamamlandı. |
| 15 - 18 Eylül | Matris backend'i, ağ entegrasyonu, ileri-geri test | Tamamlandı. |
| 19 - 20 Eylül | Etki uyarı arayüzü ve ortak entegrasyon | Tamamlandı; algoritma sahipliği Dilara'da tutulur. |
| 21 - 24 Eylül | Veritabanı indeksleri, PDF, rapor entegrasyonu/test | Tamamlandı. |
| 25 - 26 Eylül | Sıla modül testleri ve sistem entegrasyon testi | 24/24 otomatik test geçti. |
| 27 Eylül | Ortak kullanıcı testi | Katılımcı geri bildirimi olmadan tamamlandı olarak işaretlenemez. |
| 28 Eylül | Geri bildirime göre hata düzeltme | Gerçek kullanıcı geri bildirimi bekliyor. |

## Sonuç

Teknik kapsam, plandaki teknoloji yığınına ve görev sahipliğine göre yeniden hizalanmıştır. Kullanıcı testi ile danışman/ekip sahiplik onayı, yazılım testiyle ikame edilemeyecek iki açık kalemdir.
