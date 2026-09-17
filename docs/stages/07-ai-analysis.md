# Stage 7 — Yapay Zekâ Analiz Katmanı

**Durum:** ✅ Tamamlandı  
**Sorumluluk:** AI ekip bileşeni; Raspberry çalışma ortamı bu repo kapsamında

## Amaç

Normalleştirilmiş saldırı ve ağ verilerinden olay sınıfı, saldırı taktiği ve `0–100` risk skoru üretmek.

## Doğrulanan davranış

- Cowrie ve paket yakalama verilerinden özellik çıkarımı yapıldı.
- Olay sınıfı ve saldırı taktiği üretildi.
- Güven eşiğini karşılamayan örnekler `Unknown` olarak ayrıldı.
- AI yalnızca analiz/risk üretir; fiziksel izolasyonu doğrudan çalıştırmaz.

## Dökümenteryadaki ölçümler

| Ölçüm | Sonuç |
|---|---:|
| Ham doğruluk | %82,12 |
| Macro F1 | %76,79 |
| Kabul edilen sonuçlarda doğruluk | %88,23 |
| Kapsama | %91,40 |
| Unknown kayıt | 1.217 |

Bu metrikler eğitim verisi, bölme yöntemi ve deney kaydı eklenmeden bağımsız olarak yeniden üretilebilir kabul edilmez. İleride model kartı ve değerlendirme betikleri eklenmelidir.

## Kanıt alanı

![AI değerlendirme raporu](PASTE_IMAGE_URL_HERE_STAGE_07_AI_METRICS)

