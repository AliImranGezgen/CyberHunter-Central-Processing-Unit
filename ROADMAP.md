# Yol Haritası

| Öncelik | Görev | Beklenen çıktı | Başarı kriteri | Durum |
|---:|---|---|---|---|
| 1 | Kanıtları anonimleştirip ekleme | Metin çıktıları + görseller | Stage 1–17 için en az bir kanıt | ✅ |
| 2 | SSH sertleştirmesini yeniden ölçme | Efektif sshd ayarları | Parola erişimi kapalı, root girişi kapalı | ✅ |
| 3 | UFW ve geri dönüş planı | Kural dosyası + rollback | Yönetim erişimi kesilmeden test | ⬜ |
| 4 | Eksik servis kaynaklarını dışa aktarma | Güncel unit/script kopyaları | Hash + syntax doğrulaması | ⬜ |
| 5 | ESP32 firmware derleme/yükleme | Derleme logu + cihaz çıktısı | Hatasız derleme ve boot | ✅ |
| 6 | Düşük/yüksek risk röle testi | Serial + görsel kanıt | Eşik altı/üstü prototip davranışı doğru | ✅ |
| 7 | Uçtan uca kontrollü saldırı testi | Tek event_id izlenebilirliği | Cowrie → dashboard zinciri tamam | 🟡 |
| 8 | Uzun süre çalışma testi | 24–72 saat sağlık raporu | Veri kaybı/yığılma yok | ⬜ |
| 9 | Aktif soğutma kararı | Sıcaklık trendi | Throttling yok, güvenli sıcaklık | ⬜ |
| 10 | Kalıcı ağ/tünel tasarımı | Üretim topolojisi | Geçici ngrok bağımlılığı yok | ⬜ |
