# Güncel Durum

**Son repo denetimi:** 2026-10-02
Durum anahtarı: ✅ Tamamlandı/doğrulandı · 🟡 Kısmi/açık işi var · ⬜ Planlandı · 🔴 Engellendi

| Stage | Çalışma | Durum | Repo içindeki kanıt / açık nokta |
|---:|---|---|---|
| 1 | Raspberry Pi 5 + Ubuntu Server | ✅ | Sistem, kaynak, ağ, sıcaklık ve donanım kanıtı |
| 2 | SSH 22/2222/22222 ayrıştırması | ✅ | Efektif ayar, port, socket ve yönetim oturumu |
| 3 | Ayrı Python çalışma ortamları | 🟡 | Ortamlar var; bazı servisler sistem Python'unda ve yetki ayrımı eksik |
| 4 | Cowrie SSH honeypot | ✅ | Servis, dinleme, yönlendirme, olay ve ekran görüntüsü |
| 5 | PCAP paket yakalama servisi | ✅ | Servis, yapılandırma, depolama ve Cowrie korelasyonu |
| 6 | Normalizer | ✅ | Kaynak, birim testleri, servis ve 56/56 olay doğrulaması |
| 7 | AI analiz katmanı | 🟡 | Prototip/runtime doğrulandı; bağımsız etiketli saha testi ve model kartı açık |
| 8 | AI Publisher | ✅ | Servis/politika/atomik yazma ve beş canlı aktarım |
| 9 | Bridge kuyruk hattı | ✅ | Teslim, retry, archive ve rejected doğrulandı |
| 10 | Raspberry Pi ↔ ESP32 I²C | ✅ | Tarama, protokol, şifreli roundtrip ve donanım görselleri |
| 11 | AES-256-GCM veri koruması | 🟡 | Şifreleme/tamper testi başarılı; replay ve anahtar döndürme açık |
| 12 | ESP32 şema ve response doğrulaması | ✅ | Firmware incelemesi, Pi doğrulaması ve gerçek cevap testi |
| 13 | ESP32 → backend bağlantısı | 🟡 | POST entegrasyonu doğrulandı; TLS `setInsecure()` ve kalıcı URL açık |
| 14 | PostgreSQL + dashboard entegrasyonu | ✅ | API/DB/event ID/dashboard korelasyonu |
| 15 | Dinamik izolasyon eşiği | ✅ | 20/70 API değerleri, son geçerli değer ve retry testi |
| 16 | Sekiz kanallı röle testi | 🟡 | GPIO/LED kanal testi tamam; kontak sürekliliği ve yük testi açık |
| 17 | Röle LED prototip senaryosu | ✅ | Eşik altı/üstü davranışın görsel ve metin kanıtı |
| 18 | Güncel ESP32 kodu | 🟡 | Temiz derleme/runtime doğrulandı; secret provisioning ve TLS açık |
| 19 | Uçtan uca son test | 🟡 | Cowrie→Normalizer ve Bridge→Dashboard ayrı doğrulandı; tek event ID zinciri açık |

## Öncelikli eksikler

1. Tek bir kontrollü port `22` olayını Cowrie’den dashboard’a aynı `event_id`
   ile izleyip Stage 19 kanıtını üretmek.
2. Firmware'den Wi-Fi/AES/endpoint sırlarını çıkarıp güvenli provisioning ve
   anahtar döndürme prosedürü uygulamak; `setInsecure()` kullanımını kaldırmak.
3. Stage 3'te sistem Python'una bağlı servisleri kontrollü sanal ortamlara ve
   en düşük yetkili servis hesaplarına taşımak.
4. AES-GCM hattına kalıcı replay koruması eklemek ve negatif testi kaydetmek.
5. Röle kontaklarında süreklilik, güvenli test yükü ve gerçek izolasyon testini
   elektriksel güvenlik gözetimiyle yapmak.
6. UFW/rollback, uzun süreli sıcaklık ve 24–72 saat kararlılık testlerini
   tamamlamak.
7. Repoda olmayan çalışma zamanı kaynaklarını güncel kopya ve SHA-256 özetiyle
   ilgili ekiplerden almak.

## Otomatik denetim

`python scripts/validation/audit_repository.py` şu anda 19/19 stage belgesini
ve Stage 1–18 için en az bir tarihli kanıtı görür. Stage 19 kanıt eksikliği
bilinçli uyarı olarak raporlanır.
