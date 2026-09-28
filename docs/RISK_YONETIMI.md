# Risk yönetimi

| Risk | Olasılık / etki | Erken işaret | B planı |
| --- | --- | --- | --- |
| Teknik entegrasyon hatası | Orta / yüksek | API sözleşmesi veya test kırılması | Küçük modül PR'ları, pytest, migration geri dönüş planı |
| Güncel literatüre erişememe | Orta / yüksek | Tam metin/DOI doğrulanamaması | Üniversite kütüphanesi, açık erişim depo ve yalnızca doğrulanmış kaynak kullanımı |
| Üç yöntemin sonuç uyumsuzluğu | Orta / orta | Normalize tablo boş/farklı ölçek | Ortak `PriorityScore`, vaka testi ve yöntem açıklaması |
| Büyük AHP karşılaştırma yükü | Yüksek / orta | Çift sayısının artması | Gereksinimleri tema ile gruplama, hiyerarşik AHP değerlendirmesi |
| Büyük matrisin okunamaması | Orta / orta | Çok geniş tablo | Filtreleme/modüler görünüm ve ağda vurgu önerisi |
| Takvim gecikmesi | Orta / yüksek | Günlük görevlerin tamamlanmaması | Kritik yol: CRUD, üç yöntem, matris, test; belge işleri sürümleyerek paralel ilerletme |
| Veri/sürüm kaybı | Düşük / yüksek | Yerel değişiklik veya migration çakışması | Git commit, yedek, Docker volume ve Alembic revizyonu |
| Donanım/yazılım arızası | Düşük / orta | Yerel bağımlılık hatası | Docker imajı, `.env.example`, tekrar üretilebilir kurulum |
| Düşük kullanıcı memnuniyeti | Orta / orta | Form görevlerinde zorlanma | Kullanıcı testi, görev gözlemi ve geri bildirimden düzeltme |
| Danışman erişilebilirliği | Orta / yüksek | Onay gecikmesi | Düzenli kısa ilerleme özeti, soruları belgeleyip toplu doğrulama |
