# Görsel ve Kanıt Listesi

Bu dosya Stage 1–19 tamamlandıktan sonra çekilecek/eklenecek kanıtların merkez listesidir. Stage dosyalarındaki ilgili `PASTE_IMAGE_URL_HERE_...` değerini yalnızca yüklediğiniz görsel URL'siyle değiştirin.

| Öncelik | Stage | Kanıt | Format | URL anahtarı |
|---:|---:|---|---|---|
| 1 | 1 | Raspberry Pi 5, güç ve depolama düzeni | Fotoğraf | `STAGE_01_RASPBERRY_SETUP` |
| 1 | 2 | `ss -lntp`, port 22 reddi, 22222 başarı | PNG/TXT | `STAGE_02_SSH_PORTS` |
| 2 | 3 | Python sürümleri ve sanal ortam yolları | TXT/PNG | `STAGE_03_PYTHON_ENVS` |
| 1 | 4 | Cowrie login/command olayı, IP maskeli | TXT/PNG | `STAGE_04_COWRIE_EVENT` |
| 2 | 5 | Capture servis durumu ve PCAP dizini | TXT/PNG | `STAGE_05_PACKET_CAPTURE` |
| 1 | 6 | Aynı olayın ham/normalize karşılaştırması | TXT/PNG | `STAGE_06_NORMALIZER` |
| 2 | 7 | AI confusion matrix/metrik raporu | PNG | `STAGE_07_AI_METRICS` |
| 1 | 8 | Publisher'ın atomik JSON dosyası | TXT/PNG | `STAGE_08_PUBLISHER` |
| 1 | 9 | outbox/inbox/archive/rejected dizinleri | PNG | `STAGE_09_BRIDGE_QUEUES` |
| 1 | 10 | Pi–ESP32 SDA/SCL/GND bağlantısı | Fotoğraf | `STAGE_10_I2C_WIRING` |
| 1 | 11 | Frame/AES-GCM başarı çıktısı | PNG/TXT | `STAGE_11_AES_GCM` |
| 1 | 12 | ESP32 response + aynı event_id | PNG/TXT | `STAGE_12_ESP32_RESPONSE` |
| 1 | 13 | HTTPS POST ve 2xx cevabı | PNG/TXT | `STAGE_13_BACKEND_POST` |
| 1 | 14 | PostgreSQL satırı + dashboard kaydı | PNG | `STAGE_14_DASHBOARD` |
| 1 | 15 | Dashboard eşik ayarı + GET config | PNG | `STAGE_15_THRESHOLD` |
| 1 | 16 | Röle kartı, GPIO ve besleme | Fotoğraf | `STAGE_16_RELAY_WIRING` |
| 1 | 17 | Düşük/yüksek riskte LED durumları | Video/PNG | `STAGE_17_LED_BEHAVIOR` |
| 1 | 18 | Arduino build ve Serial Monitor | PNG/TXT | `STAGE_18_ARDUINO_BUILD` |
| 1 | 19 | Tek event_id'nin tüm katmanlarda izi | PNG/TXT | `STAGE_19_E2E_TRACE` |

## Dosya adlandırma

`YYYY-MM-DD_stage-NN_konu_kanit-turu.ext`; tarih bilinmiyorsa `undated_...`.

Komut çıktısını mümkünse ekran görüntüsü yerine `.txt` olarak ekleyin. Kullanıcı adı, ev dizini, IP, MAC, SSID, token, parola ve gerçek saldırgan verilerini temizleyin.

