# Stage 8 — AI Publisher ve Olay Paketleme

**Durum:** ✅ Tamamlandı  
**Sorumluluk:** AI ekip bileşeni; Raspberry servis entegrasyonu bu repo kapsamında

## Amaç

AI tahminlerini ESP32 hattının beklediği dokuz alanlı, atomik JSON olaylarına dönüştürmek.

## Olay sözleşmesi

Zorunlu alanlar: `event_id`, `timestamp`, `source_ip`, `destination_port`, `protocol`, `event_type`, `command`, `tactic`, `risk_score`.

Publisher sonuçları `/var/lib/cyberhunter/ai/output` dizinine yazar. Çoklu brute-force oturumlarının tek olaya indirgenmesi ve boş komutlarda dürüst bir fallback kullanılması geçmiş çalışmada ele alınmıştır.

Örnek başarı sonucu `Credential_Attack`, `Credential Access`, `risk_score: 55` olarak kaydedilmiştir. Servis adı `cyberhunter-ai-publisher.service`tir; anonimleştirilmiş unit örneği `configs/systemd/` altındadır.

## Kanıt alanı

![AI Publisher atomik olay çıktısı](PASTE_IMAGE_URL_HERE_STAGE_08_PUBLISHER)

