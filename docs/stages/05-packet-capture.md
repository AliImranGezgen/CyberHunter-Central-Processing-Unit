# Stage 5 — Ağ Paketlerinin Yakalanması

**Durum:** ✅ Tamamlandı
**Sorumluluk:** Merkezi İşleme Birimi

## Amaç

Cowrie uygulama loglarını ağ seviyesindeki kanıtlarla ilişkilendirmek ve
AI katmanının ilerleyen aşamalarda kullanabileceği paket yakalama
girdilerini hazırlamak.

Bu aşama PCAP üretimini ve Cowrie olaylarıyla temel korelasyonu kapsar.
Paketlerden AI özelliklerinin çıkarılması ve model tarafından
kullanılması sonraki aşamalarda doğrulanacaktır.

## Paket yakalama mimarisi

```text
wlan0 üzerindeki TCP trafiği
→ Port 22 veya port 2222 filtresi
→ tcpdump
→ Aktif .pcap.part dosyası
→ Beş dakikalık rotasyon
→ Kapanmış .pcap dosyası
→ AI işleme dizini
```

## Yapılan çalışmalar

- `wlan0` arayüzü için bağımsız paket yakalama servisi oluşturuldu.
- Yalnızca TCP port `22` ve port `2222` trafiğini seçen filtre uygulandı.
- Paket yakalama aracı olarak `tcpdump` kullanıldı.
- Aktif yakalama dosyaları `.pcap.part` uzantısıyla ayrıldı.
- Tamamlanan yakalama dosyaları `.pcap` uzantısıyla saklandı.
- Her yakalama aralığı 300 saniye, yani beş dakika olarak yapılandırıldı.
- Servis `cyberhunter-ai-capture.service` adıyla systemd üzerinden yönetildi.
- Servisin sistem başlangıcında etkin ve aktif olduğu doğrulandı.
- Cowrie kontrollü bağlantısı ile PCAP kaydı zaman ve ağ bilgileri üzerinden eşleştirildi.
- Ham PCAP dosyalarının GitHub reposuna eklenmesi `.gitignore` ile engellendi.

## Servis yapılandırması

| Alan | Değer |
|---|---|
| Servis | `cyberhunter-ai-capture.service` |
| Yakalama aracı | `/usr/bin/tcpdump` |
| Ağ arayüzü | `wlan0` |
| Trafik filtresi | `tcp port 22 or tcp port 2222` |
| Yakalama süresi | 300 saniye |
| Aktif dosya uzantısı | `.pcap.part` |
| Kapanmış dosya uzantısı | `.pcap` |
| Depolama dizini | `/var/lib/cyberhunter/ai/captures/` |
| systemd durumu | `active (running)` |
| Başlangıç durumu | `enabled` |
| Servis kullanıcısı | `root` |
| Snap length | Tam paket (`-s 0`) |

## Dosya rotasyonu

Aktif yakalama sırasında dosya aşağıdaki biçimde oluşturulur:

```text
capture-<UTC_TIMESTAMP>.pcap.part
```

Beş dakikalık yakalama tamamlandıktan sonra dosya aşağıdaki biçime
dönüştürülür:

```text
capture-<UTC_TIMESTAMP>.pcap
```

Bu ayrım, AI veya başka bir tüketicinin henüz yazılmakta olan PCAP
dosyasını işlemeye çalışmasını önler.

## PCAP dosya değerlendirmesi

PCAP dosya başlığının boyutu 24 bayttır. Bu nedenle:

- 24 baytlık dosya, geçerli PCAP başlığı içerir fakat paket içermez.
- 24 bayttan büyük dosya, filtreyle eşleşen en az bir paket içerir.

Kontrol sırasında hem boş zaman aralıkları hem de gerçek paket içeren
PCAP dosyaları gözlemlenmiştir.

Örnek paket içeren dosyalar:

| Dosya | Boyut | Değerlendirme |
|---|---:|---|
| `capture-20261001T110237Z.pcap` | 25.380 bayt | Paket içeriyor |
| `capture-20261001T110737Z.pcap` | 5.250 bayt | Paket içeriyor |
| `capture-20261001T111737Z.pcap` | 5.250 bayt | Paket içeriyor |

## Cowrie–PCAP korelasyonu

Stage 4 kapsamında port `22` üzerinden kontrollü bir SSH bağlantısı
oluşturulmuştur.

Cowrie aşağıdaki olayları üretmiştir:

```text
cowrie.client.kex
cowrie.session.closed
```

Cowrie anahtar değişimi olayı:

```text
2026-10-01T11:18:22.538978Z
```

Türkiye saati karşılığı:

```text
2026-10-01T14:18:22.538978+03:00
```

Aynı bağlantının paketleri aşağıdaki PCAP dosyasında bulunmuştur:

```text
capture-20261001T111737Z.pcap
```

PCAP zaman aralığı:

```text
2026-10-01 14:18:22.327636
→
2026-10-01 14:18:22.566179
```

Cowrie oturum kapanış zamanı:

```text
2026-10-01 14:18:22.563699+03:00
```

PCAP içinde aynı bağlantıya ait toplam 24 paket görülmüştür. TCP bağlantı
kurulumu, SSH sürüm bildirimi, şifreli SSH paketleri ve TCP kapanış
paketleri kaydedilmiştir.

Eşleştirme aşağıdaki alanlarla yapılmıştır:

