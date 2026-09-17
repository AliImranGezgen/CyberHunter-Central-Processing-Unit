# Stage 9 — Bridge ve Güvenilir Dosya Aktarımı

**Durum:** ✅ Tamamlandı  
**Sorumluluk:** Merkezi İşleme Birimi

## Amaç

Publisher olaylarını kayıp, yinelenme ve yarım yazılmış dosya riskini azaltarak ESP32 tüketicisine taşımak.

## Kuyruk modeli

`ai/output → bridge/outbox → bridge/inbox → processing → archive/rejected`

- Dosyalar `os.replace` gibi atomik hareketlerle sahiplenilir.
- `event_id` ile olay/cevap eşleşmesi yapılır.
- Geçici hatalarda sınırlı retry, kalıcı şema hatalarında rejected uygulanır.
- Başarılı olaylar archive'a taşınır; state dosyası deneme sayısı ve ESP32 cevabını kaydeder.
- Inbox Worker aynı anda birden fazla örneğin çalışmasını dosya kilidiyle engeller.

İlgili unit'ler: output-transfer service/path/timer, Bridge sender/receiver ve Inbox Worker service/timer.

## Kaynak

[`src/cyberhunter_cpu/inbox_worker.py`](../../src/cyberhunter_cpu/inbox_worker.py) ve karşılık gelen systemd dosyaları repoda bulunur.

## Kanıt alanı

![Bridge kuyruk dizinleri](PASTE_IMAGE_URL_HERE_STAGE_09_BRIDGE_QUEUES)

