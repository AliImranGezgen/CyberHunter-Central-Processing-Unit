# Stage 11 — I²C Veri Güvenliği

**Durum:** ✅ Tamamlandı
**Tamamlanma kapsamı:** Prototip kriptografik taşıma ve kontrollü güvenlik
doğrulamaları
**Sorumluluk:** Raspberry Pi–ESP32 ortak protokolü; bu repo Raspberry Pi
uygulamasını ve entegrasyon kanıtlarını kapsar

## Amaç

Raspberry Pi ile ESP32 arasındaki fiziksel I²C hattında taşınan olayların açık
metin olarak görülmesini ve fark edilmeden değiştirilmesini zorlaştırmak;
mesaj gizliliği, bütünlüğü ve kaynak anahtara dayalı kimlik doğrulaması
sağlamak.

Bu aşama I²C hattına fiziksel erişimi engellemez. Güvenlik hedefi, hatta
erişebilen bir tarafın şifreli olay içeriğini doğrudan okuyamaması ve veriyi
değiştirdiğinde AES-GCM doğrulamasının başarısız olmasıdır.

## Kullanılan yöntem

Olay mesajları Advanced Encryption Standard — Galois/Counter Mode
(AES-256-GCM) ile şifrelenir.

| Bileşen | Doğrulanan değer | Görev |
|---|---:|---|
| AES anahtarı | 32 bayt / 256 bit | Şifreleme ve kimlik doğrulama |
| Nonce | 12 bayt / 96 bit | Her şifreleme işlemini benzersizleştirme |
| GCM tag | 16 bayt / 128 bit | Bütünlük ve kimlik doğrulama |
| Header | 4 bayt | Kimliği doğrulanan ek veri (AAD) |
| Ciphertext | Plaintext ile aynı uzunluk | Şifrelenmiş JSON içeriği |

Kriptografik blob aşağıdaki sırayla hazırlanır:

```text
4 bayt header
→ 12 bayt nonce
→ 16 bayt GCM authentication tag
→ ciphertext
```

Header açık biçimde taşınsa da AES-GCM işleminin kimliği doğrulanan ek verisi
(authenticated additional data — AAD) olarak korunur. Header üzerinde yapılan
tek bitlik değişiklik doğrulama hatasına neden olur.

## Şifreleme akışı

```text
Standart JSON olay
→ UTF-8 ve deterministik JSON serileştirme
→ Rastgele 12 bayt nonce
→ AES-256-GCM şifreleme
→ Header + nonce + tag + ciphertext
→ 20 baytlık payload parçaları
→ 32 baytlık I²C frame'leri
→ ESP32
```

I²C frame'lerindeki CRC-16 aktarım hatalarını tespit eder. CRC kriptografik
bütünlük sağlamaz; kötü niyetli değişikliklere karşı doğrulama AES-GCM etiketi
tarafından gerçekleştirilir.

## Anahtar uygulaması

Kaynak kod ve çalışma zamanı incelemesinde aşağıdaki sonuçlar alındı:

- `KEY` çalışma zamanında `bytes` türündedir.
- Anahtar uzunluğu 32 bayttır ve AES-256 gereksinimini karşılar.
- AST tabanlı kontrolde anahtarın kaynak kod içinde doğrudan literal olarak
  tanımlanmadığı görüldü.
- Raspberry tarafındaki istemci dosyasının izin modu `0670` olarak doğrulandı.
- Gerçek anahtar değeri hiçbir kanıt dosyasına veya dokümana yazılmadı.

Bu sonuçlar mevcut uygulamanın anahtar uzunluğunu ve anahtarın doğrudan kaynak
kod literal'i olmadığını doğrular. Anahtarın bütün yaşam döngüsünü,
oluşturulmasını, ESP32'ye güvenli aktarılmasını, yedeklenmesini, iptalini ve
döndürülmesini tek başına doğrulamaz.

## Nonce doğrulaması

İstemcinin `build_blob()` fonksiyonu aynı kontrollü olay için 64 kez
çalıştırıldı.

