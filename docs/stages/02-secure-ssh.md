# Stage 2 — SSH Erişiminin Güvenli Hâle Getirilmesi

**Durum:** ✅ Tamamlandı  
**Sorumluluk:** Merkezi İşleme Birimi

## Amaç

Gerçek yönetim servisini saldırgana gösterilen SSH yüzeyinden ayırmak ve yönetim bağlantılarını anahtar tabanlı erişime taşımak.

## Uygulama

- Yönetim SSH portu `22`den `22222`ye taşındı.
- Port `22`, Cowrie SSH honeypot için ayrıldı; Cowrie'nin yerel servisi `2222` üzerinde konumlandırıldı.
- Yönetim ayarları `/etc/ssh/sshd_config.d/00-cyberhunter-management.conf` dosyasında toplandı.
- Ed25519 anahtar çifti oluşturularak yetkili istemciler tanımlandı.
- AI ve I²C ekiplerinin yönetim erişimi port `22222` üzerinden sağlandı.
- `PermitRootLogin no` ile doğrudan root girişi kapatıldı.
- Port `22`de gerçek SSH bağlantısının reddedildiği, `22222`de yönetim servisinin dinlediği ve iki eş zamanlı terminalin bağlanabildiği doğrulandı.

## Port sözleşmesi

| Port | Görev |
|---:|---|
| 22 | Cowrie SSH honeypot |
| 2222 | Cowrie yerel SSH servisi |
| 22222 | Gerçek sistem yönetimi |

> Güvenlik notu: Geçmişte `PasswordAuthentication yes` çıktısı görülmüştür. Güncel durumda `no` olduğuna dair anonimleştirilmiş `sshd -T` kanıtı eklenmeden tamamlanmış kabul edilmemelidir.

## Kanıt alanı

![Port 22 ve 22222 doğrulaması](PASTE_IMAGE_URL_HERE_STAGE_02_SSH_PORTS)

