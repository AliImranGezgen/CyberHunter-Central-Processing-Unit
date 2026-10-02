# Stage 8 — AI Publisher ve Olay Paketleme

**Durum:** ✅ Prototip servis ve canlı aktarım doğrulandı
**Sorumluluk:** AI ekip bileşeni; Raspberry Pi servis entegrasyonu bu repo kapsamında

## Amaç

AI analiz sonuçlarını Bridge ve ESP32 katmanlarının kullanabileceği doğrulanmış,
dokuz alanlı ve atomik yazılan JSON olaylarına dönüştürmek.

Publisher fiziksel izolasyon kararı vermez ve ESP32 ile doğrudan haberleşmez.
Olay sınıfına yayın politikası uygular, taktik ve risk skoru ekler, sözleşmeyi
doğrular ve sonucu AI output dizinine bırakır.

## Veri akışı

```text
AI çalışma zamanı çıktısı
→ AI Publisher
→ olay sınıfı politikası
→ dokuz alanlı JSON
→ /var/lib/cyberhunter/ai/output
→ Bridge aktarım katmanı
```

## Olay sözleşmesi

Zorunlu alanlar:

| Alan | Temel koşul |
|---|---|
| `event_id` | Onaylı biçim, en fazla 40 UTF-8 bayt |
| `timestamp` | Zaman dilimli RFC 3339; UTC `Z` biçimine dönüştürülür |
| `source_ip` | Geçerli IPv4 adresi |
| `destination_port` | Tam sayı |
| `protocol` | Boş olamaz |
| `event_type` | Boş olamaz |
| `command` | En fazla 256 UTF-8 bayt |
| `tactic` | Boş olamaz |
| `risk_score` | `0–100` aralığında tam sayı |

Boş komut için olay türüne göre açık fallback metni kullanılır. Aynı
`event_id` için nihai veya geçici dosya mevcutsa üzerine yazılmaz.

## Politika

Doğrulanan sınıf eşlemelerinden bazıları:

| Olay sınıfı | Taktik | Risk |
|---|---|---:|
| `Normal_Benign` | Benign | 0 |
| `Reconnaissance` | Reconnaissance | 25 |
| `Credential_Attack` | Credential Access | 55 |
| `DoS_DDoS` | Impact | 85 |
| `Malware_Botnet` | Command and Control | 90 |
| `Unknown` | Unknown | 15 |

Cowrie oturumları `cowrie.session.closed` ile tamamlanmış kabul edilir.
Oturum bazlı tekilleştirmede güvenilir sınıflandırma, en yüksek risk ve en yeni
olay zamanı sırasıyla dikkate alınır.

## Atomik yazma

Publisher olayı önce `.<event_id>.json.tmp` adına özel oluşturma modunda yazar,
ardından `os.replace()` ile `<event_id>.json` adına taşır. Durum dosyası da aynı
geçici dosya ve atomik değiştirme modeliyle güncellenir.

## Çalışma zamanı doğrulaması

2026-10-01 tarihli ilk anlık kontrolde output dizininde olay bulunmadığından
sonuç kısmi kalmıştır. Daha sonraki çalışma zamanı kaydı bu boşluğun olayların
Bridge tarafından hızla taşınmasından kaynaklandığını göstermiştir:

- Publisher beş olay dosyası oluşturdu.
- Output-transfer beş dosyayı Bridge hattına taşıdı.
- Bridge receiver beş isteğin tamamına `HTTP 201` döndürdü.
- Servis `cyberai` hesabıyla `active/running` durumunda doğrulandı.

Bu kanıt canlı yayın ve Bridge kabulünü doğrular; Publisher kaynak modülünün tam
kopyası hâlâ bu repoda değildir.

## Kanıtlar

- [Publisher servis durumu](../../evidence/command-outputs/2026-10-01_stage-08_publisher-service-status.txt)
- [Anonimleştirilmiş yayın politikası](../../evidence/command-outputs/2026-10-01_stage-08_publisher-policy-sanitized.txt)
- [Olay sözleşmesi ve atomik yazma incelemesi](../../evidence/command-outputs/2026-10-01_stage-08_atomic-write-verification.txt)
- [İlk output dizini kontrolü](../../evidence/test-results/2026-10-01_stage-08_publisher-output-validation.txt)
- [Beş olayın canlı aktarım kaydı](../../evidence/test-results/2026-10-01_stage-08_publisher-runtime-evidence.txt)
- [Anonimleştirilmiş systemd unit örneği](../../configs/systemd/cyberhunter-ai-publisher.service.example)

## Güvenlik ve sınırlamalar

- AI girdisi salt okunur; yazma izni log/durum ve output yollarıyla sınırlıdır.
- Serviste `NoNewPrivileges`, `PrivateTmp` ve `ProtectSystem=strict` kullanılır.
- Kaynak IP ve saldırı içeriği yayımlanmadan önce anonimleştirilmelidir.
- Publisher'ın güncel tam kaynak kodu ve bağımsız birim testleri repoya henüz
  alınmamıştır.
- Beş canlı olayın içerik alanları bu kanıtta tek tek gösterilmediğinden tam
  şema kontrolü kaynak incelemesi ve sözleşme doğrulamasına dayanır.

## Sonuç

Publisher servisinin çalıştığı, dokuz alanlı sözleşmeyi ve atomik yazma modelini
uyguladığı, oluşturduğu beş olayın Bridge receiver tarafından kabul edildiği
doğrulanmıştır. Kaynak kodun repoya alınması ve bağımsız test kapsamı açık
tedarik görevleridir.
