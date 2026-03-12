from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import undetected_chromedriver as uc # Yeni kütüphanemiz eklendi
from seleniumbase import Driver
from seleniumbase import SB
import google.generativeai as genai
import requests
import sys


class arz:
    def __init__(self , li_elemani):
        try:
            self.isim_elemani = li_elemani.find_element(By.CSS_SELECTOR, ".il-halka-arz-sirket")
            self.newarz = self.isim_elemani.text
        except:
            print("Bir sorun oluştu")

        try:
            self.tik = li_elemani.find_element(By.CSS_SELECTOR , ".fa-solid.fa-check.snc-badge")
            self.tik = "Bulundu"
        except:
            self.tik = "Bulunamadı."

        try:
            self.yeni = li_elemani.find_element(By.CLASS_NAME , "il-new")
            self.yeni = "Bulundu"
        except:
            self.yeni = "Bulunamadı."

print('Hosgeldiniz, tarayıcı başlatılıyor (Bot koruması atlatılıyor)...')
driver = Driver(uc=True)

driver.get("https://halkarz.com/")


genai.configure(api_key="BURAYA_API_ANAHTARINIZI_YAZIN")
model = genai.GenerativeModel('gemini-2.5-flash')

wait = WebDriverWait(driver, 30)

yeniarz = []
yeniarz = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.index-list")))
onayli_arz = []
try:
    for eleman in yeniarz:
        ilan = arz(eleman)

        if ilan.tik == "Bulundu":
            ilan.tik = "✅"
            onayli_arz.append(ilan)
        
        elif ilan.yeni == "Bulundu":
            onayli_arz.append(ilan)
        print(f"Şirket: {ilan.newarz} | Durum: {ilan.tik} | {ilan.yeni}")
except Exception as e:
    print(f"Bir sorun oluştu: {e}")

sayac = 1

for listearz in onayli_arz:
    print(f"{sayac}-{listearz.newarz}")
    sayac += 1

if sayac == 1:
    print("Aktif olarak halka arz olan bir şirket bulunamadı...")
    sys.exit(0)
    
secim = input("Lütfen halka arz seçiniz...")

try:
    secilen_numara =int(secim)
    index = secilen_numara - 1
    secilen_sirket = onayli_arz[index]
    print(f"Yapay zekaya {onayli_arz[index].newarz} şirketi soruluyor.Gelen yanıt telegramınıza gönderilecektir... ")
except:
    print("Hatalı bir giriş yaptınız...")
    sys.exit(0)



secilen_sirket.isim_elemani.click()

tablo_govdesi = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR , '.sp-table tbody'))).text


BOT_TOKEN = "BURAYA_TELEGRAM_BOT_TOKEN_YAZIN"
CHAT_ID = "BURAYA_CHAT_ID_YAZIN"

try:

    soru = f"Şu halka arz bilgilerini incele: {secilen_sirket.newarz}.Sen tarafsız bir finansal veri özetleyicisisin. Amacın yatırım tavsiyesi vermek değil, karmaşık finansal metinleri sadeleştirmektir. Sana verilen şirketin halka arz izahname verilerini ve fon kullanım yerlerini incele. \n\nŞirketin halka arzdan elde edeceği geliri ağırlıklı olarak nerelere (geçmiş borç ödemesi, Ar-Ge, kapasite artırımı, işletme sermayesi vb.) harcayacağını sadece matematiksel gerçeklerle ve tarafsız bir dille 3-4 maddede özetle. Şirketin iyi veya kötü olduğu, mantıklı olup olmadığı veya gelecekte kazandırıp kazandırmayacağı hakkında KESİNLİKLE yorum yapma.Şirketin halka arz bilgileri şunlar {tablo_govdesi}"
    cevap = model.generate_content(soru)
    gonderilecek_mesaj = f"🚨 YENİ HALKA ARZ BİLDİRİMİ!\n\n🤖 Emlak/Borsa Botu Analizi:\n{cevap.text}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    parametreler = {"chat_id": CHAT_ID, "text": gonderilecek_mesaj}

    requests.post(url, data=parametreler)
except Exception as e:
    print(f"Bir sorun oluştu {e}")

finally:
    driver.quit()











