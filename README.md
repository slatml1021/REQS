# REQS

**Yazılım Projelerinde Gereksinim Önceliklendirmesi ve İzlenebilirlik İçin Karar Destek Sistemi**
TÜBİTAK 2209-A bitirme projesi — Dilara Topal ve Sıla Temel — Danışman: Salih Türk

REQS; gereksinimleri AHP, Wiegers ve Volere yöntemleriyle önceliklendirir, ilişkileri matriste ve ağ görünümünde izler, değişiklik etkisini sorgular ve sonuçları PDF olarak dışa aktarır. Uygulama web sitesidir; yerel olarak `http://127.0.0.1:8000/` adresinden açılır.

![REQS sistem özeti](docs/assets/reqs-sistem-ozeti.svg)

## Teknoloji yığını

| Katman | Teknoloji |
| --- | --- |
| API ve arayüz | Python 3, FastAPI, Jinja2, Bootstrap |
| Veri | PostgreSQL 16, SQLAlchemy, Alembic |
| Uyumluluk | MySQL 8.4, aynı migration zinciri |
| Karar desteği | NumPy (AHP), Wiegers, Volere |
| İzlenebilirlik | NetworkX, vis-network.js |
| Görselleştirme | Chart.js |
| Raporlama | WeasyPrint, HTML/CSS |
| Doğrulama | pytest, Docker, Git |

Bu teknoloji listesi, paylaşılan görev dağılımı belgesindeki teknoloji yığınıyla uyumludur. PostgreSQL ana geliştirme veritabanıdır. MySQL ikinci çalışma ortamı değil, başvuruda yer alan alternatif için şema/migration uyumluluk profilidir.

## Hızlı başlangıç

Docker Desktop açıkken proje kökünde:

```bash
cp .env.example .env
docker compose --profile app up -d --build
docker compose exec -T -w /workspace app alembic upgrade head
docker compose exec -T -w /workspace app python -m scripts.load_sample_data --reset
```

Sonra tarayıcıdan `http://127.0.0.1:8000/` açılır. API sözleşmesi `http://127.0.0.1:8000/docs` adresindedir.

### MySQL uyumluluk doğrulaması

```bash
docker compose up -d mysql
DATABASE_URL=mysql+pymysql://reqs:reqs@localhost:3307/reqs alembic upgrade head
```

MySQL kullanımı, PostgreSQL'deki veriyi otomatik olarak paylaşmaz. Aynı migration'ların ayrı MySQL şeması üzerinde çalıştığını doğrular.

### Testler

```bash
docker compose --profile test build test
docker compose --profile test run --rm test
```

Test hizmeti uygulama hizmetinin klasör bağlama ayarından bağımsızdır. Son doğrulama: **29 test geçti; 1 üçüncü taraf kullanım uyarısı; hata yok.** Ayrıntı: [test sonuçları](docs/TEST_SONUCLARI.md).

## Proje yapısı

```text
app/                 FastAPI, modeller, şemalar, API, servisler, şablonlar, statik dosyalar
alembic/             Şema migration'ları
tests/unit/          Birim testleri
tests/integration/   API ve uçtan uca kabul testleri
sample_data/         KOBİ stok/sipariş vaka verisi
scripts/             Örnek veri yükleyici
reports/             Üretilmiş PDF vaka raporu
docs/                Teknik, akademik ve teslim dokümanları
literature/          Yerel tam metin arşivi ve kaynak denetimi
```

## Önemli dokümanlar

- [Mimari](docs/MIMARI.md), [veritabanı tasarımı](docs/VERITABANI_TASARIMI.md), [API dokümantasyonu](docs/API_DOKUMANTASYONU.md)
- [AHP](docs/AHP_YONTEMI.md), [Wiegers](docs/WIEGERS_YONTEMI.md), [Volere](docs/VOLERE_YONTEMI.md)
- [İzlenebilirlik ve etki analizi](docs/IZLENEBILIRLIK_VE_ETKI_ANALIZI.md), [vaka çalışması](docs/VAKA_CALISMASI.md)
- [Görev dağılımı](docs/GOREV_DAGILIMI.md), [takvim](docs/CALISMA_TAKVIMI.md), [uygunluk denetimi](docs/GOREV_UYUMLULUK_DENETIMI.md)
- [Literatür taraması](docs/LITERATUR_TARAMASI.md), [kullanıcı kılavuzu](docs/KULLANICI_KILAVUZU.md), [teslim kontrolü](docs/TUBITAK_2209A_BASVURU_KONTROL_LISTESI.md)
- [Kaynak belgeler envanteri](docs/KAYNAK_BELGELER.md) ve [vaka PDF raporu](reports/reqs-vaka-raporu.pdf)

## Dürüst kanıt sınırı

Örnek vaka, uygulama testleri ve PDF üretimi doğrulanmıştır. Gerçek kullanıcı testi, danışman onayı ve uzak GitHub/PR süreci henüz kanıtlanmış değildir; bunlar gerçek katılımcı/kurum işlemi olmadan tamamlanmış olarak beyan edilmez. Şu anda bir uzak GitHub deposu tanımlı değildir.
