# Stage 18 — Güncel ESP32 Kodunun Hazırlanması

**Durum:** 🟡 Devam ediyor  
**Sorumluluk:** ESP32 ekibi; arayüz doğrulaması bu repo kapsamında

Mevcut I²C, AES-GCM, Wi-Fi ve backend hattı korunarak sekiz kanallı röle kontrolü ve dinamik config alma davranışı eklendi. Sabit eşik kaldırıldı; `device_id` ve eşik aralığı doğrulaması ile Serial Monitor gözlemleri hazırlandı.

## Tamamlanmayan doğrulamalar

- Arduino IDE'de güncel kaynakla temiz derleme
- ESP32'ye yükleme ve yeniden başlatma
- Eski ngrok adresinin yapılandırmadan çıkarılması
- Düşük/yüksek risk olaylarıyla gerçek röle testi
- Config ulaşılamadığında son geçerli eşik/fail-safe testi

Bu aşama, derleme ve donanım kanıtları eklenene kadar “tamamlandı” olarak işaretlenmez.

## Kanıt alanı

![Arduino derleme ve Serial Monitor](PASTE_IMAGE_URL_HERE_STAGE_18_ARDUINO_BUILD)

