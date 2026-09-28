# AHP yöntemi

Analitik Hiyerarşi Prosesi (AHP), alternatifleri ikili karşılaştırmalarla değerlendirir. REQS, Saaty'nin 1-9 ölçeğini ve karşılıklı değerlerini kabul eder. Karşılaştırmalar kanonik gereksinim çiftiyle saklanır; ters yönden girilen değer otomatik tersine çevrilir.

## Hesaplama

Karşılaştırma matrisi `A` için NumPy ile en büyük özdeğerin özvektörü bulunur ve toplamı 1 olacak biçimde normalize edilir. Her gereksinim puanı `w_i * 100` olarak ortak ekrana aktarılır.

Tutarlılık indeksi `CI = (λmax - n) / (n - 1)`; tutarlılık oranı `CR = CI / RI` biçimindedir. `CR < 0,10` uygun kabul edilir. Uygulama, değeri döndürür ve ekran 0,10 üstünde açık uyarı gösterir.

Örnek: iki gereksinimde `REQ-A / REQ-B = 3` seçilirse ağırlıklar yaklaşık `0,75` ve `0,25` olur; iki alternatifte rastgele indeks 0 olduğundan CR 0'dır.

Çok sayıda gereksinimde çift sayısı `n(n-1)/2` olur. Bu nedenle büyük backlog'larda temaya göre gruplama ve hiyerarşik AHP önerilir.
