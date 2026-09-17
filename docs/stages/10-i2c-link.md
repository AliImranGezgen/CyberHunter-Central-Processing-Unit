# Stage 10 — Raspberry Pi ve ESP32 Arasında I²C

**Durum:** ✅ Tamamlandı  
**Sorumluluk:** Raspberry tarafı bu repo kapsamında; firmware entegrasyon sınırında

## Bağlantı

| Raspberry Pi | ESP32 / değer |
|---|---|
| SDA | GPIO21 |
| SCL | GPIO22 |
| GND | GND |
| `/dev/i2c-1` | I²C bus |
| Hedef adres | `0x08` |

## Protokol

Büyük JSON mesajları küçük frame'lere bölünür. Frame'lerde mesaj kimliği ve sıra bilgisi bulunur; ESP32 parçaları yeniden birleştirir. İşlem sonrasında Raspberry'ye `0xA1` ACK ve olay cevabı gönderilir. Inbox Worker'ın kullandığı istemcinin ACK destekli `esp32_tests/esp32_client.py` sürümü olduğu doğrulanmıştır.

## Kanıt alanı

![Raspberry Pi–ESP32 I²C bağlantısı](PASTE_IMAGE_URL_HERE_STAGE_10_I2C_WIRING)

