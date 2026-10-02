# Stage 16 — Sekiz Kanallı Röle Test Sonucu

**Tarih:** 2026-10-01  
**Test ortamı:** ESP32 ve 5 V sekiz kanallı röle modülü  
**Test türü:** Yüksüz GPIO, gösterge LED’i ve mekanik röle testi  
**Sonuç:** ✅ Başarılı, açılış geçişi uyarısıyla

## Amaç

ESP32’ye bağlı sekiz röle kanalının GPIO seviyelerini, active-low kontrol
mantığını, test sonundaki pasif durumu ve test sırasında ESP32’nin yeniden
başlayıp başlamadığını doğrulamak.

Rölelerin `COM`, `NO` ve `NC` kontaklarına test sırasında gerçek ağ hattı,
şebeke elektriği veya başka bir yük bağlanmamıştır.

## Kanal eşlemesi

| Kanal | ESP32 GPIO | Etkin komut | Pasif komut |
|---:|---:|---|---|
| 1 | `13` | `LOW` | `HIGH` |
| 2 | `14` | `LOW` | `HIGH` |
| 3 | `18` | `LOW` | `HIGH` |
| 4 | `19` | `LOW` | `HIGH` |
| 5 | `23` | `LOW` | `HIGH` |
| 6 | `25` | `LOW` | `HIGH` |
| 7 | `26` | `LOW` | `HIGH` |
| 8 | `27` | `LOW` | `HIGH` |

## Başlangıç çıktısı

```text
=== CyberHunter Stage 16 Relay Test ===
BOOT_COUNT=1
RESET_REASON=1
ACTIVE_LEVEL=LOW
INACTIVE_LEVEL=HIGH
CHANNEL_COUNT=8
INITIALIZED CHANNEL=1 GPIO=13 STATE=OFF
INITIALIZED CHANNEL=2 GPIO=14 STATE=OFF
INITIALIZED CHANNEL=3 GPIO=18 STATE=OFF
INITIALIZED CHANNEL=4 GPIO=19 STATE=OFF
INITIALIZED CHANNEL=5 GPIO=23 STATE=OFF
INITIALIZED CHANNEL=6 GPIO=25 STATE=OFF
INITIALIZED CHANNEL=7 GPIO=26 STATE=OFF
INITIALIZED CHANNEL=8 GPIO=27 STATE=OFF
```

`RESET_REASON=1`, test başlangıcındaki normal power-on reset durumudur. Test
sırasında yeni bir başlangıç dizisi veya artan `BOOT_COUNT` gözlenmemiştir.

## Kanal çıktıları

```text
TEST_START

CHANNEL=1 GPIO=13 COMMAND=LOW EXPECTED=ON
CHANNEL=1 GPIO=13 READBACK=LOW
CHANNEL=1 GPIO=13 COMMAND=HIGH EXPECTED=OFF

CHANNEL=2 GPIO=14 COMMAND=LOW EXPECTED=ON
CHANNEL=2 GPIO=14 READBACK=LOW
CHANNEL=2 GPIO=14 COMMAND=HIGH EXPECTED=OFF

CHANNEL=3 GPIO=18 COMMAND=LOW EXPECTED=ON
CHANNEL=3 GPIO=18 READBACK=LOW
CHANNEL=3 GPIO=18 COMMAND=HIGH EXPECTED=OFF

CHANNEL=4 GPIO=19 COMMAND=LOW EXPECTED=ON
CHANNEL=4 GPIO=19 READBACK=LOW
CHANNEL=4 GPIO=19 COMMAND=HIGH EXPECTED=OFF

CHANNEL=5 GPIO=23 COMMAND=LOW EXPECTED=ON
CHANNEL=5 GPIO=23 READBACK=LOW
CHANNEL=5 GPIO=23 COMMAND=HIGH EXPECTED=OFF

CHANNEL=6 GPIO=25 COMMAND=LOW EXPECTED=ON
CHANNEL=6 GPIO=25 READBACK=LOW
CHANNEL=6 GPIO=25 COMMAND=HIGH EXPECTED=OFF

CHANNEL=7 GPIO=26 COMMAND=LOW EXPECTED=ON
CHANNEL=7 GPIO=26 READBACK=LOW
CHANNEL=7 GPIO=26 COMMAND=HIGH EXPECTED=OFF

CHANNEL=8 GPIO=27 COMMAND=LOW EXPECTED=ON
CHANNEL=8 GPIO=27 READBACK=LOW
CHANNEL=8 GPIO=27 COMMAND=HIGH EXPECTED=OFF

FINAL_OUTPUT_STATE=ALL_OFF
TEST_RESULT=PASS
TEST_COMPLETE
```

