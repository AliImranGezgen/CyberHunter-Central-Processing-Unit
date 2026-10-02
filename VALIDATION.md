# Repo Doğrulama Kaydı

**Tarih:** 2026-10-02
**Ortam:** Yerel macOS, Python 3.11 uyumlu sanal ortam

| Kontrol | Sonuç |
|---|---|
| Python bytecode derleme | ✅ |
| Pytest | ✅ 9 test geçti |
| Ruff | ✅ Hata yok |
| JSON parse | ✅ |
| Stage belgeleri | ✅ 19/19 |
| Tarihli kanıt dosyaları | ✅ 74 dosya |
| Göreli Markdown bağlantıları | ✅ Kırık bağlantı yok |
| Markdown kod blokları | ✅ Kapanmamış blok yok |
| Stage 1–18 kanıt kapsamı | ✅ Her stage için en az bir dosya |
| Stage 19 ortak kabul kanıtı | ⚠️ Tek event ID zinciri henüz yok |
| Görsel örneklerde gizlilik kontrolü | ✅ Maskeli/test verisi; açık secret görülmedi |

Kullanılan komutlar:

```bash
python scripts/validation/audit_repository.py
python -m compileall -q src tests scripts
ruff check .
pytest -q
git diff --check
```

Bu kayıt GitHub Actions sonucunun yerine geçmez. Donanım ve uzak Raspberry Pi
çalışma zamanı yalnızca repoya alınmış tarihli kanıtlar ölçüsünde doğrulanmıştır.
Stage 19, NTP, replay koruması, TLS/secret provisioning ve fiziksel röle
izolasyonu gibi açık saha işleri yerel testle tamamlanmış sayılmamıştır.
