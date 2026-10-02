# Stage 4 — Cowrie SSH Honeypot Kurulumu

**Durum:** ✅ Tamamlandı
**Sorumluluk:** Merkezi İşleme Birimi

## Amaç

Port `22` üzerinden gelen saldırı ve yetkisiz erişim denemelerini gerçek
yönetim servisine ulaştırmadan Cowrie SSH honeypot servisine yönlendirmek
ve oluşan olayları JSON formatında kaydetmek.

## Yapılan çalışmalar

- Cowrie, Raspberry Pi üzerine ayrı bir servis hesabıyla kuruldu.
- Cowrie SSH servisi yerel olarak port `2222` üzerinde çalıştırıldı.
- `wlan0` arayüzündeki port `22` trafiği nftables ile port `2222`ye yönlendirildi.
- Gerçek OpenSSH yönetim servisi port `22222` üzerinde ayrı tutuldu.
- Cowrie bağlantı, anahtar değişimi ve oturum kapanış olayları JSON loglarına kaydedildi.
- Cowrie, `cyberhunter-cowrie.service` adıyla systemd servisi olarak yapılandırıldı.
- Servisin sistem başlangıcında etkin olduğu ve aktif çalıştığı doğrulandı.
- Servis için temel systemd güvenlik seçenekleri uygulandı.

## Servis ve port ayrımı

```text
Saldırgana gösterilen SSH portu
Port 22 → nftables yönlendirmesi → Cowrie port 2222

Gerçek yönetim SSH servisi
Yetkili istemci → OpenSSH port 22222
```

Port `22` üzerinde doğrudan bir OpenSSH yönetim dinleyicisi
bulunmamaktadır. Bu porta gelen TCP bağlantıları nftables tarafından
Cowrie'nin port `2222` dinleyicisine yönlendirilmektedir.
Gerçek yönetim erişimi port `22222` üzerinden sağlanmaktadır.

## Port 22 yönlendirme doğrulaması

Port `22` üzerinden gerçek parola veya SSH anahtarı gönderilmeden kontrollü
bir bağlantı oluşturulmuştur.

Cowrie bu bağlantı için aşağıdaki olayları üretmiştir:

```text
cowrie.client.kex
cowrie.session.closed
```

Her iki olayın aynı oturum kimliğiyle oluşturulduğu görülmüştür. Böylece
kontrollü bağlantının Cowrie tarafından işlendiği doğrulanmıştır.

Doğrulanan akış:

```text
İstemci
→ Raspberry Pi port 22
→ nftables yönlendirmesi
→ Cowrie port 2222
→ Cowrie JSON olay kaydı
```

> **Tamamlanma kapsamı:** Cowrie kurulumu, systemd servisi, port ayrımı,
> nftables yönlendirmesi ve temel JSON olay üretimi doğrulanmıştır.
> Kullanıcı adı/parola denemesi ve sahte oturum komutlarının kaydedilmesi
> ek davranış testleri olarak planlanmıştır ve temel kurulumun tamamlanma
> durumunu değiştirmez.

## Test sonucu

| Kontrol | Beklenen sonuç | Gerçekleşen sonuç | Durum |
|---|---|---|---|
| Cowrie port kontrolü | `twistd` port `2222` üzerinde dinlemeli | Port `2222` üzerinde dinledi | ✅ Başarılı |
| Yönetim SSH kontrolü | OpenSSH port `22222` üzerinde dinlemeli | Port `22222` üzerinde dinledi | ✅ Başarılı |
| Port `22` yönlendirmesi | Trafik port `2222`ye yönlendirilmeli | nftables yönlendirme kuralı doğrulandı | ✅ Başarılı |
| Cowrie systemd servisi | Servis aktif ve etkin olmalı | `active (running)` ve `enabled` görüldü | ✅ Başarılı |
| Kontrollü port `22` bağlantısı | Cowrie olayı oluşturulmalı | `cowrie.client.kex` olayı oluştu | ✅ Başarılı |
| Oturum kapanışı | Aynı oturum için kapanış olayı oluşmalı | `cowrie.session.closed` olayı oluştu | ✅ Başarılı |
| Kullanıcı adı/parola denemesi | Cowrie login olayı oluşturmalı | Ayrı kontrollü test beklenecek | ⬜ Planlandı |
| Sahte oturum komutları | Girilen komutlar kaydedilmeli | Ayrı kontrollü test beklenecek | ⬜ Planlandı |

## Kanıtlar

### İlgili teknik belge

- [Stage 2 — SSH erişiminin güvenli hâle getirilmesi](02-secure-ssh.md)

### Servis ve port kanıtları

- [Cowrie dinleme portu](../../evidence/command-outputs/2026-10-01_stage-04_cowrie-listening-port.txt)
- [Port 22 yönlendirme kuralı](../../evidence/command-outputs/2026-10-01_stage-04_cowrie-port22-redirect-sanitized.txt)
- [Cowrie servis durumu](../../evidence/command-outputs/2026-10-01_stage-04_cowrie-service-status.txt)
- [Anonimleştirilmiş Cowrie systemd yapılandırması](../../evidence/sanitized-configs/2026-10-01_cyberhunter-cowrie.service)

### Kontrollü bağlantı kanıtları

- [Port 22 istemci yanıtı](../../evidence/screenshots/2026-10-01_stage-04_cowrie-port22-response_sanitized.png)
- [Cowrie JSON olay kaydı](../../evidence/command-outputs/2026-10-01_stage-04_cowrie-port22-event-sanitized.txt)

## Güvenlik sınırı

Cowrie tarafından üretilen veriler güvenilir girdi olarak kabul edilmemelidir.

- Log içeriği doğrudan komut çalıştırmak amacıyla kullanılmamalıdır.
- Yüklenen dosyalar izole bir ortamda tutulmalıdır.
- Gerçek saldırgan IP adresleri paylaşılmadan önce anonimleştirilmelidir.
- Kullanıcı adı ve parola denemeleri hassas veri olarak değerlendirilmelidir.
- Ham Cowrie logları doğrudan herkese açık repoya eklenmemelidir.
- İncelenecek zararlı dosyalar bu repoda çalıştırılmamalıdır.

## Sonuç

Cowrie SSH honeypot servisinin port `2222` üzerinde çalıştığı, port `22`
trafiğinin Cowrie'ye yönlendirildiği ve gerçek OpenSSH yönetim servisinin
port `22222` üzerinde ayrı tutulduğu doğrulanmıştır.

Kontrollü port `22` bağlantısı Cowrie tarafından işlenmiş ve ilgili JSON
olayları başarıyla oluşturulmuştur.