## Fiziksel gözlem

Test sırasında:

- Sekiz röle kartı LED’inin yandığı gözlemlendi.
- Kanalların ilerleyen test sırasıyla kapandığı görüldü.
- Rölelerin mekanik anahtarlama sesi duyuldu.
- Test bittikten sonra bütün gösterge LED’leri kapalı kaldı.
- ESP32’nin yeniden başlamadığı gözlemlendi.

Bu gözlem, röle kartının GPIO komutlarına görsel ve mekanik tepki verdiğini
göstermektedir. Röle kontaklarının elektriksel durumu multimetreyle ayrıca
ölçülmemiştir.

## Açılış geçişi bulgusu

Test firmware’i yüklendikten sonraki açılış aşamasında röle LED’lerinin geçici
olarak açık olduğu gözlemlenmiştir. GPIO pinleri firmware tarafından pasif
seviyeye geçirildikçe LED’ler kapanmıştır.

Bu gözlem önemlidir: yalnızca `setup()` içindeki yazılım başlangıcına güvenmek,
fiziksel izolasyon sisteminde güvenli başlangıcı garanti etmez.

Üretim tasarımında değerlendirilmesi gerekenler:

- Röle girişleri için güvenli donanımsal pull-up/pull-down düzeni
- Ayrı sürücü veya global enable hattı
- Röle bobinleri için ayrı ve yeterli 5 V güç kaynağı
- ESP32 ve röle kartı için doğru ortak referans/toprak tasarımı
- Brownout ve yeniden başlama testleri
- Açılış sırasında rölelerin fiziksel olarak pasif tutulması

## Test değerlendirmesi

| Kontrol | Sonuç |
|---|---|
| Sekiz GPIO tanımlandı | ✅ Başarılı |
| Her kanalda `LOW` readback alındı | ✅ Başarılı |
| Her kanal için `HIGH` pasif komutu gönderildi | ✅ Başarılı |
| Test sonunda bütün çıkışlar pasif | ✅ Başarılı |
| Active-low kontrol mantığı | ✅ Doğrulandı |
| Gösterge LED tepkisi | ✅ Gözlemlendi |
| Mekanik anahtarlama sesi | ✅ Gözlemlendi |
| ESP32 test sırasında yeniden başladı mı? | ✅ Hayır |
| Açılışta geçici röle etkinleşmesi | ⚠️ Gözlemlendi |
| Röle kontağı süreklilik testi | ⬜ Yapılmadı |
| Gerçek ağ/güç hattı izolasyonu | ⬜ Yapılmadı |
| Sekiz kanal uzun süreli eş zamanlı yük testi | ⬜ Yapılmadı |

## Sonuç

Sekiz GPIO çıkışının active-low röle kartını kontrol edebildiği, bütün
kanalların yazılım testinden geçtiği, kartın görsel ve mekanik tepki verdiği ve
test sonunda bütün çıkışların pasif duruma döndüğü doğrulanmıştır.

Açılış sırasında geçici röle etkinleşmesi gözlendiği için mevcut düzen üretim
tipi fiziksel izolasyon sistemi olarak kabul edilmemelidir.