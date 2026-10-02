# Stage 13 — ESP32'nin Backend'e Bağlanması

**Durum:** ✅ Olay POST entegrasyonu doğrulandı
**Tamamlanma kapsamı:** ESP32 olay gönderimi, HTTP `2xx` başarı koşulu ve
Raspberry Pi'ye sonuç aktarımı
**Sorumluluk:** Backend kapsam dışı bileşendir; bu repo yalnızca ESP32–backend
arayüz sözleşmesini ve Raspberry Pi'ye yansıyan sonucu belgeler

## Amaç

ESP32'nin I²C üzerinden aldığı ve doğruladığı güvenlik olayını Wi-Fi üzerinden
backend'e iletmesi, backend sonucunu değerlendirmesi ve işlem durumunu
Raspberry Pi'ye şifreli cevap olarak döndürmesi.

Bu aşama backend uygulamasının iç kodunu, PostgreSQL yapısını veya dashboard
uygulamasını doğrulamaz.

## Doğrulanan HTTP sözleşmesi

Firmware kaynak incelemesinde üç ayrı backend işlemi belirlendi:

| İşlem | HTTP yöntemi | Endpoint | Runtime durumu |
|---|---|---|---|
| Güvenlik olayı gönderme | `POST` | `/api/security-events` | ✅ Doğrulandı |
| Güvenlik olayı sorgulama | `POST` | `/api/security-events/query` | 🟡 Kaynak kodda mevcut |
| Cihaz yapılandırması alma | `GET` | `/api/device-config/esp32-cyberhunter-01` | 🟡 Kaynak kodda mevcut |

> Önceki taslakta sorgulama endpoint'i için `GET` yazılmıştır. Güncel firmware
> kaynak kodu `/api/security-events/query` çağrısını `POST` yöntemiyle
> gerçekleştirmektedir.

## Olay gönderme akışı

```text
Raspberry Pi olayı
→ I2C üzerinden ESP32
→ AES-GCM ve şema doğrulaması
→ ESP32 karar üretimi
→ HTTPS POST /api/security-events
→ Backend HTTP cevabı
├── 2xx → processed: true
└── diğer/hata → processed: false
→ Şifreli ESP32 cevabı
→ Raspberry Pi Inbox Worker
```

## Backend'e gönderilen olay alanları

Firmware, doğrulanmış olaydan aşağıdaki alanlarla backend isteği hazırlar:

```text
event_id
timestamp
source_ip
destination_port
protocol
event_type
command
tactic
input_risk_score
esp32_risk_score
decision
processed
device_id
```

ESP32, `input_risk_score` ve `esp32_risk_score` alanlarına mevcut prototipte
aynı risk değerini yazar. Bu durum ESP32 üzerinde bağımsız ikinci model
çıktısının henüz bu akışta kullanılmadığını gösterir.

## HTTP başarı kriteri

Firmware'deki olay gönderme fonksiyonu yalnızca aşağıdaki aralıktaki cevapları
başarılı kabul eder:

```text
200 <= HTTP durum kodu < 300
```

Backend POST işleminin sonucu `saved` değerine aktarılır. Raspberry Pi'ye
dönen cevapta:

```text
processed = saved
```

ilişkisi kullanılır. Bu nedenle `processed: true`, yalnızca ESP32'nin JSON
olayını ayrıştırdığı anlamına gelmez; backend POST işleminin bir `2xx` cevabıyla
tamamlandığını gösterir.

## Gerçek entegrasyon sonucu

Kontrollü testte ESP32'nin Raspberry Pi'ye döndürdüğü cevap:

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

Bu cevapta:

- `event_id` gönderilen olayla eşleşmiştir.
- `processed` değeri `true` olmuştur.
- Inbox Worker olayı `success` olarak kaydetmiştir.
- Olay Bridge `archive` dizinine taşınmıştır.

Firmware kaynak mantığıyla birlikte değerlendirildiğinde bu sonuç, güvenlik
olayının backend'e gönderilmesi ve backend'den `2xx` cevap alınması zincirini
doğrular.

