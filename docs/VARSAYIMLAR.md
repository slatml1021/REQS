# Varsayımlar ve doğrulama sınırları

## Teknik varsayımlar

- PostgreSQL 16, REQS'in ana geliştirme ve çalışma veritabanıdır. MySQL 8.4, önceki 2209-A altyapı tercihine uygun olarak aynı Alembic zincirini doğrulayan isteğe bağlı uyumluluk profilidir; uygulamanın varsayılanı değildir.
- WeasyPrint, macOS'ta gereken Pango/GObject kütüphaneleri bulunmadığı için doğrudan yerel Python ortamında çalışmayabilir. Proje Docker imajı bu bağımlılıkları içerir; PDF üretimi bu tekrarlanabilir ortamda doğrulanır.
- Uygulama tek kullanıcı/tez prototipi kapsamındadır. Kimlik doğrulama, yetkilendirme ve çok kullanıcılı eşzamanlı düzenleme araştırma sorusunun dışında tutulmuştur.
- AHP'nin tüm ikili karşılaştırmaları, küçük ve orta ölçekli örneklerde tamamlanır. Çok büyük backlog'larda hiyerarşik/gruplu AHP önerilir.

## Akademik ve etik varsayımlar

- `literature/full_text/` içindeki PDF'ler erişilebilir tam metin arşividir; bir PDF'nin indirilmiş olması, onun otomatik olarak ana tez kaynağı olduğu anlamına gelmez.
- Kullanıcı testi, katılımcı verisi ve danışman onayı gerçekte yapılmadan yapılmış kabul edilmez. Bu paket yalnızca etik bilgilendirme, görev ve değerlendirme formlarını sağlar.
- Ek literatür kaynakları kaynakça listesine ancak künye, yayın türü ve erişim bağlantısı doğrulandıktan sonra yazılır.

## Takvim ve başvuru bilgisi

Sağlanan çalışma takvimindeki günler ile 2209-A başvuru formundaki yıl/dönem alanları aynı sürümden gelmeyebilir. Başvuru yılı, dönemi, resmi son tarih, danışman onayı ve başvuru sahibi bilgisi gönderimden önce **Salih Türk ile doğrulanmalıdır**. Bu belge, doğrulanmamış tarihleri resmî başvuru bilgisi olarak kullanmaz.
