# Teslim envanteri

**Hazırlık tarihi:** 29 Eylül 2026
**Proje:** REQS — Yazılım Projelerinde Gereksinim Önceliklendirmesi ve İzlenebilirlik İçin Karar Destek Sistemi

## Çalıştırılabilir ürün

| Öğe | Konum | Durum |
| --- | --- | --- |
| FastAPI web uygulaması | `app/` | Hazır |
| PostgreSQL ana profil | `docker-compose.yml` | Hazır |
| MySQL uyumluluk profili | `docker-compose.yml` | Hazır |
| Migration zinciri | `alembic/` | Hazır; baş `20260928_03` |
| Vaka verisi yükleyici | `scripts/load_sample_data.py` | Hazır |
| Birim/entegrasyon testleri | `tests/` | Hazır; 29/29 geçti |
| Sistem üretimli vaka PDF'i | `reports/reqs-vaka-raporu.pdf` | Hazır |
| Biçimlendirilmiş teslim raporu | `reports/REQS_Teslim_Raporu.docx` | Hazır; 4 sayfa görsel denetim yapıldı |
| Sistem özeti görseli | `docs/assets/reqs-sistem-ozeti.svg` | Hazır; GitHub README'de görünür |

## Dokümantasyon

| Alan | Belge |
| --- | --- |
| Tanım, mimari, veri akışı | `PROJE_TANIMI.md`, `MIMARI.md`, `VERITABANI_TASARIMI.md`, `VERI_AKIS_DIYAGRAMI.md` |
| API ve yöntemler | `API_DOKUMANTASYONU.md`, `AHP_YONTEMI.md`, `WIEGERS_YONTEMI.md`, `VOLERE_YONTEMI.md` |
| İzlenebilirlik/test/vaka | `IZLENEBILIRLIK_VE_ETKI_ANALIZI.md`, `TEST_PLANI.md`, `TEST_SONUCLARI.md`, `VAKA_CALISMASI.md` |
| Tez ve teslim | `KAVRAMSAL_CERCEVE_TASLAGI.md`, `LITERATUR_TARAMASI.md`, `SONUC_RAPORU_TASLAGI.md`, `SUNUM_PLANI.md`, `TUBITAK_2209A_BASVURU_KONTROL_LISTESI.md` |
| Ekip ve ilerleme | `GOREV_DAGILIMI.md`, `CALISMA_TAKVIMI.md`, `GOREV_UYUMLULUK_DENETIMI.md`, `2026-09-29-gunluk-ilerleme-raporu.md` |
| Kaynak Word belgeleri | `KAYNAK_BELGELER.md`, `kaynak-belgeler/2209-uygulama.docx`, `kaynak-belgeler/Dilara_Sila_Gorev_Dagilimi_Guncel.docx` |

## Teslimden önce insanla tamamlanacaklar

- [ ] Gerçek kullanıcı testi katılımcı formu ve özet bulgusu
- [ ] Danışman inceleme/onay kaydı
- [ ] Nihai tez kaynakçasında her ön baskı için yayımlanmış künye/DOI denetimi
- [ ] Sunum provası
- [ ] Uzak GitHub deposu adresi tanımlanırsa yerel Git geçmişinin gönderilmesi

Bu envanter teknik dosyaların hazır olduğunu gösterir; işaretlenmemiş maddelerin tamamlandığını iddia etmez.
