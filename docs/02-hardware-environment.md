# 02 — Donanım Ortamı

| Bileşen | Özellik | Durum | Not |
|---|---|---|---|
| Raspberry Pi 5 | 16 GB RAM | Aktif | Merkezi işlem birimi |
| microSD | 64 GB SanDisk Ultra | Aktif | Ubuntu Server |
| USB bellek | 128 GB | Mevcut | İlk boot/yardımcı depolama denemeleri |
| Adaptör | 5 V / 3 A | Prototip | Güç marjı izlenmeli |
| Aktif fan | Yok | Açık görev | Uzun süreli sıcaklık testi gerekli |
| ESP32 | Adres `0x08` | Entegre | SDA/SCL/GND |

Geçmişte Ubuntu ortamında yaklaşık `56,2°C`, Raspberry Pi OS ortamında yaklaşık `45°C` ölçülmüştür. Farklı işletim/çalışma koşulları nedeniyle doğrudan kıyas sonucu çıkarılmamalıdır.

