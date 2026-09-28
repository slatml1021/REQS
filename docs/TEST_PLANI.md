# Test planı

## Amaç

Fonksiyonların doğru sonuç üretmesini, geçersiz veriyi reddetmesini ve modüllerin aynı veri modeli üzerinde bütünleşmesini doğrulamak.

| Katman | Kapsam | Başarı ölçütü |
| --- | --- | --- |
| Birim | Model bütünlüğü, AHP/Wiegers/Volere hesapları | Beklenen skor veya doğrulama hatası |
| API | CRUD, ilişki güncelleme, matris, iz sorguları, etki | Doğru HTTP kodu ve JSON sözleşmesi |
| Entegrasyon | Beş/on gereksinimli vaka, üç yöntem, PDF | Ortak sonuç ve PDF yanıtı |
| Performans | 100 gereksinimli matris gözlemi | Yanıtın yerel testte 5 sn altında kalması |
| Kullanıcı | Formlar, anlaşılabilirlik, rapor | Formdaki görevlerin gerçek katılımcılarla tamamlanması |

## Senaryolar

1. Benzersiz olmayan gereksinim anahtarı 409 döner.
2. Öz-ilişki ve yinelenen ilişki reddedilir.
3. Yönsüz benzerlik ilişkisi matriste iki yönde görünür.
4. İlişki türü/yönlülük güncellemesi matris ve grafiğe yansır.
5. AHP eksik çiftte 422, tutarsız matriste CR uyarısı döndürür.
6. Wiegers 1-9 dışı değerleri; Volere beşinci kriteri ve toplamı 100 olmayan ağırlıkları reddeder.
7. Üç yöntemin skorları 0-100 aralığında ortak sonuçta görünür.
8. İleri/geri izlenebilirlik ve iki yönlü etki yolu doğru döner.
9. WeasyPrint raporu yöntem, sonuç, SVG grafik, matris ve etki özetini içerir.
10. 100 gereksinimlik matris üretilir.

Kullanıcı testi sonucu ancak katılımcılar gerçek formu doldurduktan sonra `TEST_SONUCLARI.md` dosyasına eklenir.
