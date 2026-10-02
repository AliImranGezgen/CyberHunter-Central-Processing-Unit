# Stage 6 — Normalizer Servisinin Geliştirilmesi

**Durum:** ✅ Tamamlandı
**Sorumluluk:** Merkezi İşleme Birimi

## Amaç

Cowrie ve SMTP servislerinden gelen farklı ham olay yapılarını tek,
tahmin edilebilir ve sonraki işleme katmanları tarafından kullanılabilir
bir CyberHunter olay şemasına dönüştürmek.

## Normalizasyon akışı

```text
Cowrie JSONL veya SMTP JSONL
→ cyberhunter-normalizer.timer
→ cyberhunter-normalizer.service
→ cyberhunter_ai.pipeline
→ Kaynağa uygun normalizer
→ Ortak CyberHunter JSONL şeması
```

## Ortak olay şeması

Normalleştirilmiş olaylar aşağıdaki üst seviye alanları içerir:

```text
schema_version
event_id
timestamp
sensor
source
raw_event_type
event_type
session_id
network
identity
details
```

Eksik veya kaynak olayda bulunmayan isteğe bağlı değerler `unknown`
değeriyle temsil edilir.

## Uygulanan işlevler

- Kaynağa göre Cowrie veya SMTP normalizer seçimi
- Deterministik UUIDv5 `event_id` üretimi
- Ham olay türünün `raw_event_type` alanında korunması
- Ortak `event_type` değerine dönüştürme
- Ağ bilgilerinin `network` nesnesine taşınması
- Kimlik bilgilerinin `identity` nesnesine taşınması
- Kaynağa özgü bilgilerin `details` nesnesine taşınması
- Eksik isteğe bağlı alanlarda `unknown` kullanılması
- Cowrie komut olaylarının ortak komut olayına dönüştürülmesi
- SMTP gönderici olaylarının ortak SMTP olayına dönüştürülmesi
- JSONL girdi ve çıktı desteği

## Cowrie komut eşlemesi

Aşağıdaki Cowrie olayı:

```text
cowrie.command.input
```

şu ortak olay türüne dönüştürülür:

```text
command.executed
```

Komut içeriği aşağıdaki alanda korunur:

```text
details.command
```

2026-10-01 doğrulamasında iki `cowrie.command.input` olayının ikisi de
`command.executed` olarak eşlenmiş ve `details.command` alanında
korunmuştur.

## SMTP eşlemesi

Kontrollü testte aşağıdaki sentetik SMTP olayı kullanılmıştır:

```json
{
  "event_type": "mail_from",
  "timestamp": "2026-10-01T11:50:00Z",
  "source_ip": "192.0.2.20",
  "source_port": 40123,
  "mail_from": "sender@example.invalid"
}
```

Test sonucunda:

```text
source: smtp
raw_event_type: mail_from
event_type: smtp.sender.declared
event_id UUID version: 5
network protocol: smtp
destination port: 2525
```

değerleri üretilmiştir.

Test verisinde yalnızca dokümantasyon için ayrılmış IP adresi ve alan adı
kullanılmıştır.

## Servis çalışma modeli

Normalizer aşağıdaki systemd birimleriyle çalışmaktadır:

```text
cyberhunter-normalizer.service
cyberhunter-normalizer.timer
```

Servis `oneshot` türündedir. Timer tarafından her dakika tetiklenir,
normalizasyon tamamlandıktan sonra kapanır.

Bu nedenle:

```text
cyberhunter-normalizer.service → static / inactive
cyberhunter-normalizer.timer   → enabled / active
```

durumu beklenen çalışma biçimidir.

Timer yapılandırması:

```text
OnBootSec=2min
OnUnitActiveSec=1min
AccuracySec=5s
Persistent=true
```

## Canlı uygulama

Raspberry Pi üzerinde kullanılan pipeline:

```text
/opt/cyberhunter/workspaces/ai/src/cyberhunter_ai/pipeline.py
```

Kaynağa özgü normalizasyon işlevleri:

```text
/opt/cyberhunter/workspaces/ai/src/cyberhunter_ai/normalizer.py
```

Çalıştırma biçimi:

```text
/usr/bin/python3 -m cyberhunter_ai.pipeline
```

Normalizer şu anda sistem Python 3.12.3 ortamını kullanmaktadır. Uygun
sanal ortama taşınması Stage 3 kapsamında açık iyileştirme olarak
kaydedilmiştir.

## Repo kaynak kodu

Repo içerisinde ortak olay şemasını uygulayan taşınabilir normalizer
kaynak kodu ve birim testleri bulunmaktadır:

- [`src/cyberhunter_cpu/normalizer.py`](../../src/cyberhunter_cpu/normalizer.py)
- [`tests/unit/test_normalizer.py`](../../tests/unit/test_normalizer.py)

Repodaki testler aşağıdaki davranışları kontrol eder:

- Cowrie komut eşlemesi
- Komut içeriğinin korunması
- Deterministik olay kimliği
- SMTP gönderici eşlemesi
- Bilinmeyen kaynakların reddedilmesi

Raspberry Pi uygulaması `cyberhunter_ai` paket adını, repo uygulaması ise
`cyberhunter_cpu` paket adını kullanmaktadır. Güncellemelerde iki
uygulamanın davranış sözleşmesi birlikte korunmalıdır.

## Cowrie doğrulama sonucu

2026-10-01 tarihinde gerçekleştirilen doğrulama:

