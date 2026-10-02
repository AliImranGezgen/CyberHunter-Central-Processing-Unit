# Stage 12 — ESP32 Olay Doğrulama Katmanı

**Durum:** ✅ Tamamlandı
**Tamamlanma kapsamı:** Prototip firmware kaynak incelemesi, Raspberry Pi
doğrulama testleri ve başarılı gerçek ESP32 cevabı
**Sorumluluk:** ESP32 entegrasyon sınırı; Raspberry Pi tarafındaki doğrulama
ve cevap kabul koşulları bu repo kapsamındadır

## Amaç

Raspberry Pi'den ESP32'ye ulaşan olayların şifre çözme, JSON ayrıştırma, şema
ve değer kontrollerinden geçirilmesini; yalnızca geçerli olayların işlenmesini
ve Raspberry Pi'ye olayla ilişkilendirilebilir bir cevap döndürülmesini
sağlamak.

## Doğrulama katmanları

Olay, ESP32 uygulama mantığına ulaşmadan önce birden fazla kontrolden geçer:

```text
I2C frame kontrolü
→ CRC-16 kontrolü
→ Frame yeniden birleştirme
→ AES-256-GCM kimlik doğrulaması
→ JSON ayrıştırma
→ Şema kontrolü
→ Değer ve uzunluk kontrolü
→ Olay işleme
→ Backend kayıt sonucu
→ Şifreli ESP32 cevabı
```

## Raspberry Pi tarafındaki olay sözleşmesi

Inbox Worker olayın tam olarak dokuz zorunlu alan içermesini bekler:

| Alan | Beklenen tür veya sınır |
|---|---|
| `event_id` | Boş olmayan metin, en fazla 40 karakter |
| `timestamp` | Boş olmayan metin |
| `source_ip` | Boş olmayan metin |
| `destination_port` | Tam sayı, `1–65535` |
| `protocol` | Boş olmayan metin |
| `event_type` | Boş olmayan metin |
| `command` | Boş olmayan metin, en fazla 256 karakter |
| `tactic` | Boş olmayan metin |
| `risk_score` | Tam sayı, `0–100` |

Raspberry Pi doğrulayıcısı eksik ve fazladan alanları reddeder. Boolean
değerler Python'da tam sayı alt türü olmasına rağmen `risk_score` ve
`destination_port` için ayrıca reddedilir.

### Timestamp sınırı

Raspberry Pi tarafı `timestamp` alanının yalnızca boş olmayan bir metin
olduğunu kontrol eder. Kontrollü testte `gecersiz-zaman` değeri kabul
edilmiştir. Bu nedenle Raspberry doğrulayıcısının ISO 8601 biçimini kontrol
ettiği iddia edilmez.

ESP32 firmware'i ise tarih-saat alanında aşağıdaki yapıyı denetler:

- `YYYY-MM-DDTHH:MM:SSZ` biçimi
- İsteğe bağlı kesirli saniye bölümü
- Ay, gün, saat, dakika ve saniye sınırları
- Şubat ve artık yıl gün sayısı
- Son karakterin `Z` olması

## ESP32 JSON ve şema doğrulaması

Firmware kaynak incelemesinde ArduinoJson `deserializeJson()` ile ayrıştırma
yapıldığı doğrulandı.

ESP32 aşağıdaki dokuz alanın türünü kontrol eder:

```text
event_id            → metin
timestamp           → metin
source_ip           → metin
destination_port    → tam sayı
protocol            → metin
event_type          → metin
command             → metin
tactic              → metin
risk_score          → tam sayı
```

Değer kontrolleri:

| Kontrol | Kabul edilen değer |
|---|---|
| `event_id` | Boş değil, en fazla 40 karakter |
| `timestamp` | Firmware'in doğruladığı UTC biçimi |
| `command` | En fazla 256 karakter |
| `destination_port` | `1–65535` |
| `risk_score` | `0–100` |

`source_ip`, `protocol`, `event_type` ve `tactic` alanlarında firmware tür
kontrolü yapar. Kaynak incelemesinde IP adresinin sözdizimini veya protokolün
izin verilen bir listede bulunmasını denetleyen ek bir kontrol görülmemiştir.

## Hata kodları

Firmware kaynak kodunda aşağıdaki hata cevapları tanımlanmıştır:

