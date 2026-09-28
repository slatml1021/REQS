# Vaka çalışması

## Senaryo

REQS, kurgusal fakat gerçekçi bir KOBİ stok ve sipariş yönetim sistemi üzerinde değerlendirilir. Vaka verisi, kişisel veri veya gerçek müşteri kaydı içermez. Amaç, 10 gereksinimlik bir kümede üç önceliklendirme yönteminin, ilişki matrisi/ağının ve etki analizinin birlikte çalışmasını göstermektir.

Kaynak veri: [`sample_data/reqs_vaka_calismasi.json`](../sample_data/reqs_vaka_calismasi.json). Veriyi PostgreSQL ana ortamına tekrar yüklemek için `docker compose exec -T -w /workspace app python -m scripts.load_sample_data --reset` komutu kullanılır.

## Gereksinim kümesi

| Anahtar | Gereksinim | Tür |
| --- | --- | --- |
| REQS-01 | Kullanıcı girişi ve yetkilendirme | İşlevsel |
| REQS-02 | Rol bazlı erişim | İşlevsel |
| REQS-03 | Ürün ve stok kartı yönetimi | İşlevsel |
| REQS-04 | Stok hareketi kaydı | İşlevsel |
| REQS-05 | Kritik stok uyarısı | İşlevsel |
| REQS-06 | Tedarikçi yönetimi | İşlevsel |
| REQS-07 | Satın alma siparişi | İşlevsel |
| REQS-08 | Satış siparişi | İşlevsel |
| REQS-09 | Stok ve satış raporları | İşlevsel |
| REQS-10 | Denetim kaydı | İşlevsel olmayan |

## Deney akışı

1. Her gereksinim için AHP ikili karşılaştırmaları, Wiegers dört faktör puanları ve Volere kriter puanları örnek veride tanımlanır.
2. AHP sonuçları, özdeğer yöntemiyle hesaplanır; tutarlılık oranı sonuçla birlikte döner.
3. `depends_on`, `prerequisite_of`, `related_to`, `refines`, `similar_to` ve `conflicts_with` ilişkileri ilişki tablosuna kaydedilir. Benzerlik ve çelişki ilişkileri yönsüz işaretlenir.
4. Sonuç ekranı, yöntem seçicisiyle normalize skorları; matris ve ağ ekranı ilişki yapısını; etki ekranı doğrudan/dolaylı bağlantıları gösterir.
5. Aynı vaka verisinden PDF raporu üretilir. Rapor, karar sonucu değil sistem çıktısıdır; insan paydaş değerlendirmesi içermez.

## Değerlendirme ölçütleri

| Ölçüt | Kanıt |
| --- | --- |
| Veri yükleme | 10 gereksinim ve 10 ilişki oluşturan yükleyici çıktısı |
| Öncelik hesapları | API'nin üç yöntem için normalize sonuç döndürmesi |
| İzlenebilirlik | Matris hücreleri, yön bilgili ağ kenarları ve ileri/geri sorgular |
| Etki analizi | NetworkX erişilebilirlik sonucunda doğrudan/dolaylı etki listesi |
| Raporlama | PDF yanıtının `%PDF` imzası, A4 sayfa yapısı ve görsel denetim |

Vaka çalışması, gerçek bir kurum performans iddiası değildir. Kullanıcı deneyimi ve alan doğrulaması için gerçek katılımcılarla ayrı test yapılmalıdır.
