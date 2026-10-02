# Betikler

- `setup/`: idempotent kurulum işlemleri
- `validation/`: salt-okunur doğrulamalar
- `maintenance/`: yedekleme, log rotasyonu ve kontrollü bakım

Yeni betikler `set -euo pipefail` yaklaşımını, açık loglamayı ve SSH/firewall değişikliklerinde geri dönüş yöntemini içermelidir. Bu repoda doğrulanmamış kurulum betiği oluşturulmaz.

## Repo bütünlük denetimi

`python scripts/validation/audit_repository.py` komutu 19 stage belgesinin
varlığını, Markdown kod bloklarını, yerel bağlantıları, JSON dosyalarını ve
görsel dosya imzalarını ve stage başına tarihli kanıt dağılımını salt okunur biçimde denetler. Kanıtı
olmayan stage bir uyarıdır; kırık belge yapısı veya bağlantı hatadır.
