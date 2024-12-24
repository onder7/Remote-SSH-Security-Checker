Bu script ile uzak sunucudaki SSH güvenlik durumunu kolayca kontrol edebilirsiniz.
Karşı cihazda SSH güvenlik kontrolü yapmak için script'i aşağıdaki gbi çalıştırın

Script hakkında:

OpenSSH'ın yüklü olup olmadığını kontrol eder
Versiyon bulunamazsa uygun mesaj gösterir
None değerleri için güvenli kontroller yapar
Daha açıklayıcı hata mesajları verir

Not: Bu scriptin çalışması için sisteminizde OpenSSH yüklü olması gerekir. Eğer yüklü değilse, önce OpenSSH'ı yüklemeniz önerilir.

Kullanım talimatları:

1. Önce gerekli kütüphaneyi yükleyin:
```bash
pip install paramiko
```

2. Scripti çalıştırın:
```bash
python remote_ssh_check.py
```

3. İstenilen bilgileri girin:
- Hedef sunucu IP adresi
- Kullanıcı adı
- Şifre

Önemli Notlar:
- Bu scripti kullanmak için hedef sunucuda SSH erişiminizin olması gerekir
- Root yetkilerine sahip bir kullanıcı ile çalıştırmak daha detaylı sonuç verir
- Bazı kontroller için sudo yetkisi gerekebilir
- Script'i kullanmadan önce gerekli izinleri aldığınızdan emin olun

Güvenlik Kontrolleri:
- SSH versiyon kontrolü
- Konfigürasyon dosyası analizi
- Güvenlik riskleri tespiti
- Öneriler sunma

  Önder AKÖZ / https://ondernet.net
