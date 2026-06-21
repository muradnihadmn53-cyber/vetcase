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

# Canonicalize common aliases (ör. ringer / izotonik gibi kısa yazımları eşleştir)
def canonicalize(text):
    n = normalize_tr(text)
    if not n:
        return ""
    # Ringer varyantlarını birleştir
    if "ringer" in n or "ringerlaktat" in n or "ringer laktat" in n:
        return normalize_tr("ringer laktat (iv sıvı)")
    # İzotonik varyantları
    if "izoton" in n:
        return normalize_tr("izotonik %0.9 nacl (iv sıvı)")
    return n

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
        "raporlar": {"biyokimya (geniş panel)": "Sodyum: Düşük, Potasyum: Çok Yüksek.", "ekg (elektrokardiyografi)": "P dalgası kaybolmuş, T dalgaları uzun ve sivri.", "Bazal Kortizol": "Düşük (Addison ile uyumlu)"}, 
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
         "raporlar": {"hormon paneli (t4, tsh)": "Total T4: Belirlenemeyecek kadar düşük, TSH: Çok Yüksek.", "Total T4 (Total Tiroksin)": "<5 nmol/L (Çok düşük)", "TSH (Tiroit Uyarıcı Hormon)": "Çok yüksek"}, 
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
         "raporlar": {"hormon paneli (t4, tsh)": "Total T4: 15 μg/dL (Referansın 4 katı yüksek).", "Total T4 (Total Tiroksin)": "15 μg/dL"}, 
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
         "raporlar": {"biyokimya (geniş panel)": "ALK: Çok yüksek.", "kortizol testi (acth stimülasyonu)": "Bazal Kortizol çok yüksek.", "Bazal Kortizol": "Yüksek (Cushing ile uyumlu)"}, 
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
        # kapsamlı tetkik listesi (teşhis amaçlı)
        "Hemogram (Tam Kan Sayımı)", "Biyokimya (Geniş Panel)", "Elektrolit Paneli (Na, K, Cl)",
        "İdrar Tahlili (Tam İdrar Tetkiki)", "Üriner Kültür ve Antibiogram", "Kan Gazı Analizi",
        "Pancreas Lipaz (Spec cPL)", "Amilaz", "Lipaz", "Bile Acid Testi",
        "Parvovirüs (CPV) Hızlı Test", "FIV / FeLV Hızlı Test", "Giardia SNAP Test", "PCR (Patogen Paneli)",
        "Röntgen (Radyografi) - Thorax", "Röntgen (Radyografi) - Abdomen", "USG (Ultrasonografi) - Abdomen",
        "USG (Doppler)", "Ekokardiyografi (EKO)", "EKG (Elektrokardiyografi)", "Göz Muayenesi (Oftalmik İnceleme)",
        "Kan Basıncı Ölçümü", "Koagülasyon Paneli (PT/aPTT)", "Mikroskobik İnceleme (Kan Frotisi)",
        "Bakteriyel Kültür (Yara/Örnek)", "Cytology (FNA/Biopsy)",
        # Spesifik hormon testleri
        "Total T4 (Total Tiroksin)", "Free T4 (Serbest T4)", "TSH (Tiroit Uyarıcı Hormon)", "T3 (Triiyodotironin)",
        "Bazal Kortizol", "ACTH Stimülasyon Testi", "Progesteron", "Estradiol (E2)", "Testosteron",
        "İnsülin (Serum İnsülin)", "Fruktozamin", "PTH (Paratiroid Hormon)",
        "Bilirubin / Karaciğer Fonksiyon Testleri", "İnce Bağırsak / Dışkı Muayenesi (Fekal Flotasyon)"
    ]

    # Ayır: Teşhis için tetkikler (raporları vakadaki 'raporlar' anahtarlarıyla eşleşecek şekilde)
    test_havuzu = [
        "hemogram (tam kan sayımı)", "biyokimya (geniş panel)", "usg (ultrasonografi)",
        "parvovirüs (cpv) hızlı test", "röntgen (radyografi)", "ekg (elektrokardiyografi)",
        "idrar tahlili (tam idrar tetkiki)", "kan gazı analizi"
    ]

    # Müdahaleler / uygulamalar listesi (sadece "uygulandı" göstereceğiz)
    intervention_havuzu = [
        "Damar Yolu Açmak (IV Kateter)", "IV Sıvı Terapisi (Bolus/Şok Dozu)", "İntravenöz İnfüzyon (Drip)",
        "Üriner Kateterizasyon (Sonda)", "Oksijen Desteği (Maske/Kabin)", "Entübasyon (Endotrakeal Tüp)",
        "Nazal Oksijen Kanülü", "CPR (Kalp Masajı + Solunum)", "Kan Transfüzyonu", "Plazma Transfüzyonu (TDP)",
        "Mide Yıkama (Lavaj)", "Mide Sondası Uygulaması", "Yara Debridmanı ve Bandaj", "Vakum Drainaj (JP)",
        "Abdominosentez", "Sistosentez (İdrar Alımı)", "Peritoneal Lavaj", "Etkisizleştirme (Antidot Uygulama)",
        "Cerrahi Operasyon (Acil Laparotomi)", "Ovariohisterektomi (Pyometra/Kısırlaştırma)", "Ortopedik Fiksasyon (Platin/Pin)",
        "Trakeostomi", "Endoskopik İnceleme (Gastroskopi/Endoskopi)", "Wound Lavage & Debridement",
        "Fasiyal/Sinus Drainaj", "Dializ / Hemodiyaliz (Destek tesis varsa)", "İntravenöz Antibiyotik Infüzyon"
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
        "vaka_sirasi": 0,
        "tetkik_rapor_map": {},
        "tetkik_widgets": {}
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
        # normalize edilmiş rapor lookup (anahtarlar normalize_tr ile eşleşecek)
        state["aktif_rapor_lookup"] = {normalize_tr(k): v for k, v in state["aktif_vaka"].get("raporlar", {}).items()}
        # temiz widget map for tetkik display
        state["tetkik_widgets"] = {}

    if state["aktif_vaka"] is None:
        yeni_vaka_sec()

    # Tasarım Şablonu (Kutu)
    def ozel_kart_tasarimi(bilesenler):
        return ft.Container(
            content=ft.Column(bilesenler, tight=True),
            bgcolor="#111827",
            padding=22,
            border_radius=18
        )

    # 📱 SAYFA 1: GİRİŞ ACİL SERVİS
    def git_sayfa_1(e=None):
        if e is not None: 
            yeni_vaka_sec()
        state["yapilan_islemler"].clear()
        state["verilen_tedaviler"].clear()
        state["secilen_teshis"] = None
        state["tetkik_rapor_map"].clear()
        page.controls.clear()
        
        triyaj = state["aktif_vaka"]["triyaj"]
        t_renk = "red" if "KIRMIZI" in triyaj else ("orange" if "SARI" in triyaj else "green")

        page.add(
            ft.Container(
                content=ft.Row([
                    ft.Text(f"⚕️ BAŞARI SKORU: {state['kurtarilan']} TABURCU | {state['kaybedilen']} KAYIP", color="white", weight="bold")
                ], alignment="center"),
                bgcolor="#0f172a", padding=14, border_radius=12
            ),
            ft.Text(""),
            ft.Text("🚨 ACİL SERVİS ÇAĞRISI", size=28, color="#38bdf8", weight="bold"),
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

    # 🛠️ SAYFA: MÜDAHALELER / UYGULAMALAR
    def git_sayfa_mudahale(e=None):
        page.controls.clear()
        txt_arama = ft.TextField(label="🔎 Müdahale Ara veya Aşağıdan Manuel Seçin...", width=380)
        arama_sonuclari = ft.Column()
        secilen_islemler_kutusu = ft.Column()
        intervention_pool_norm = {normalize_tr(x) for x in intervention_havuzu}

        def is_intervention(item):
            norm = normalize_tr(item)
            return any(norm == i or norm in i or i in norm for i in intervention_pool_norm)

        def render_secilen_islemler():
            secilen_islemler_kutusu.controls.clear()
            secilen_islemler_kutusu.controls.append(ft.Text("Uygulanan Müdahaleler:", color="white", weight="bold"))
            displayed = [islem for islem in state["yapilan_islemler"] if is_intervention(islem)]
            if not displayed:
                secilen_islemler_kutusu.controls.append(ft.Text("Henüz hiç müdahale seçilmedi.", color="grey"))
            for islem in displayed:
                remove_btn = ft.ElevatedButton("✖", bgcolor="#1f2937", color="red", width=36, height=36, on_click=lambda e, m=islem: toggle_islem(m))
                secilen_islemler_kutusu.controls.append(ft.Row([ft.Text(f"✔️ {islem}", color="lime", weight="bold"), remove_btn], alignment="spaceBetween"))

        def toggle_islem(secilen_oge):
            if secilen_oge in state["yapilan_islemler"]:
                state["yapilan_islemler"].remove(secilen_oge)
            else:
                state["yapilan_islemler"].append(secilen_oge)
            txt_arama.value = ""
            arama_yenile(None)
            render_secilen_islemler()
            page.update()

        def arama_yenile(e):
            arama_sonuclari.controls.clear()
            aranan_kelime = normalize_tr(txt_arama.value)
            for oge in intervention_havuzu:
                if not aranan_kelime or aranan_kelime in normalize_tr(oge):
                    arama_sonuclari.controls.append(
                        ft.ElevatedButton(oge, bgcolor="#0b525b", color="white", width=380, on_click=lambda e, sec=oge: toggle_islem(sec))
                    )
                    if oge in state["yapilan_islemler"]:
                        arama_sonuclari.controls.append(ft.Text(f"✔️ {oge} uygulandı. Tekrar basarak geri alabilirsiniz.", color="lime", weight="bold"))
            page.update()

        txt_arama.on_change = arama_yenile
        arama_yenile(None)
        render_secilen_islemler()

        page.add(
            ft.Row([ft.ElevatedButton("⬅️ ANAMNEZE DÖN", bgcolor="grey", color="white", on_click=git_sayfa_2),
                    ft.Text("🛠️ Müdahaleler / Uygulamalar", size=22, color="#34d399", weight="bold")], alignment="spaceBetween"),
            txt_arama,
            arama_sonuclari,
            ft.Text(""),
            ozel_kart_tasarimi([secilen_islemler_kutusu]),
            ft.Text(""),
            ft.ElevatedButton("İLAÇLARA GEÇ 💊", bgcolor="green", color="white", width=380, height=50, on_click=git_sayfa_4)
        )
        page.update()

    # 📋 SAYFA 2: DETAYLI ANAMNEZ VE VİTAL BULGULAR
    def git_sayfa_2(e=None):
        page.controls.clear()
        v = state["aktif_vaka"]
        
        page.add(
            ft.Row([ft.ElevatedButton("⬅️ ACİL SERVİSE DÖN", bgcolor="grey", color="white", on_click=lambda _: git_sayfa_1(None)),
                    ft.Text("LABORATUVAR & TETKİKLER", size=22, color="#38bdf8", weight="bold")], alignment="spaceBetween"),
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
            ft.ElevatedButton("LABORATUVAR & TETKİKLER (TEŞHİS) 🔍", bgcolor="blue", color="white", width=380, height=50, on_click=git_sayfa_3)
        )
        page.update()

    # 🔍 SAYFA 3: TETKİK PANELİ
    def git_sayfa_3(e=None):
        page.controls.clear()
        txt_arama = ft.TextField(label="🔍 Tetkik Ara veya Aşağıdan Manuel Seçin...", width=380)
        arama_sonuclari = ft.Column()

        def listeye_ekle(secilen_oge):
            if secilen_oge not in state["yapilan_islemler"]:
                state["yapilan_islemler"].append(secilen_oge)
                txt_arama.value = ""
                arama_yenile(None)

        def arama_yenile(e):
            arama_sonuclari.controls.clear()
            aranan_kelime = normalize_tr(txt_arama.value)
            lookup = state.get("aktif_rapor_lookup", {})

            # laboratuvar tipleri için varsayılan mesaj 'Değerler normal' olmalı
            lab_tests = {
                "hemogram (tam kan sayımı)", "biyokimya (geniş panel)", "idrar tahlili (tam idrar tetkiki)", "kan gazı analizi",
                "total t4 (total tiroksin)", "free t4 (serbest t4)", "tsh (tiroit uyarıcı hormon)", "t3 (triiyodotironin)",
                "bazal kortizol", "acth stimülasyon testi", "progesteron", "estradiol (e2)", "testosteron",
                "insülin (serum insülin)", "fruktozamin", "pth (paratiroid hormon)"
            }

            for oge in tetkik_havuzu:
                if not aranan_kelime or aranan_kelime in normalize_tr(oge):
                    # ensure a text widget exists for this test
                    if oge not in state["tetkik_widgets"]:
                        state["tetkik_widgets"][oge] = ft.Text("", color="cyan", weight="bold")
                    text_ctrl = state["tetkik_widgets"][oge]

                    def show_result(secilen_oge, tc):
                        if secilen_oge not in state["yapilan_islemler"]:
                            state["yapilan_islemler"].append(secilen_oge)
                        norm2 = normalize_tr(secilen_oge)
                        if norm2 in lookup:
                            result_text = lookup[norm2]
                        else:
                            result_text = "Değerler normal"
                        tc.value = f"📄 {secilen_oge}: {result_text}"
                        page.update()

                    btn = ft.ElevatedButton(oge, bgcolor="#0d47a1", color="white", width=380, on_click=lambda e, sec=oge, tc=text_ctrl: show_result(sec, tc))
                    arama_sonuclari.controls.append(ft.Column([btn, text_ctrl]))
            page.update()

        txt_arama.on_change = arama_yenile
        arama_yenile(None)

        page.add(
            ft.ElevatedButton("⬅️ ANAMNEZE DÖN", bgcolor="grey", color="white", on_click=git_sayfa_2),
            ft.Text("🔬 Laboratuvar & Tetkikler (Teşhis)", size=20, color="white", weight="bold"),
            txt_arama,
            arama_sonuclari, 
            ft.Text(""),
            ft.ElevatedButton("MÜDAHALELERE GEÇ 🛠️", bgcolor="#0b525b", color="white", width=380, height=50, on_click=git_sayfa_mudahale)
        )
        page.update()

    # 💊 SAYFA 4: TEDAVİ REÇETE PANELİ
    def git_sayfa_4(e=None):
        page.controls.clear()
        txt_arama = ft.TextField(label="💊 İlaç Ara veya Aşağıdan Manuel Seçin...", width=380)
        arama_sonuclari = ft.Column()

        secilenler_kutusu = ft.Column()

        def render_secilenler():
            secilenler_kutusu.controls.clear()
            secilenler_kutusu.controls.append(ft.Text("Yazılan Reçete Protokolü:", color="white", weight="bold"))
            for ilac in state["verilen_tedaviler"]:
                # each med as row with delete icon
                remove_btn = ft.ElevatedButton("✖", bgcolor="#1f2937", color="red", width=36, height=36, on_click=lambda e, m=ilac: remove_med(m))
                secilenler_kutusu.controls.append(ft.Row([ft.Text(f"✔️ {ilac}", color="green", weight="bold"), remove_btn], alignment="spaceBetween"))

        def remove_med(ilac):
            if ilac in state["verilen_tedaviler"]:
                state["verilen_tedaviler"].remove(ilac)
            render_secilenler()
            page.update()

        def listeye_ekle(secilen_oge):
            if secilen_oge not in state["verilen_tedaviler"]:
                state["verilen_tedaviler"].append(secilen_oge)
            txt_arama.value = ""
            render_secilenler()
            arama_yenile(None)

        def clear_all(e):
            state["verilen_tedaviler"].clear()
            render_secilenler()
            page.update()

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
        render_secilenler()

        page.add(
            ft.Row([ft.ElevatedButton("⬅️ TETKİKLERE GERİ DÖN", bgcolor="grey", color="white", on_click=git_sayfa_3),
                    ft.Text("💊 Akut Sıvı & Reçete Sağaltımı", size=22, color="#f97316", weight="bold")], alignment="spaceBetween"),
            txt_arama,
            arama_sonuclari,
            ft.Divider(color="grey"),
            ozel_kart_tasarimi([secilenler_kutusu, ft.ElevatedButton("Reçeteyi Temizle 🗑️", bgcolor="red", color="white", on_click=clear_all)]),
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
        # categorize and normalize applied items (keep tests/interventions/meds separated)
        # applied raw lists
        applied_all = [x for x in state.get("yapilan_islemler", [])]

        # intervention pool normalized (to identify which applied items are interventions)
        intervention_pool_norm = {normalize_tr(x) for x in intervention_havuzu}
        tetkik_pool_norm = {normalize_tr(x) for x in tetkik_havuzu}

        # normalize applied lists (keep original strings for substring checks)
        applied_all_norm = [normalize_tr(x) for x in applied_all]
        applied_ilaclar_norm = [canonicalize(x) for x in state.get("verilen_tedaviler", [])]

        # implied mappings: if a panel/test is performed, it may imply subtests were done
        implied_map = {
            normalize_tr("hormon paneli (t4, tsh)"): [normalize_tr("total t4 (total tiroksin)"), normalize_tr("tsh (tiroit uyarıcı hormon)")],
            normalize_tr("biyokimya (geniş panel)"): [normalize_tr("amilaz"), normalize_tr("lipaz")],
        }

        # expand applied norms with implied items and build (norm, original) pairs
        applied_pairs = [(applied_all_norm[i], applied_all[i]) for i in range(len(applied_all_norm))]
        for a_norm, a_orig in list(applied_pairs):
            if a_norm in implied_map:
                for implied in implied_map[a_norm]:
                    if implied not in [p[0] for p in applied_pairs]:
                        applied_pairs.append((implied, None))

        # required lists
        # tetkikler: use vakadaki 'raporlar' keys (tests specifically ordered by report)
        req_tetkikler_list = list(v.get("raporlar", {}).keys())
        # interventions: take dogru_mudahaleler but exclude items that are tetkikler
        raw_req_islemler = v.get("dogru_mudahaleler", [])
        req_islemler_list = [x for x in raw_req_islemler if normalize_tr(x) not in tetkik_pool_norm]
        req_ilaclar_list = v.get("dogru_serumlar", [])

        # normalized/canonical required sets for comparison
        req_islemler_norm = {normalize_tr(x) for x in req_islemler_list}
        req_ilaclar_norm = {canonicalize(x) for x in req_ilaclar_list}
        req_tetkikler_norm = {normalize_tr(x) for x in req_tetkikler_list}

        # helper: tolerant matching (exact or substring either way)
        def matched(req_norm, applied_norms):
            for a in applied_norms:
                if not a:
                    continue
                if req_norm == a or req_norm in a or a in req_norm:
                    return True
            return False

        # build lists for display (separate tests vs interventions using tolerant matching)
        applied_norms = [p[0] for p in applied_pairs]

        def is_tetkik_item(item):
            return any(normalize_tr(item) == t or normalize_tr(item) in t or t in normalize_tr(item) for t in tetkik_pool_norm)

        applied_tetkikler_list = [x for x in state.get("yapilan_islemler", []) if is_tetkik_item(x)]
        applied_islemler_list = [x for x in state.get("yapilan_islemler", []) if not is_tetkik_item(x)]

        # hesaplamalar (sadece kendi kategorileri içinde karşılaştırma)
        yapılan_req_islemler = [x for x in req_islemler_list if matched(normalize_tr(x), applied_norms)]
        eksik_islemler = [x for x in req_islemler_list if not matched(normalize_tr(x), applied_norms)]

        yapılan_req_tetkikler = [x for x in req_tetkikler_list if matched(normalize_tr(x), applied_norms)]
        eksik_tetkikler = [x for x in req_tetkikler_list if not matched(normalize_tr(x), applied_norms)]

        verilen_req_ilaclar = [x for x in req_ilaclar_list if matched(canonicalize(x), applied_ilaclar_norm)]
        eksik_ilaclar = [x for x in req_ilaclar_list if not matched(canonicalize(x), applied_ilaclar_norm)]

        # build detailed mapping (which required item matched which applied item)
        tetkik_mappings = []
        for r in req_tetkikler_list:
            r_norm = normalize_tr(r)
            matched_applied = None
            for a_norm, a_orig in applied_pairs:
                if matched(r_norm, [a_norm]):
                    matched_applied = a_orig if a_orig is not None else f"(implied: {a_norm})"
                    break
            tetkik_mappings.append((r, matched_applied))

        islem_mappings = []
        for r in req_islemler_list:
            r_norm = normalize_tr(r)
            matched_applied = None
            for a_norm, a_orig in applied_pairs:
                if matched(r_norm, [a_norm]):
                    matched_applied = a_orig if a_orig is not None else f"(implied: {a_norm})"
                    break
            islem_mappings.append((r, matched_applied))

        ilac_mappings = []
        for r in req_ilaclar_list:
            r_can = canonicalize(r)
            matched_applied = None
            for idx, a_med_norm in enumerate(applied_ilaclar_norm):
                if matched(r_can, [a_med_norm]):
                    matched_applied = state.get('verilen_tedaviler', [])[idx]
                    break
            ilac_mappings.append((r, matched_applied))

        teshis_dogru = (state.get("secilen_teshis") == v.get("gercek_teshis"))
        # check lethal/contraindicated meds against canonicalized applied meds
        olumcul_hata_var = any(canonicalize(x) in applied_ilaclar_norm for x in v.get("olumcul_ilaclar", []))

        # basit yaşam/ölüm kararı: yeterli müdahale ve ilaçların uygulanması
        dogru_tedavi_var = (len(eksik_islemler) == 0) and (len(eksik_ilaclar) == 0)
        hasta_yasadi = False

        missing_count = len(eksik_islemler) + len(eksik_ilaclar)
        if olumcul_hata_var:
            durum_baslik = "❌ HASTA KONTRENDİKE İLAÇTAN KAYBEDİLDİ"
            durum_renk = "red"
            durum_detay = "Reçetede kontrendike bir ilaç uygulandı; hasta toksik reaksiyon sonucu kaybedildi."
        elif dogru_tedavi_var and teshis_dogru:
            hasta_yasadi = True
            durum_baslik = "🎉 TEBRİKLER! HASTA YAŞADI VE TABURCU OLDU"
            durum_renk = "green"
            durum_detay = "Kusursuz Tanı ve Tedavi: Gereken tetkik, müdahale ve ilaçlar uygulanmış." 
        elif missing_count <= 1:
            hasta_yasadi = True
            durum_baslik = "⚠️ HASTA YAŞADI (NEREDEYSE DOĞRU TEDAVİ)"
            durum_renk = "orange"
            durum_detay = "Çok yakın bir tedavi yapıldı; yalnızca bir öğe eksikti, hasta hayatta kaldı ama dikkatli olunmalı."
        elif dogru_tedavi_var and not teshis_dogru:
            hasta_yasadi = True
            durum_baslik = "⚠️ HASTA YAŞADI (ŞANS ESERİ)"
            durum_renk = "orange"
            durum_detay = "Doğru destek tedavisi yapıldı; teşhis yanlış olsa da hasta hayatta kaldı."
        else:
            durum_baslik = "❌ HASTA EKSİK PROTOKOLDEN KAYBEDİLDİ"
            durum_renk = "red"
            durum_detay = "Gereken acil müdahaleler veya ilaçlar eksik bırakıldı; bu yüzden hasta kaybedildi."

        if hasta_yasadi:
            state["kurtarilan"] += 1
        else:
            state["kaybedilen"] += 1

        # Kullanıcıya ayrıntılı çıktı
        page.add(
            ft.Text(f"📌 GERÇEK PATOLOJİ: {v.get('gercek_teshis','?').upper()}", size=18, color="#38bdf8", weight="bold"),
            ft.Divider(color="grey"),
            ft.Text(durum_baslik, size=16, color=durum_renk, weight="bold"),
            ft.Text(durum_detay, color="white"),
            ft.Text(""),
            ozel_kart_tasarimi([
                ft.Text("👨‍⚕️ Sizin Kayıtlarınız:", color="purple", weight="bold"),
                ft.Text(f"Koyduğunuz Teşhis: {state.get('secilen_teshis') if state.get('secilen_teshis') else 'Koyulmadı'}", color="grey"),
                ft.Text(f"Yapılan Tetkikler: {', '.join(applied_tetkikler_list) if applied_tetkikler_list else 'Hiçbiri'}", color="grey"),
                ft.Text(f"Yapılan Müdahaleler: {', '.join(applied_islemler_list) if applied_islemler_list else 'Hiçbiri'}", color="grey"),
                ft.Text(f"Yazdığınız Reçete: {', '.join(state.get('verilen_tedaviler')) if state.get('verilen_tedaviler') else 'Hiçbiri'}", color="grey"),
            ]),
            ft.Text(""),
            ozel_kart_tasarimi([
                ft.Text("📖 GEREKENLER (Detaylı)", color="orange", weight="bold"),
                ft.Text("🔬 Gereken Tetkikler:", color="green"),
                # detailed per-test mapping
                *[ft.Text(f"- {req} → Yapılan: {matched if matched else '—'}", color=("green" if matched else "red")) for req, matched in tetkik_mappings],
                ft.Text(""),
                ft.Text(""),
                ft.Text("🛠️ Gereken Müdahaleler:", color="green"),
                *[ft.Text(f"- {req} → Yapılan: {matched if matched else '—'}", color=("green" if matched else "red")) for req, matched in islem_mappings],
                ft.Text(""),
                ft.Text(""),
                ft.Text("💊 Gereken İlaçlar / Serumlar:", color="green"),
                *[ft.Text(f"- {req} → Verilen: {matched if matched else '—'}", color=("green" if matched else "red")) for req, matched in ilac_mappings],
            ]),
            ft.Text(""),
            ft.ElevatedButton("YENİ ACİL VAKAYA GEÇ 🔄", bgcolor="white", color="black", width=380, height=50, on_click=git_sayfa_1)
        )
        page.update()

    git_sayfa_1(None)

ft.app(target=main)