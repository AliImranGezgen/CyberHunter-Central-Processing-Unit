# Stage 2 — SSH Erişiminin Güvenli Hâle Getirilmesi

**Durum:** ✅ Tamamlandı
**Sorumluluk:** Merkezi İşleme Birimi

## Amaç

Gerçek OpenSSH yönetim servisini saldırgana gösterilen SSH yüzeyinden
ayırmak, yönetim bağlantılarını anahtar tabanlı erişime taşımak ve
parola tabanlı uzaktan erişimi kapatmak.

## Yapılan çalışmalar

- OpenSSH Server kurulumu tamamlandı.
- Kurulum sırasında karşılaşılan `/run/sshd` dizini problemi giderildi.
- Yönetim SSH portu `22`den `22222`ye taşındı.
- Yönetim ayarları aşağıdaki dosyada toplandı:

```text
/etc/ssh/sshd_config.d/00-cyberhunter-management.conf
```

- Ed25519 anahtar çifti yetkili istemci üzerinde oluşturuldu.
- Public key tabanlı SSH bağlantısı doğrulandı.
- `PermitRootLogin no` ile doğrudan root girişi kapatıldı.
- `PasswordAuthentication no` ile parola tabanlı SSH erişimi kapatıldı.
- `ssh.socket` port `22222` üzerinde çalışacak şekilde yapılandırıldı.
- Port `22222` üzerinden yönetim oturumu açıldığı doğrulandı.
- Port `22`, daha sonraki Cowrie aşamasında honeypot giriş noktası olarak ayrıldı.
- Cowrie yerel SSH servisi port `2222` üzerinde çalıştırıldı.

## Etkin SSH yapılandırması

`sshd -T` komutuyla doğrulanan güncel yapılandırma:

```text
port 22222
permitrootlogin no
pubkeyauthentication yes
passwordauthentication no
```

Bu çıktı, OpenSSH tarafından etkin olarak kullanılan yapılandırmayı
göstermektedir.

## Port sözleşmesi

| Port | Servis | Erişim biçimi |
|---:|---|---|
| `22` | Cowrie SSH honeypot giriş noktası | nftables ile port `2222`ye yönlendirilir |
| `2222` | Cowrie yerel SSH servisi | `twistd` tarafından dinlenir |
| `22222` | Gerçek OpenSSH yönetim servisi | Yetkili istemciler için kullanılır |

## Güncel bağlantı akışı

```text
Yetkisiz veya saldırgan bağlantısı
→ Raspberry Pi port 22
→ nftables yönlendirmesi
→ Cowrie port 2222

Yetkili yönetim bağlantısı
→ Raspberry Pi port 22222
→ OpenSSH
→ Anahtar tabanlı kimlik doğrulama
```

## Önemli durum açıklaması

Yönetim portu ilk kez `22222`ye taşındığında port `22` bağlantısının
reddedildiği doğrulanmıştır. Bu, o tarihte port `22` üzerinde hiçbir
servisin çalışmadığını göstermiştir.

Cowrie kurulumu tamamlandıktan sonra mevcut durum değişmiştir. Güncel
sistemde port `22` bağlantıyı reddetmek yerine nftables üzerinden
Cowrie'nin port `2222` dinleyicisine yönlendirmektedir.

Dolayısıyla güncel güvenlik koşulu şudur:

> Port `22`, gerçek OpenSSH yönetim servisine ulaşmamalıdır; Cowrie
> honeypot servisine yönlendirilmelidir.

## Test ve doğrulama sonuçları

| Kontrol | Beklenen sonuç | Gerçekleşen sonuç | Durum |
|---|---|---|---|
| OpenSSH yönetim portu | Port `22222` | `sshd -T` ile doğrulandı | ✅ Başarılı |
| Root girişi | Kapalı olmalı | `permitrootlogin no` | ✅ Başarılı |
| Public key doğrulaması | Açık olmalı | `pubkeyauthentication yes` | ✅ Başarılı |
| Parola doğrulaması | Kapalı olmalı | `passwordauthentication no` | ✅ Başarılı |
| SSH socket | Aktif olmalı | `active (running)` | ✅ Başarılı |
| SSH socket başlangıcı | Etkin olmalı | `enabled` | ✅ Başarılı |
| IPv4 yönetim dinleyicisi | Port `22222` | `0.0.0.0:22222` | ✅ Başarılı |
| IPv6 yönetim dinleyicisi | Port `22222` | `[::]:22222` | ✅ Başarılı |
| Port `22` OpenSSH dinleyicisi | Bulunmamalı | Doğrudan dinleyici bulunmuyor | ✅ Başarılı |
| Yönetim bağlantısı | Port `22222` üzerinden açılmalı | Oturum açıldı | ✅ Başarılı |
| Hedef sistem doğrulaması | `cyberhunter-pi` görülmeli | Hostname doğrulandı | ✅ Başarılı |
| Cowrie ayrımı | Port `2222` üzerinde çalışmalı | `twistd` dinleyicisi görüldü | ✅ Başarılı |
| Port `22` yönlendirmesi | Cowrie'ye ulaşmalı | Cowrie olayıyla doğrulandı | ✅ Başarılı |

