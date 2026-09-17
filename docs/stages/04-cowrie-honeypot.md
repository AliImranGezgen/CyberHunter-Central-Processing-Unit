# Stage 4 — Cowrie SSH Honeypot Kurulumu

**Durum:** ✅ Tamamlandı  
**Sorumluluk:** Merkezi İşleme Birimi

## Amaç

Port `22`ye yönelen saldırı ve yetkisiz erişim denemelerini gerçek yönetim servisine ulaştırmadan kaydetmek.

## Yapılan çalışmalar

- Cowrie Raspberry Pi'ye ayrı servis hesabıyla kuruldu.
- Yerel Cowrie SSH servisi `2222` üzerinde çalıştırıldı; dış port `22` bu servise yönlendirildi.
- Gerçek SSH yönetimi port `22222`de tutuldu.
- Kullanıcı adı/parola denemeleri, oturum başlangıç-bitişi ve saldırgan komutları Cowrie JSON loglarına yazıldı.
- Servis `cyberhunter-cowrie.service` adıyla systemd üzerinden yönetilebilir hâle getirildi.

## Güvenlik sınırı

Cowrie verileri güvenilir girdi değildir. Log içeriği komut çalıştırma amacıyla kullanılmamalı; dosya yüklemeleri izole tutulmalı; gerçek kimlik bilgileri ve saldırgan IP'leri paylaşılmadan önce anonimleştirilmelidir.

## Kanıt alanı

![Cowrie bağlantısı ve olay kaydı](PASTE_IMAGE_URL_HERE_STAGE_04_COWRIE_EVENT)

