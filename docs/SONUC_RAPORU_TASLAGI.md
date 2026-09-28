# REQS sonuç raporu taslağı

## Özet

Bu çalışma, yazılım projelerinde gereksinim önceliklendirmesi ile izlenebilirliği tek bir karar destek prototipinde birleştirir. REQS; AHP, Wiegers ve Volere yöntemleriyle öncelik puanı üretir, sonuçları 0-100 aralığında karşılaştırılabilir biçimde sunar, gereksinimler arasındaki yönlü/yönsüz ilişkileri izlenebilirlik matrisi ve ağ görünümünde gösterir ve NetworkX tabanlı etki analizi gerçekleştirir. FastAPI, PostgreSQL, SQLAlchemy/Alembic, NumPy, NetworkX, Jinja2/Bootstrap, Chart.js, vis-network.js ve WeasyPrint kullanılmıştır. Kurgusal KOBİ stok/sipariş vakasında 10 gereksinim ve 10 ilişki üzerinden uçtan uca akış çalıştırılmıştır. Ayrı Docker test hizmetinde 29 otomatik test başarıyla tamamlanmıştır. Bu sonuç, teknik doğrulama kanıtıdır; gerçek kullanıcı memnuniyeti ya da yöntemlerden birinin üstünlüğü hakkında ampirik iddia değildir.

## Giriş ve amaç

Gereksinim sayısı ve bağımlılıkları arttıkça kararların yalnızca sezgiyle verilmesi gecikme, maliyet ve değişiklik riski doğurur. Çalışmanın amacı, karar vericinin girdiği değerlendirmeleri tekrarlanabilir puanlara dönüştürmek ve bir değişikliğin bağlı gereksinimlere etkisini görünür kılmaktır. Araştırma soruları ve kavramlar [kavramsal çerçevede](KAVRAMSAL_CERCEVE_TASLAGI.md) tanımlanmıştır.

## Yöntem ve sistem tasarımı

AHP modülü Saaty ölçeğindeki ikili karşılaştırmalardan özvektör öncelik vektörü ve tutarlılık oranı hesaplar. Wiegers modülü fayda, ceza, maliyet ve risk girdilerini; Volere modülü en çok dört, toplamı %100 olan kriteri ve 0-10 puanları kullanır. Her yöntem sonucu ortak 0-100 biçiminde listelenir. İlişkiler `depends_on`, `prerequisite_of`, `refines`, `related_to`, `similar_to` ve `conflicts_with` türleriyle kaydedilir; son iki tür yönsüz de tanımlanabilir. Mimari ayrıntısı [mimari](MIMARI.md) ve [veritabanı tasarımı](VERITABANI_TASARIMI.md) belgelerindedir.

## Vaka ve bulgular

KOBİ stok/sipariş vakası; yetkilendirme, stok, sipariş, raporlama ve denetim kaydı alanlarında 10 gereksinim içerir. Örnek veri üç yöntemin puanlarını ve 10 ilişkiyi yükler. Uygulama; ortak sonuç ekranını, ilişki matrisini, odaklanabilir ağ grafiğini, ileri/geri etki listesini ve aynı veriden üretilen PDF raporunu sunar. Vaka yöntemin gerçek kurumda etkinliğini ispatlamaz; işlevsel akışın kontrollü örneği olarak kullanılır.

## Test ve sınırlılıklar

29 birim/entegrasyon testi geçmiştir; API bütünlüğü, hesaplama sınırları, ilişki yönü, matris, etki analizi, PDF yanıtı ve 100 gereksinimli matris gözlemi kapsanır. Ayrıntı [test sonuçlarında](TEST_SONUCLARI.md) yer alır. AHP'nin karşılaştırma sayısı büyük kümelerde hızla artar; hiyerarşik/gruplu AHP ve büyük matrislerde filtreleme bu sürümde uygulanmamıştır. Gerçek kullanıcı testi, danışman onayı ve ekip kod incelemesi henüz insan kanıtı gerektiren adımlardır.

## Sonuç ve gelecek çalışma

REQS, başvuruda öngörülen araçlarla çalışır bir web prototipi ve tekrar üretilebilir vaka/test paketi sunar. Sonraki adım gerçek paydaşlarla kullanılabilirlik çalışması, tez kaynakçasının yayımlanmış künyelerle kesinleştirilmesi, büyük kümeler için gruplama/filtreleme ve NLP destekli ilişki önerisinin değerlendirilmesidir.
