# Stage 1 — Raspberry Pi ve İşletim Sistemi Kurulumu

**Durum:** ✅ Tamamlandı  
**Sorumluluk:** Merkezi İşleme Birimi

## Amaç

CyberHunter'ın sürekli çalışacak merkezi düğümünü Raspberry Pi 5 üzerinde kurmak; güvenli uzaktan yönetim ve sonraki servisler için kararlı bir Ubuntu Server temeli hazırlamak.

## Yapılan çalışmalar

- Ana işlem birimi olarak 16 GB Raspberry Pi 5 seçildi.
- USB bellekten başlatma denemeleri ve güç/LED davranışları incelendi; kurulum 64 GB microSD üzerinden sürdürüldü.
- Raspberry Pi Imager ile Ubuntu Server 24.04.4 LTS (`noble`, `arm64`) kuruldu.
- Üniversite ortak ağına bağlantı sağlanamayınca geliştirme için `CyberHunter-Lab` mobil erişim noktası kullanıldı.
- OpenSSH Server kuruldu; başlangıçtaki `/run/sshd` sorunu giderildi ve `ssh.socket` doğrulandı.
- Hostname `cyberhunter-pi`, saat dilimi `Europe/Istanbul` olarak ayarlandı; NTP daha sonra doğrulandı.

## Başarı kriteri ve sonuç

Sistem ağdan erişilebilir hâle geldi, SSH servisi çalıştı ve sonraki güvenlik/servis kurulumları için temel hazırlandı. Gerçek IP ve MAC bilgileri dokümantasyonda tutulmaz.

## Kanıt alanı

![Raspberry Pi 5 ve Ubuntu kurulumu](PASTE_IMAGE_URL_HERE_STAGE_01_RASPBERRY_SETUP)

Eklenmesi önerilen metin kanıtları: `lsb_release -a`, `uname -a`, `hostnamectl`, `timedatectl`, `free -h`, `df -h`.

