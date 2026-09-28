# İzlenebilirlik ve değişiklik etki analizi

İzlenebilirlik, bir gereksinimin başka gereksinimlerle olan gerekçe, bağımlılık ve ayrıntı ilişkisini takip edebilme yeteneğidir. REQS bu ilişkileri `RequirementRelation` içinde kanonik olarak saklar; matris, vis-network ağı ve NetworkX etki grafiği aynı tablodan türetilir.

## İlişki türleri

| Tür | Anlam | Yön |
| --- | --- | --- |
| `depends_on` | Kaynak hedefe bağımlıdır | Yönlü |
| `prerequisite_of` | Kaynak hedef için ön koşuldur | Yönlü |
| `similar_to` | Benzer gereksinim | Genellikle yönsüz |
| `refines` | Kaynak hedefi detaylandırır / üst-alt bağ | Yönlü |
| `conflicts_with` | Birlikte uygulanması çelişki yaratır | Genellikle yönsüz |
| `related_to` | Genel ilişki | Yönlü veya yönsüz |

Matris yönsüz ilişkiyi iki hücrede; ağ ise kesikli, ok ucu olmayan kenarla gösterir. İleri ve geri sorgular yönsüz bağlantıları her iki yönden de görünür kılar.

## Etki analizi

NetworkX `MultiDiGraph`, ilişki türlerini kenar etiketiyle taşır. Seçilen gereksinimden en kısa yollar hesaplanır; ileri ve geri yön için doğrudan/dolaylı etkilenen anahtar, mesafe ve ilişki yolu döndürülür. Gereksinim düzenleme ekranı başarılı `PATCH` sonrasında bu endpoint'i otomatik çağırır ve etki varsa kullanıcıya uyarı gösterir.

Örnek: `REQS-02 → REQS-03 → REQS-04` zincirinde REQS-02 değişirse REQS-03 birinci, REQS-04 ikinci seviye ileri etkidir.
