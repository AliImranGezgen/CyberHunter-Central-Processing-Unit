# Stage 7 — Yapay Zekâ Analiz Katmanı

**Durum:** ✅ Tamamlandı (prototip çalışma kapsamı)
**Üretim durumu:** 🟡 Bağımsız Cowrie saha değerlendirmesi bekleniyor
**Sorumluluk:** AI ekip bileşeni; Raspberry Pi çalışma ortamı bu repo kapsamında

## Amaç

Kapanmış PCAP dosyalarından ağ özellikleri çıkarmak, bu özellikleri
kalibre edilmiş sınıflandırma modeliyle değerlendirmek ve saldırı sınıfı,
güven değeri, margin ve kabul/Unknown sonucu üretmek.

Normalleştirilmiş Cowrie olayları ağ pencereleriyle ilişkilendirilerek
çıktılara uygulama katmanı bağlamı eklenmektedir.

AI katmanı doğrudan taktik, `0–100` risk skoru veya fiziksel izolasyon
kararı üretmez. Taktik ve risk skoru Publisher katmanında onaylı politika
eşlemeleriyle oluşturulur.

## Sistem kapsamı

Bu aşama aşağıdaki bileşenleri kapsar:

- PCAP dosyalarının kararlı hâle gelmesini bekleme
- Ağ paketlerinden özellik çıkarımı
- Model ön işleme adımları
- Kalibre edilmiş sınıflandırma
- Güven eşiği kontrolü
- Margin kontrolü
- Dağılım dışı örnek (out-of-distribution — OOD) kontrolü
- Düşük güvenli sonuçların `Unknown` olarak işaretlenmesi
- Normalleştirilmiş Cowrie olaylarıyla korelasyon
- JSONL analiz çıktısı üretimi
- Yalnızca kayıt üretme (`log_only`) davranışı

Bu aşama aşağıdaki işlemleri kapsamaz:

- Taktik eşlemesi
- `0–100` risk skoru üretimi
- I2C mesajı oluşturma
- ESP32’ye veri gönderme
- GPIO veya röle kontrolü
- Fiziksel ağ izolasyonu

## Veri akışı

```text
Kapanmış PCAP
→ 39 ağ özelliği
→ Ön işleme artefaktı
→ Kalibre edilmiş model
→ Güven, margin ve OOD kontrolleri
→ attack_class veya Unknown
→ Normalleştirilmiş Cowrie korelasyonu
→ network_ai.jsonl
```

Normalleştirilmiş Cowrie olayları:

```text
/var/lib/cyberhunter/ai/input/cowrie.normalized.jsonl
```

AI çıktıları:

```text
/var/log/cyberhunter/ai/network_ai.jsonl
```

## Raspberry Pi çalışma ortamı

| Bileşen | Değer |
|---|---|
| Servis | `cyberhunter-ai.service` |
| Servis hesabı | `cyberai` |
| Python | 3.11.15 |
| Python ortamı | `/opt/cyberhunter/workspaces/ai/.venv` |
| Çalışan modül | `cyberhunter_ai.watch_pcap` |
| Yapılandırma | `configs/runtime_config.yaml` |
| Kontrol aralığı | 5 saniye |
| Kararlılık süresi | 15 saniye |
| Event input | `normalized_only` |
| Eylem modu | `log_only` |
| Feature version | `2.0.0` |

Servisin `enabled`, `active` ve `running` durumda olduğu doğrulanmıştır.

## Girdi sözleşmesi

Yapılandırmada aşağıdaki değer zorunludur:

```text
event_input: normalized_only
```

Bu değer, olay korelasyonu sırasında yalnızca normalleştirilmiş Cowrie
JSONL verisinin kullanılmasını sağlar. Ham Cowrie günlüklerinin doğrudan
AI korelasyon katmanına verilmesi kabul edilmez.

PCAP dosyaları model özelliklerinin çıkarılmasında kullanılır.
Normalleştirilmiş Cowrie olayları ise zaman, kaynak ve oturum bağlamının
ilişkilendirilmesinde kullanılır.

## Model artefaktları

| Artefakt | Boyut | SHA-256 |
|---|---:|---|
| `calibrated_tree.joblib` | 3.801.802 bayt | `7140e5e6f95d548034137ff2779025e7abc75be6d50921b1924d4cd6f9b7abaa` |
| `preprocessing.joblib` | 2.217 bayt | `2514958ab2b7579e170f5ee346329cb54b119757beb274f5c79591f25fd39a4a` |

Model artefaktlarının bütünlük özetleri kanıt dosyasına kaydedilmiştir.

> Güvenlik uyarısı: Güvenilmeyen joblib veya pickle dosyaları
> yüklenmemelidir. Bu dosyalar açılırken kod çalıştırabilir.

## Model seçimi

Validation Macro F1 sonuçları:

| Model | Validation Macro F1 |
|---|---:|
| Logistic Regression | 0.6252 |
| ANN | 0.7223 |
| Extra Trees | 0.7538 |
| HistGradientBoosting | 0.7679 |

