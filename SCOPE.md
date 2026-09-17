# Kapsam ve Sorumluluk Sınırları

## Kapsam içi

- Raspberry Pi 5 ve Ubuntu Server kurulumu
- Ağ ve güvenli yönetim SSH yapılandırması
- Gerçek SSH ile sahte SSH servisinin ayrıştırılması
- Raspberry tarafındaki Cowrie ve SMTP honeypot bileşenleri
- Paket yakalama, olay toplama ve log normalizasyonu
- AI çalışma ortamı, Publisher ve dosya kuyrukları
- Raspberry tarafındaki I²C bridge ve ESP32 mesaj sözleşmesi
- systemd servisleri, sağlık kontrolleri ve doğrulama testleri
- Teknik ilerleme ile kanıtların anonimleştirilmiş biçimde belgelenmesi

## Entegrasyon sınırında

Aşağıdaki bileşenler, Merkezi İşleme Birimiyle arayüzleri bakımından belgelenir; kaynak kodlarının tamamı bu reponun sorumluluğunda değildir:

- ESP32 firmware'i
- FastAPI backend
- PostgreSQL veritabanı
- Dashboard
- Dinamik izolasyon eşiği
- Sekiz kanallı röle prototipi

## Kapsam dışı

- İki ESP cihazı arasındaki haberleşme
- Röle kartının elektronik tasarımı
- Fiziksel güç veya Ethernet kesme devresinin nihai tasarımı
- Ana sunucunun uygulama kaynak kodu
- Patent, lisanslama ve iş modeli dokümantasyonu
- Diğer ekip üyelerinin sahipliğindeki tam kaynak kodlar

