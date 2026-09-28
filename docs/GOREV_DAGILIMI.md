# Görev dağılımı

Bu belge, sağlanan Dilara-Sıla planındaki ana sorumluluğu korur. Uygulamada ortak entegrasyon bulunması, diğer kişinin katkısının sahiplenildiği anlamına gelmez.

| Modül | Sıla Temel | Dilara Topal | Ortak çıktı |
| --- | --- | --- | --- |
| Veri katmanı | PostgreSQL, SQLAlchemy, Alembic, CRUD | Veri modeli değerlendirmesi | Şema incelemesi |
| AHP | Ekran/API entegrasyonu, test | Algoritma ve CR yaklaşımı | Entegrasyon testi |
| Wiegers | Algoritma, doğrulama, test, ekran entegrasyonu | Arayüz geri bildirimi | Sonuç analizi |
| Volere | Literatür, ekran/API/test desteği | Algoritma ve ölçüt yaklaşımı | Sonuç analizi |
| İzlenebilirlik | Matris algoritması, vis-network ağ | İlişki modeli/matris UX | Uçtan uca test |
| Etki analizi | Uyarı arayüzü | Analiz yaklaşımı | Senaryo testi |
| PDF | WeasyPrint rapor ve doğrulama | Grafik bileşeni katkısı | Rapor inceleme |
| Akademik çıktı | Giriş/sonuç, Wiegers/Volere taraması | Yöntem/bulgular | Nihai bütünlük |

## Denge ve ekip takibi

Sıla'nın sorumlulukları veri altyapısı, Wiegers, izlenebilirlik/ağ, etki uyarısı, PDF ve ilgili literatür ekseninde; Dilara'nın sorumlulukları AHP/Volere algoritmik yaklaşımı, ilişki modeli/arayüz ve küresel bulgular eksenindedir. Kod inceleme, Git/GitHub, test, kullanıcı testi, sonuç analizi, nihai rapor ve sunum ortak yürütülür. Her görev; tarih, sorumlu, gözden geçiren ve kanıt bağlantısıyla ekip panosuna işlenmelidir.