- Olay zamanı
- Kaynak IP adresi
- Hedef IP adresi
- Kaynak port
- Hedef port `22`
- TCP protokolü
- SSH bağlantı başlangıcı ve kapanışı

PCAP dosyasında Cowrie oturum kimliği bulunmadığı için oturum kimliği
doğrudan eşleştirme alanı değildir.

## Test sonuçları

| Kontrol | Beklenen sonuç | Gerçekleşen sonuç | Durum |
|---|---|---|---|
| Capture servisi | Aktif olmalı | `active (running)` | ✅ Başarılı |
| Başlangıç durumu | Etkin olmalı | `enabled` | ✅ Başarılı |
| Ağ arayüzü | `wlan0` kullanılmalı | Script ile doğrulandı | ✅ Başarılı |
| Port filtresi | Port `22` ve `2222` | Filtre doğrulandı | ✅ Başarılı |
| Aktif dosya | `.pcap.part` olmalı | Aktif süreçte görüldü | ✅ Başarılı |
| Kapanmış dosya | `.pcap` olmalı | Depolama dizininde görüldü | ✅ Başarılı |
| Dosya rotasyonu | 300 saniye | Çalışan süreçte doğrulandı | ✅ Başarılı |
| Paket içeren PCAP | 24 bayttan büyük olmalı | Birden fazla dosya bulundu | ✅ Başarılı |
| Cowrie korelasyonu | Aynı bağlantı bulunmalı | 24 paketle eşleştirildi | ✅ Başarılı |
| AI tarafından tüketim | Sonraki aşamada doğrulanmalı | Bu aşamanın kapsamında değil | ⬜ Planlandı |

## Kanıtlar

- [Paket yakalama servisi](../../evidence/command-outputs/2026-10-01_stage-05_capture-service-status.txt)
- [Anonimleştirilmiş yakalama yapılandırması](../../evidence/command-outputs/2026-10-01_stage-05_capture-configuration-sanitized.txt)
- [PCAP depolama metadata bilgileri](../../evidence/command-outputs/2026-10-01_stage-05_pcap-storage-metadata-sanitized.txt)
- [Cowrie ve PCAP korelasyonu](../../evidence/command-outputs/2026-10-01_stage-05_cowrie-pcap-correlation-sanitized.txt)
- [Stage 4 — Cowrie SSH Honeypot](04-cowrie-honeypot.md)

## Güvenlik ve veri yönetimi

PCAP dosyaları aşağıdaki hassas bilgileri içerebilir:

- Kaynak ve hedef IP adresleri
- Kaynak ve hedef portlar
- İstemci yazılım sürümleri
- Ağ protokolü özellikleri
- Şifrelenmemiş protokol başlıkları
- Trafik zamanları ve davranış kalıpları
- Uygulamaya bağlı olarak payload verileri

Bu nedenle:

- Ham PCAP dosyaları herkese açık repoya eklenmez.
- PCAP dosyaları paylaşılmadan önce içerik incelemesi yapılır.
- Gerçek IP adresleri anonimleştirilir.
- Gereksiz payload verileri paylaşılmaz.
- Dosyalara yalnızca gerekli servis hesapları erişebilmelidir.
- Saklama ve otomatik silme politikası hazırlanmalıdır.

## Bilinen sınırlamalar

- Paket yakalama servisi `root` hesabıyla çalışmaktadır.
- `tcpdump`, `-Z root` seçeneğiyle ayrıcalıklarını korumaktadır.
- `-s 0` seçeneği paketlerin tamamının yakalanmasına neden olmaktadır.
- PCAP saklama süresi henüz belgelenmemiştir.
- Boş trafik aralıklarında 24 baytlık başlık dosyaları oluşmaktadır.
- NTP servisi aktif olsa da güncel sistem senkronizasyonu henüz doğrulanmamıştır.
- PCAP üretimi doğrulanmıştır; AI özellik çıkarımı bu aşamada doğrulanmamıştır.

## Planlanan güvenlik iyileştirmeleri

- Paket yakalama için ayrı servis hesabı oluşturulması
- Gerekli Linux capability değerlerinin belirlenmesi
- `CAP_NET_RAW` kullanımının değerlendirilmesi
- Gerekirse `CAP_NET_ADMIN` kullanımının değerlendirilmesi
- `-Z root` kullanımının kaldırılması
- Snap length değerinin veri minimizasyonuna göre değerlendirilmesi
- PCAP saklama ve otomatik silme süresinin tanımlanması
- Disk kullanım kotası veya üst sınır oluşturulması
- systemd sandbox seçeneklerinin eklenmesi

## Sonuç

CyberHunter paket yakalama servisi `wlan0` arayüzünde port `22` ve
`2222` trafiğini kaydedecek şekilde yapılandırılmıştır. Servisin aktif
ve sistem başlangıcında etkin olduğu doğrulanmıştır.

Aktif ve kapanmış PCAP dosyaları birbirinden ayrılmış, beş dakikalık
dosya rotasyonu doğrulanmış ve gerçek paket içeren PCAP dosyaları
oluşturulmuştur.

Kontrollü SSH bağlantısı hem Cowrie JSON olay günlüğünde hem de PCAP
dosyasında zaman ve ağ bilgileri üzerinden eşleştirilmiştir. Böylece
uygulama katmanı olayı ile ağ katmanı kanıtı arasında temel korelasyon
başarıyla doğrulanmıştır.