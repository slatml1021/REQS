# REQS Kullanım Kılavuzu

REQS, yazılım gereksinimlerini AHP, Wiegers ve Volere ile karşılaştırmak; ilişkileri izlemek; değişiklik etkisini incelemek ve PDF raporu almak için geliştirilmiş bir karar destek prototipidir.

## Kurulum ve çalıştırma

```bash
docker compose up -d db
python -m pip install -e '.[dev]'
uvicorn app.main:app --reload
```

Tarayıcıda `http://127.0.0.1:8000` adresini açın. API sözleşmesi `http://127.0.0.1:8000/docs` altında otomatik olarak yayınlanır.

## Önerilen çalışma akışı

1. Ana çalışma alanından gereksinimleri `REQ-001` gibi benzersiz anahtarlarla ekleyin.
2. İhtiyaca göre AHP, Wiegers veya Volere ekranından puanlama yapın. AHP'de tüm ikili karşılaştırmalar tamamlandıktan sonra tutarlılık oranını denetleyin; `CR < 0,10` tercih edilir.
3. İzlenebilirlik matrisinde gereksinimler arası yönlü ilişki tanımlayın. Aynı veri ağ görünümüne otomatik yansır.
4. Etki analizi ekranından değişmesi planlanan gereksinimi seçin. İleri ve geri yönlerdeki doğrudan/dolaylı etkiler seviye ve ilişki yolu ile gösterilir.
5. Sonuçlar ekranından normalize puanları karşılaştırın; PDF raporu için ana ekrandaki indirme düğmesini kullanın.

## Doğrulama

```bash
python -m pytest -q
```

Test paketi API, hesaplama, veri bütünlüğü, izlenebilirlik, etki analizi ve PDF dışa aktarmayı kapsar.
