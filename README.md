# 📧 Erasmus+ Internship Automation Bot

Bu proje, Erasmus+ staj arayış sürecini hızlandırmak ve profesyonelleştirmek için tasarlanmış bir **Python otomasyon aracıdır**. Excel listesindeki her şirkete/üniversiteye özel hitaplarla ve kişiselleştirilmiş cümlelerle mail gönderimi yapar.

## ✨ Temel Özellikler

- **Dinamik İçerik:** Her mail, alıcı kurumun ismine göre özelleştirilir.
- **Kişiselleştirilmiş Cümleler:** Excel'de her satır için özel bir motivasyon cümlesi (`Ozel_Cumle`) tanımlanabilir. Eğer boş bırakılırsa bot, profesyonel bir varsayılan cümle kullanır.
- **Spam Koruması:** Mailler arasında rastgele (2-4 dakika) bekleme süreleri ekleyerek Gmail'in spam filtrelerine takılmayı önler.
- **Güvenli Mimari:** E-posta adresi, uygulama şifresi ve sosyal medya linkleri `.env` dosyasında saklanır; kod içerisinde asla açık metin olarak barındırılmaz.
- **Bağlantı Tazeleme:** Her mail gönderiminde SMTP sunucusuna yeniden bağlanarak uzun süreli işlemlerde kopma riskini minimize eder.

---

## 🛠️ Kurulum

1. **Depoyu Klonlayın:**
   ```
   git clone [https://github.com/Solynae/erasmus-internship-automation-bot.git](https://github.com/Solynae/erasmus-internship-automation-bot.git)
   cd erasmus-internship-automation-bot
```

2. **Gereksinimleri Yükleyin:**

```
pip install -r requirements.txt
```

3. **Yapılandırma (.env):**
Ana dizinde bir .env dosyası oluşturun ve aşağıdaki şablonu doldurun:

```
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
MY_EMAIL=ornek@gmail.com
MY_LINKEDIN=[https://linkedin.com/in/kullaniciadin](https://linkedin.com/in/kullaniciadin)
MY_GITHUB=[https://github.com/kullaniciadin](https://github.com/kullaniciadin)
```

**🔑 Gmail Uygulama Şifresi (App Password) Nasıl Alınır?**
Botun mail gönderebilmesi için Gmail "Uygulama Şifresi"ne ihtiyacı vardır. Normal şifreniz güvenlik nedeniyle çalışmayacaktır:

Google Hesabınıza gidin.

Güvenlik sekmesine tıklayın.

"Google'da oturum açma" altında 2 Adımlı Doğrulama'nın açık olduğundan emin olun.

Sayfanın en altına inip Uygulama Şifreleri'ne tıklayın.

"Uygulama seçin" kısmında "Diğer"i seçip bir isim verin (Örn: ErasmusBot).

Oluşturulan 16 haneli kodu kopyalayıp .env dosyanızdaki GMAIL_APP_PASSWORD kısmına yapıştırın.

📊 Excel Dosyası Yapısı (liste.xlsx) Botun düzgün çalışması için ana dizinde liste.xlsx adında bir Excel dosyası bulunmalıdır. Başlıklar tam olarak şu şekilde olmalıdır:
E-posta Adresi      Üniversite/Birim    Ozel_Cumle
info@company.com    Tech University     I am impressed by your research on AI.hr@startup.deFuture AI LabYour project on cloud computing is inspiring.

Not: Ozel_Cumle sütunu boşsa, bot otomatik olarak şirket ismini içeren genel bir profesyonel cümle oluşturur.

🚀 Çalıştırma
Tüm hazırlıklar tamamsa terminale şu komutu yazarak botu başlatabilirsiniz:

```
python mail_gonder.py
```

Geliştiren: Nazlıcan Ezeroğlu

3rd Year Software Engineering Student @ Istanbul Sabahattin Zaim University






