# Stage 6 — Normalizer Servisinin Geliştirilmesi

**Durum:** ✅ Tamamlandı  
**Sorumluluk:** Merkezi İşleme Birimi

## Amaç

Cowrie ve SMTP'den gelen farklı ham olay yapılarını tek, tahmin edilebilir bir CyberHunter şemasına dönüştürmek.

## İşlevler

- Kaynağa göre olay türü eşleme
- Deterministik UUIDv5 `event_id` üretimi
- Ağ, kimlik ve ayrıntı alanlarının ortak yapıya taşınması
- Eksik alanlarda `unknown` kullanımı
- `cowrie.command.input` olayının `command.executed` olarak eşlenmesi ve komutun `details.command` alanına eklenmesi
- Normalleştirilmiş JSONL çıktısının `/var/lib/cyberhunter/ai/input/cowrie.normalized.jsonl` yoluna yazılması

Normalizer periyodik `cyberhunter-normalizer.service` ve `.timer` birimleriyle çalıştırıldı. Dökümenteryada 754 Cowrie olayının normalleştirildiği kaydedilmiştir.

## Kaynak

Güncel tam içerik: [`src/cyberhunter_cpu/normalizer.py`](../../src/cyberhunter_cpu/normalizer.py). Birim testleri `tests/unit/test_normalizer.py` altındadır.

## Kanıt alanı

![Ham ve normalleştirilmiş olay karşılaştırması](PASTE_IMAGE_URL_HERE_STAGE_06_NORMALIZER)