| Ölçüm | Sonuç |
|---|---:|
| Ham Cowrie olayı | 56 |
| Normalleştirilmiş olay | 56 |
| Geçersiz JSON satırı | 0 |
| UUIDv5 event_id | 56 |
| Eksik event_id | 0 |
| Tekrarlanan event_id | 0 |
| `command.executed` olayı | 2 |
| `details.command` bulunan olay | 2 |
| `event_type=unknown` | 30 |

Daha önce belirtilen `754 olay` sayısı güncel kanıtla desteklenmediği için
bu belgeden çıkarılmıştır.

## Unknown olay analizi

Normalleştirilmiş 30 olayın ortak `event_type` değeri `unknown` olarak
üretilmiştir:

| Ham olay türü | Sayı | Durum |
|---|---:|---|
| `cowrie.command.failed` | 28 | 🟡 Eşleme planlandı |
| `cowrie.client.var` | 2 | 🟡 Eşleme planlandı |

Bu olaylar kaybedilmemiştir. Ham olay türleri `raw_event_type` alanında
korunmuş ve ortak JSON şemasıyla çıktı dosyasına yazılmıştır.

Önerilen gelecekteki eşlemeler:

```text
cowrie.command.failed → command.failed
cowrie.client.var     → client.variable.detected
```

Bu değerler uygulanmadan önce AI ve dashboard sözleşmeleriyle birlikte
değerlendirilmelidir.

## Test sonuçları

| Kontrol | Beklenen sonuç | Gerçekleşen sonuç | Durum |
|---|---|---|---|
| Timer | Aktif olmalı | `active` | ✅ Başarılı |
| Timer başlangıcı | Etkin olmalı | `enabled` | ✅ Başarılı |
| Çalışma aralığı | Bir dakika | Doğrulandı | ✅ Başarılı |
| Ham/çıktı sayısı | Eşit olmalı | 56/56 | ✅ Başarılı |
| JSONL geçerliliği | Hatalı satır olmamalı | 0 hatalı satır | ✅ Başarılı |
| UUIDv5 kimlikleri | Her olayda bulunmalı | 56/56 | ✅ Başarılı |
| Tekrarlanan kimlik | Olmamalı | 0 | ✅ Başarılı |
| Cowrie komut eşlemesi | Komut korunmalı | 2/2 | ✅ Başarılı |
| SMTP normalizasyonu | Ortak şema üretilmeli | Sentetik test başarılı | ✅ Başarılı |
| Unknown fallback | Ham tür korunmalı | `raw_event_type` korundu | ✅ Başarılı |
| Olay eşleme kapsamı | Bilinen türler eşlenmeli | İki tür için eksik | 🟡 İyileştirme |

## Kanıtlar

- [Normalizer servis ve timer durumu](../../evidence/command-outputs/2026-10-01_stage-06_normalizer-service-status.txt)
- [Cowrie normalizasyon doğrulaması](../../evidence/command-outputs/2026-10-01_stage-06_normalizer-output-validation-sanitized.txt)
- [Kontrollü SMTP normalizasyon testi](../../evidence/command-outputs/2026-10-01_stage-06_smtp-normalization-test.txt)
- [Örnek normalleştirilmiş olay](../../examples/normalized-event.example.json)

## Güvenlik sınırı

Normalizer tarafından işlenen bütün olaylar güvenilir olmayan dış veri
olarak kabul edilmelidir.

- Komut alanları hiçbir koşulda çalıştırılmamalıdır.
- Kullanıcı tarafından sağlanan metinler shell komutuna dönüştürülmemelidir.
- Gerçek parolalar normalleştirilmiş çıktıda paylaşılmamalıdır.
- IP adresleri herkese açık kanıtlarda anonimleştirilmelidir.
- Ham Cowrie ve SMTP logları doğrudan repoya eklenmemelidir.
- JSON alanları tüketici katmanlarında tekrar doğrulanmalıdır.
- Dosya yolları sabit ve izinleri sınırlandırılmış olmalıdır.

## Bilinen sınırlamalar

- Normalizer sistem Python ortamını kullanmaktadır.
- `cowrie.command.failed` için özel eşleme bulunmamaktadır.
- `cowrie.client.var` için özel eşleme bulunmamaktadır.
- Canlı üretim çıktısında yalnızca Cowrie kaynaklı olaylar bulunmaktadır.
- SMTP işlevi sentetik olayla doğrulanmıştır; üretim SMTP akışı ayrıca test edilmelidir.
- Repo ve Raspberry Pi uygulamaları farklı Python paket adları kullanmaktadır.
- NTP senkronizasyonu sistem genelinde henüz doğrulanmamıştır.

## Sonuç

Normalizer servisi Cowrie olaylarını ortak CyberHunter JSONL şemasına
başarıyla dönüştürmektedir. Ham ve normalleştirilmiş olay sayılarının
eşit olduğu, bütün çıktıların geçerli JSON olduğu ve her olayın UUIDv5
kimliği içerdiği doğrulanmıştır.

Cowrie komut eşlemesi ve sentetik SMTP normalizasyonu başarıyla test
edilmiştir. Bilinmeyen olay türleri kaybedilmeden `raw_event_type`
alanında korunmaktadır.

Temel normalizasyon işlevi tamamlanmıştır. İki Cowrie olay türünün özel
eşlemelerinin eklenmesi, sanal ortam geçişi ve üretim SMTP entegrasyonu
iyileştirme görevleri olarak devam etmektedir.
