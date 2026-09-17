# 14 — Bilinen Sorunlar ve Çözümler

| Sorun | Belirti | Olası neden | Uygulanan çözüm | Sonuç |
|---|---|---|---|---|
| USB boot | LED/boot kararsızlığı | Medya/güç/boot ayarı | microSD kurulumu | Sistem açıldı |
| Üniversite ağı | Bağlantı yok | Ortak ağ politikası | Mobil hotspot | Geliştirme sürdü |
| OpenSSH | Servis başlamıyor | `/run/sshd` yok | Dizin oluşturuldu | SSH çalıştı |
| Port 22 açık kalıyor | ssh.socket dinliyor | Socket activation | Yönetim 22222ye ayrıldı | 22 Cowrie'ye kaldı |
| NTP | Zaman aşımı | UDP 123/ağ kısıtı | Saat kaynağı yeniden doğrulandı | Sorun çözüldü |
| Boş komut | Worker rejected | Brute-force'ta shell komutu yok | Publisher fallback | Olay işlenebilir oldu |
| ACK uyumsuzluğu | Cevap timeout | İki farklı client sürümü | ACK destekli test client seçildi | Worker yolu netleşti |
| Ngrok offline | `processed:false` | Geçici tünel kapalı | Tünel yenilendi | Backend ulaşıldı |

