# Katkı Rehberi

## Branch adları

`feature/*`, `config/*`, `docs/*`, `test/*`, `security/*`, `fix/*`

## Commit türleri

`feat:`, `fix:`, `docs:`, `config:`, `test:`, `security:`, `refactor:`, `chore:`

## Pull request kuralları

- `main` branch'ine doğrudan push yapılmaz.
- En az bir onay gerekir; kod sahibi kendi PR'ını tek başına onaylayamaz.
- CI kontrolleri geçmeden merge yapılmaz.
- Squash merge tercih edilir; merge commit ve rebase merge kapatılır.
- Branch güncel değilse merge engellenir.
- Konuşmalar çözülmeden merge yapılamaz.

## PR kontrol listesi

- [ ] Hassas bilgi ve gerçek IP/MAC kontrol edildi.
- [ ] Test sonucu veya neden test edilemediği açıklandı.
- [ ] Dokümantasyon ve durum tablosu güncellendi.
- [ ] Yapılandırma değişikliği için geri dönüş yöntemi var.
- [ ] SSH/firewall değişikliği yönetim erişimini kesmiyor.
- [ ] Yeni dosyanın kökeni ve sahipliği açık.

