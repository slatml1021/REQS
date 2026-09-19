# Etki Analizi Arayüz Entegrasyon Sözleşmesi

Bu belge, Sıla'nın uyarı arayüzünün Dilara'nın etki analizi servisiyle bağlanabilmesi için gerekli asgari API sözleşmesini tanımlar. Bu bir çalışma çıktısı değil, entegrasyon ön koşuludur.

## Önerilen uç nokta

`GET /api/v1/impact-analysis/{requirement_key}`

Başarılı yanıtta en az aşağıdaki alanlar bulunmalıdır:

```json
{
  "requirement_key": "REQ-001",
  "affected_requirements": [
    {
      "key": "REQ-002",
      "title": "Rapor üretimi",
      "direction": "forward",
      "distance": 1,
      "relation_path": ["depends_on"]
    }
  ]
}
```

## Arayüz davranışı

- Kullanıcı değiştirilecek gereksinimi seçer.
- Arayüz, servisten `affected_requirements` listesini ister.
- Liste boşsa etkilenen gereksinim olmadığı açıkça gösterilir.
- Liste doluysa her kayıt anahtar, başlık, yön, uzaklık ve ilişki yoluyla uyarı olarak gösterilir.
- Ağ veya sonuç ekranına yönlendirme, anahtar üzerinden yapılır.

## Sınır

Bu sözleşme etki analizi algoritmasını tanımlamaz veya yerine geçmez. Algoritmanın hesaplama mantığı Dilara'nın sahipliğindedir; Sıla'nın arayüzü bu sözleşme sağlandığında entegre edilir.
