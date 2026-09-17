# 05 — SSH Yönetim Yapılandırması

OpenSSH kurulumundaki `/run/sshd` sorunu çözüldü; başlangıçta `ssh.socket` ile port 22 doğrulandı. Ed25519 anahtarı oluşturuldu, yönetim servisi `22222`ye taşındı ve port 22 Cowrie'ye ayrıldı.

Etkin yapılandırma `sshd -T`, dinleme durumu `ss -lntp`, servis durumu `systemctl` ve iki eş zamanlı terminal bağlantısıyla doğrulandı. Root girişi kapalıdır.

Geçmişte doğrulanan durum:

```text
Port 22222
PermitRootLogin no
PubkeyAuthentication yes
PasswordAuthentication yes
```

Hedef durum `PasswordAuthentication no`dur; güncel kanıt eklenmelidir.