| Kontrol | Sonuç | Durum |
|---|---:|---|
| Üretilen nonce | 64 | ✅ Başarılı |
| Benzersiz nonce | 64 | ✅ Başarılı |
| Nonce uzunluğu | 12 bayt | ✅ Başarılı |
| Benzersiz GCM tag | 64 | ✅ Başarılı |
| Benzersiz şifreli blob | 64 | ✅ Başarılı |

Aynı anahtarla AES-GCM kullanılırken nonce tekrarının oluşmaması kritik bir
güvenlik gereksinimidir. Kontrollü testte tekrar görülmemiştir. Bu test,
gelecekte sınırsız sayıda mesajda hiçbir zaman tekrar oluşmayacağını matematiksel
olarak kanıtlamaz; uygulamanın doğrulanmış örneklemde benzersiz nonce ürettiğini
gösterir.

## Pozitif şifre çözme testi

Kontrollü olay `build_blob()` ile şifrelendi. Blob içinden header, nonce, tag
ve ciphertext ayrıştırıldı. Aynı AES-256 anahtarı ve header AAD olarak
kullanılarak şifre çözme gerçekleştirildi.

| Kontrol | Sonuç | Durum |
|---|---|---|
| AES-256 anahtar uzunluğu | 32 bayt | ✅ Başarılı |
| Şifre çözme | Orijinal plaintext elde edildi | ✅ Başarılı |
| Plaintext blob içinde aranması | Bulunmadı | ✅ Başarılı |
| Plaintext uzunluğu | 229 bayt | Bilgi |
| Şifreli blob uzunluğu | 261 bayt | Bilgi |

Plaintext'in şifreli blob içinde doğrudan bulunmaması, olay JSON'unun açık
metin olarak taşınmadığını gösterir.

## Negatif değişiklik testleri

Şifreli mesaj bileşenlerinin her biri kontrollü olarak bir bit değiştirilecek
şekilde bozuldu. Her durumda AES-GCM `InvalidTag` hatasıyla veriyi reddetti.

| Değiştirilen alan | Beklenen sonuç | Gerçekleşen sonuç | Durum |
|---|---|---|---|
| Ciphertext | Kimlik doğrulama reddedilmeli | Reddedildi | ✅ Başarılı |
| Authentication tag | Kimlik doğrulama reddedilmeli | Reddedildi | ✅ Başarılı |
| Nonce | Kimlik doğrulama reddedilmeli | Reddedildi | ✅ Başarılı |
| Header / AAD | Kimlik doğrulama reddedilmeli | Reddedildi | ✅ Başarılı |

Bu sonuç, şifreli mesajın veya doğrulanan header bilgisinin fark edilmeden
değiştirilemediğini kontrollü test kapsamında doğrular.

## Gerçek I²C entegrasyon doğrulaması

Stage 10'daki kontrollü donanım testi sırasında aşağıdaki sonuçlar alındı:

```text
FRAME REASSEMBLY: OK
AES-GCM AUTH: OK
AES-GCM DECRYPT: OK
EVENT_ID MATCH: OK
```

ESP32'nin cevabı 10 frame'den ve 187 bayt şifreli blob'dan yeniden
birleştirilmiştir. AES-GCM doğrulaması ve şifre çözme tamamlandıktan sonra
cevaptaki `event_id`, gönderilen olayın `event_id` değeriyle eşleştirilmiştir.

Bu test yalnızca yerel Python kriptografi testini değil, Raspberry Pi–ESP32
arasındaki gerçek şifreli mesaj alışverişini de doğrular.

## Sağlanan ve sağlanmayan güvenlik özellikleri

| Güvenlik özelliği | Durum | Açıklama |
|---|---|---|
| Gizlilik | ✅ Sağlandı | JSON içeriği AES-256-GCM ile şifreleniyor |
| Mesaj bütünlüğü | ✅ Sağlandı | Ciphertext ve tag değişiklikleri reddediliyor |
| Header bütünlüğü | ✅ Sağlandı | Header AAD olarak doğrulanıyor |
| Olay eşleştirme | ✅ Sağlandı | Cevap `event_id` üzerinden eşleştiriliyor |
| Aktarım hata kontrolü | ✅ Sağlandı | Frame seviyesinde CRC-16 kullanılıyor |
| Anahtarın kaynak kodda açık tutulmaması | ✅ Doğrulandı | Literal anahtar tespit edilmedi |
| Anahtar döndürme prosedürü | ⬜ Planlandı | Ayrı prosedür hazırlanmalı |
| Cihaz provisioning prosedürü | ⬜ Planlandı | İlk anahtar yükleme süreci belgelenmeli |
| Kriptografik replay koruması | ⬜ Planlandı | Sayaç/zaman penceresi veya kalıcı nonce kaydı gerekli |
| Donanım güvenli anahtar saklama | ⬜ Değerlendirilecek | Secure element veya güvenli depolama incelenmeli |

