# API dokümantasyonu

Canlı OpenAPI arayüzü: `http://127.0.0.1:8000/docs`
Makine-okunur şema: `http://127.0.0.1:8000/openapi.json`

| Uç nokta | İşlev |
| --- | --- |
| `POST/GET /api/v1/requirements` | Gereksinim oluşturma ve listeleme |
| `GET/PATCH/DELETE /api/v1/requirements/{id}` | Ayrıntı, güncelleme, silme |
| `PUT/GET /api/v1/ahp/comparisons` | AHP ikili karşılaştırma kaydetme/listeleme |
| `POST /api/v1/ahp/comparisons/calculate` | Öncelik vektörü ve CR hesaplama |
| `PUT /api/v1/wiegers/scores` | Toplu Wiegers puanlama |
| `PUT /api/v1/volere/scores` | Volere puanlama |
| `GET /api/v1/prioritization/results` | Ortak normalize sonuçlar |
| `POST/GET /api/v1/relations` | İlişki oluşturma/listeleme |
| `PATCH/DELETE /api/v1/relations/{id}` | İlişki güncelleme/silme |
| `GET /api/v1/traceability/matrix` | Dinamik matris |
| `GET /api/v1/traceability/graph` | Ağ düğüm/kenar verisi |
| `GET /api/v1/traceability/{key}/forward` | İleri izlenebilirlik |
| `GET /api/v1/traceability/{key}/backward` | Geri izlenebilirlik |
| `GET /api/v1/impact-analysis/{key}` | Doğrudan/dolaylı etki |
| `GET /api/v1/reports/pdf` | WeasyPrint PDF raporu |

Örnek gereksinim isteği:

```json
{"key":"REQ-001","title":"Kullanıcı girişi","description":"Rol tabanlı giriş","requirement_type":"functional","status":"draft"}
```

Örnek ilişki isteği:

```json
{"source_requirement_id":1,"target_requirement_id":2,"relation_type":"depends_on","is_directional":true}
```

Doğrulama hataları `422`, bulunamayan kayıtlar `404`, benzersiz anahtar veya yinelenen ilişki hataları `409` ile döner. AHP tüm çiftler kaydedilmeden hesaplanırsa eksik çiftler `422` yanıtında bildirilir.
