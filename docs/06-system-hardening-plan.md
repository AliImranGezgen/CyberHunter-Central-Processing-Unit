# 06 — Sistem Sertleştirme Planı

| Görev | Durum |
|---|---|
| Parola tabanlı SSH'ı kapatma | Doğrulama bekliyor |
| UFW temel kuralları + rollback | Planlandı |
| Fail2ban değerlendirmesi | Planlandı |
| Yönetim kaynağını IP/VPN ile sınırlama | Planlandı |
| Ayrı servis kullanıcıları | Uygulandı; audit bekliyor |
| systemd sandbox seçenekleri | Kısmen uygulandı |
| Dosya izinleri ve sahiplik | Uygulandı; audit bekliyor |
| Log rotasyonu ve yedekleme | Planlandı |
| Güncelleme politikası | Planlandı |

SSH/firewall değişikliği, ikinci aktif oturum ve geri dönüş komutu hazır olmadan uygulanmamalıdır.

