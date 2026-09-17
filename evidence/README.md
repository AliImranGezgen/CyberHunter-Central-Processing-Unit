# Kanıt Ekleme Rehberi

## Klasörler

- `command-outputs/`: aranabilir `.txt` çıktıları
- `screenshots/`: terminal, dashboard ve Serial Monitor görselleri
- `hardware-photos/`: Raspberry Pi, ESP32 ve röle fotoğrafları
- `test-results/`: test raporları
- `sanitized-configs/`: anonimleştirilmiş etkin yapılandırmalar

## İsimlendirme

`YYYY-MM-DD_konu_kanit-turu.ext`; tarih bilinmiyorsa `undated_konu_kanit-turu.ext`.

Örnekler:

- `undated_ssh-port-22222_command-output.txt`
- `undated_port-22-refused_screenshot.png`
- `undated_raspberry-pi5-setup_photo.jpg`

## Zorunlu temizlik

IP, MAC, kullanıcı adı, kişisel yol, SSID, token, parola, özel anahtar ve gerçek saldırgan kimliği silinmeli veya açık placeholder ile değiştirilmelidir. Kanıtın neyi doğruladığını anlatan kısa bir `.md` açıklaması eklenmelidir.

