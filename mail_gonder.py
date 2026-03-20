import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time
import random
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# ================= AYARLAR (GÜVENLİ) =================
DOSYA_ADI = "liste.xlsx"
CV_DOSYASI = "nazlican-ezeroglu-cv.pdf" # Bu dosya ismi genel kalabilir
GONDEREN_MAIL = os.getenv("MY_EMAIL") # .env'den çeker
UYGULAMA_SIFRESI = os.getenv("GMAIL_APP_PASSWORD") 
LINKEDIN_URL = os.getenv("MY_LINKEDIN")
GITHUB_URL = os.getenv("MY_GITHUB")
# ===========================================

def mail_gonder():
    print("🚀 Başvuru robotu (ŞİRKET MODU) başlatılıyor...")
    print("⚠️ Konu Başlığı: Erasmus+ Internship - Nazlıcan Ezeroğlu")
    print("⚠️ Hitap: Dear Hiring Manager")
    print("⚠️ Her mail için sunucuya tekrar bağlanılacak (Kopma riski yok).")
    
    # Şifre Kontrol
    if not UYGULAMA_SIFRESI:
        print("❌ HATA: .env dosyasında şifre yok!")
        return
    if not os.path.exists(DOSYA_ADI) or not os.path.exists(CV_DOSYASI):
        print("❌ HATA: Dosyalar eksik!")
        return

    # Excel Oku
    try:
        df = pd.read_excel(DOSYA_ADI)
        print(f"✅ Excel okundu. Toplam {len(df)} kişi var.")
    except Exception as e:
        print(f"❌ Excel hatası: {e}")
        return

    gonderilen_sayisi = 0

    for index, row in df.iterrows():
        # Gerçek alıcı bilgilerini al
        alici_mail = str(row.get('E-posta Adresi')).strip()
        sirket = str(row.get('Üniversite / Birim')).strip()
        ozel_cumle = str(row.get('Ozel_Cumle')).strip()

        # Mail adresi geçersizse atla
        if "@" not in alici_mail or len(alici_mail) < 5:
            continue

        # --- BAĞLANTIYI BURADA AÇIYORUZ (HER KİŞİ İÇİN YENİDEN) ---
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(GONDEREN_MAIL, UYGULAMA_SIFRESI)
        except Exception as e:
            print(f"❌ Sunucu bağlantı hatası: {e}")
            time.sleep(60) # Hata olursa 1 dk bekle ve diğer kişiye geç
            continue

        # --- ŞİRKETLER İÇİN ÖZEL HİTAP ---
        hitap = "Hiring Manager"

        # Özel Cümle Kontrolü
        if len(ozel_cumle) < 10 or ozel_cumle == "nan":
             ozel_cumle = f"I have been closely following how {sirket} is redefining industry standards, and I want to be part of this transformation."

        # --- SABİT KONU BAŞLIĞI ---
        konu_basligi = "Erasmus+ Internship - Nazlıcan Ezeroğlu"
        
        # HTML İçerik
        icerik_html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; font-size: 11pt; color: #000000;">
            <p>Dear {hitap},</p>
            
            <p>As a third-year Software Engineering student (3.20/4.00 GPA) at Istanbul Sabahattin Zaim University, I am writing to propose my candidacy as an Erasmus+ intern to transform my academic and practical background in Cloud Computing and Artificial Intelligence into value at {sirket}.</p>
            
            <p>{ozel_cumle}</p>
            
            <p>I am not just a student with theoretical knowledge, but an engineering candidate who transforms learning into projects and community benefit:</p>
            
            <ul>
                <li><b>AI & Technical Competence:</b> During the Akbank GenAI Bootcamp, I developed an end-to-end virtual assistant using LLMs and RAG architecture. Additionally, in my "Renewable Energy Data Analysis" project using Python, I demonstrated my ability to derive meaningful insights from complex datasets.</li>
                <br>
                <li><b>Leadership & Communication:</b> As a Huawei Student Developers Campus Ambassador and Volunteer Cloud Trainer, I am someone who not only applies technical knowledge but also transmits it. Through the technical workshops and trainings I organized, I honed my skills in explaining complex technical concepts to diverse audiences in simple terms and improved my intra-team communication skills.</li>
                <br>
                <li><b>Global Vision:</b> My achievements in global leadership programs such as Aspire Leaders and McKinsey Forward have strengthened my problem-solving abilities and adaptation to international working cultures.</li>
            </ul>

            <p><b>Important Note (Financial & Time Constraints):</b><br>
            I will be supported by the Erasmus+ grant, covering my own living and insurance expenses. However, due to the grant procedures, I am required to submit an acceptance letter by <b>February 2nd</b>. Therefore, I would greatly appreciate your timely evaluation.</p>

            <p>I have attached my CV for your review and I am available for a quick call at your convenience to discuss how I can contribute to {sirket}.</p>

            <p>Thank you for your time and consideration.</p>

            <p>Sincerely,</p>

            <p><b>Nazlıcan Ezeroğlu</b><br>
            Software Engineering Student | Huawei Student Developers Campus Ambassador<br>
            <a href="{LINKEDIN_URL}" style="text-decoration: none; color: #0077b5;">LinkedIn Profile</a> | <a href="{GITHUB_URL}" style="text-decoration: none; color: #333;">GitHub Profile</a></p>
          </body>
        </html>
        """

        msg = MIMEMultipart()
        msg['From'] = GONDEREN_MAIL
        msg['To'] = alici_mail
        msg['Subject'] = konu_basligi
        msg.attach(MIMEText(icerik_html, 'html'))

        # CV Ekle
        try:
            with open(CV_DOSYASI, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename= {CV_DOSYASI}")
            msg.attach(part)
        except Exception as e:
            print(f"⚠️ HATA: CV dosyası eklenemedi! ({e})")
            server.quit()
            continue

        # Gönder
        try:
            server.send_message(msg)
            gonderilen_sayisi += 1
            print(f"✅ [{gonderilen_sayisi}] {sirket} ({alici_mail}) adresine GÖNDERİLDİ.")
        except Exception as e:
            print(f"❌ GÖNDERİLEMEDİ: {sirket}. Hata: {e}")
        
        # --- BAĞLANTIYI KAPAT (HATA ALMAMAK İÇİN) ---
        finally:
            try:
                server.quit()
            except:
                pass

        # Spam Koruması (2-4 dakika bekle)
        bekleme = random.randint(120, 240) 
        print(f"⏳ Spam koruması: {bekleme} saniye bekleniyor...")
        time.sleep(bekleme)

    print("\n🎉 TEBRİKLER! Tüm liste tamamlandı.")

if __name__ == "__main__":
    mail_gonder()