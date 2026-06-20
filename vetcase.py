import os
import ssl
import random
import flet as ft

ssl._create_default_https_context = ssl._create_unverified_context

# 🛠️ TÜRKÇE KARAKTER VE ARAMA KÜTÜPHANESİ SENKRONİZASYONU
def normalize_tr(text):
    if not text:
        return ""
    text = text.replace("İ", "i").replace("I", "ı").replace("Ş", "ş").replace("Ğ", "ğ").replace("Ü", "ü").replace("Ö", "ö").replace("Ç", "ç")
    return text.lower().strip()

def main(page: ft.Page):
    page.title = "VetCase - Profesyonel Hekim Simülasyonu"
    page.theme_mode = "dark" 
    page.bgcolor = "#0f172a" 
    page.window.width = 480             
    page.window.height = 850
    page.window.resizable = False       
    # Kutu içi scroll yerine tüm sayfanın kaydırılmasını sağlıyoruz (Çökmeyi engeller)
    page.scroll = "adaptive"

    # ================= TAM 30 VAKALIK ULTRA DETAYLI MEGA HAVUZ =================
    vaka_havuzu = [
        {"isim": "Çakıl", "tur": "Köpek", "irk": "Golden", "yas": 4, "kilo": "32.0 kg", "ates": "39.4 °C", "triyaj": "🟡 SARI ALAN", 
         "semptomlar": "İnatçı safra kusması, tam iştahsızlık, Poliüri/Polidipsi, karın muayenesinde ağrı.", 
         "ozgecmis": "Hasta 5 yıldır kliniğimize kayıtlı. Daha önce böbrek taşı şüphesiyle tedavi gördü.", 
         "ilaclar": "ACE İnhibitörü", 
         "hikaye": "Sahibi: 'Hekim bey sabahtan beri resmen perişan olduk. Çakıl sabah erkenden kalktı, önce köpüklü sonra tamamen sarı safra şeklinde 4 defa kustu. Su kabını doldurmaktan bıktım, dakikalarca su içiyor ve hemen ardından çişe çıkıyor ama mamasını koklayıp arkasını dönüyor. Hiç hâli yok, sürekli kuytu köşelerde uyumak istiyor, ne olur yardım edin.'", 
         "vital": "Dehidrasyon: %10 | Nabız: 120 bpm | CRT: 2.5 sn | Solunum: 28/dk", 
         "raporlar": {"hemogram (tam kan sayımı)": "RBC: 4.2 M/μL (Düşük), HCT: %28", "biyokimya (geniş panel)": "BUN: 145 mg/dL, Kreatinin: 6.5 mg/dL", "usg (ultrasonografi)": "Her iki böbrekte belirgin kortikomedüller sınır kaybı."}, 
         "dogru_mudahaleler": ["damar yolu açmak (iv kateter)", "biyokimya (geniş panel)", "hemogram (tam kan sayımı)"], 
         "dogru_serumlar": ["ringer laktat (iv sıvı)", "izotonik %0.9 nacl (iv sıvı)", "maropitant (cerenia - antiemetik)"], 
         "olumcul_ilaclar": ["meloksikam (maxicam - nsaii)", "furosemid (lasix - diüretik)", "karprofen (rimadyl - nsaii)"], 
         "gercek_teshis": "Kronik Böbrek Yetmezliği (KBY)"},

        {"isim": "Susam", "tur": "Kedi", "irk": "Tekir", "yas": 1, "kilo": "2.8 kg", "ates": "40.5 °C", "triyaj": "🔴 KIRMIZI ALAN (KRİTİK)", 
         "semptomlar": "Fışkırır tarzda kusma, kanlı ve aşırı kötü kokulu ishal, letarji.", 
         "ozgecmis": "Sokaktan bir hafta önce sahiplenilmiş. Viral aşıları henüz hiç yapılmamış.", 
         "ilaclar": "Yok", 
         "hikaye": "Sahibi: 'Dün akşama kadar hiçbir şeyi yoktu, birden bire kusmaya başladı. Su içiyor, içtiği an fışkırır gibi geri çıkarıyor. Gece tuvalet kabına baktığımda resmen şok oldum; tamamen su gibi, kıpkırmızı kanlı ve hayatımda duymadığım kadar kötü kokan bir ishal yapmıştı. Şu an kafasını bile kaldıramıyor.'", 
         "vital": "Dehidrasyon: %12 (Şiddetli) | Nabız: 160 bpm | CRT: 3 sn", 
         "raporlar": {"hemogram (tam kan sayımı)": "WBC: 1.1 K/μL (Kritik Lökopeni)", "parvovirüs (cpv) hızlı test": "SONUÇ: POZİTİF (++)"}, 
         "dogru_mudahaleler": ["damar yolu açmak (iv kateter)", "parvovirüs (cpv) hızlı test", "hemogram (tam kan sayımı)"], 
         "dogru_serumlar": ["ringer laktat (iv sıvı)", "izotonik %0.9 nacl (iv sıvı)", "amoksisilin + klavulanik asit", "c vitamini"], 
         "olumcul_ilaclar": ["deksametazon (kortikosteroid)"], 
         "gercek_teshis": "Kedi Panlökopenisi (FPV)"},

        {"isim": "Müsibak", "tur": "Köpek", "irk": "Kangal Melezi", "yas": 6, "kilo": "54.0 kg", "ates": "37.9 °C", "triyaj": "🔴 KIRMIZI ALAN (KRİTİK)", 
         "semptomlar": "Karın bölgesinde ani genişleme, aralıksız öğürme (kusamama), beyaz köpüklü salya.", 
         "ozgecmis": "Günde tek öğün ve akşamları bol mama yiyor.", 
         "ilaclar": "Yok", 
         "hikaye": "Sahibi: 'Hekim bey acil yetiştik! Akşam mamasını iştahla yedi, arkasından bahçedeki köpekle oynamaya, sağa sola koşturmaya başladı. Yarım saat geçmeden hayvan birden acı acı inlemeye başladı. Karnına bir baktım davul gibi şişmiş. Öğürüyor ama ağzından sadece köpük çıkıyor.'", 
         "vital": "Nabız: 175 bpm (Taşikardi) | Solunum: 55/dk | CRT: 4 sn", 
         "raporlar": {"röntgen (radyografi)": "Midenin gazla aşırı büyüklükte şiştiği, Ters C görüntüsü izlendi."}, 
         "dogru_mudahaleler": ["damar yolu açmak (iv kateter)", "röntgen (radyografi)", "cerrahi operasyon (acil laparotomi)"], 
         "dogru_serumlar": ["şok dozu sıvı", "ringer laktat (iv sıvı)"], 
         "olumcul_ilaclar": ["metoklopramid (mide motilitesi)"], 
         "gercek_teshis": "Mide Dönmesi (GDV)"},

        {"isim": "Gece", "tur": "Kedi", "irk": "British Shorthair", "yas": 3, "kilo": "5.6 kg", "ates": "38.3 °C", "triyaj": "🟡 SARI ALAN", 
         "semptomlar": "Kum kabına sık gitme, ıkınma, ağlama, damla damla kanlı idrar.", 
         "ozgecmis": "Kısır erkek kedi. Suyu az içiyor, sadece kuru mama tüketiyor.", 
         "ilaclar": "Yok", 
         "hikaye": "Sahibi: 'Dünden beri kum kabından çıkmıyor. İçeri giriyor, dakikalarca kasılarak ıkınıyor ve ağlar gibi acı sesler çıkarıyor. Kabına baktığımda hiç idrar yoktu, sadece bugün halının üzerine bir iki damla tamamen kanlı idrar bıraktı. Karnına dokunmaya çalıştığımda tıslıyor.'", 
         "vital": "Palpasyon: Mesane portakal büyüklüğünde, taş gibi sert.", 
         "raporlar": {"usg (ultrasonografi)": "Mesanede yoğun kristalizasyon, uretra girişinde tam tıkanıklık.", "biyokimya (geniş panel)": "Kreatinin: 5.2 mg/dL, Potasyum: 6.9 mEq/L (Hiperkalemi)"}, 
         "dogru_mudahaleler": ["üriner kateterizasyon (sonda)", "usg (ultrasonografi)", "biyokimya (geniş panel)"], 
         "dogru_serumlar": ["izotonik %0.9 nacl (iv sıvı)", "spazmolitik"], 
         "olumcul_ilaclar": ["furosemid (lasix - diüretik)"], 
         "gercek_teshis": "FLUTD (Feline Lower Urinary Tract Disease)"},

        {"isim": "Şila", "tur": "Köpek", "irk": "Terrier", "yas": 8, "kilo": "7.2 kg", "ates": "40.1 °C", "triyaj": "🟡 SARI ALAN", 
         "semptomlar": "Kötü kokulu vajinal akıntı, aşırı su tüketimi, letarji.", 
         "ozgecmis": "Kısırlaştırılmamış dişi. 1.5 ay önce kızgınlık kanaması geçirdi.", 
         "ilaclar": "Yok", 
         "hikaye": "Sahibi: 'Kızım son bir haftadır su kabının başından ayrılmıyor, litrelerce su içiyor ve sürekli dışarı çıkmak istiyor. Bugün kuyruğunun altında, cinsel organından gelen koyu sarı, iltihap gibi ve çok pis kokan bir akıntı gördüm.'", 
         "vital": "Nabız: 135 bpm | Karın palpasyonunda uterus kornuları dolgun.", 
         "raporlar": {"usg (ultrasonografi)": "Uterus lümeninde aşırı miktarda irin birikimi.", "hemogram (tam kan sayımı)": "WBC: 38.0 K/μL (Şiddetli Lökositoz)"}, 
         "dogru_mudahaleler": ["usg (ultrasonografi)", "ovariohisterektomi (pyometra/kısırlaştırma)"], 
         "dogru_serumlar": ["ringer laktat (iv sıvı)", "amoksisilin + klavulanik asit"], 
         "olumcul_ilaclar": [], 
         "gercek_teshis": "Pyometra (Açık/Kapalı)"},

        {"isim": "Tarçın", "tur": "Köpek", "irk": "Dachshund", "yas": 5, "kilo": "8.5 kg", "ates": "38.6 °C", "triyaj": "🟡 SARI ALAN", 
         "semptomlar": "Arka bacaklarda ani başlayan felç, sırt ağrısı.", 
         "ozgecmis": "Kondrodistrofik ırk, gövdesi uzun. Sürekli yüksek yerlerden atlıyor.", 
         "ilaclar": "Yok", 
         "hikaye": "Sahibi: 'Tarçın her zamanki gibi kanepeden halıya doğru zıpladı. Atlar atlamaz tiz bir sesle çığlık attı ve yere yığıldı. Şu an arka iki bacağını hiç kıpırdatamıyor, arkasını sürükleyerek yürümeye çalışıyor.'", 
         "vital": "Nörolojik bulgu: Arka ekstremitelerde derin ağrı duyusu azalmış.", 
         "raporlar": {"nörolojik muayene": "Propriosepsiyon kaybı. L1-L3 bölgesi şüphesi.", "röntgen (radyografi)": "T13-L2 intervertebral disk aralığında daralma."}, 
         "dogru_mudahaleler": ["nörolojik muayene", "röntgen (radyografi)"], 
         "dogru_serumlar": ["meloksikam (maxicam - nsaii)", "deksametazon (kortikosteroid)"], 
         "olumcul_ilaclar": ["furosemid (lasix - diüretik)"], 
         "gercek_teshis": "Disk Hernisi (IVDD)"},

        {"isim": "Rüzgar", "tur": "Köpek", "irk": "Sokak Köpeği", "yas": 2, "kilo": "19.0 kg", "ates": "36.8 °C", "triyaj": "🔴 KIRMIZI ALAN (KRİTİK)", 
         "semptomlar": "Açık femur kırığı, solgun mukozalar, şok tablosu.", 
         "ozgecmis": "Sokakta bulundu, aşısız.", 
         "ilaclar": "Yok", 
         "hikaye": "Bulan Kişi: 'Yolun kenarında kanlar içinde yatarken gördük. Süratli geçen bir araba çarpmış galiba. Arka bacağının kemiği dışarı fırlamıştı ve fışkırır gibi kanıyordu. Hemen bezle bağladık ama kendinden geçmiş durumda.'", 
         "vital": "CRT: 4.5 sn | Nabız: 185 bpm | Şiddetli Hipotermi.", 
         "raporlar": {"röntgen (radyografi)": "Sağ femur diafizinde parçalı açık kırık.", "hemogram (tam kan sayımı)": "HCT: %19, Hb: 5.5 g/dL (Akut kan kaybı)."}, 
         "dogru_mudahaleler": ["damar yolu açmak (iv kateter)", "yara debridmanı ve bandaj", "röntgen (radyografi)", "kan transfüzyonu"], 
         "dogru_serumlar": ["şok dozu sıvı", "ringer laktat (iv sıvı)", "c vitamini"], 
         "olumcul_ilaclar": ["deksametazon (kortikosteroid)"], 
         "gercek_teshis": "Künt Travma / Hipovolemik Şok"},

        {"isim": "Pamuk", "tur": "Kedi", "irk": "Van Kedisi", "yas": 2, "kilo": "3.9 kg", "ates": "37.4 °C", "triyaj": "🔴 KIRMIZI ALAN (KRİTİK)", 
         "semptomlar": "Çamur rengi mukozalar, yüz/patilerde akut ödem, nefes darlığı.", 
         "ozgecmis": "Ev ortamında yaşıyor, evdeki hapları yemiş.", 
         "ilaclar": "Minoset/Parol (Parasetamol)", 
         "hikaye": "Sahibi: 'Hekim bey çok pişmanım. Sabah ateşi var diye insan ağrı kesicisi olan Parol'dan çeyrek kırıp yutturdum. 2 saat sonra yüzü gözleme gibi şişti. Dili ve diş etleri simsiyah, çamur gibi oldu!'", 
         "vital": "Solunum: 65/dk | Mukozalar: Siyanotik kahverengi", 
         "raporlar": {"hemogram (tam kan sayımı)": "Heinz body anemisi saptandı.", "kan gazı analizi": "Methemoglobin düzeyi çok yüksek."}, 
         "dogru_mudahaleler": ["oksijen desteği (maske/kabin)", "damar yolu açmak (iv kateter)"], 
         "dogru_serumlar": ["n-asetilsistein (nac)", "izotonik %0.9 nacl (iv sıvı)", "c vitamini"], 
         "olumcul_ilaclar": ["meloksikam (maxicam - nsaii)"], 
         "gercek_teshis": "Parasetamol Zehirlenmesi (Toksikasyonu)"},

        {"isim": "Limon", "tur": "Köpek", "irk": "Cocker", "yas": 1, "kilo": "11.5 kg", "ates": "36.5 °C", "triyaj": "🔴 KIRMIZI ALAN (KRİTİK)", 
         "semptomlar": "Şiddetli bradikardi, kanlı ishal, bayılma.", 
         "ozgecmis": "Stres anında ishal olma öyküsü.", 
         "ilaclar": "Yok", 
         "hikaye": "Sahibi: 'Köpeğimiz yürüyüşte birden bire arka bacakları titreyerek taş gibi yere yığıldı. Ağzından ve arkasından koyu renkli sıvılar geldi. Kalbi duracak kadar yavaş atıyor.'", 
         "vital": "Nabız: 42 bpm (Şiddetli Bradikardi)", 
         "raporlar": {"biyokimya (geniş panel)": "Sodyum: Düşük, Potasyum: Çok Yüksek.", "ekg (elektrokardiyografi)": "P dalgası kaybolmuş, T dalgaları uzun ve sivri."}, 
         "dogru_mudahaleler": ["biyokimya (geniş panel)", "ekg (elektrokardiyografi)", "damar yolu açmak (iv kateter)"], 
         "dogru_serumlar": ["izotonik %0.9 nacl (iv sıvı)", "deksametazon (kortikosteroid)"], 
         "olumcul_ilaclar": ["ringer laktat (iv sıvı)"], 
         "gercek_teshis": "Addison Krizi (Hipoadrenokortisizm)"},

        {"isim": "Tarzan", "tur": "Kedi", "irk": "Tekir", "yas": 4, "kilo": "4.2 kg", "ates": "37.1 °C", "triyaj": "🔴 KIRMIZI ALAN (KRİTİK)", 
         "semptomlar": "Karnıyla nefes alma, göğüste kalp sesinin duyulamaması.", 
         "ozgecmis": "Pencereden kuş izlemeyi çok sever.", 
         "ilaclar": "Yok", 
         "hikaye": "Sahibi: 'Apartman boşluğunda buldum, sanırım 4. kattaki penceremizden düşmüş. Göğsü hiç oynamıyor, sadece karnını şişirip indirerek nefes almaya çalışıyor, dili mosmor.'", 
         "vital": "Solunum: 68/dk (Zorlu) | Oskültasyon: Göğüs boşluğunda bağırsak sesleri duyuluyor.", 
         "raporlar": {"röntgen (radyografi)": "Diyafram bütünlüğü kaybolmuş, mide ve bağırsaklar göğüs boşluğuna geçmiş."}, 
         "dogru_mudahaleler": ["röntgen (radyografi)", "oksijen desteği (maske/kabin)", "cerrahi operasyon (acil laparotomi)"], 
         "dogru_serumlar": ["şok dozu sıvı", "izotonik %0.9 nacl (iv sıvı)"], 
         "olumcul_ilaclar": [], 
         "gercek_teshis": "Yüksekten Düşme / Diyafram Fıtığı"},

        {"isim": "Toros", "tur": "Köpek", "irk": "St. Bernard", "yas": 6, "kilo": "68.0 kg", "ates": "35.8 °C", "triyaj": "🔴 KIRMIZI ALAN (KRİTİK)", 
         "semptomlar": "Koma benzeri uyku hali, şiddetli hipotermi, ödemli yüz yapısı.", 
         "ozgecmis": "Son 1 yıldır aşırı kilo alımı ve sürekli üşüme.", 
         "ilaclar": "Yok", 
         "hikaye": "Sahibi: 'Aylardır çok uyuşuktu ama bugün uyandıramadık. Vücudu resmen buz gibi, donmuş gibi yatıyor. Yüzü gözü şişmiş, torba gibi olmuş.'", 
         "vital": "Nabız: 48 bpm | Solunum: 8/dk", 
         "raporlar": {"hormon paneli (t4, tsh)": "Total T4: Belirlenemeyecek kadar düşük, TSH: Çok Yüksek."}, 
         "dogru_mudahaleler": ["damar yolu açmak (iv kateter)", "hormon paneli (t4, tsh)", "oksijen desteği (maske/kabin)"], 
         "dogru_serumlar": ["izotonik %0.9 nacl (iv sıvı)", "deksametazon (kortikosteroid)", "b kompleks vitamini"], 
         "olumcul_ilaclar": [], 
         "gercek_teshis": "Hipotiroidizm / Miksödem Krizi"},

        {"isim": "Şeker", "tur": "Kedi", "irk": "Ankara Kedisi", "yas": 12, "kilo": "2.1 kg", "ates": "39.8 °C", "triyaj": "🟡 SARI ALAN", 
         "semptomlar": "Aşırı yemek yemesine rağmen şiddetli kilo kaybı, taşikardi, hiperaktivite.", 
         "ozgecmis": "Geriatrik yaşta, son aylarda aşırı sinirli.", 
         "ilaclar": "Yok", 
         "hikaye": "Sahibi: 'Kedim her gün çifter porsiyon mama yiyor ama resmen bir deri bir kemik kaldı. Evin içinde deli gibi koşturuyor, kalbine dokunduğumda göğsü yerinden fırlayacakmış gibi hızlı atıyor.'", 
         "vital": "Nabız: 240 bpm (Taşikardi) | Tiroid bezi palpasyonda büyümüş.", 
         "raporlar": {"hormon paneli (t4, tsh)": "Total T4: 15 μg/dL (Referansın 4 katı yüksek)."}, 
         "dogru_mudahaleler": ["hormon paneli (t4, tsh)", "biyokimya (geniş panel)"], 
         "dogru_serumlar": ["izotonik %0.9 nacl (iv sıvı)"], 
         "olumcul_ilaclar": ["adrenalin / epinefrin (acil / şok)"], 
         "gercek_teshis": "Hipertiroidizm"},

        {"isim": "Çapkın", "tur": "Köpek", "irk": "Pomeranian", "yas": 8, "kilo": "3.2 kg", "ates": "40.3 °C", "triyaj": "🔴 KIRMIZI ALAN (KRİTİK)", 
         "semptomlar": "Karında sarkık şişlik (Pendulöz abdomen), deride simetrik tüy dökülmesi.", 
         "ozgecmis": "Yıllardır aşırı su içme ve kortizon kullanım geçmişi.", 
         "ilaclar": "Kortizonlu Deri Pomadı", 
         "hikaye": "Sahibi: 'Köpeğimin karnı aylardır davul gibi sarkıktı. Bugün derisindeki yaralardan irin akmaya başladı ve birden ateşi çıktı, tir tir titreyerek yığıldı.'", 
         "vital": "Ateş: 40.3 °C | Nabız: 165 bpm", 
         "raporlar": {"biyokimya (geniş panel)": "ALK: Çok yüksek.", "kortizol testi (acth stimülasyonu)": "Bazal Kortizol çok yüksek."}, 
         "dogru_mudahaleler": ["biyokimya (geniş panel)", "kortizol testi (acth stimülasyonu)", "damar yolu açmak (iv kateter)"], 
         "dogru_serumlar": ["izotonik %0.9 nacl (iv sıvı)", "amoksisilin + klavulanik asit"], 
         "olumcul_ilaclar": ["deksametazon (kortikosteroid)"], 
         "gercek_teshis": "Hiperadrenokortisizm (Cushing Sendromu)"},

        {"isim": "Lokum", "tur": "Köpek", "irk": "Cocker", "yas": 5, "kilo": "13.0 kg", "ates": "39.9 °C", "triyaj": "🟡 SARI ALAN", 
         "semptomlar": "Şiddetli kusma, 'Dua Pozisyonu' (ön ayaklar yerde, kalça havada).", 
         "ozgecmis": "Bayramda yağlı et artıklarıyla beslendi.", 
         "ilaclar": "Yok", 
         "hikaye": "Sahibi: 'Hayvana sürekli kavurma verdiler. Dün geceden beri durmadan kusuyor, karnına dokundurmuyor. Resmen ön patilerini yere uzatıp kalçasını havaya dikerek acı çekiyor.'", 
         "vital": "Kranial abdomende şiddetli ağrı.", 
         "raporlar": {"biyokimya (geniş panel)": "Amilaz ve Lipaz değerleri yüksek.", "usg (ultrasonografi)": "Pankreas etrafında ödem."}, 
         "dogru_mudahaleler": ["usg (ultrasonografi)", "biyokimya (geniş panel)"], 
         "dogru_serumlar": ["ringer laktat (iv sıvı)", "maropitant (cerenia - antiemetik)"], 
         "olumcul_ilaclar": ["metoklopramid (mide motilitesi)"], 
         "gercek_teshis": "Akut Pankreatit"},

        {"isim": "Reçel", "tur": "Kedi", "irk": "Tekir", "yas": 2, "kilo": "3.5 kg", "ates": "37.2 °C", "triyaj": "🔴 KIRMIZI ALAN (KRİTİK)", 
         "semptomlar": "Akut anüri (idrarın kesilmesi), ataksi, nörolojik nöbetler.", 
         "ozgecmis": "Oto sanayide yaşayan meraklı kedi.", 
         "ilaclar": "Yok", 
         "hikaye": "Sahibi: 'Dün arabanın altına sızan yeşil antifriz sıvısını yalarken görmüşler. Bugün sarhoş gibi sallanıyor, ağzından köpükler akıyor ve hiç idrar yapmadı.'", 
         "vital": "Böbrekler palpasyonda aşırı büyümüş.", 
         "raporlar": {"biyokimya (geniş panel)": "BUN ve Kreatinin çok yüksek. Akut Böbrek Hasarı.", "idrar tahlili (tam idrar tetkiki)": "Kalsiyum oksalat kristalleri."}, 
         "dogru_mudahaleler": ["üriner kateterizasyon (sonda)", "idrar tahlili (tam idrar tetkiki)", "biyokimya (geniş panel)"], 
         "dogru_serumlar": ["izotonik %0.9 nacl (iv sıvı)", "furosemid (lasix - diüretik)", "c vitamini"], 
         "olumcul_ilaclar": ["meloksikam (maxicam - nsaii)"], 
         "gercek_teshis": "Antifriz (Etilen Glikol) Zehirlenmesi"}
    ]

    # Dinamik Olarak Vakaları Çoğaltıp 30'a tamamlama
    # NOT: Kilo atamasını artık rastgele yapmak yerine hayvanın orijinal kilosuna yakın (+/- %20) ayarlıyoruz ki "27 kiloluk kedi" olmasın!
    while len(vaka_havuzu) < 30:
        klon = random.choice(vaka_havuzu[:15]).copy()
        klon["isim"] = klon["isim"] + f" (Kayıt {len(vaka_havuzu)+1})"
        klon["yas"] = random.randint(1, 10)
        
        # Orijinal kiloyu al ve gerçekçi bir sapma yarat (+/- %20)
        orijinal_kilo_str = klon["kilo"].replace(" kg", "")
        orijinal_kilo = float(orijinal_kilo_str)
        yeni_kilo = round(orijinal_kilo * random.uniform(0.8, 1.2), 1)
        klon["kilo"] = f"{yeni_kilo} kg"
        
        vaka_havuzu.append(klon)

    # ================= GENİŞLETİLMİŞ TETKİK VE İLAÇ HAVUZLARI =================
    tetkik_havuzu = [
        "Damar Yolu Açmak (IV Kateter)", "Üriner Kateterizasyon (Sonda)", "Oksijen Desteği (Maske/Kabin)", 
        "Entübasyon (Endotrakeal Tüp)", "CPR (Kalp Masajı + Solunum)", "Kan Transfüzyonu", 
        "Mide Yıkama (Lavaj)", "Mide Sondası Uygulaması", "Yara Debridmanı ve Bandaj", 
        "Abdominosentez", "Sistosentez (İdrar Alımı)", "Cerrahi Operasyon (Acil Laparotomi)", 
        "Ovariohisterektomi (Pyometra/Kısırlaştırma)", "Hemogram (Tam Kan Sayımı)", 
        "Biyokimya (Geniş Panel)", "Kan Gazı Analizi", "Koagülasyon Paneli (PT/aPTT)", 
        "Röntgen (Radyografi)", "USG (Ultrasonografi)", "Ekokardiyografi (EKO)", 
        "Mikroskobik İnceleme (Kan Frotisi)", "Dışkı Muayenesi (Fekal Yüzdürme)", 
        "İdrar Tahlili (Tam İdrar Tetkiki)", "Parvovirüs (CPV) Hızlı Test", 
        "FCoV (FIP) Hızlı Test", "FIV / FeLV Hızlı Test", "Canine Distemper (Gençlik Hastalığı) Testi", 
        "Nörolojik Muayene", "EKG (Elektrokardiyografi)", "Glukometre ile Kan Şekeri Ölçümü",
        "Hormon Paneli (T4, TSH)", "Kortizol Testi (ACTH Stimülasyonu)", "Progesteron Testi"
    ]

    ilac_havuzu = [
        "Ringer Laktat (IV Sıvı)", "İzotonik %0.9 NaCl (IV Sıvı)", "Dekstroz %5 (IV Sıvı)", "Şok Dozu Sıvı",
        "Hipertonik Salin (%7.2 NaCl)", "Taze Donmuş Plazma (TDP)",
        "Aktif Kömür (Oral Toksikoloji)", "Kristalize İnsülin (IV)", "İmidokarb (Babesiozis Spesifik)",
        "Maropitant (Cerenia - Antiemetik)", "Ondansetron (Zofran - Antiemetik)", "Metoklopramid (Mide Motilitesi)",
        "Omeprazol (Mide Koruyucu)", "Famotidin (Mide Koruyucu)", "Sukralfat", "Laktuloz",
        "Amoksisilin + Klavulanik Asit", "Enrofloksasin (Baytril)", "Metronidazol (Flagyl)", "Klindamisin", "Sefazolin", "Gentamisin", "Doksisiklin",
        "Meloksikam (Maxicam - NSAİİ)", "Karprofen (Rimadyl - NSAİİ)", "Deksametazon (Kortikosteroid)",
        "Prednizolon (Kortikosteroid)", "Tramadol (Opioid Analjezik)", "Buprenorfin (Güçlü Ağrı Kesici)", "Gabapentin (Nöropatik Ağrı)",
        "Furosemid (Lasix - Diüretik)", "Spironolakton", "Mannitol (Osmotik Diüretik)",
        "Pimobendan (Vetmedin)", "Benazepril (ACE İnhibitörü)", "Amlodipin",
        "Diazepam (Sedatif/Antikonvülzan)", "Fenobarbital (Antiepileptik)", "Mirtazapin (İştah Açıcı)",
        "Adrenalin / Epinefrin (Acil / Şok)", "Atropin (Acil / Bradikardi)", "Lidokain (Anti-aritmik)",
        "K Vitamini (Zehirlenme Antidotu)", "Kalsiyum Glukonat", "B Kompleks Vitamini", "Aminofilin (Bronkodilatör)", "N-Asetilsistein (NAC)",
        "Spazmolitik", "C Vitamini", "Taurin", "L-Karnitin"
    ]

    teshis_havuzu = [
        "Kronik Böbrek Yetmezliği (KBY)", "Kedi Panlökopenisi (FPV)", "Mide Dönmesi (GDV)", 
        "FLUTD (Feline Lower Urinary Tract Disease)", "Pyometra (Açık/Kapalı)", "Disk Hernisi (IVDD)", 
        "Künt Travma / Hipovolemik Şok", "Feline İnfeksiyöz Peritonit (FIP)", "Yabancı Cisim Obstrüksiyonu", 
        "Kedi Astımı", "Çikolata Zehirlenmesi", "Hepatik Lipidoz", "Eklampsi (Hipokalsemi)", 
        "Hipertrofik Kardiyomiyopati (HCM) / Tromboemboli", "Fare Zehiri Toksikasyonu", 
        "FeLV / FIV Enfeksiyonu", "Babesiosis / Ehrlichiosis", "Canine Distemper (Gençlik Hastalığı)", 
        "Dilate Kardiyomiyopati (DCM)", "Diyabetik Ketoasidoz (DKA)", "Parasetamol Zehirlenmesi (Toksikasyonu)", 
        "Addison Krizi (Hipoadrenokortisizm)", "Yüksekten Düşme / Diyafram Fıtığı", 
        "Kuru Üzüm Zehirlenmesi (ABY)", "Tetanoz", "Akut Pankreatit", "Antifriz (Etilen Glikol) Zehirlenmesi",
        "Hipotiroidizm / Miksödem Krizi", "Hipertiroidizm", "Hiperadrenokortisizm (Cushing Sendromu)"
    ]

    # ================= KARIŞIK DESTE SİSTEMİ (Tekrarsız Seçim Motoru) =================
    state = {
        "aktif_vaka": None,
        "yapilan_islemler": [],
        "verilen_tedaviler": [],
        "secilen_teshis": None,
        "kurtarilan": 0,    
        "kaybedilen": 0,
        "karisik_havuz": vaka_havuzu.copy(),
        "vaka_sirasi": 0
    }

    # Uygulama açılışında desteyi karıştır
    random.shuffle(state["karisik_havuz"])

    def yeni_vaka_sec():
        # Deste bittiyse yeniden karıştır
        if state["vaka_sirasi"] >= len(state["karisik_havuz"]):
            random.shuffle(state["karisik_havuz"])
            state["vaka_sirasi"] = 0
            
        state["aktif_vaka"] = state["karisik_havuz"][state["vaka_sirasi"]]
        state["vaka_sirasi"] += 1

    if state["aktif_vaka"] is None:
        yeni_vaka_sec()

    # Tasarım Şablonu (Kutu)
    def ozel_kart_tasarimi(bilesenler):
        return ft.Container(
            content=ft.Column(bilesenler),
            bgcolor="#1e293b", 
            padding=20,
            border_radius=12
        )

    # 📱 SAYFA 1: GİRİŞ ACİL SERVİS
    def git_sayfa_1(e=None):
        if e is not None: 
            yeni_vaka_sec()
        state["yapilan_islemler"].clear()
        state["verilen_tedaviler"].clear()
        state["secilen_teshis"] = None
        page.controls.clear()
        
        triyaj = state["aktif_vaka"]["triyaj"]
        t_renk = "red" if "KIRMIZI" in triyaj else ("orange" if "SARI" in triyaj else "green")

        page.add(
            ft.Container(
                content=ft.Row([
                    ft.Text(f"⚕️ BAŞARI SKORU: {state['kurtarilan']} TABURCU | {state['kaybedilen']} KAYIP", color="white", weight="bold")
                ], alignment="center"),
                bgcolor="#1e293b", padding=12, border_radius=10
            ),
            ft.Text(""),
            ft.Text("🚨 ACİL SERVİS ÇAĞRISI", size=24, color="white", weight="bold"),
            ft.Text(f"Triyaj Kodu: {triyaj}", size=16, color=t_renk, weight="bold"),
            ft.Text(""),
            ozel_kart_tasarimi([
                ft.Text("Gelen Akut Semptomlar:", size=16, color="amber", weight="bold"),
                ft.Text(state["aktif_vaka"]["semptomlar"], size=16, color="white")
            ]),
            ft.Text(""),
            ft.ElevatedButton("HASTAYI KLİNİĞE AL 🩺", bgcolor="blue", color="white", width=380, height=50, on_click=git_sayfa_2)
        )
        page.update()

    # 📋 SAYFA 2: DETAYLI ANAMNEZ VE VİTAL BULGULAR
    def git_sayfa_2(e=None):
        page.controls.clear()
        v = state["aktif_vaka"]
        
        page.add(
            ft.ElevatedButton("⬅️ ACİL SERVİSE DÖN", bgcolor="grey", color="white", on_click=lambda _: git_sayfa_1(None)),
            ft.Text(""),
            ozel_kart_tasarimi([
                ft.Text(f"🐾 Hasta Protokolü: {v['isim']}", size=20, color="white", weight="bold"),
                ft.Text(f"Tür: {v['tur']} | Irk: {v['irk']}", size=14, color="grey"),
                ft.Text(f"Yaş: {v['yas']} | Ağırlık: {v['kilo']}", size=14, color="grey"),
                ft.Text(""),
                ft.Text("🧬 ANAMNEZ VE ÖZGEÇMİŞ:", size=14, color="#38bdf8", weight="bold"),
                ft.Text(v["ozgecmis"], color="white"),
                ft.Text("🗣️ HASTA SAHİBİNİN PANİK ANLATIMI:", size=14, color="#38bdf8", weight="bold"),
                ft.Text(v["hikaye"], color="white", italic=True),
                ft.Text("🌡️ REKTAL ATEŞ VE VİTAL BULGULAR:", size=14, color="red", weight="bold"),
                ft.Text(f"Ateş: {v['ates']} | {v['vital']}", size=15, color="#10b981", weight="bold"),
            ]),
            ft.Text(""),
            ft.ElevatedButton("LABORATUVAR & TETKİK PANELİ 🔍", bgcolor="blue", color="white", width=380, height=50, on_click=git_sayfa_3)
        )
        page.update()

    # 🔍 SAYFA 3: TETKİK PANELİ
    def git_sayfa_3(e=None):
        page.controls.clear()
        txt_arama = ft.TextField(label="🔍 Tetkik Ara veya Aşağıdan Manuel Seçin...", width=380)
        arama_sonuclari = ft.Column()
        raporlar_kutusu = ft.Column()
        
        for eski_islem in state["yapilan_islemler"]:
            norm_isim = normalize_tr(eski_islem)
            rapor_metni = state["aktif_vaka"]["raporlar"].get(norm_isim, "Bulgu normal sınırlar içerisindedir.")
            raporlar_kutusu.controls.append(ft.Text(f"📄 {eski_islem}: {rapor_metni}", color="cyan", weight="bold"))

        def listeye_ekle(secilen_oge):
            if secilen_oge not in state["yapilan_islemler"]:
                state["yapilan_islemler"].append(secilen_oge)
                norm_isim = normalize_tr(secilen_oge)
                rapor_metni = state["aktif_vaka"]["raporlar"].get(norm_isim, "Bulgu normal sınırlar içerisindedir.")
                raporlar_kutusu.controls.insert(0, ft.Text(f"📄 {secilen_oge}: {rapor_metni}", color="cyan", weight="bold"))
                txt_arama.value = ""
                arama_yenile(None)

        def arama_yenile(e):
            arama_sonuclari.controls.clear()
            aranan_kelime = normalize_tr(txt_arama.value)
            
            for oge in tetkik_havuzu:
                if not aranan_kelime or aranan_kelime in normalize_tr(oge):
                    arama_sonuclari.controls.append(
                        ft.ElevatedButton(oge, bgcolor="#0d47a1", color="white", width=380, on_click=lambda e, sec=oge: listeye_ekle(sec))
                    )
            page.update()

        txt_arama.on_change = arama_yenile
        arama_yenile(None)

        page.add(
            ft.ElevatedButton("⬅️ ANAMNEZE DÖN", bgcolor="grey", color="white", on_click=git_sayfa_2),
            ft.Text("🔬 Laboratuvar & Görüntüleme İstemi", size=20, color="white", weight="bold"),
            txt_arama,
            arama_sonuclari, 
            ft.Divider(color="grey"),
            ft.Text("📋 ÇIKAN LABORATUVAR SONUÇLARI", color="#94a3b8", weight="bold"),
            raporlar_kutusu,
            ft.Text(""),
            ft.ElevatedButton("REÇETE YAZMAYA GEÇ 💊", bgcolor="green", color="white", width=380, height=50, on_click=git_sayfa_4)
        )
        page.update()

    # 💊 SAYFA 4: TEDAVİ REÇETE PANELİ
    def git_sayfa_4(e=None):
        page.controls.clear()
        txt_arama = ft.TextField(label="💊 İlaç Ara veya Aşağıdan Manuel Seçin...", width=380)
        arama_sonuclari = ft.Column()
        
        secilenler_kutusu = ft.Column([ft.Text("Yazılan Reçete Protokolü:", color="white", weight="bold")])
        for ilac in state["verilen_tedaviler"]: 
            secilenler_kutusu.controls.append(ft.Text(f"✔️ {ilac}", color="green", weight="bold"))

        def listeye_ekle(secilen_oge):
            if secilen_oge not in state["verilen_tedaviler"]:
                state["verilen_tedaviler"].append(secilen_oge)
                secilenler_kutusu.controls.append(ft.Text(f"✔️ {secilen_oge}", color="green", weight="bold"))
                txt_arama.value = ""
                arama_yenile(None)

        def oge_sil(e):
            state["verilen_tedaviler"].clear()
            git_sayfa_4(None)

        def arama_yenile(e):
            arama_sonuclari.controls.clear()
            aranan_kelime = normalize_tr(txt_arama.value)
            
            for oge in ilac_havuzu:
                if not aranan_kelime or aranan_kelime in normalize_tr(oge):
                    arama_sonuclari.controls.append(
                        ft.ElevatedButton(oge, bgcolor="#1b5e20", color="white", width=380, on_click=lambda e, sec=oge: listeye_ekle(sec))
                    )
            page.update()

        txt_arama.on_change = arama_yenile
        arama_yenile(None)

        page.add(
            ft.ElevatedButton("⬅️ TETKİKLERE GERİ DÖN", bgcolor="grey", color="white", on_click=git_sayfa_3),
            ft.Text("💊 Akut Sıvı & Reçete Sağaltımı", size=20, color="white", weight="bold"),
            txt_arama,
            arama_sonuclari,
            ft.Divider(color="grey"),
            ozel_kart_tasarimi([secilenler_kutusu, ft.ElevatedButton("Reçeteyi Temizle 🗑️", bgcolor="red", color="white", on_click=oge_sil)]),
            ft.Text(""),
            ft.ElevatedButton("NİHAİ KLİNİK TEŞHİSİ KOY 🩺", bgcolor="orange", color="white", width=380, height=50, on_click=git_sayfa_5)
        )
        page.update()

    # 🩺 SAYFA 5: TEŞHİS KOYMA PANELİ
    def git_sayfa_5(e=None):
        page.controls.clear()
        txt_arama = ft.TextField(label="🔎 Hastalık / Teşhis Ara veya Seç...", width=380)
        arama_sonuclari = ft.Column()
        
        if state["secilen_teshis"]:
            lbl_secilen = ft.Text(f"✅ Koyulan Kesin Teşhis: {state['secilen_teshis']}", color="green", size=16, weight="bold")
        else:
            lbl_secilen = ft.Text("⚠️ Henüz Teşhis Koyulmadı", color="red", size=16, weight="bold")

        def listeye_ekle(secilen_oge):
            state["secilen_teshis"] = secilen_oge
            lbl_secilen.value = f"✅ Koyulan Kesin Teşhis: {secilen_oge}"
            lbl_secilen.color = "green"
            txt_arama.value = ""
            arama_yenile(None)

        def arama_yenile(e):
            arama_sonuclari.controls.clear()
            aranan_kelime = normalize_tr(txt_arama.value)
            
            for oge in teshis_havuzu:
                if not aranan_kelime or aranan_kelime in normalize_tr(oge):
                    arama_sonuclari.controls.append(
                        ft.ElevatedButton(oge, bgcolor="#581c87", color="white", width=380, on_click=lambda e, sec=oge: listeye_ekle(sec))
                    )
            page.update()

        txt_arama.on_change = arama_yenile
        arama_yenile(None)

        page.add(
            ft.ElevatedButton("⬅️ TEDAVİYE GERİ DÖN", bgcolor="grey", color="white", on_click=git_sayfa_4),
            ft.Text("🩺 Nihai Klinik Teşhis", size=20, color="white", weight="bold"),
            ft.Text("Klinik bulgulara dayanarak nihai kararı verin.", color="#94a3b8"),
            txt_arama,
            arama_sonuclari,
            ft.Divider(color="grey"),
            ozel_kart_tasarimi([lbl_secilen]),
            ft.Text(""),
            ft.ElevatedButton("VAKAYI KİLİTLE VE ANALİZİ GÖR 📊", bgcolor="blue", color="white", width=380, height=50, on_click=git_sayfa_6)
        )
        page.update()

    # 📊 SAYFA 6: AKADEMİK EPİKRİZ VE ÖĞRETİCİ ANALİZ PANELİ
    def git_sayfa_6(e=None):
        page.controls.clear()
        v = state["aktif_vaka"]
        islemler_str = " ".join(state["yapilan_islemler"]).lower()
        tedaviler_str = " ".join(state["verilen_tedaviler"]).lower()

        teshis_dogru = (state["secilen_teshis"] == v["gercek_teshis"])
        damar_yolu_var = any(x in islemler_str for x in v["dogru_mudahaleler"])
        serum_var = any(x in tedaviler_str for x in v["dogru_serumlar"])
        dogru_tedavi_var = damar_yolu_var and serum_var
        olumcul_hata_var = any(x in tedaviler_str for x in v["olumcul_ilaclar"])

        hasta_yasadi = False

        if olumcul_hata_var:
            durum_baslik = "❌ HASTA KONTRENDİKE İLAÇTAN KAYBEDİLDİ"
            durum_renk = "red"
            durum_detay = "Teşhis doğru veya yanlış olsa da reçeteye eklediğiniz ölümcül etken madde hastayı toksik şoka sokarak öldürdü."
        elif dogru_tedavi_var and teshis_dogru:
            hasta_yasadi = True
            durum_baslik = "🎉 TEBRİKLER! HASTA YAŞADI VE TABURCU OLDU"
            durum_renk = "green"
            durum_detay = "Kusursuz Tanı ve Sağaltım! Klinik vizit kurallarına tam uyum sağladınız."
        elif dogru_tedavi_var and not teshis_dogru:
            hasta_yasadi = True
            durum_baslik = "⚠️ HASTA YAŞADI (ŞANS ESERİ)"
            durum_renk = "orange"
            durum_detay = "Teşhisiniz yanlıştı fakat kurduğunuz sıvı ve destek protokolü hastayı hayatta tuttu."
        else:
            durum_baslik = "❌ HASTA EKSİK PROTOKOLDEN KAYBEDİLDİ"
            durum_renk = "red"
            durum_detay = "Teşhis doğru olsa dahi hastanın ihtiyacı olan acil sıvı veya tahlil müdahalesi yapılmadığı için patoloji engellenemedi."

        if hasta_yasadi:
            state["kurtarilan"] += 1
        else:
            state["kaybedilen"] += 1

        eksik_islemler = [x for x in v["dogru_mudahaleler"] if x not in islemler_str]
        eksik_ilaclar = [x for x in v["dogru_serumlar"] if x not in tedaviler_str]

        page.add(
            ft.Text(f"📌 GERÇEK PATOLOJİ: {v['gercek_teshis'].upper()}", size=18, color="#38bdf8", weight="bold"),
            ft.Divider(color="grey"),
            ft.Text(durum_baslik, size=16, color=durum_renk, weight="bold"),
            ft.Text(durum_detay, color="white"),
            ft.Text(""),
            ozel_kart_tasarimi([
                ft.Text("👨‍⚕️ Sizin Kayıtlarınız:", color="purple", weight="bold"),
                ft.Text(f"Koyduğunuz Teşhis: {state['secilen_teshis'] if state['secilen_teshis'] else 'Koyulmadı'}", color="grey"),
                ft.Text(f"İstediğiniz Tetkikler: {', '.join(state['yapilan_islemler']) if state['yapilan_islemler'] else 'Hiçbiri'}", color="grey"),
                ft.Text(f"Yazdığınız Reçete: {', '.join(state['verilen_tedaviler']) if state['verilen_tedaviler'] else 'Hiçbiri'}", color="grey"),
            ]),
            ft.Text(""),
            ozel_kart_tasarimi([
                ft.Text("📖 AKADEMİK REHBER VE REÇETE ANALİZİ", color="orange", weight="bold"),
                ft.Text(f"İstenmesi Gereken Doğru Tetkikler:\n{', '.join(v['dogru_mudahaleler']).title()}", color="green"),
                ft.Text(f"Sizin Yapmadığınız Eksikler:\n{', '.join(eksik_islemler).title() if eksik_islemler else 'Eksik Yok, Kusursuz! ✅'}", color="red"),
                ft.Text(""),
                ft.Text(f"Uygulanması Gereken Doğru Reçete:\n{', '.join(v['dogru_serumlar']).title()}", color="green"),
                ft.Text(f"Sizin Vermediğiniz Eksik İlaçlar:\n{', '.join(eksik_ilaclar).title() if eksik_ilaclar else 'Eksik Yok, Kusursuz! ✅'}", color="red"),
            ]),
            ft.Text(""),
            ft.ElevatedButton("YENİ ACİL VAKAYA GEÇ 🔄", bgcolor="white", color="black", width=380, height=50, on_click=git_sayfa_1)
        )
        page.update()

    git_sayfa_1(None)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port)