## Başarısızlık ve yeniden deneme davranışı

İlk kontrollü denemede ESP32 şu sonucu üretmiştir:

```text
processed: false
```

Inbox Worker bu cevabı başarı olarak kabul etmemiş ve olayı yeniden denemek
üzere kuyruğa almıştır. İkinci denemede `processed: true` alınmış ve olay
arşivlenmiştir.

Bu davranış backend hatasının başarılı teslim olarak işaretlenmesini engeller.
ESP32 üzerinde kalıcı bir olay kuyruğu bulunduğu doğrulanmamıştır; güvenilir
yeniden deneme Raspberry Pi Bridge katmanı tarafından sağlanır.

## Wi-Fi bağlantı yönetimi

Firmware aşağıdaki bağlantı davranışlarını uygular:

- ESP32 başlangıcında `WiFi.begin()` çağrılır.
- Bağlantı durumu düzenli olarak kontrol edilir.
- Bağlantı koptuğunda `WiFi.reconnect()` denenir.
- Yeniden bağlantı başarısız olursa `WiFi.begin()` tekrar çağrılır.
- Backend isteği öncesinde DNS çözümlemesi `WiFi.hostByName()` ile kontrol
  edilir.
- Wi-Fi bağlı değilse HTTP işlemi başlatılmaz ve hata sonucu üretilir.

Bu mekanizma Wi-Fi bağlantısını yeniden kurmayı hedefler. Uzun süreli bağlantı
kesintisi, erişim noktası değişimi ve yeniden başlatma sonrası toparlanma ayrı
dayanıklılık testleriyle henüz ölçülmemiştir.

## Sorgulama ve cihaz yapılandırması

Firmware'de güvenlik olayı sorgulaması için:

```text
POST /api/security-events/query
```

çağrısı bulunur. Sorgu gövdesi backend'e iletilir ve başarılı `2xx` cevap
şifrelenerek Raspberry Pi'ye döndürülür. Bu akış kaynak kodda doğrulanmış,
ancak mevcut Stage 13 kanıtlarında ayrı bir başarılı runtime sorgusu
gösterilmemiştir.

Cihaz yapılandırması için:

```text
GET /api/device-config/esp32-cyberhunter-01
```

çağrısı kullanılır. Dönen yapılandırmada cihaz kimliği ve izolasyon eşiği
kontrol edilir. Bu işlev dinamik eşik aşamasında ayrıca belgelenir.

## HTTPS ve sertifika doğrulaması

Firmware `WiFiClientSecure` ve `https://` adresleri kullanmaktadır. Ancak
istemci kurulurken:

```cpp
setInsecure();
```

çağrısı yapılmaktadır. Bu nedenle trafik TLS ile şifreleniyor olsa da sunucu
sertifikasının güvenilirliği doğrulanmamaktadır.

> Mevcut yapı prototip geliştirme bağlantısıdır. Sertifika doğrulaması kapalı
> olduğu için üretim seviyesinde güvenli HTTPS bağlantısı olarak kabul
> edilmemelidir.

Üretim sürümünde CA sertifikası veya sertifika/public-key pinning
kullanılmalı; bağlantı geçerli hostname ve sertifika zinciriyle
doğrulanmalıdır.

## Geçici adresleme ve yapılandırma riski

İncelenen firmware kaynak kodunda geçici bir ngrok alan adının doğrudan
tanımlandığı görülmüştür. Gerçek alan adı kanıt dosyalarına alınmamıştır.

Ayrıca ham firmware içinde aşağıdaki hassas değerler bulunmaktadır:

- Wi-Fi SSID
- Wi-Fi parolası
- Backend ve yapılandırma adresleri
- AES anahtarı

Ham firmware mevcut hâliyle public repoya eklenmemelidir. Adresler ve gizli
değerler kaynak koddan ayrılmalıdır.

Önerilen ayrım:

