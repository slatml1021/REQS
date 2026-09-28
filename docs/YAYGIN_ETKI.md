# Yaygın etki ve sürdürülebilirlik

REQS'in öngörülen etkisi, küçük ve orta ölçekli yazılım ekiplerinde gereksinim kararlarını tek kişi bilgisine bağımlı olmaktan çıkarıp gerekçeli kayıtlarla desteklemektir. Bu ifade bir saha etkisi sonucu değil, prototipin hedeflenen kullanım değeridir.

| Boyut | Hedeflenen katkı | Ölçüm/kanıt yolu |
| --- | --- | --- |
| Akademik | Üç yöntem ile izlenebilirlik/etki analizinin birlikte incelenmesi | Tez, kaynakça ve vaka analizi |
| Teknik | Tekrarlanabilir açık kaynak prototip | Docker, migration, testler ve örnek veri |
| Sektörel | Karar gerekçesi, ilişki görünürlüğü ve rapor çıktısı | Gerçek ekip vaka testi ve geri bildirim formu |
| Eğitimsel | Gereksinim mühendisliği derslerinde örnek araç | Ders/proje uygulamasında eğitmen ve öğrenci geri bildirimi |

Sürdürülebilirlik için PostgreSQL ana profil olarak korunur; 2209-A başvurusunda yer alan MySQL ise aynı şema zincirini denetleyen uyumluluk profili olarak bulunur. Kaynak kodu, migration'lar, örnek veri ve testler birlikte sürümlenmelidir. Uzak GitHub deposu eklendiğinde yerel Git geçmişi gönderilmeli, dal/PR inceleme akışı ekipçe belirlenmelidir.