En yüksek validation Macro F1 değerine sahip HistGradientBoosting modeli
seçilmiştir.

Model seçimi yalnızca validation bölümüyle yapılmıştır. Kalibrasyon
verisi ve haricî Cowrie verisi model seçiminde kullanılmamıştır.

## Kalibrasyon ve rejection katmanı

Ayrılmış kalibrasyon verisi deterministik olarak iki bölüme ayrılmıştır:

| Bölüm | Satır sayısı |
|---|---:|
| Calibration fit | 14.154 |
| Rejection tuning | 14.153 |

Sigmoid calibration sonrasında multiclass log loss değeri:

```text
0.4677 → 0.4597
```

Sınıfa özel güven eşikleri ve OOD sınırları sonucunda:

| Ölçüm | Sonuç | Açıklama |
|---|---:|---|
| Validation Macro F1 | %76,79 | Model seçim validation sonucu |
| Kabul edilenlerde iç doğruluk | %88,23 | Rejection-tuning kabul edilenleri |
| İç kapsama | %91,40 | Rejection-tuning kabul oranı |
| Unknown tuning satırı | 1.217 | Reddedilen iç tuning satırı |

Bu değerler bağımsız test veya canlı Cowrie performansı değildir.

Daha önce belirtilen `%82,12` ham doğruluk değerinin kaynak kaydı
bulunamadığı için doğrulanmış metriklerden çıkarılmıştır.

## Runtime çıktı doğrulaması

AI çıktı dosyası:

```text
/var/log/cyberhunter/ai/network_ai.jsonl
```

2026-10-01 doğrulama sonucu:

| Ölçüm | Sonuç |
|---|---:|
| Toplam geçerli JSON çıktısı | 711 |
| Geçersiz JSON satırı | 0 |
| `Credential_Attack` | 658 |
| `Unknown` | 53 |
| `detected` durumu | 658 |
| `unknown` durumu | 53 |
| `log_only` eylemi | 711 |
| Feature version `2.0.0` | 711 |
| Cowrie kanıtı bulunan çıktı | 711 |

Bütün pencerelerde aday sınıf `Credential_Attack` olmuştur. Güven, margin
veya OOD kontrollerini geçemeyen 53 sonuç nihai sınıfta `Unknown`
olarak işaretlenmiştir.

Bu doğrulama yalnızca gözlemlenen runtime verisini açıklar. Diğer saldırı
sınıflarının saha performansını kanıtlamaz.

## AI çıktı sözleşmesi

Ham AI çıktısında bulunan temel alanlar:

```text
timestamp
attack_class
candidate_class
class_id
confidence
margin
status
action
probabilities
reasons
ood_features_outside
features_received
feature_version
cowrie
production_evidence
metadata
```

Ham AI çıktısında aşağıdaki alanlar bulunmamaktadır:

```text
tactic
risk_score
```

Bu alanlar Publisher katmanında:

```text
attack_class
→ tactic_by_event_type
→ risk_score_by_event_type
```

eşlemeleriyle oluşturulmaktadır.

Publisher davranışı [Stage 8](08-ai-publisher.md) kapsamında
doğrulanacaktır.

## Güven ve margin değerleri

Gözlemlenen runtime aralıkları:

| Alan | Minimum | Maksimum |
|---|---:|---:|
| Confidence | 0.44414260656297366 | 0.9957998706820408 |
| Margin | 0.011276975675774126 | 0.9938400975438193 |

Bu aralıklar performans metriği değildir; oluşturulan 711 runtime
çıktısındaki gözlemlenen değer aralıklarıdır.

## Güvenli eylem sınırı

Yapılandırmada aşağıdaki değer zorunludur:

```text
action: log_only
```

`watch_pcap.py`, farklı bir eylem değeri verildiğinde başlatmayı reddeder:

```text
prototype runtime action must be log_only
```

AI kaynak kodunda doğrudan I2C, GPIO, röle veya fiziksel izolasyon
çağrısı bulunmamıştır.

AI katmanının sorumluluğu analiz sonucu üretmek ve kaydetmekle sınırlıdır.

## systemd güvenlik kontrolleri

AI servisine aşağıdaki kontroller uygulanmıştır:

```text
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
```

Girdi dizinleri salt okunurdur:

```text
/var/lib/cyberhunter/ai/captures
/var/lib/cyberhunter/ai/input
```

Yalnızca AI log dizinine yazma izni verilmiştir:

```text
/var/log/cyberhunter/ai
```

## Test sonuçları