> Önemli: AES-GCM tek başına eski ve geçerli bir şifreli mesajın yeniden
> gönderilmesini engellemez. `event_id` eşleştirmesi yanlış cevabı tespit etmeye
> yardımcı olur; tam replay koruması için kalıcı sayaç, zaman penceresi veya
> işlenmiş mesaj kimliği kaydı ayrıca tasarlanmalıdır.

## Kanıtlar

- [Kriptografik uygulama doğrulaması](../../evidence/command-outputs/2026-10-01_stage-11_crypto-implementation.txt)
- [AES-GCM pozitif ve negatif testleri](../../evidence/test-results/2026-10-01_stage-11_aes-gcm-validation.txt)
- [Gerçek şifreli I²C gidiş-dönüş testi](../../evidence/test-results/2026-10-01_stage-10_encrypted-i2c-roundtrip.txt)
- [Stage 10 — Raspberry Pi ve ESP32 Arasında I²C](10-i2c-link.md)

Bu aşamada ekran görüntüsü yerine aranabilir ve yeniden değerlendirilebilir
metin kanıtları kullanılmıştır. Böylece gerçek anahtar veya diğer gizli
değerler görüntülere yanlışlıkla dâhil edilmeden test sonuçları belgelenmiştir.

## Güvenlik kuralları

- AES anahtarı GitHub reposuna eklenmez.
- Anahtar değeri terminal çıktısında, ekran görüntüsünde veya loglarda
  gösterilmez.
- Nonce benzersiz olmalıdır; aynı anahtar altında nonce tekrarına izin
  verilmemelidir.
- Kimlik doğrulaması tamamlanmadan plaintext işlenmemelidir.
- `InvalidTag`, eksik frame, CRC uyuşmazlığı ve `event_id` uyuşmazlığı başarı
  olarak kaydedilmemelidir.
- Anahtar değiştirildiğinde Raspberry Pi ve ESP32 kontrollü ve atomik bir
  geçiş prosedürüyle birlikte güncellenmelidir.
- Eski anahtarlar gereksiz yere tutulmamalı ve loglanmamalıdır.

## Açık iyileştirmeler

1. Anahtar oluşturma ve cihaz provisioning prosedürünü yazmak.
2. Anahtar döndürme, iptal ve geri dönüş sürecini tanımlamak.
3. Replay koruması için kalıcı sayaç veya zaman penceresi eklemek.
4. Anahtar dosyası ve üst dizin izinlerini otomatik test etmek.
5. Hatalı tag ve tekrarlanan mesaj denemelerini güvenli biçimde loglamak.
6. Uzun süreli testte nonce tekrarını ve hata oranını izlemek.
7. Donanım destekli anahtar saklama seçeneklerini değerlendirmek.

## Sonuç

Raspberry Pi istemcisinin 32 baytlık anahtarla AES-256-GCM kullandığı,
12 baytlık benzersiz nonce ve 16 baytlık authentication tag ürettiği
doğrulanmıştır. Kontrollü testte plaintext başarıyla geri elde edilmiş;
ciphertext, tag, nonce ve header değişikliklerinin tamamı reddedilmiştir.

Gerçek Raspberry Pi–ESP32 testinde frame yeniden birleştirme, AES-GCM kimlik
doğrulaması, şifre çözme ve `event_id` eşleşmesi başarıyla tamamlanmıştır.
Stage 11, prototip kriptografik taşıma kapsamında tamamlanmıştır. Üretim
seviyesinde anahtar yaşam döngüsü ve replay koruması ayrı güvenlik görevleri
olarak açık bırakılmıştır.