# Güncel Durum

Durum anahtarı: ✅ Tamamlandı · 🟡 Devam ediyor · ⬜ Planlandı · 🔴 Engellendi

| Stage | Çalışma | Durum | Kanıt |
|---:|---|---|---|
| 1 | Raspberry Pi 5 + Ubuntu Server | ✅ | URL bekleniyor |
| 2 | SSH 22/2222/22222 ayrıştırması | ✅ | URL bekleniyor |
| 3 | Ayrı Python çalışma ortamları | ✅ | URL bekleniyor |
| 4 | Cowrie SSH honeypot | ✅ | URL bekleniyor |
| 5 | PCAP paket yakalama servisi | ✅ | URL bekleniyor |
| 6 | Normalizer | ✅ | Kaynak kod repoda |
| 7 | AI analiz katmanı | ✅ | Test raporu bekleniyor |
| 8 | AI Publisher | ✅ | Unit örneği repoda |
| 9 | Bridge kuyruk hattı | ✅ | Worker kaynak kodu repoda |
| 10 | Raspberry Pi ↔ ESP32 I²C | ✅ | Fotoğraf/çıktı bekleniyor |
| 11 | AES-256-GCM veri koruması | ✅ | Test çıktısı bekleniyor |
| 12 | ESP32 şema ve response doğrulaması | ✅ | Serial çıktısı bekleniyor |
| 13 | ESP32 → backend bağlantısı | ✅ | HTTP kanıtı bekleniyor |
| 14 | PostgreSQL + dashboard entegrasyonu | ✅ | Ekran görüntüsü bekleniyor |
| 15 | Dinamik izolasyon eşiği | ✅ | Endpoint çıktısı bekleniyor |
| 16 | Sekiz kanallı röle testi | ✅ | Donanım fotoğrafı bekleniyor |
| 17 | Röle LED prototip senaryosu | ✅ | Video/görsel bekleniyor |
| 18 | Güncel ESP32 kodu | 🟡 | Arduino derleme/yükleme bekliyor |
| 19 | Uçtan uca son test | ⬜ | Henüz uygulanmadı |

## Açık güvenlik görevleri

- `PasswordAuthentication no` geçişini güncel sistemde yeniden doğrulamak.
- UFW kuralları ve geri dönüş planını kanıtlamak.
- Aktif soğutma ihtiyacını uzun süreli sıcaklık testiyle değerlendirmek.
- Ngrok gibi geçici tünelleri kalıcı üretim mimarisinden ayırmak.
- Tüm servis dosyalarının güncel kopyalarını Raspberry Pi'den anonimleştirerek repoya almak.

