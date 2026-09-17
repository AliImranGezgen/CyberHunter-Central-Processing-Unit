# 07 — Honeypot Servisleri

| Servis | Dış kimlik | Kaydedilen veri | İzolasyon | Test |
|---|---|---|---|---|
| SSH/Cowrie | Port 22 SSH | Login, komut, oturum | Ayrı kullanıcı + port 2222 | Kontrollü SSH bağlantısı |
| SMTP | Sahte SMTP/2525 | EHLO, sender, recipient, mesaj özeti | Ayrı `smtpot` hesabı | Test SMTP oturumu |
| HTTPS | Planlanan sahte web yüzeyi | İstek metadatası | Container/systemd sandbox | Kontrollü HTTP istekleri |

Honeypot hiçbir zaman gerçek yönetim kimliği, gerçek dosya sistemi veya ayrıcalıklı token barındırmamalıdır.