| Hata kodu | Üretilme koşulu |
|---|---|
| `invalid_json` | JSON ayrıştırılamadığında veya kök değer nesne olmadığında |
| `invalid_schema` | Zorunlu alanlardan biri yoksa ya da türü yanlışsa |
| `invalid_value` | Uzunluk, timestamp, port veya risk sınırı geçersizse |
| `aes_auth_failed` | AES-GCM kimlik doğrulaması veya şifre çözme başarısızsa |

Bu hata yolları firmware kaynak kodu üzerinden doğrulanmıştır. Bu aşamada
bozuk ciphertext veya geçersiz JSON gerçek I2C hattına kasıtlı olarak
gönderilerek ayrı bir donanım negatif testi yapılmamıştır.

## Frame ve kriptografik kontroller

ESP32, olay blob'unu oluşturan frame'lerde aşağıdaki kontrolleri uygular:

- 32 bayt frame uzunluğu
- `0xC7` magic değeri
- Protokol sürümü
- Frame türü
- CRC-16 doğrulaması
- Mesaj kimliği tutarlılığı
- Sıra numarası
- Toplam frame sayısı
- Payload uzunluğu
- Toplam blob uzunluğu
- Eksiksiz yeniden birleştirme

Yeniden birleştirme tamamlandıktan sonra `mbedtls_gcm_auth_decrypt()` ile
AES-256-GCM kimlik doğrulaması ve şifre çözme gerçekleştirilir. Başarısız
sonuç olay işleme fonksiyonuna aktarılmaz.

## ESP32 cevap sözleşmesi

İşlenen olay için ESP32 aşağıdaki alanları üretir:

| Alan | Anlamı |
|---|---|
| `event_id` | Gönderilen olayın kimliği |
| `device_id` | Cevabı üreten ESP32 kimliği |
| `input_risk_score` | Raspberry Pi'den alınan risk skoru |
| `esp32_risk_score` | ESP32'nin cevapta bildirdiği risk skoru |
| `decision` | Risk seviyesine göre üretilen karar |
| `processed` | Backend kayıt işleminin başarı durumu |

Firmware'de `processed` değeri yalnızca JSON ayrıştırmasının başarılı olduğunu
göstermez. Bu alan, ESP32'nin olayı HTTPS backend'e gönderme işlemi başarılı
bir `2xx` cevapla tamamlandığında `true` olur.

## Raspberry Pi cevap kabul koşulları

Inbox Worker bir ESP32 cevabını başarılı saymak için iki koşulu zorunlu tutar:

```python
response.get("event_id") == event_id
response.get("processed") is True
```

`event_id` uyuşmazsa çalışma zamanı hatası oluşturulur. `processed` tam olarak
`true` değilse olay başarı sayılmaz ve retry politikası uygulanır.

## Gerçek cevap doğrulaması

Kontrollü entegrasyon testinde aşağıdaki cevap alınmıştır:

```json
{
  "event_id": "evt-stage09-20261001T122857Z",
  "device_id": "esp32-cyberhunter-01",
  "input_risk_score": 0,
  "esp32_risk_score": 0,
  "decision": "safe",
  "processed": true
}
```

Doğrulanan sonuçlar:

| Kontrol | Sonuç | Durum |
|---|---|---|
| İstek `event_id` | `evt-stage09-20261001T122857Z` | Bilgi |
| Cevap `event_id` | İstekle aynı | ✅ Başarılı |
| `device_id` | `esp32-cyberhunter-01` | ✅ Mevcut |
| Risk skorları | `0` ve `0` | ✅ Mevcut |
| Karar | `safe` | ✅ Mevcut |
| `processed` | `true` | ✅ Başarılı |
| Worker sonucu | `success` | ✅ Başarılı |
| Toplam deneme | 2 | Bilgi |

İlk denemede `processed: false` cevabı alınmış ve Inbox Worker bunu başarı
olarak kabul etmemiştir. İkinci denemede `processed: true` alınmış, olay
başarılı sayılmış ve arşive taşınmıştır.

## Firmware kaynak doğrulaması

İncelenen dosya:

```text
CyberHunterV2.ino
```

Kaynak dosya özeti:

