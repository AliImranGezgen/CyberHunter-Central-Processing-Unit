# Stage 9 — Bridge ve Güvenilir Dosya Aktarımı

**Durum:** ✅ Kontrollü teslim, retry ve rejected akışları doğrulandı
**Sorumluluk:** Merkezi İşleme Birimi

## Amaç

Publisher olaylarını kayıp, yinelenme ve yarım yazılmış dosya riskini azaltarak
ESP32 tüketicisine taşımak; ESP32 cevabını doğrulayıp işlem sonucunu kalıcı
durum ve kuyruk kayıtlarına yansıtmak.

## Kuyruk modeli

```text
AI output
→ Bridge outbox
→ Bridge receiver
→ Bridge inbox
→ processing
├── başarı → archive
└── geçici hata → inbox/retry → deneme sınırı aşılırsa rejected
```

`rejected` yalnızca şema hatalarını değil, üç teslim denemesini aşan I²C veya
ESP32 iletişim hatalarını da içerir.

## Güvenilirlik mekanizmaları

| Katman | Doğrulanan koruma |
|---|---|
| Output transfer | `fcntl.flock`, geçici dosya, `os.replace()` |
| Outbox sender | Tek süreç kilidi, hata hâlinde dosyayı koruma, timer retry |
| Receiver | Olay bazlı kilit, hash tabanlı dosya adı, atomik inbox yazımı |
| Inbox Worker | Worker kilidi, `processing`, atomik state, en fazla üç deneme |
| ESP32 cevabı | `event_id` eşleşmesi ve `processed=true` kabul koşulu |

Oneshot servislerin tamamlandıktan sonra `inactive/dead` görünmesi normaldir;
path veya timer birimleri sonraki çalıştırmayı tetikler.

## Publisher → inbox doğrulaması

2026-10-01 tarihinde Publisher tarafından oluşturulan beş dosya output-transfer
ile outbox'a taşınmış, sender tarafından yerel receiver'a gönderilmiş ve tüm
istekler `HTTP 201` ile kabul edilmiştir. Aktarım sonunda output ve outbox'ta
bekleyen olay kalmamıştır.

## Kontrollü ESP32 teslim testi

`evt-stage09-20261001T122857Z` kimlikli, risk skoru `0` olan kontrollü olay:

- `/dev/i2c-1` üzerindeki `0x08` adresine gönderildi.
- 15 gidiş ve 10 dönüş frame'i başarıyla birleştirildi.
- AES-GCM doğrulama ve şifre çözme başarılı oldu.
- İlk cevapta `processed=false` görüldü ve olay retry kuyruğuna alındı.
- İkinci cevapta aynı `event_id` ile `processed=true` alındı.
- Olay `archive` dizinine taşındı; state kaydı `attempts: 2` oldu.

## Retry ve rejected testi

ESP32 inaktifken iki gerçek Publisher olayı için `Remote I/O error` üretildi.
Worker olayları ilk iki hatada inbox'a geri taşıdı, üçüncü hatada `rejected`
dizinine aldı. Böylece olay kaybetmeme, kalıcı deneme sayısı ve sonsuz retry
uygulamama davranışları doğrulandı.

## Kaynaklar

- [Inbox Worker](../../src/cyberhunter_cpu/inbox_worker.py)
- [Inbox Worker service](../../configs/systemd/cyberhunter-inbox-worker.service)
- [Inbox Worker timer](../../configs/systemd/cyberhunter-inbox-worker.timer)
- [Output-transfer service örneği](../../configs/systemd/cyberhunter-ai-output-transfer.service.example)
- [Output-transfer path örneği](../../configs/systemd/cyberhunter-ai-output-transfer.path.example)
- [Output-transfer timer örneği](../../configs/systemd/cyberhunter-ai-output-transfer.timer.example)

## Kanıtlar

- [Bridge servis durumu](../../evidence/command-outputs/2026-10-01_stage-09_bridge-service-status.txt)
- [Publisher'dan inbox'a aktarım](../../evidence/command-outputs/2026-10-01_stage-09_publisher-to-inbox-transfer-sanitized.txt)
- [Kuyruk güvenilirliği incelemesi](../../evidence/command-outputs/2026-10-01_stage-09_queue-reliability-verification.txt)
- [Kontrollü ESP32 teslim testi](../../evidence/test-results/2026-10-01_stage-09_controlled-delivery-test.txt)
- [Retry ve rejected testi](../../evidence/test-results/2026-10-01_stage-09_retry-and-rejection-test.txt)

## Sınırlamalar

- Receiver, outbox sender, output-transfer ve ESP32 istemcisinin tam kaynakları
  bu repoya henüz alınmamıştır.
- Kaynak incelemesinde kaydedilen SHA-256 özetleri, ilgili dosyalar repoya
  alınana kadar burada yeniden üretilemez.
- Bu aşama röle kontaklarının fiziksel izolasyon oluşturduğunu kanıtlamaz.

## Sonuç

Publisher'dan Bridge inbox'a canlı aktarım, kontrollü I²C teslimi, cevap
eşleştirme, archive, retry ve rejected davranışları doğrulanmıştır. Repo içindeki
Inbox Worker test edilebilir kaynak olarak korunurken diğer çalışma zamanı
bileşenlerinin güncel kopyalarının alınması açık kalmıştır.
