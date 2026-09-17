# Stage 17 — Geçici Röle LED Senaryosu

**Durum:** ✅ Görsel prototip tamamlandı  
**Sorumluluk:** Entegrasyon sınırı

Ethernet hattının fiziksel izolasyonu henüz bağlanmadığı için röle LED'leri davranış göstergesi olarak kullanıldı.

| Koşul | Prototip davranışı |
|---|---|
| Cihaz açılışı | Tüm LED'ler kapalı |
| Risk < eşik | LED'ler kısa aralıklarla açık |
| Risk ≥ eşik | Tüm LED'ler kapalı |
| Geçersiz olay | Röle durumu değişmez |

Bu mantık yalnızca görsel prototip içindir. Gerçek Ethernet veya güç izolasyonunda “enerjili = bağlı” ve “enerjisiz = güvenli” yaklaşımı, elektriksel bağlantı ve tehdit modeline göre yeniden tasarlanmalıdır.

## Kanıt alanı

![Düşük ve yüksek risk LED karşılaştırması](PASTE_IMAGE_URL_HERE_STAGE_17_LED_BEHAVIOR)

