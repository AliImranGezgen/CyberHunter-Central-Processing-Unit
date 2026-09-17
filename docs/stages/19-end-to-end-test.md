# Stage 19 — Uçtan Uca Son Test

**Durum:** ⬜ Planlandı  
**Sorumluluk:** Tüm ekiplerin ortak kabul testi

## Test sırası

1. Raspberry Pi tarih/NTP ve servis sağlıkları doğrulanır.
2. Backend, PostgreSQL, dashboard ve güvenli tünel çalıştırılır.
3. ESP32 config endpoint'i doğrulanır.
4. Güncel firmware derlenir ve cihaza yüklenir.
5. Düşük riskli benzersiz bir olay oluşturulur; `event_id` kaydedilir.
6. Olay Cowrie/Normalizer/AI veya kontrollü test girişinden Bridge'e ulaşır.
7. Inbox Worker I²C üzerinden gönderir; ESP32 response doğrulanır.
8. Düşük riskte beklenen LED/röle davranışı gözlenir.
9. Yüksek riskli ikinci olayla eşik üstü davranış doğrulanır.
10. İki olayın PostgreSQL ve dashboard kaydı aynı `event_id`lerle kontrol edilir.
11. Aynı olay yeniden gönderilerek idempotency testi yapılır.
12. Backend/I²C kesintisi uygulanarak retry ve rejected/archive davranışı ölçülür.

## Kabul kriteri

Tek bir olay kimliği port 22 girişinden dashboard satırına kadar izlenebilmeli; hiçbir aşamada hassas bilgi açık loglanmamalı; yinelenen kayıt oluşmamalı; geçici hata veri kaybına neden olmamalıdır.

## Kanıt alanı

![Uçtan uca event_id izleme](PASTE_IMAGE_URL_HERE_STAGE_19_E2E_TRACE)

