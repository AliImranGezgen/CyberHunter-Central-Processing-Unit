# Stage 3 — Python Çalışma Ortamlarının Hazırlanması

**Durum:** ✅ Tamamlandı  
**Sorumluluk:** Merkezi İşleme Birimi

## Amaç

İşletim sistemi paketleriyle proje servislerinin bağımlılıklarını ayırmak ve bir servisteki güncellemenin diğerlerini bozmasını engellemek.

## Yapı

- Ubuntu'nun sistem Python'u `3.12` olarak korundu.
- Proje bileşenleri için Python `3.11.15` tabanlı bağımsız sanal ortamlar kullanıldı.
- Cowrie/decoy, AI ve Bridge bileşenleri ayrı kullanıcılar ve çalışma dizinleriyle izole edildi.
- systemd unit'lerinde mutlak Python yolu, çalışma dizini ve gerektiğinde `PYTHONPATH` açıkça tanımlandı.

## Bileşenler

SMTP honeypot, Cowrie, Normalizer, AI analiz, paket yakalama, Publisher, output transfer, Bridge sender/receiver ve Inbox Worker Python tabanlı ana süreçlerdir.

## Mühendislik gerekçesi

Bu ayrım bağımlılık çakışmasını azaltır; servis hesabı yetkilerini daraltır; güncelleme, geri dönüş ve olay incelemesini kolaylaştırır. Üretim kodu sahibi ile çalışma kullanıcısının farklı olması hedeflenir.

## Kanıt alanı

![Python sanal ortamları ve servis hesapları](PASTE_IMAGE_URL_HERE_STAGE_03_PYTHON_ENVS)

