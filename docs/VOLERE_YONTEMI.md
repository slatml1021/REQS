# Volere yöntemi

Volere ekranı en fazla dört kriter tanımlar. Her kriterin yüzde ağırlığı ve her gereksinim için 0-10 puanı vardır. Ağırlık toplamı tam 100, kriter adları benzersiz olmalıdır.

`Ham puan = Σ(kriter ağırlığı × kriter puanı / 100)`
`Normalize puan = ham puan × 10`

Örnek: müşteri değeri %40 ve 10; iş değeri %60 ve 8 ise ham puan `8,8`, normalize puan `88` olur. Bu değer, AHP ve Wiegers sonuçlarıyla ortak tabloda karşılaştırılır.

Kriter sayısı beşi geçtiğinde, ağırlık toplamı 100 olmadığında, aynı ad iki kez verildiğinde veya puan 0-10 dışına çıktığında API 422 hata döndürür.
