# Stage 17 — Geçici Röle LED Senaryosu

**Durum:** ✅ Görsel prototip ve dinamik eşik senaryosu doğrulandı
**Sorumluluk:** Entegrasyon sınırı

## Amaç

Gerçek Ethernet veya güç hattı henüz röle kontaklarına bağlanmadığı için
izolasyon kararını sekiz kanallı röle modülünün gösterge LED’leri üzerinden
görsel olarak doğrulamak.

Bu aşamada LED durumu fiziksel izolasyonun kendisi değil, ESP32’nin ürettiği
röle komutunun göstergesidir.

## Prototip davranışı

| Koşul | İzolasyon kararı | Röle bobini | LED |
|---|---|---|---|
| Firmware başlangıcı tamamlandı, eşik bekleniyor | Beklemede | Enerjisiz | Kapalı |
| `risk_score < isolation_threshold` | Pasif | Enerjili | Açık |
| `risk_score >= isolation_threshold` | Aktif | Enerjisiz | Kapalı |
| Geçersiz olay | Karar üretilmez | Mevcut durum korunur | Değişmez |
| Config hatası ve önceki geçerli eşik mevcut | Son geçerli eşik kullanılır | Karşılaştırmaya göre | Karşılaştırmaya göre |

Röle kartı active-low çalışmaktadır:

```text
LOW  → Röle bobini enerjili → LED açık
HIGH → Röle bobini enerjisiz → LED kapalı
```

## Açılış geçişi

Stage 16 donanım testinde ESP32 boot aşamasında, GPIO pinleri firmware
tarafından yapılandırılmadan önce röle LED’lerinin geçici olarak açılabildiği
gözlemlenmiştir.

Ana firmware başlangıcı tamamlandığında:

```text
ROLELER=KAPALI ESIK=BEKLENIYOR
```

sonucu alınmış ve röleler kapalı duruma getirilmiştir.

Bu nedenle “cihaz açılışında LED’ler her zaman kapalıdır” iddiası
kullanılmamaktadır. Üretim tasarımında boot süresince pasif durumu garanti eden
donanımsal bir enable veya güvenli giriş seviyesi gereklidir.

## Senaryo A — Risk 55, eşik 50

Karşılaştırma:

```text
55 >= 50
```

Doğrulanan çıktı:

```text
CONFIG=OK ESIK=50
ISOLATION=ACTIVE
RELAY_COIL=DEENERGIZED
LED=OFF
FEEDBACK=UNVERIFIED
HTTP_CODE=201
```

Sonuç:

- Dinamik eşik `50` olarak alındı.
- Risk skoru eşik değerine eşit veya yüksek bulundu.
- İzolasyon kararı aktif üretildi.
- Röle bobini enerjisiz duruma geçirildi.
- Gösterge LED’leri kapandı.

![Risk 55 ve eşik 50 için aktif izolasyon kararı](../../evidence/screenshots/2026-10-01_stage-17_risk55-threshold50_isolation-active_sanitized.png)

## Senaryo B — Risk 55, eşik 70

Karşılaştırma:

```text
55 < 70
```

Doğrulanan çıktı:

```text
CONFIG=OK ESIK=70
ISOLATION=PASSIVE
RELAY_COIL=ENERGIZED
LED=ON
FEEDBACK=UNVERIFIED
HTTP_CODE=201
```

Sonuç:

- Dinamik eşik `70` olarak alındı.
- Risk skoru eşik değerinin altında bulundu.
- İzolasyon kararı pasif üretildi.
- Röle bobini enerjili duruma geçirildi.
- Gösterge LED’leri açıldı.

![Risk 55 ve eşik 70 için pasif izolasyon kararı](../../evidence/screenshots/2026-10-01_stage-17_risk55-threshold70_isolation-passive_sanitized.png)

Pasif senaryo görselinde Serial Monitor’daki son test olayı ile dashboard’da
açık olan olay farklı `event_id` değerleri taşımaktadır. Bu görsel uçtan uca
olay korelasyonu için kullanılmaz; yalnızca eşik, röle komutu ve LED durumunu
kanıtlar.

## Risk sınıfı ve izolasyon kararının ayrımı

Her iki senaryoda risk skoru `55` olduğu için risk sınıfı `warning` olarak
kalmıştır. Değişen değer dinamik izolasyon eşiğidir.

| Risk | Eşik | Risk sınıfı | İzolasyon |
|---:|---:|---|---|
| `55` | `50` | `warning` | Aktif |
| `55` | `70` | `warning` | Pasif |

Bu ayrım, risk sınıflandırması ile fiziksel kontrol politikasının birbirinden
bağımsız olduğunu gösterir.

## Kanıtlar

- [Anonimleştirilmiş röle karar çıktıları](../../evidence/command-outputs/2026-10-01_stage-17_relay-decision-output-sanitized.txt)
- [Dinamik eşik ve röle LED test sonucu](../../evidence/test-results/2026-10-01_stage-17_dynamic-threshold-test.md)
- [Aktif izolasyon görseli](../../evidence/screenshots/2026-10-01_stage-17_risk55-threshold50_isolation-active_sanitized.png)
- [Pasif izolasyon görseli](../../evidence/screenshots/2026-10-01_stage-17_risk55-threshold70_isolation-passive_sanitized.png)

## Doğrulama sınırı

Serial Monitor’da:

```text
FEEDBACK=UNVERIFIED
```

sonucu görülmüştür. Bu nedenle test:

- Risk/eşik karşılaştırmasını doğrular.
- ESP32 izolasyon kararını doğrular.
- Röle bobini komutunu doğrular.
- Gösterge LED durumunu doğrular.
- Backend’in olayı kabul ettiğini doğrular.

Ancak test:

- Röle kontaklarının fiziksel durumunu doğrulamaz.
- Ethernet hattının gerçekten kesildiğini kanıtlamaz.
- Güç hattının gerçekten kesildiğini kanıtlamaz.
- Üretim tipi elektriksel fail-safe davranışını kanıtlamaz.

## Sonuç

Aynı `55` risk skoru için eşik `50` olduğunda aktif, eşik `70` olduğunda pasif
izolasyon kararı üretildiği doğrulanmıştır. Röle modülünün LED durumları bu
kararlara uygun biçimde değişmiştir.

Bu aşama görsel prototip doğrulamasıdır. Gerçek fiziksel izolasyon iddiası,
röle kontakları ve gerçek hat üzerinde elektriksel test yapılmadan
kullanılmamalıdır.