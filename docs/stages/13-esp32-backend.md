# Stage 13 — ESP32'nin Backend'e Bağlanması

**Durum:** ✅ Entegrasyon doğrulandı  
**Sorumluluk:** Kapsam dışı bileşen; yalnızca arayüz sözleşmesi

ESP32'nin Wi-Fi üzerinden backend'e olay göndermesi sağlandı. Olaylar `POST /api/security-events` uç noktasına iletilir; sorgulama için `GET /api/security-events/query` kullanılır. HTTP `2xx` başarılı işlem sayılır ve ESP32 Raspberry'ye `processed:true` cevabı verir.

Bağlantı kesilmesi durumunda yeniden bağlanma uygulanır. Geçmiş testlerde geçici ngrok alan adları kullanılmıştır; bunlar kaynak koda sabitlenmemeli, secret olmayan ortam/yapılandırma üzerinden yönetilmelidir. Üretim mimarisinde TLS sertifika doğrulaması ve kalıcı adresleme ayrıca ele alınmalıdır.

## Kanıt alanı

![ESP32 HTTPS POST ve HTTP 2xx](PASTE_IMAGE_URL_HERE_STAGE_13_BACKEND_POST)

