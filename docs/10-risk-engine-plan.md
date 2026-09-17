# 10 — Risk Motoru

İlk katman açıklanabilir kurallar ve özelliklerden `0–100` risk skoru üretir; AI modeli sınıf/taktik ve güven bilgisi sağlar. Güveni yetersiz sonuçlar `Unknown` olarak işaretlenir.

AI fiziksel röleyi doğrudan çalıştırmaz. Nihai eşik cihaz yapılandırmasından alınır ve ESP32 tarafında karşılaştırılır. Gelecek sürüm için model kartı, veri seti kökeni, train/test ayrımı ve yeniden üretilebilir değerlendirme betikleri gereklidir.

