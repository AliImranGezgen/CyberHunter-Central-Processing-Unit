# 11 — ESP32 I²C Arayüzü

Raspberry Pi `/dev/i2c-1` bus'ında master, ESP32 `0x08` adresinde slave olarak çalışır. Pi; JSON hazırlama, AES-GCM koruması, frame'leme, sıra/mesaj kimliği, gönderme, `0xA1` ACK, cevap okuma, timeout, retry ve hata loglamadan sorumludur.

ESP32'nin firmware içi uygulaması kapsam dışıdır. Ortak sözleşme `event_id` eşleşmesi ve `processed:true` başarı kriterini içerir.

