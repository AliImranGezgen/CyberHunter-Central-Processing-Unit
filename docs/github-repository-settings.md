# GitHub Repository Ayarları

`.github/settings.yml` dosyası Settings App kuruluysa ayarların önemli bölümünü otomatik uygular. App kullanılmayacaksa aşağıdaki ayarları GitHub arayüzünden yapın.

## General

- Default branch: `main`
- Issues: açık
- Projects ve Wiki: ihtiyaç yoksa kapalı
- Squash merge: açık
- Merge commit: kapalı
- Rebase merge: kapalı
- Head branch'i otomatik sil: açık
- Auto-merge: yalnızca tüm zorunlu kontrollerden sonra açık olabilir

## Ruleset / Branch protection: `main`

- Pull request zorunlu
- En az 1 onay
- Yeni commit geldiğinde eski onayları düşür
- CODEOWNERS onayı zorunlu
- Son push başka bir kişi tarafından onaylanmalı
- Tüm konuşmalar çözülmeli
- Branch merge öncesi güncel olmalı
- Zorunlu kontroller: `Python quality / test`, `Secret scan / gitleaks`, `Markdown links / lychee`
- Force push ve deletion kapalı
- Admin bypass kullanılmamalı; acil durum prosedürü ayrıca kayıt altına alınmalı

## Actions

- Workflow izinleri: read repository contents
- GitHub Actions'ın PR oluşturma/onaylama izni kapalı
- Dependabot security updates açık
- Secret scanning ve push protection, plan destekliyorsa açık

## PR kabul politikası

Bir PR yalnızca kapsamı açık, testleri geçmiş, hassas bilgi kontrolü tamamlanmış ve dokümantasyonu güncellenmişse kabul edilir. Donanım/SSH/firewall değişikliklerinde geri dönüş planı zorunludur.

