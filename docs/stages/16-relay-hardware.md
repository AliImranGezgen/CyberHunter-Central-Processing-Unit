# Stage 16 — Sekiz Kanallı Röle Bağlantısı

**Durum:** ✅ Prototip testi tamamlandı  
**Sorumluluk:** Entegrasyon sınırı

Fiziksel izolasyon prototipinde 5 V, sekiz kanallı röle modülü kullanıldı. Girişler sırasıyla GPIO `13`, `14`, `18`, `19`, `23`, `25`, `26`, `27` pinlerine bağlandı. Prototipte röle VCC hattı ESP32'nin USB ile beslenen VIN/5V pininden alındı ve GND ortaklandı.

Kartın active-low çalıştığı doğrulandı: `LOW` röleyi etkinleştirip LED'i açar; `HIGH` röleyi pasif hâle getirir. Sekiz kanalın LED ve mekanik çekme davranışı ayrı ayrı test edildi, ESP32'nin yeniden başlamadığı gözlendi.

> Geçici besleme düzeni nihai tasarım değildir. Röle bobin akımı, USB kaynağı, optik izolasyon ve ortak topraklama üretim öncesi elektriksel olarak yeniden değerlendirilmelidir.

## Kanıt alanı

![Sekiz kanallı röle ve ESP32 bağlantısı](PASTE_IMAGE_URL_HERE_STAGE_16_RELAY_WIRING)

