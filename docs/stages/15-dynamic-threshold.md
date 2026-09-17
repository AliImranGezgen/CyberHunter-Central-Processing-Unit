# Stage 15 — Dinamik İzolasyon Eşiği

**Durum:** ✅ Entegrasyon doğrulandı  
**Sorumluluk:** Dashboard/backend/ESP32 ortak sözleşmesi

İzolasyon eşiğinin firmware içinde sabit `70` tutulması bırakıldı. Dashboard'da cihaz bazlı belirlenen değer, `GET /api/device-config/esp32-cyberhunter-01` uç noktasından alınır.

Beklenen cevap:

```json
{
  "device_id": "esp32-cyberhunter-01",
  "isolation_threshold": 70
}
```

Karar koşulu `risk_score >= isolation_threshold` şeklindedir. Config isteği başarısız olursa son geçerli değer kullanılır; cihaz daha önce geçerli eşik almamışsa röle durumu değiştirilmez. Bu fail-safe davranış son testte ayrıca kanıtlanmalıdır.

## Kanıt alanı

![Dashboard eşik ayarı ve config endpoint](PASTE_IMAGE_URL_HERE_STAGE_15_THRESHOLD)