## Doğrulama kanıtları

### OpenSSH kanıtları

- [Etkin SSH yapılandırması](../../evidence/command-outputs/2026-10-01_stage-02_sshd-effective-config.txt)
- [Dinlenen SSH portları](../../evidence/command-outputs/2026-10-01_stage-02_ssh-listening-ports.txt)
- [SSH socket durumu](../../evidence/command-outputs/2026-10-01_stage-02_ssh-socket-status.txt)
- [Yönetim oturumu](../../evidence/command-outputs/2026-10-01_stage-02_management-session.txt)

### Cowrie ayrım kanıtları

- [Port 22 yönlendirme kuralı](../../evidence/command-outputs/2026-10-01_stage-04_cowrie-port22-redirect-sanitized.txt)
- [Port 22 istemci yanıtı](../../evidence/screenshots/2026-10-01_stage-04_cowrie-port22-response_sanitized.png)
- [Cowrie JSON olay kaydı](../../evidence/command-outputs/2026-10-01_stage-04_cowrie-port22-event-sanitized.txt)
- [Stage 4 — Cowrie SSH Honeypot](04-cowrie-honeypot.md)

## Güvenlik değerlendirmesi

### Uygulanan kontroller

- Yönetim ve honeypot servisleri farklı portlarda çalışmaktadır.
- Doğrudan root girişi kapatılmıştır.
- Parola tabanlı kimlik doğrulama kapatılmıştır.
- Public key tabanlı kimlik doğrulama kullanılmaktadır.
- Port `22` gerçek yönetim servisine ulaşmamaktadır.
- Yönetim servisi ayrı bir SSH yapılandırma dosyasıyla yönetilmektedir.

### Açık iyileştirmeler

- Yönetim portuna erişebilecek IP aralığı daraltılmalıdır.
- Geniş yerel ağ izni güvenli erişim testi sonrasında kaldırılmalıdır.
- SSH yapılandırma değişiklikleri için geri dönüş prosedürü hazırlanmalıdır.
- Anahtar iptal ve yenileme prosedürü belgelenmelidir.
- Başarısız yönetim bağlantıları için alarm mekanizması değerlendirilmelidir.
- IPv6 yönetim erişiminin gerekli olup olmadığı değerlendirilmelidir.

> Uyarı: Firewall veya SSH erişim kuralları değiştirilmeden önce ikinci
> bir yönetim oturumu açık tutulmalı ve geri dönüş yöntemi hazırlanmalıdır.

## Tarihsel yapılandırma notu

İlk kurulum aşamasında aşağıdaki değer doğrulanmıştır:

```text
passwordauthentication yes
```

Sertleştirme çalışmasının ardından güncel etkin değer şu olmuştur:

```text
passwordauthentication no
```

Bu iki değer farklı zamanlardaki sistem durumlarını göstermektedir.
Güncel yapılandırma `sshd -T` kanıtıyla doğrulanmıştır.

## Sonuç

OpenSSH yönetim servisi port `22222` üzerinde çalışmaktadır. Doğrudan root
girişi ve parola tabanlı kimlik doğrulama kapatılmış, public key tabanlı
erişim etkinleştirilmiştir.

Port `22` üzerinde gerçek OpenSSH dinleyicisi bulunmamaktadır. Bu porta
gelen bağlantılar Cowrie honeypot servisinin port `2222` dinleyicisine
yönlendirilmektedir.

Böylece gerçek yönetim yüzeyi ile saldırgana gösterilen sahte SSH yüzeyi
birbirinden ayrılmıştır.