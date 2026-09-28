# Karl Wiegers yöntemi

REQS, her gereksinim için fayda (`B`), ceza (`P`), maliyet (`C`) ve risk (`R`) değerlerini 1-9 aralığında alır. Proje düzeyinde her faktör için kullanıcı ağırlığı seçilir.

Kullanılan göreceli öncelik formülü:

`Öncelik = (B × ağırlık_B + P × ağırlık_P) / (C × ağırlık_C + R × ağırlık_R)`

Payda sıfır veya negatif olamaz. Tüm ham sonuçlar içindeki en yüksek değer 100 kabul edilerek diğer sonuçlar 0-100 ölçeğine taşınır. API, eksik gereksinim, yinelenen değerlendirme ve 1-9 dışı değerleri reddeder.

Örnek: B=9, P=8, C=3, R=2 ve tüm ağırlıklar 1 olduğunda ham skor `(9+8)/(3+2)=3,4` olur. Bu skor, batch içindeki maksimum ham skora göre normalize edilir.
