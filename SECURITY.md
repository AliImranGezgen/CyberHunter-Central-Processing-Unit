# Güvenlik Politikası

## Repoya eklenmemesi gerekenler

- SSH private key ve gerçek `authorized_keys` içeriği
- Wi-Fi parolası, gerçek SSID gerekiyorsa maskesiz hâli
- Gerçek IP, MAC, gateway ve DNS bilgileri
- `.env`, token, API anahtarı ve GitHub kimlik bilgileri
- `/etc/shadow`, `/etc/gshadow` ve shell history
- Anonimleştirilmemiş saldırı logları
- İncelenmemiş PCAP dosyaları
- Seri numarası, QR kod veya kişisel bilgi içeren fotoğraflar

## Olay bildirimi

Güvenlik açığını public issue olarak açmayın. Repo sahibiyle özel kanal üzerinden iletişime geçin. Raporda etki, yeniden üretim adımları ve önerilen azaltım bulunmalıdır; gerçek saldırı verileri eklenmemelidir.

## Yanlışlıkla sızıntı

Hassas dosyayı son commit'ten silmek yeterli değildir. İlgili anahtar/token/parola derhâl iptal edilmeli veya döndürülmeli; Git geçmişi temizlenmeli ve olay kayıt altına alınmalıdır.

