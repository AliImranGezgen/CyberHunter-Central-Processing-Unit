# Stage 11 — I²C Veri Güvenliği

**Durum:** ✅ Tamamlandı  
**Sorumluluk:** Raspberry–ESP32 ortak protokolü

## Amaç

Fiziksel I²C hattında taşınan olayların açık metin okunmasını ve değiştirilmesini zorlaştırmak; gizlilik ve bütünlük sağlamak.

## Tasarım

- JSON olay AES-256-GCM ile şifrelenir.
- Her mesaj için benzersiz nonce üretilir.
- Authentication tag ile bütünlük ve kimlik doğrulama kontrol edilir.
- Şifreli içerik frame'lere bölünür; ESP32 yeniden birleştirip doğrular.
- Kimlik doğrulaması başarısız olan veri işlenmez.

## Doğrulama

Dökümenteryada `FRAME REASSEMBLY OK`, `AES-GCM AUTH OK`, `DECRYPT OK` ve `EVENT_ID MATCH OK` sonuçlarının alındığı kaydedilmiştir.

> Anahtarın repoya konması yasaktır. Anahtar yaşam döngüsü, döndürme ve cihaz provisioning prosedürü ayrı güvenlik dokümanı gerektirir.

## Kanıt alanı

![AES-GCM ve frame doğrulama çıktısı](PASTE_IMAGE_URL_HERE_STAGE_11_AES_GCM)

