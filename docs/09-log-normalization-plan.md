# 09 — Log Normalizasyonu

Cowrie ve SMTP olayları `schema_version`, deterministik `event_id`, zaman, sensör, kaynak, olay türü, oturum, ağ, kimlik ve ayrıntı alanlarına dönüştürülür. Eksik değerler `unknown` olur.

Uygulanan kaynak kod [normalizer.py](../src/cyberhunter_cpu/normalizer.py) dosyasındadır. Ham olay ve normalleştirilmiş olay aynı kalıcı kimlikle test edilmelidir.

