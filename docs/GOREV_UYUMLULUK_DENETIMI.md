# REQS görev uygunluk denetimi

**Denetim tarihi:** 29 Eylül 2026
**Esas belge:** Dilara Sıla Görev Dağılımı ve Yoğunlaştırılmış Uygulama Planı

Bu denetim, plandaki teknoloji ve modül sahipliğini korur. Ortak entegrasyon kodu, diğer ekip üyesinin ana sorumluluğunu Sıla adına yazmaz.

## Teknoloji yığını

| Planlanan teknoloji | Uygulamadaki doğrulama |
| --- | --- |
| Python 3, FastAPI | REST API, Jinja2 ekranları ve OpenAPI `/docs` çalışır |
| PostgreSQL, SQLAlchemy, Alembic | PostgreSQL 16 ana servis, `20260928_03` migration başı |
| MySQL | 2209-A başvurusunda belirtilen alternatif için MySQL 8.4 uyumluluk profili, aynı migration başı |
| NumPy | AHP özdeğer, öncelik vektörü ve tutarlılık oranı |
| NetworkX | Yönlü/yönsüz ilişkiler üzerinden ileri/geri etki analizi |
| Jinja2, Bootstrap | Responsive çalışma alanı ve puanlama ekranları |
| Chart.js | Yöntem seçicili çubuk ve doughnut grafik |
| vis-network.js | Yön bilgili, etkileşimli ilişki ağı |
| WeasyPrint | HTML/CSS şablonundan yöntem özeti, grafik, matris ve etki listeli PDF |
| pytest, Git/GitHub | 29 otomatik test geçti; yerel Git aktiftir. Uzak GitHub deposu tanımlı değildir. |

## Modül sahipliği

| Modül | Belgedeki ana sahip | Sıla'nın doğrulanmış kapsamı | Ortak/diğer sahiplik sınırı |
| --- | --- | --- | --- |
| Gereksinim veri modeli ve veritabanı | Sıla | SQLAlchemy şeması, Alembic, CRUD, indeks/uyumluluk | Dilara performans değerlendirmesinde destekleyicidir |
| AHP | Dilara | Ekran/API entegrasyonu ve test | Algoritma/CR sahipliği Dilara'dadır |
| Wiegers | Sıla | Formül, puanlama, test ve ekran/API entegrasyonu | Dilara ekran/inceleme desteği verir |
| Volere | Dilara | Kriter ekranı, API entegrasyonu ve test desteği | Algoritma/kriter yaklaşımı Dilara'dadır |
| Üç yöntemin entegrasyonu | Ortak | Normalize sonuç sorgusu ve doğrulama | Ortak çıktı |
| İzlenebilirlik | Ortak | Matris backend'i ve vis-network ağı | Dilara ilişki modeli ve matris kullanıcı deneyiminden sorumludur |
| Etki analizi | Ortak | Etki uyarı akışı ve senaryo doğrulaması | Algoritmik yaklaşım Dilara'dadır |
| PDF raporlama | Sıla | WeasyPrint şablonu, grafik/matris/etki raporu | Dilara grafik entegrasyonunda destek verir |
| Genel UI ve Chart.js | Dilara | Tasarım tutarlılığı ve test desteği | Ana sahiplik Dilara'dadır |

## Günlük checklist karşılığı

| Tarih | Sıla görevi | Durum / kanıt |
| --- | --- | --- |
| 30 Ağustos - 1 Eylül | Wiegers/Volere literatürü, çerçeve, gereksinim listesi, şema | 15 PDF arşivi, çerçeve ve vaka/şema dokümanı hazır; ana kaynak künye doğrulaması sürdürülmeli |
| 2 - 3 Eylül | PostgreSQL, SQLAlchemy, Alembic, CRUD | Tamamlandı; migration ve API testleri var |
| 4 - 7 Eylül | AHP ekranı, API entegrasyonu ve ekran testi | Tamamlandı; algoritma sahipliği Dilara'da korunur |
| 8 - 10 Eylül | Wiegers algoritması, formül doğrulama, test | Tamamlandı; entegrasyon testleri geçti |
| 11 - 13 Eylül | Volere ekranı, API entegrasyonu, test | Tamamlandı; sınır testleri geçti |
| 14 Eylül | Normalize skor karşılaştırılabilirliği | Tamamlandı; ortak 0-100 sonuç API'si |
| 15 - 18 Eylül | Matris backend'i, ağ entegrasyonu, ileri/geri test | Tamamlandı; yönlü/yönsüz ilişki testi eklendi |
| 19 - 20 Eylül | Etki uyarı arayüzü ve ortak entegrasyon | Tamamlandı; değişiklik sonrası etki akışı görünür |
| 21 - 24 Eylül | Sorgu inceleme, WeasyPrint PDF, rapor entegrasyonu | Tamamlandı; 4 sayfalı vaka PDF'i görsel olarak denetlendi |
| 25 - 28 Eylül | Sıla modül testleri, entegrasyon, düzeltme | Tamamlandı; 29/29 otomatik test geçti |
| 27 Eylül | Ortak kullanıcı testi | Gerçek katılımcı verisi olmadığı için tamamlandı sayılmaz |
| 29 Eylül | Nihai raporun giriş/sonuç bölümü ve ortak sunum taslağı | Taslak belgeler hazır; danışman incelemesi ve sunum provası insan katılımı gerektirir |
| 30 Eylül | 2209-A format kontrolü ve sunum provası | Teslim öncesi yapılacak; [kontrol listesi](TUBITAK_2209A_BASVURU_KONTROL_LISTESI.md) hazır |

## Sonuç

Teknik ürün kapsamı, planın zorunlu araçlarıyla çalışır durumdadır. Gerçek kullanıcı testi, danışman onayı, takımın birbirinin işini gözden geçirme kanıtı ve uzak GitHub yedeği otomatik testle ikame edilemez; bunlar bu belgede beklemede tutulmuştur.
