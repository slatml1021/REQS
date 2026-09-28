# Kavramsal çerçeve taslağı

REQS, yazılım gereksinimlerinin sınırlı zaman ve kaynak altında hangi sırayla ele alınacağını görünür kılmak ve gereksinimler arasındaki bağlantılardan doğan değişiklik etkisini izlemek için geliştirilmiş bir karar destek prototipidir. Çalışma, gereksinim mühendisliğinin iki tamamlayıcı problemine odaklanır: önceliklendirme ve izlenebilirlik.

## Problem alanı

Yazılım projelerinde gereksinim sayısı arttıkça aynı anda her gereksinimi gerçekleştirmek mümkün değildir. Önceliklendirme, paydaş değeri, gecikme cezası, maliyet ve risk gibi ölçütlerle gerekçeli bir sıralama üretir. İzlenebilirlik ise bir gereksinimin diğerleriyle olan bağımlılık, ön koşul, ayrıntılandırma, benzerlik, çelişki ve ilgili olma ilişkilerini kayıt altında tutar. Bu iki alan birlikte ele alınmadığında, yüksek öncelikli görünen bir gereksinimin ön koşulları ya da değişiklikten etkilenecek alt gereksinimler gözden kaçabilir.

## Araştırma soruları

1. AHP, Wiegers ve Volere yöntemleri tek bir sistemde karşılaştırılabilir sonuçlar üretebilir mi?
2. Gereksinim ilişkilerinden otomatik üretilen matris ve ağ görünümü, ileri-geri izlenebilirliği destekler mi?
3. Bir gereksinim seçildiğinde yönlü ve yönsüz ilişkilerden doğan doğrudan/dolaylı etki alanı gösterilebilir mi?
4. Üretilen sonuçlar, tekrar kullanılabilir bir PDF raporunda karar gerekçesiyle birlikte sunulabilir mi?

## Kavramlar ve REQS karşılıkları

| Kavram | REQS'teki karşılığı | Ölçülebilir çıktı |
| --- | --- | --- |
| Gereksinim | Benzersiz anahtar, başlık, açıklama, tür ve durum kaydı | CRUD kayıtları |
| AHP | İkili karşılaştırmalar, özvektör öncelik vektörü ve CR | Göreli ağırlık, CR, tutarlılık uyarısı |
| Wiegers | Fayda, ceza, maliyet ve risk puanları ile ağırlıklar | 0-100 normalize öncelik |
| Volere | En fazla dört, toplamı %100 olan kriter ve 0-10 puanlar | Ağırlıklı toplam ve 0-100 normalize puan |
| İzlenebilirlik | Yönlü/yönsüz ilişki türleri | Matris, ağ, ileri/geri sorgu |
| Etki analizi | NetworkX üzerinde erişilebilirlik sorgusu | Doğrudan/dolaylı etki listesi |

## Sınırlar

Bu prototip karar vericinin yerine otomatik karar vermez; girilen değerlendirmeleri görünür, karşılaştırılabilir ve denetlenebilir hale getirir. AHP'de karşılaştırma sayısı n(n-1)/2 olduğundan büyük gereksinim kümelerinde gruplama veya hiyerarşik uygulama değerlendirilmelidir. Kullanılabilirlik veya memnuniyet sonucu ise gerçek katılımcı verisi olmadan raporlanamaz; bunun için [kullanıcı testi formu](KULLANICI_TESTI_FORMU.md) kullanılacaktır.
