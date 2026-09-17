# Yeni GitHub Reposunu Açma

## Önerilen ilk durum

Repo ilk aşamada **private** açılmalıdır. Kanıtlar eklendikten, secret scan çalıştıktan ve PCAP/log politikası doğrulandıktan sonra public yapma kararı yeniden değerlendirilmelidir.

Önerilen ad: `CyberHunter-Central-Processing-Unit`

Önerilen açıklama: `CyberHunter Raspberry Pi merkezi işleme birimi, honeypot, AI ve ESP32 bridge çalışmaları`

Önerilen konular: `raspberry-pi`, `honeypot`, `cowrie`, `cybersecurity`, `esp32`, `i2c`, `systemd`, `python`

## Yerel başlangıç

```bash
git init -b main
git add .
git status
```

İlk commit öncesinde:

```bash
python -m pip install -e '.[dev]'
pytest
ruff check .
```

Ardından GitHub'da boş, README/License eklenmemiş repo oluşturun ve arayüzün verdiği remote/push komutlarını kullanın. Bu paket hazırlanırken commit veya push yapılmamıştır.

## GitHub ayar sırası

1. Actions workflow'larının ilk kez çalışmasını bekleyin.
2. `main` ruleset/branch protection oluşturun.
3. Zorunlu status check'leri seçin.
4. CODEOWNERS onayını açın.
5. Secret scanning/push protection'ı etkinleştirin.
6. Settings App kullanacaksanız `.github/settings.yml` erişimini onaylayın.

