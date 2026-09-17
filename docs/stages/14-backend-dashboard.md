# Stage 14 — Backend, PostgreSQL ve Dashboard

**Durum:** ✅ Entegrasyon doğrulandı  
**Sorumluluk:** Kapsam dışı bileşen; yalnızca arayüz sözleşmesi

FastAPI backend ESP32 olaylarını kabul eder, PostgreSQL'e kaydeder ve aynı `event_id`nin tekrar eklenmesini engeller. Dashboard; kaynak IP, olay türü, komut, risk skoru, ESP32 skoru ve kararı görüntüler.

Geçmiş doğrulamada FastAPI → PostgreSQL → GET API → Dashboard hattında bir güvenlik olayının görüntülendiği kaydedilmiştir. Merkezi İşleme Birimi açısından gerekli kanıt, Raspberry'den çıkan `event_id`nin veritabanı ve dashboard kaydıyla aynı olmasıdır.

Backend ve dashboard kaynaklarının tamamı bu repoya alınmaz; ilgili ekip reposuna bağlantı daha sonra eklenmelidir.

## Kanıt alanı

![PostgreSQL kaydı ve dashboard olay satırı](PASTE_IMAGE_URL_HERE_STAGE_14_DASHBOARD)

