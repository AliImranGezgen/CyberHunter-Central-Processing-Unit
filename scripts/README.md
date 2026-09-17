# Betikler

- `setup/`: idempotent kurulum işlemleri
- `validation/`: salt-okunur doğrulamalar
- `maintenance/`: yedekleme, log rotasyonu ve kontrollü bakım

Yeni betikler `set -euo pipefail` yaklaşımını, açık loglamayı ve SSH/firewall değişikliklerinde geri dönüş yöntemini içermelidir. Bu repoda doğrulanmamış kurulum betiği oluşturulmaz.

