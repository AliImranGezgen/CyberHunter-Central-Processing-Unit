# Stage 12 — ESP32 Olay Doğrulama Katmanı

**Durum:** ✅ Tamamlandı  
**Sorumluluk:** Entegrasyon sınırı

## Doğrulamalar

- JSON parse ve zorunlu alan kontrolü
- `risk_score` için `0–100` aralığı
- Port, zaman damgası, komut uzunluğu ve event ID kontrolü
- AES-GCM kimlik doğrulaması
- Raspberry'ye aynı `event_id` ile cevap dönülmesi

Hata kodları `invalid_json`, `invalid_schema`, `invalid_value` ve `aes_auth_failed` olarak tanımlandı. Başarılı cevap `device_id`, girdi/ESP32 risk skoru, karar ve `processed` alanlarını taşır.

Merkezi İşleme Birimi açısından başarı kriteri, cevaptaki `event_id`nin gönderilen olayla eşleşmesi ve `processed` değerinin `true` olmasıdır. Inbox Worker bu iki koşulu kontrol eder.

## Kanıt alanı

![ESP32 doğrulama ve response](PASTE_IMAGE_URL_HERE_STAGE_12_ESP32_RESPONSE)

