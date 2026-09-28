# Çalışma takvimi ve günlük kontrol durumu

Bu kayıt, 30 Ağustos-30 Eylül 2026 tarihli yoğunlaştırılmış plandaki Sıla görevlerini izler. Dilara'ya ait ana sorumluluklar Sıla tamamlamış gibi işaretlenmez. "Hazır" teknik kanıtı ifade eder; kullanıcı testi ve onay için insan kanıtı gerekir.

| Tarih aralığı | Sıla'nın planlı işi | Durum | Kanıt |
| --- | --- | --- | --- |
| 30 Ağustos | Wiegers ve Volere ile ilgili ilk 8 makaleyi notlandırma | Hazır/kısmi | 15 yerel PDF ve [literatür denetimi](LITERATUR_TARAMASI.md); nihai künye kontrolü sürer |
| 31 Ağustos | Kalan 7 makale ve kavramsal çerçeve | Hazır/kısmi | [Kavramsal çerçeve](KAVRAMSAL_CERCEVE_TASLAGI.md) |
| 1 Eylül | Gereksinim listesi ve veritabanı şeması | Hazır | [Vaka](VAKA_CALISMASI.md), [veritabanı tasarımı](VERITABANI_TASARIMI.md) |
| 2-3 Eylül | PostgreSQL, SQLAlchemy modelleri, Alembic, CRUD | Hazır | Migration'lar ve API testleri |
| 4-7 Eylül | AHP ekranı/API entegrasyonu, ekran testleri | Hazır | AHP ekranı ve kabul testleri; algoritma Dilara sahipliğinde |
| 8-10 Eylül | Wiegers algoritması, formül doğrulama ve birim test | Hazır | Wiegers API ve testleri |
| 11-13 Eylül | Volere kriter ekranı, API entegrasyonu ve test | Hazır | Volere API ve testleri; yöntem tasarımı Dilara sahipliğinde |
| 14 Eylül | Normalize skor karşılaştırılabilirlik testi | Hazır | Ortak sonuç API'si |
| 15-18 Eylül | Matris backend'i, ağ görselleştirmesi, ileri/geri test | Hazır | Matris, vis-network ve yön testi |
| 19-20 Eylül | Etki uyarı arayüzü ve entegrasyon testi | Hazır | Etki analizi ekranı ve kabul senaryosu |
| 21-24 Eylül | Sorgu performansı, WeasyPrint PDF, rapor entegrasyonu | Hazır | Vaka PDF'i ve 100 gereksinimli matris testi |
| 25-26 Eylül | Kendi modüllerinin ve sistemin otomatik testleri | Hazır | 29/29 test geçti |
| 27 Eylül | Ortak kullanıcı testi planı/yürütümü | Form hazır | [Kullanıcı testi formu](KULLANICI_TESTI_FORMU.md); gerçek katılımcı kaydı yok |
| 28 Eylül | Geri bildirime göre düzeltme | Teknik düzeltme hazır | İlişki güncellemesi, yönsüz ilişkiler, UI akışları ve PDF iyileştirildi |
| 29 Eylül | Giriş/sonuç taslağı ve ortak sunum taslağı | Taslak hazır | [Sonuç raporu](SONUC_RAPORU_TASLAGI.md), [sunum planı](SUNUM_PLANI.md) |
| 30 Eylül | 2209-A uygunluk kontrolü ve sunum provası | İnsan işlemi bekliyor | [Teslim kontrol listesi](TUBITAK_2209A_BASVURU_KONTROL_LISTESI.md) |

## Başarı ölçütleri

| Hedef | Teknik durum |
| --- | --- |
| AHP, Wiegers, Volere birlikte çalışır | Hazır |
| Otomatik matris ve interaktif ağ | Hazır |
| Değişiklik etkisi sorgulanır | Hazır |
| PDF raporu üretilebilir | Hazır |
| Test senaryolarının %90'ından fazlası başarılı | Otomatik test paketi 29/29 geçti |
| Kullanıcı memnuniyeti/gerçek geri bildirim | Kanıt bekliyor |

Takvimde "hazır" olanlar sürümlenmiş ürün ve test kanıtına dayanır; danışman onayı ile gerçek kullanıcı değerlendirmesi bu işaretle eşdeğer değildir.
