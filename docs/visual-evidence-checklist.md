# Kanıt Kapsam Matrisi

Bu matris, her stage için repoda bulunan kanıt türünü ve kalan kabul boşluğunu
özetler. Ayrıntılı bağlantılar ilgili stage belgesindedir. Dosya adları
`YYYY-MM-DD_stage-NN_...` biçimindedir.

| Stage | Hedef kanıt | Mevcut durum | Kalan boşluk |
|---:|---|---|---|
| 1 | Pi, işletim sistemi, kaynak ve sıcaklık | ✅ 4 çıktı + 1 fotoğraf | Uzun süreli termal test |
| 2 | SSH efektif ayarları ve portlar | ✅ 4 çıktı | UFW/rollback ayrı görev |
| 3 | Python ortamları ve servis bağları | ✅ 3 çıktı | Sistem Python servislerini taşıma |
| 4 | Cowrie port 22 yönlendirmesi ve olay | ✅ 4 çıktı + 1 ekran görüntüsü | Kontrollü login/komut oturumu |
| 5 | Capture servisi, PCAP ve korelasyon | ✅ 4 çıktı | Saklama/rotasyon politikası |
| 6 | Normalizer servis ve olay doğrulaması | ✅ 3 çıktı + repo testleri | İki Cowrie türü için özel eşleme |
| 7 | AI servis, model, metrik ve runtime | ✅ 4 çıktı | Bağımsız etiketli saha testi/model kartı |
| 8 | Publisher servis, sözleşme ve canlı aktarım | ✅ 3 çıktı + 2 test sonucu | Tam kaynak ve bağımsız birim testleri |
| 9 | Kuyruk, teslim, retry ve rejected | ✅ 3 çıktı + 2 test sonucu | Eksik runtime kaynaklarının dışa aktarımı |
| 10 | I²C bağlantı ve şifreli roundtrip | ✅ 2 çıktı + 1 test + 4 fotoğraf | Uzun süre/gürültü testi |
| 11 | AES-GCM ve negatif doğrulama | ✅ 1 çıktı + 1 test | Replay/anahtar döndürme testi |
| 12 | Şema ve ESP32 response | ✅ 3 çıktı + 1 test | Secret provisioning prosedürü |
| 13 | Backend POST ve `2xx` | ✅ 1 çıktı + 1 test | TLS doğrulaması ve kalıcı endpoint |
| 14 | API, PostgreSQL ve dashboard | ✅ 3 çıktı + 1 test + 1 ekran görüntüsü | Açık tekrar-gönderme idempotency testi |
| 15 | Eşik API'si ve fail-safe | ✅ 3 çıktı + 1 test + 2 görsel | İlk açılışta config kesintisi testi |
| 16 | Röle kanalları ve restorasyon | ✅ 2 çıktı + 1 test + 1 fotoğraf | Kontak sürekliliği/yük testi |
| 17 | Eşik altı/üstü röle LED davranışı | ✅ 1 çıktı + 1 test + 3 görsel | Gerçek hat izolasyonu |
| 18 | Temiz firmware derleme/runtime | ✅ 1 ekran görüntüsü | Kaynak güvenliği ve provisioning |
| 19 | Tek `event_id` ile tam zincir | ⚠️ Parçalı stage kanıtları var | Cowrie → dashboard ortak kabul kaydı |

## Otomatik kontrol

```bash
python scripts/validation/audit_repository.py
```

Komut yapısal hatalarda başarısız olur. Stage 19 gibi bilinçli kanıt boşlukları
uyarı olarak kalır; donanım veya saha kanıtı uydurulmaz.
