# Kaynak Kod Envanteri ve Kökeni

Bu envanter, sohbet geçmişinden görülebilen dosyalarla repoya gerçekten alınan dosyaları ayırır.

## Repoya alınan tam kaynaklar

| Repo yolu | Geçmişteki çalışma yolu | Köken | Durum |
|---|---|---|---|
| `src/cyberhunter_cpu/normalizer.py` | `/opt/cyberhunter/workspaces/ai/src/cyberhunter_ai/normalizer.py` | Terminalde tam kaynak çıktısı + sonraki patch doğrulaması | Doğrulandı |
| `src/cyberhunter_cpu/inbox_worker.py` | `/opt/cyberhunter/apps/bridge/inbox_worker.py` | Önceki çalışmada oluşturulmuş tam dosya | Doğrulandı |
| `configs/systemd/cyberhunter-inbox-worker.service` | `/etc/systemd/system/...` | Önceki çalışmada oluşturulmuş tam dosya | Doğrulandı |
| `configs/systemd/cyberhunter-inbox-worker.timer` | `/etc/systemd/system/...` | Önceki çalışmada oluşturulmuş tam dosya | Doğrulandı |

## Geri kazanılmış yapılandırma örnekleri

`*.example` dosyaları gerçek `systemctl cat` çıktısından çıkarılmıştır; ortama bağlı yollar içerir ve doğrudan kurulumdan önce gözden geçirilmelidir.

## Tam içeriği henüz alınamayan dosyalar

- `esp32_tests/esp32_client.py`
- `live_esp32_db_test.py`
- `ai_bridge_receiver.py`
- `bridge_cli.py`
- `frontend_publisher.py`
- `watch_pcap` AI modülü ve model dosyaları
- `cyberhunter-ai-output-transfer` yürütülebilir betiği
- Cowrie ve SMTP uygulama kaynaklarının güncel tam kopyaları
- ESP32 `CyberHunterV2.cpp`
- FastAPI/backend ve dashboard kaynakları

Bu dosyalar yalnızca adları, yolları veya parçalı çıktıları görülebildiği için yeniden yazılmamıştır. Raspberry Pi/ekip repolarından güncel tam kopya ve hash alındığında eklenmelidir.

## Ekler hakkında

Paylaşılan sohbet sayfasında “Bir dosya yüklendi” biçiminde görünen bazı eski eklerin baytlarına erişilememiştir. Bu nedenle eklerden kod tahmin edilmemiştir.