```text
Firmware kaynak kodu
├── doğrulama ve haberleşme mantığı
└── secrets.example.h
    ├── <WIFI_SSID>
    ├── <WIFI_PASSWORD>
    ├── <BACKEND_BASE_URL>
    └── <AES_256_KEY>

Yerel ve paylaşılmayan dosya
└── secrets.h
```

Gerçek `secrets.h` dosyası `.gitignore` kapsamına alınmalıdır.

## Kanıtlar

- [Anonimleştirilmiş HTTP sözleşmesi](../../evidence/command-outputs/2026-10-01_stage-13_firmware-http-contract.txt)
- [Backend POST entegrasyon sonucu](../../evidence/test-results/2026-10-01_stage-13_backend-post-validation.txt)
- [Gerçek ESP32 cevap doğrulaması](../../evidence/test-results/2026-10-01_stage-12_esp32-response-validation.txt)
- [Stage 12 firmware doğrulama özeti](../../evidence/command-outputs/2026-10-01_stage-12_firmware-validation-summary.txt)

Bu aşamada ekran görüntüsü yerine hassas adresleri göstermeyen aranabilir metin
kanıtları kullanılmıştır.

## Doğrulanan ve bekleyen bileşenler

| Bileşen | Durum | Açıklama |
|---|---|---|
| Olay POST isteği | ✅ Doğrulandı | `processed: true` ile backend `2xx` sonucu doğrulandı |
| Event ID korelasyonu | ✅ Doğrulandı | İstek ve cevap kimlikleri eşleşti |
| Backend hata sonucu | ✅ Doğrulandı | `processed: false` retry oluşturdu |
| Wi-Fi reconnect mantığı | ✅ Kaynakta mevcut | `reconnect()` ve yeniden `begin()` kullanılıyor |
| Query endpoint uygulaması | ✅ Kaynakta mevcut | `POST /api/security-events/query` |
| Query runtime testi | ⬜ Planlandı | Başarılı gerçek sorgu kanıtı gerekli |
| Config endpoint uygulaması | ✅ Kaynakta mevcut | `GET /api/device-config/...` |
| TLS sertifika doğrulaması | 🔴 Uygulanmadı | `setInsecure()` kullanılıyor |
| Kalıcı üretim adresi | ⬜ Planlandı | Geçici ngrok adresi kaldırılmalı |
| ESP32 kalıcı offline kuyruğu | ⬜ Doğrulanmadı | Retry Raspberry Pi tarafından sağlanıyor |

## Açık iyileştirmeler

1. `setInsecure()` kullanımını kaldırıp CA doğrulaması veya pinning eklemek.
2. Geçici ngrok adresini firmware kaynak kodundan çıkarmak.
3. Wi-Fi ve backend yapılandırmasını paylaşılmayan bir secret dosyasına veya
   güvenli provisioning sürecine taşımak.
4. `/api/security-events/query` için gerçek runtime test kanıtı eklemek.
5. Config endpoint'inin başarılı, hatalı ve erişilemez durumlarını test etmek.
6. Uzun süreli Wi-Fi kesintisi ve yeniden bağlantı testleri yapmak.
7. Backend'e aynı `event_id` ile yinelenen POST gönderiminin idempotency
   davranışını doğrulamak.
8. ESP32 ve backend saat sapması davranışını değerlendirmek.

## Sonuç

ESP32 firmware'inin doğrulanmış güvenlik olayını
`POST /api/security-events` üzerinden backend'e gönderdiği ve yalnızca HTTP
`2xx` sonucunda Raspberry Pi'ye `processed: true` bildirdiği kaynak kod ve
gerçek entegrasyon cevabıyla doğrulanmıştır.

Stage 13, olay POST entegrasyonu kapsamında tamamlanmıştır. Query ve config
endpoint'leri kaynak kodda mevcuttur ancak ayrı runtime kanıtları beklemektedir.
TLS sertifika doğrulaması ve kalıcı secret/adres yönetimi üretim öncesinde
tamamlanması gereken güvenlik görevleridir.