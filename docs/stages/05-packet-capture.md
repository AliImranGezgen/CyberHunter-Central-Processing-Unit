# Stage 5 — Ağ Paketlerinin Yakalanması

**Durum:** ✅ Tamamlandı  
**Sorumluluk:** Merkezi İşleme Birimi

## Amaç

Cowrie uygulama loglarını ağ seviyesindeki kanıtlarla ilişkilendirmek ve AI katmanına paket tabanlı özellikler sağlamak.

## Yapılan çalışmalar

- Port `22` ve yerel `2222` trafiği için paket yakalama düzeni oluşturuldu.
- Yakalanan trafik PCAP biçiminde, aktif ve kapanmış dosyalar ayrılarak saklandı.
- İşlem `cyberhunter-ai-capture.service` adıyla bağımsız servis hâline getirildi.
- Zaman damgası, kaynak IP/port ve oturum bilgileri üzerinden Cowrie kayıtlarıyla korelasyon altyapısı kuruldu.

## Güvenlik ve veri yönetimi

PCAP dosyaları kimlik bilgisi, payload ve kişisel veri içerebilir. Bu nedenle repo tarafından varsayılan olarak yok sayılır. Paylaşım öncesinde içerik incelemesi, minimizasyon ve anonimleştirme zorunludur.

## Kanıt alanı

![Paket yakalama servisi ve PCAP dizini](PASTE_IMAGE_URL_HERE_STAGE_05_PACKET_CAPTURE)

