# Stage 3 — Python Çalışma Ortamlarının Hazırlanması

**Durum:** 🟡 Devam ediyor
**Sorumluluk:** Merkezi İşleme Birimi

## Amaç

İşletim sistemi paketleriyle CyberHunter servislerinin Python
bağımlılıklarını birbirinden ayırmak ve bir bileşende yapılan güncellemenin
diğer bileşenleri bozma riskini azaltmak.

Ayrıca her servisin yalnızca gerekli kullanıcı, çalışma dizini ve Python
ortamıyla çalışması hedeflenmektedir.

## Sistem Python ortamı

Ubuntu Server tarafından sağlanan sistem Python ortamı:

```text
Yol: /usr/bin/python3
Gerçek yol: /usr/bin/python3.12
Sürüm: Python 3.12.3
Sanal ortam: Hayır
```

Sistem Python'u işletim sistemi araçları tarafından da kullanılabileceği
için proje bağımlılıklarının doğrudan bu ortama kurulmasından
kaçınılması hedeflenmektedir.

## Hazırlanan sanal ortamlar

| Ortam | Python sürümü | Konum | Durum |
|---|---:|---|---:|
| Decoy | 3.11.15 | `/opt/cyberhunter/venvs/decoy` | ✅ Doğrulandı |
| Bridge | 3.11.15 | `/opt/cyberhunter/venvs/bridge` | ✅ Doğrulandı |
| AI merkezi ortam | 3.11.15 | `/opt/cyberhunter/venvs/ai` | ✅ Doğrulandı |
| AI workspace ortamı | 3.11.15 | `/opt/cyberhunter/workspaces/ai/.venv` | ✅ Doğrulandı |
| SMTP | 3.12.3 | `/opt/cyberhunter-smtp/venv` | ✅ Doğrulandı |

Ana sanal ortam dizinleri `root` kullanıcısına aittir. Servis gruplarına
okuma ve çalıştırma izni vermek için grup sahipliği ve `750` izinleri
kullanılmıştır.

```text
decoy  → root:cyberdecoy 750
bridge → root:cyberbridge 750
ai     → root:cyberai 750
```

## Servis ve Python ortamı eşleşmeleri

| Servis | Çalıştırıcı | Servis hesabı | Değerlendirme |
|---|---|---|---|
| Cowrie | Decoy sanal ortamı | `cyberdecoy` | ✅ İzole |
| Inbox Worker | Bridge sanal ortamı | `cyberbridge` | ✅ İzole |
| AI analiz | AI workspace sanal ortamı | `cyberai` | ✅ İzole |
| AI Publisher | AI workspace sanal ortamı | `cyberai` | ✅ İzole |
| SMTP honeypot | SMTP sanal ortamı | `smtpot` | ✅ İzole |
| AI Bridge Receiver | Sistem Python | `cyberbridge` | 🟡 Taşınmalı |
| Bridge Outbox Sender | Sistem Python | `cyberbridge` | 🟡 Taşınmalı |
| Normalizer | Sistem Python ve `PYTHONPATH` | `cybernormalize` | 🟡 Taşınmalı |
| AI Capture | Bash script | `root` | 🟡 Yetki incelenmeli |
| AI Output Transfer | Sistem Python | `root` | 🟡 Yetki ve ortam incelenmeli |

## Tamamlanan çalışmalar

- Ubuntu sistem Python sürümü doğrulandı.
- Python 3.11.15 tabanlı Decoy, Bridge ve AI sanal ortamları oluşturuldu.
- AI workspace için ayrı Python 3.11.15 sanal ortamı oluşturuldu.
- SMTP honeypot için Python 3.12.3 sanal ortamı oluşturuldu.
- Cowrie ayrı `cyberdecoy` hesabıyla çalışacak şekilde yapılandırıldı.
- Bridge Inbox Worker ayrı `cyberbridge` hesabıyla çalışacak şekilde yapılandırıldı.
- AI servisleri ayrı `cyberai` hesabıyla çalışacak şekilde yapılandırıldı.
- SMTP honeypot ayrı `smtpot` hesabıyla çalışacak şekilde yapılandırıldı.
- Normalizer için ayrı `cybernormalize` hesabı kullanıldı.
- systemd servislerinde çalışma dizinleri ve çalıştırıcı yolları açıkça tanımlandı.
- Normalizer için gerekli `PYTHONPATH` systemd yapılandırmasında tanımlandı.

## Açık çalışmalar

- AI Bridge Receiver, Bridge sanal ortamına taşınmalıdır.
- Bridge Outbox Sender, Bridge sanal ortamına taşınmalıdır.
- Normalizer için uygun AI sanal ortamı seçilmeli ve sistem Python kullanımı kaldırılmalıdır.
- AI Output Transfer ayrı bir sanal ortama taşınmalıdır.
- AI Output Transfer için ayrı servis hesabı değerlendirilmelidir.
- AI Capture servisinin root gereksinimi incelenmelidir.
- Paket yakalama için Linux capability kullanımı değerlendirilmelidir.
- Kullanılmıyorsa `/opt/cyberhunter/venvs/ai` ortamının amacı netleştirilmelidir.
- Sanal ortam dizinleri ve Python sürümleri için ortak standart hazırlanmalıdır.
- Her sanal ortamın bağımlılık kilit dosyası oluşturulmalıdır.