| Kontrol | Beklenen sonuç | Gerçekleşen sonuç | Durum |
|---|---|---|---|
| AI servisi | Aktif olmalı | `active/running` | ✅ Başarılı |
| Python ortamı | Sanal ortam olmalı | Python 3.11.15 | ✅ Başarılı |
| Model artefaktları | Bulunmalı | İki artefakt doğrulandı | ✅ Başarılı |
| Model bütünlüğü | Hash alınabilmeli | SHA-256 kaydedildi | ✅ Başarılı |
| JSONL çıktı | Geçerli olmalı | 711/711 geçerli | ✅ Başarılı |
| Unknown davranışı | Düşük güveni reddetmeli | 53 runtime sonucu | ✅ Başarılı |
| Cowrie korelasyonu | Çıktıda bulunmalı | 711/711 | ✅ Başarılı |
| Eylem sınırı | Yalnızca `log_only` | 711/711 | ✅ Başarılı |
| Doğrudan röle/I2C | Bulunmamalı | Kaynak aramasında bulunmadı | ✅ Başarılı |
| Taktik üretimi | Publisher tarafından yapılmalı | Stage 8’e ait | ⬜ Sonraki aşama |
| Risk skoru | Publisher tarafından yapılmalı | Stage 8’e ait | ⬜ Sonraki aşama |
| Yeni canlı tahmin | Kontrollü testte oluşmalı | Son gözlemde oluşmadı | 🟡 Tekrarlanmalı |
| Bağımsız Cowrie testi | Etiketli veriyle yapılmalı | Toplanmadı | ⬜ Planlandı |

## Kanıtlar

- [AI servis durumu](../../evidence/command-outputs/2026-10-01_stage-07_ai-service-status.txt)
- [Model artefaktları ve SHA-256 özetleri](../../evidence/command-outputs/2026-10-01_stage-07_ai-model-artifacts.txt)
- [İç değerlendirme sonuçları](../../evidence/command-outputs/2026-10-01_stage-07_internal-evaluation.txt)
- [Anonimleştirilmiş AI çıktı doğrulaması](../../evidence/command-outputs/2026-10-01_stage-07_ai-output-validation-sanitized.txt)
- [Stage 6 — Normalizer](06-normalizer.md)
- [Stage 8 — AI Publisher](08-ai-publisher.md)

## Sorumluluk sınırı

Model geliştirme, veri kümesi yönetimi ve eğitim süreci AI ekibinin
sorumluluğundadır.

Bu reponun kapsamı:

- Raspberry Pi çalışma ortamı
- Python sanal ortamı
- systemd servisi
- Model artefaktlarının varlık ve bütünlük kanıtı
- Girdi ve çıktı yolları
- Çalışma zamanı doğrulaması
- Cowrie korelasyonu
- Güvenli `log_only` sınırı

olarak belirlenmiştir.

## Bilinen sınırlamalar

- Haricî test verisi toplanmamıştır.
- Bağımsız ve etiketli Cowrie oturumlarıyla değerlendirme yapılmamıştır.
- Gözlemlenen 711 runtime çıktısı yalnızca `Credential_Attack` adayı içermektedir.
- Diğer saldırı sınıflarının saha performansı doğrulanmamıştır.
- Son servis gözleminde yeni tahmin üretilmemiştir.
- `%82,12` ham doğruluk değerinin kaynağı bulunamamıştır.
- NTP senkronizasyonu sistem genelinde henüz doğrulanmamıştır.
- Model dosyaları için imzalı sürümleme mekanizması bulunmamaktadır.
- Model kartı henüz repo içerisinde bulunmamaktadır.

## Sonraki geliştirmeler

- Etiketli Cowrie test oturumlarının oluşturulması
- Normal SSH, port tarama, brute-force, komut çalıştırma ve indirme senaryoları
- Oturum seviyesinde değerlendirme
- Bağımsız test veri setinin kilitlenmesi
- Confusion matrix oluşturulması
- Model kartının eklenmesi
- Model veri kökeninin belgelenmesi
- Model artefaktlarının imzalanması
- Raspberry Pi inference performans ölçümü
- Kontrollü yeni canlı tahmin testi

## Sonuç

AI prototipi Raspberry Pi üzerinde ayrı servis hesabı ve Python sanal
ortamıyla çalışmaktadır. Model ve ön işleme artefaktlarının varlığı,
boyutları ve SHA-256 özetleri doğrulanmıştır.

Model validation Macro F1 değeri `%76,79` olarak kaydedilmiştir.
Rejection-tuning verisinde kabul edilen sonuçlar için iç doğruluk
`%88,23`, kapsama `%91,40` ve Unknown satır sayısı `1.217` olarak
doğrulanmıştır. Bu değerler bağımsız saha performansı değildir.

Runtime çıktı dosyasında 711 geçerli kayıt bulunmuştur. Bunların 658'i
`Credential_Attack`, 53'ü `Unknown` olarak sonuçlanmıştır. Bütün çıktılar
`log_only` modundadır ve Cowrie korelasyon bilgisi içermektedir.

Prototip çalışma ortamı tamamlanmıştır. Bağımsız Cowrie değerlendirmesi,
diğer saldırı sınıflarının testi ve üretim kabulü henüz
tamamlanmamıştır.
