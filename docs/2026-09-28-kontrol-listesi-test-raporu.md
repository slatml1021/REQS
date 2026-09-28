# REQS ana kontrol listesi test raporu

**İlk denetim:** 28 Eylül 2026
**Revizyon:** 29 Eylül 2026
**Kapsam:** Sıla Temel için paylaşılan ana kontrol listesi

## Revizyon özeti

İlk denetimde saptanan teknik eksikler bu revizyonda giderildi: ilişki güncelleme uç noktası, `conflicts_with` ve yönsüz ilişki türleri, çalışma alanındaki gereksinim ekleme akışı, değişiklik sonrası etki bildirimi, dolu örnek veriyle grafik/ağ, yöntem açıklamalı ve grafik içeren WeasyPrint PDF'i eklendi. Testler, ana uygulama klasörü bağlanmadan çalışan Docker test hizmetinde yeniden yürütüldü.

| Kontrol | Revize sonuç |
| --- | --- |
| Tüm pytest paketi | **29 geçti**, 1 üçüncü taraf kullanım uyarısı; başarısız test yok |
| 5 gereksinimli uçtan uca kabul senaryosu | AHP, Wiegers, Volere, ortak sonuçlar, ilişki, etki ve PDF geçti |
| 100 gereksinimli matris | Testte 5 saniye eşiği altında üretildi |
| PostgreSQL 16 | Alembic `20260928_03` baş sürümü |
| MySQL 8.4 uyumluluk profili | Alembic `20260928_03` baş sürümü |
| Örnek vaka | 10 gereksinim, 10 ilişki, 30 öncelik kaydı |
| PDF | WeasyPrint 66.0 ile 4 A4 sayfa; yöntem özeti, SVG grafik, matris ve etki listesi |

## Kontrol listesi durumu

| Kriter | Durum | Kanıt / sınır |
| --- | --- | --- |
| Gereksinim CRUD, benzersiz anahtar ve tür bilgisi | Geçti | Entegrasyon testleri |
| İlişki oluşturma, güncelleme, silme ve bütünlük | Geçti | `PATCH /api/v1/relations/{id}` ve test |
| Bağımlılık, ön koşul, ayrıntılandırma, benzerlik, çelişki | Geçti | Yönlü/yönsüz türler ve matris/ağ görünümü |
| Dinamik matris, ileri/geri izlenebilirlik | Geçti | Kabul testleri |
| Değişiklik etkisi ve görünür uyarı akışı | Geçti | NetworkX sorgusu ve çalışma alanı bildirimi |
| AHP, Wiegers, Volere veri giriş ekranları | Geçti | Ekran/API testleri |
| Sonuç grafikleri ve interaktif ağ | Geçti | Chart.js ve vis-network veri sözleşmesi |
| PDF raporu | Geçti | WeasyPrint raporu |
| 5-10 gereksinimli vaka | Geçti | 10 gereksinimli KOBİ stok/sipariş vakası |
| Büyük AHP için gruplama/hiyerarşik AHP | Sınır notu | Uygulanmadı; ölçeklenebilirlik için gelecek çalışma |
| Büyük matris filtreleme/modüler görünüm | Sınır notu | Uygulanmadı; ağ odağı var, tam filtreleme yok |

## İnsan kanıtı gerektiren kalemler

Gerçek katılımcı kullanıcı testi, danışman onayı, ekip içi kod incelemesi ve uzak GitHub yedek/PR süreci henüz tamamlanmış sayılmaz. Mevcut arşivde 15 açılabilir PDF vardır; bunların nihai tez kaynakçasına uygun künyeleri danışmanla doğrulanmalıdır. Bu sınırlar teknik test başarısından ayrı tutulur.