## Mühendislik gerekçesi

Sanal ortamlar aşağıdaki faydaları sağlar:

- Bileşenler arasında bağımlılık çakışmasını azaltır.
- Paket güncellemelerinin etki alanını sınırlar.
- Geri dönüş işlemlerini kolaylaştırır.
- Sistem Python ortamının bozulmasını önler.
- Her servis için tekrar üretilebilir çalışma ortamı oluşturur.
- Olay incelemesi sırasında kullanılan bağımlılık sürümlerinin belirlenmesini kolaylaştırır.

Ayrı servis hesapları ise bir bileşenin ele geçirilmesi durumunda
saldırganın erişebileceği sistem kaynaklarını sınırlandırır.

## Test ve doğrulama sonuçları

| Kontrol | Beklenen sonuç | Gerçekleşen sonuç | Durum |
|---|---|---|---|
| Sistem Python | Python 3.12 | Python 3.12.3 | ✅ Başarılı |
| Decoy ortamı | Sanal ortam olmalı | Python 3.11.15, `True` | ✅ Başarılı |
| Bridge ortamı | Sanal ortam olmalı | Python 3.11.15, `True` | ✅ Başarılı |
| AI merkezi ortam | Sanal ortam olmalı | Python 3.11.15, `True` | ✅ Başarılı |
| AI workspace ortamı | Sanal ortam olmalı | Python 3.11.15, `True` | ✅ Başarılı |
| SMTP ortamı | Sanal ortam olmalı | Python 3.12.3, `True` | ✅ Başarılı |
| Cowrie izolasyonu | Decoy ortamını kullanmalı | Doğrulandı | ✅ Başarılı |
| Inbox Worker izolasyonu | Bridge ortamını kullanmalı | Doğrulandı | ✅ Başarılı |
| AI servis izolasyonu | AI ortamını kullanmalı | Doğrulandı | ✅ Başarılı |
| SMTP izolasyonu | SMTP ortamını kullanmalı | Doğrulandı | ✅ Başarılı |
| Bridge Receiver izolasyonu | Bridge ortamını kullanmalı | Sistem Python kullanıyor | 🟡 Açık |
| Outbox Sender izolasyonu | Bridge ortamını kullanmalı | Sistem Python kullanıyor | 🟡 Açık |
| Normalizer izolasyonu | AI ortamını kullanmalı | Sistem Python kullanıyor | 🟡 Açık |
| Root servislerinin azaltılması | En düşük yetki uygulanmalı | İki servis root kullanıyor | 🟡 Açık |

## Kanıtlar

- [Sistem Python sürümü](../../evidence/command-outputs/2026-10-01_stage-03_system-python.txt)
- [Python sanal ortamları](../../evidence/command-outputs/2026-10-01_stage-03_virtual-environments.txt)
- [Servis ve Python ortamı eşleşmeleri](../../evidence/command-outputs/2026-10-01_stage-03_python-service-bindings-sanitized.txt)

## Güvenlik değerlendirmesi

Sistem Python'u kullanan proje servisleri işletim sistemi paketleriyle
bağımlılık çakışması yaşayabilir. Ayrıca root hesabıyla çalışan servisler,
ele geçirilmeleri durumunda daha geniş bir etki alanı oluşturabilir.

Paket yakalama işlemi bazı yüksek yetkiler gerektirebilir. Ancak servisin
tamamen root olarak çalıştırılması yerine aşağıdaki yöntemler
değerlendirilmelidir:

- Ayrı paket yakalama servis hesabı
- `CAP_NET_RAW`
- Gerekiyorsa `CAP_NET_ADMIN`
- Yazılabilir dizinlerin sınırlandırılması
- systemd sandbox seçenekleri
- Salt okunur sistem dizinleri

Bu değişiklikler kontrollü test ve geri dönüş planı olmadan
uygulanmamalıdır.

## Sonuç

CyberHunter bileşenleri için birden fazla bağımsız Python sanal ortamı
oluşturulmuş ve temel servislerin önemli bir bölümü ayrı servis
hesaplarıyla bu ortamlara bağlanmıştır.

Bununla birlikte AI Bridge Receiver, Bridge Outbox Sender, Normalizer ve
AI Output Transfer hâlen sistem Python ortamını kullanmaktadır. AI
Capture ve AI Output Transfer servisleri root hesabıyla
yapılandırılmıştır.

Bu nedenle Python ortamlarının hazırlanması büyük ölçüde tamamlanmış,
ancak tam bağımlılık ve yetki izolasyonu henüz tamamlanmamıştır.