| Özellik | Değer |
|---|---|
| Dosya boyutu | 13.239 bayt |
| Satır sayısı | 53 |
| SHA-256 | `2a1e8e8418c2d3e60b692060fbf2c69fa36cc794b11b6365ef675ac0760e61dd` |

Bu özet, incelenen kaynak sürümünü tanımlar. Çalışan ESP32 üzerindeki binary
ile kaynak dosya arasında kriptografik firmware attestation yapılmamıştır.
Derleme ve karta yükleme kanıtları Stage 18 kapsamında ayrıca ele alınacaktır.

## Kritik güvenlik bulgusu

İncelenen ham `.ino` dosyasında aşağıdaki hassas yapılandırmaların kaynak kod
içinde tanımlandığı görülmüştür:

- Wi-Fi SSID ve parolası
- Backend/servis adresleri
- 32 baytlık AES anahtarı

Bu değerlerin kendileri dokümana veya kanıt dosyalarına alınmamıştır.

> Ham `CyberHunterV2.ino` dosyası mevcut hâliyle public GitHub reposuna
> eklenmemelidir. Gerçek değerler daha önce herkese açık bir konuma
> yüklendiyse Wi-Fi parolası ve AES anahtarı değiştirilmelidir.

Firmware repoya eklenmeden önce hassas değerler kaynak koddan çıkarılmalı;
örnek yapılandırmada yalnızca aşağıdaki gibi placeholder değerler
kullanılmalıdır:

```text
<WIFI_SSID>
<WIFI_PASSWORD>
<BACKEND_URL>
<AES_256_KEY>
```

## Kanıtlar

- [Raspberry Pi olay doğrulama testi](../../evidence/command-outputs/2026-10-01_stage-12_raspberry-validation.txt)
- [Raspberry Pi cevap kabul sözleşmesi](../../evidence/command-outputs/2026-10-01_stage-12_response-contract.txt)
- [Anonimleştirilmiş firmware inceleme özeti](../../evidence/command-outputs/2026-10-01_stage-12_firmware-validation-summary.txt)
- [Gerçek ESP32 cevap doğrulaması](../../evidence/test-results/2026-10-01_stage-12_esp32-response-validation.txt)
- [Stage 10 şifreli I2C gidiş-dönüş testi](../../evidence/test-results/2026-10-01_stage-10_encrypted-i2c-roundtrip.txt)
- [Stage 11 AES-GCM doğrulaması](../../evidence/test-results/2026-10-01_stage-11_aes-gcm-validation.txt)

Bu aşamada ekran görüntüsü yerine aranabilir metin kanıtları kullanılmıştır.

## Açık iyileştirmeler

1. Raspberry Pi tarafına gerçek ISO 8601 timestamp doğrulaması eklemek.
2. `source_ip` için IPv4/IPv6 sözdizimi kontrolü eklemek.
3. `protocol`, `event_type` ve `tactic` alanları için izin verilen değerleri
   ortak şemada tanımlamak.
4. Firmware'deki Wi-Fi bilgilerini, URL'leri ve AES anahtarını kaynak koddan
   çıkarmak.
5. `invalid_json`, `invalid_schema`, `invalid_value` ve `aes_auth_failed`
   yollarını gerçek donanım üzerinde kontrollü negatif testlerle doğrulamak.
6. Derlenen firmware ile incelenen kaynak sürümünü hash veya imzalı sürüm
   bilgisiyle ilişkilendirmek.
7. ESP32 hata cevaplarına mümkün olduğunda güvenli korelasyon kimliği eklemek.

## Sonuç

Raspberry Pi ve ESP32 tarafındaki olay doğrulama katmanları kaynak kod ve
kontrollü testlerle incelenmiştir. Dokuz alanlı olay sözleşmesi, risk ve port
sınırları, uzunluk kontrolleri, ESP32 timestamp doğrulaması, AES-GCM kimlik
doğrulaması ve cevap üretimi doğrulanmıştır.

Gerçek entegrasyon testinde ESP32 cevabındaki `event_id` istekle eşleşmiş ve
`processed: true` alınmıştır. Stage 12, prototip olay doğrulama ve başarılı
cevap entegrasyonu kapsamında tamamlanmıştır. Negatif donanım testleri,
firmware secret yönetimi ve binary attestation üretim sertleştirmesi olarak
açık bırakılmıştır.