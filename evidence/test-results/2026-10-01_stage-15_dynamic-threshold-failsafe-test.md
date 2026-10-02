# Stage 15 — Dinamik Eşik ve Fail-safe Test Sonucu

**Tarih:** 2026-10-01  
**Cihaz:** `esp32-cyberhunter-01`  
**Kontrollü risk skoru:** `55`  
**Son geçerli izolasyon eşiği:** `70`

## Amaç

Dashboard/backend üzerinden değiştirilen izolasyon eşiğinin ESP32 tarafından
alındığını, risk karşılaştırmasında kullanıldığını, config isteği başarısız
olduğunda son geçerli değerin korunduğunu ve başarısız olayın Raspberry Pi
tarafından yeniden denendiğini doğrulamak.

## Test A — Backend eşik değerleri

| Beklenen eşik | HTTP durumu | API değeri | Eşleşme | Sonuç |
|---:|---:|---:|---|---|
| `20` | `200` | `20` | `True` | ✅ Başarılı |
| `70` | `200` | `70` | `True` | ✅ Başarılı |

Her iki değer aynı `device_id` için dashboard üzerinden kaydedilmiş ve backend
API üzerinden okunmuştur.

## Test B — Geçerli eşik ile normal işlem

Kontrollü olay:

```text
event_id: evt-s15-load70-150451
risk_score: 55
isolation_threshold: 70
```

ESP32 çıktısının ilgili bölümü:

```text
AES_GCM=OK TYPE=1 LENGTH=263
CONFIG=OK ESIK=70
ROLE_LED=ACIK
HTTP_CODE=201
EVENT=evt-s15-load70-150451 RISK=55 ESIK=70 DECISION=warning ROLE_LED=ACIK HTTP=201
TX TAMAMLANDI
```

Raspberry state sonucu:

```json
{
  "status": "success",
  "attempts": 1,
  "event_id": "evt-s15-load70-150451",
  "response": {
    "event_id": "evt-s15-load70-150451",
    "device_id": "esp32-cyberhunter-01",
    "input_risk_score": 55,
    "esp32_risk_score": 55,
    "decision": "warning",
    "processed": true
  }
}
```

Sonuç: `55 < 70` olduğu için prototip izolasyon komutu uygulanmamış ve olay
backend tarafından `HTTP 201` ile kaydedilmiştir.

## Test C — Config erişimi kesildiğinde son geçerli değerin korunması

Backend geçici olarak durdurulmuş, ESP32 açık ve aynı çalışma oturumunda
bırakılmıştır. Ardından risk skoru `55` olan kontrollü olay gönderilmiştir.

```text
event_id: evt-s15-retain70-150625
risk_score: 55
önceki geçerli eşik: 70
```

ESP32 çıktısının anonimleştirilmiş ilgili bölümü:

```text
AES_GCM=OK TYPE=1 LENGTH=267
CONFIG_HTTP=502
HTTP_CODE=502
EVENT=evt-s15-retain70-150625 RISK=55 ESIK=70 DECISION=warning ROLE_LED=ACIK HTTP=502
TX TAMAMLANDI
```

Uzun HTTP hata gövdesi, geçici tünel ve altyapı ayrıntıları içerebildiği için
kanıt dosyasına alınmamıştır.

İlk Raspberry state sonucu:

```json
{
  "status": "retry_scheduled",
  "attempts": 1,
  "event_id": "evt-s15-retain70-150625",
  "file": "evt-s15-retain70-150625.json",
  "response_summary": {
    "input_risk_score": 55,
    "esp32_risk_score": 55,
    "decision": "warning",
    "processed": false
  }
}
```

Sonuç:

- Config isteği `HTTP 502` ile başarısız olmuştur.
- ESP32 son geçerli eşik olan `70` değerini korumuştur.
- Karşılaştırma `55 < 70` olarak devam etmiştir.
- Backend kaydı başarısız olduğu için `processed:false` dönmüştür.
- Raspberry Pi olay dosyasını kaybetmeden retry kuyruğuna almıştır.

## Test D — Backend geri geldikten sonra retry

Backend yeniden çalıştırılmış ve aynı olay tekrar işlenmiştir.

```text
FRAME REASSEMBLY: OK
AES-GCM AUTH    : OK
AES-GCM DECRYPT : OK
EVENT_ID MATCH  : OK
status          : success
event_id        : evt-s15-retain70-150625
attempts        : 2
archive         : /var/lib/cyberhunter/bridge/archive/evt-s15-retain70-150625.json
```

İlk denemede başarısız olan aynı `event_id`, backend geri geldikten sonra ikinci
denemede başarıyla tamamlanmış ve archive dizinine taşınmıştır.

## Test E — Kuyruk ve timer son durumu

Test sonunda:

```text
Inbox: boş
Processing: boş

Archive:
evt-s15-load70-150451.json
evt-s15-retain70-150625.json
evt-s15-retain70-150634.json
evt-s15-retain70-150728.json

Inbox Worker timer:
enabled
active
```

Son olayın state sonucu:

```json
{
  "status": "success",
  "attempts": 1,
  "event_id": "evt-s15-retain70-150728",
  "response": {
    "event_id": "evt-s15-retain70-150728",
    "device_id": "esp32-cyberhunter-01",
    "input_risk_score": 55,
    "esp32_risk_score": 55,
    "decision": "warning",
    "processed": true
  }
}
```

Son manuel worker kontrolünde kuyruk boş olduğu için aşağıdaki sonuç alınmıştır:

```text
status: empty
```

## Değerlendirme

| Kontrol | Sonuç |
|---|---|
| Dashboard/backend eşik güncellemesi | ✅ Başarılı |
| Eşik `20` API okuması | ✅ Başarılı |
| Eşik `70` API okuması | ✅ Başarılı |
| ESP32'nin eşik `70` değerini alması | ✅ Başarılı |
| `55 < 70` karşılaştırması | ✅ Başarılı |
| Config hatasında son geçerli değerin korunması | ✅ Başarılı |
| Backend hatasında `processed:false` | ✅ Başarılı |
| Raspberry retry planlaması | ✅ Başarılı |
| İkinci denemede başarı | ✅ Başarılı |
| Event ID korelasyonu | ✅ Başarılı |
| Inbox ve processing temizliği | ✅ Başarılı |
| Timer'ın yeniden etkinleşmesi | ✅ Başarılı |
| İlk açılışta config alınamaması | ⬜ Kaynakta doğrulandı, çalışma zamanı testi yapılmadı |
| Fiziksel röle kontağı ve gerçek hat izolasyonu | ⬜ Bu testin kapsamında değil |

## Güvenlik ve kapsam notları

- Gerçek yerel IP adresi kanıt içeriğine alınmamıştır.
- Geçici tünel adresi ve HTTP hata sayfası yayımlanmamıştır.
- Wi-Fi parolası, API anahtarı ve AES anahtarı paylaşılmamıştır.
- `decision=warning`, dinamik izolasyon kararını değil risk sınıfını gösterir.
- Bu test röle/LED komutunu doğrular; fiziksel röle kontaklarının gerçek ağı
  kestiğini kanıtlamaz.