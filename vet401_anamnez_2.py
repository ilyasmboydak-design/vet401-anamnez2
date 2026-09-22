import streamlit as st
import re
import os

# Page Config
st.set_page_config(
    page_title="VET401 Akıllı Anamnez & Bulgu Sorgu Konsolu II",
    page_icon="🐄",
    layout="wide",
)

# Custom Styling
st.markdown("""
    <style>
    .main-title {
        color: #1F4E79;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2px;
    }
    .sub-title {
        color: #595959;
        font-family: 'Arial', sans-serif;
        font-style: italic;
        text-align: center;
        font-size: 15px;
        margin-bottom: 20px;
    }
    .vaka-box {
        background-color: #EBF1F5;
        border: 2px solid #1F4E79;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .vaka-header {
        background: linear-gradient(90deg, #1F4E79 0%, #2F5597 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .card-found {
        background-color: #F2F4F8;
        border-left: 6px solid #1F4E79;
        padding: 14px 18px;
        border-radius: 6px;
        margin-bottom: 12px;
        box-shadow: 1px 1px 5px rgba(0,0,0,0.05);
    }
    .badge-category {
        background-color: #D9E1F2;
        color: #1F4E79;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
    }
    .card-content {
        font-size: 15px;
        color: #262626;
        line-height: 1.5;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🐄 Çukurova Üniversitesi Veteriner Fakültesi</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='sub-title'>VET401 İç Hastalıkları I — Akıllı Anamnez & Bulgu Sorgu Konsolu II</h3>", unsafe_allow_html=True)

# Helper function to find images in gorseller_2 or other directories
def find_gorsel_2(image_name):
    if not image_name:
        return None
    search_dirs = ["gorseller_2", "gorseller", "/workspace/artifacts", "."]
    possible_exts = [".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"]
    
    for s_dir in search_dirs:
        if os.path.exists(s_dir):
            for fname in os.listdir(s_dir):
                fname_no_ext = os.path.splitext(fname)[0]
                if fname_no_ext.lower() == image_name.lower():
                    return os.path.join(s_dir, fname)
                for ext in possible_exts:
                    if fname.lower() == (image_name + ext).lower():
                        return os.path.join(s_dir, fname)
    return None

# FULL 15 CASES KNOWLEDGE BASE
CASES = {
    "Vaka 1 (Pamuk)": {
        "kod": "VAKA_1",
        "gorsel_adi": "papillomatosis",
        "sikayet": "Hocam, bizim düvenin memesinde ve boyun etrafında irili ufaklı siğil gibi sert yumrular çıkmaya başladı. İnek kendisini bir yere sürtmüyor ama bu siğiller her geçen gün çoğalıyor, sağım yaparken elimize takılıyor...",
        "categories": {
            "RASYON_YEM": {"name": "Rasyon & Yemleme Öyküsü", "keywords": ["rasyon", "yem", "silaj", "ot", "besleme"], "content": "Mera dönüşü günlük 4 kg süt yemi ve kuru ot verilmektedir. Yem kalitesinde belirgin sorun yok."},
            "LOKASYON_RAKIM": {"name": "Lokasyon & Coğrafi Öykü", "keywords": ["lokasyon", "rakım", "nerede", "bölge", "mera"], "content": "Ova merasında ortak sürüde otlama geçmişi var. Diğer işletme hayvanlarıyla temas yüksek."},
            "GECMIS_HASTALIK": {"name": "Geçmiş Hastalık & Sağlık Geçmişi", "keywords": ["geçmiş", "sağlık", "aşı", "önceki"], "content": "Daha önce geçirilmiş sistemik hastalık yok. Rutin parazit ilaçlaması yapılmış."},
            "ISTAH_DURUMU": {"name": "İştah & Yutma / Çiğneme Durumu", "keywords": ["iştah", "yem yiyor mu", "yutma", "geviş"], "content": "İştah ve geviş getirme tamamen normaldir. Sağım esnasında siğillere dokunulunca huzursuzluk gösteriyor."},
            "VITAL_BULGULAR": {"name": "Genel Muayene & Vital Bulgular", "keywords": ["ateş", "sıcaklık", "nabız", "kalp", "solunum", "mukoza"], "content": "Vücut Sıcaklığı: 38.6 °C | Nabız: 68 atım/dk | Solunum: 22 nefes/dk | Mukoza: Pembe | Deride ağrısız karnabahar benzeri pediküllü hiperkeratotik nodüller."},
            "OSKULTASYON": {"name": "Kalp, Akciğer & Göğüs Oskültasyonu", "keywords": ["kalp ses", "oskültasyon", "akciğer", "dinleme"], "content": "Kalp ve akciğer sesleri tamamen fizyolojik sınırlar içerisindedir."},
            "AGRI_TESTLERI": {"name": "Retikulum, Perküsyon & Ağrı Testleri", "keywords": ["ağrı", "retikulum", "test", "perküsyon"], "content": "Withers pinch ve ksilofoit testleri negatiftir."},
            "HEMOGRAM": {"name": "Tam Hemogram (CBC) Tahlili", "keywords": ["hemogram", "cbc", "kan", "lökosit", "eritrosit", "mcv", "hct"], "content": "RBC: 6.8 x10^6/µL | Hb: 11.2 g/dL | PCV: %34 | MCV: 50 fL | MCH: 16.4 pg | MCHC: 32.9 g/dL | RDW: %16.2 | PLT: 320 x10^3/µL | WBC: 7.8 x10^3/µL | Çomak: %1 | Segmenter: %38 | Lenfosit: %55 | Monosit: %4 | Eozinofil: %2 | Bazofil: %0 | Fibrinojen: 3.2 g/L | PP/F: 21.8"},
            "BIYOKIMYA_PANELI": {"name": "Bütünsellikli Serum Biyokimyası & Enzim Paneli", "keywords": ["biyokimya", "ast", "ggt", "alt", "alp", "ck", "ldh", "üre", "kreatinin", "glikoz", "bilirubin", "protein", "albümin", "globülin", "na", "k", "cl", "ca", "p", "mg", "fe", "cu", "zn", "se"], "content": "AST: 78 U/L | GGT: 24 U/L | ALT: 18 U/L | ALP: 62 U/L | CK: 110 U/L | LDH: 620 U/L | Troponin I: 0.02 ng/mL | BUN: 14 mg/dL | Kreatinin: 1.1 mg/dL | Glikoz: 62 mg/dL | Total Bilirubin: 0.3 mg/dL | Total Protein: 7.2 g/dL | Albümin: 3.4 g/dL | Globülin: 3.8 g/dL | A/G: 0.89 | Na: 140 mEq/L | K: 4.6 mEq/L | Cl: 102 mEq/L | Ca: 9.8 mg/dL | P: 5.8 mg/dL | Mg: 2.2 mg/dL | Fe: 110 µg/dL | Cu: 95 µg/dL | Zn: 105 µg/dL | Se: 72 µg/L"},
            "KAN_GAZI": {"name": "Venöz / Arteriyel Kan Gazı Analizi", "keywords": ["kan gazı", "ph", "po2", "pco2", "hco3", "be", "laktat"], "content": "pH: 7.41 | pO2: 42 mmHg | pCO2: 40 mmHg | HCO3-: 25 mEq/L | BE: +1.2 mEq/L | Laktat: 1.1 mmol/L"},
            "IDRAR_TAHLILI": {"name": "Tam İdrar Tahlili (Urinalysis)", "keywords": ["idrar", "urinalysis", "dansite", "protein", "glikoz", "keton", "sediment"], "content": "Dansite: 1.025 | pH: 8.0 | Protein: Negatif | Glikoz: Negatif | Keton: Negatif | Bilirubin: Negatif | Hemoglobin: Negatif | Sediment: Temiz"},
            "GORUNTULEME_MIKROBIYOLOJI": {"name": "Görüntüleme, Mikrobiyoloji & Biyopsi", "keywords": ["mikroskop", "biyopsi", "kültür", "frotı", "histopatoloji"], "content": "Biyopsi Histopatolojisi: Epidermal hiperkeratoz, akantoz ve koilositler tespit edildi."}
        },
        "egitmen_bilgisi": {
            "kesin_tani": "Sığır Papillomavirus (BPV - Bovine Papillomavirus) Kaynaklı Papillomatosis.",
            "patofizyoloji": "BPV sıyrık ve mikrotravmalardan epitel bazal hücrelerine girer. E6 ve E7 onkoproteinleri epitel hücre proliferasyonunu uyararak benign akantotik nodüller (siğil) oluşturur.",
            "ayirici_tani": "LSD (Çiçek) lezyonlarından ağrısız olması, ateş yapmaması ve nekrotik 'sitno' oluşturmaması ile ayrılır.",
            "tedavi_protokolu": "1. Otohemoterapi: 1-2 hafta arayla 3 kez 10-20 mL venöz kan alınıp İM uygulanır.\n2. Cerrahi koterizasyon veya ligasyon.\n3. İmmünomodülatör destek.",
            "koruma_biyogüvenlik": "Sağım ekipmanları dezenfekte edilmeli, enfekte hayvanlar ayrılmalı ve sürüde mukoza sıyrıklarına yol açan çalı/tel engellenmelidir."
        }
    },
    "Vaka 2 (Sarıkız)": {
        "kod": "VAKA_2",
        "gorsel_adi": "LSD",
        "sikayet": "Hocam, hayvan iki gündür ateşler içinde yanıyor, yemden sudan kesildi. Vücudunda, bacaklarında ve memesinde ceviz büyüklüğünde sert yumrular belirdi. Sütü birden bıçak gibi kesildi, bacakları da ödem yaptı şişti...",
        "categories": {
            "RASYON_YEM": {"name": "Rasyon & Yemleme Öyküsü", "keywords": ["rasyon", "yem", "besleme"], "content": "Ateş ve ağrı nedeniyle yem tüketimi tamamen durmuştur (anoreksi)."},
            "LOKASYON_RAKIM": {"name": "Lokasyon & Coğrafi Öykü", "keywords": ["lokasyon", "sinek", "dere", "mera"], "content": "Dere yatağına yakın merada otlatılmaktadır. Kan emici sinek ve kene popülasyonu çok yüksektir."},
            "GECMIS_HASTALIK": {"name": "Geçmiş Hastalık & Sağlık Geçmişi", "keywords": ["geçmiş", "aşı"], "content": "LSD aşısı yapılmamıştır."},
            "ISTAH_DURUMU": {"name": "İştah & Yutma / Çiğneme Durumu", "keywords": ["iştah", "anoreksi"], "content": "Şiddetli iştahsızlık ve depresyon mevcuttur."},
            "VITAL_BULGULAR": {"name": "Genel Muayene & Vital Bulgular", "keywords": ["ateş", "sıcaklık", "nabız", "kalp", "solunum", "ödem", "yumru"], "content": "Vücut Sıcaklığı: 41.2 °C | Nabız: 96 atım/dk | Solunum: 48 nefes/dk | Tüm vücutta 0.5-5 cm çaplı etrafı belirgin sert nodüller (sitno), bacaklarda ve gerdanda şiddetli ödem."},
            "OSKULTASYON": {"name": "Kalp, Akciğer & Göğüs Oskültasyonu", "keywords": ["kalp ses", "akciğer", "oskültasyon"], "content": "Akciğerlerde sert veziküler solunum sesleri, taşikardi."},
            "AGRI_TESTLERI": {"name": "Retikulum, Perküsyon & Ağrı Testleri", "keywords": ["ağrı", "test"], "content": "Nodüllere dokunulduğunda aşırı ağrı duyarlılığı."},
            "HEMOGRAM": {"name": "Tam Hemogram (CBC) Tahlili", "keywords": ["hemogram", "cbc", "kan", "lökosit", "fibrinojen"], "content": "RBC: 5.2 x10^6/µL | Hb: 8.8 g/dL | PCV: %28 | MCV: 53.8 fL | MCH: 16.9 pg | MCHC: 31.4 g/dL | RDW: %18.1 | PLT: 140 x10^3/µL | WBC: 14.8 x10^3/µL | Çomak: %6 | Segmenter: %68 | Lenfosit: %20 | Monosit: %4 | Eozinofil: %2 | Bazofil: %0 | Fibrinojen: 8.4 g/L | PP/F: 11.2"},
            "BIYOKIMYA_PANELI": {"name": "Bütünsellikli Serum Biyokimyası & Enzim Paneli", "keywords": ["biyokimya", "ast", "ggt", "alt", "alp", "ck", "ldh", "saa", "üre", "kreatinin", "protein", "albümin", "globülin"], "content": "AST: 142 U/L | GGT: 38 U/L | ALT: 28 U/L | ALP: 95 U/L | CK: 280 U/L | LDH: 890 U/L | SAA: 180 µg/mL | BUN: 28 mg/dL | Kreatinin: 1.6 mg/dL | Glikoz: 78 mg/dL | Total Bilirubin: 0.8 mg/dL | Total Protein: 8.6 g/dL | Albümin: 2.6 g/dL | Globülin: 6.0 g/dL | A/G: 0.43 | Na: 135 mEq/L | K: 3.8 mEq/L | Cl: 96 mEq/L | Ca: 8.4 mg/dL | P: 4.2 mg/dL | Mg: 1.9 mg/dL | Fe: 62 µg/dL | Cu: 125 µg/dL | Zn: 70 µg/dL | Se: 55 µg/L"},
            "KAN_GAZI": {"name": "Venöz / Arteriyel Kan Gazı Analizi", "keywords": ["kan gazı", "ph", "po2", "pco2", "hco3", "be", "laktat"], "content": "pH: 7.34 | pO2: 36 mmHg | pCO2: 48 mmHg | HCO3-: 21 mEq/L | BE: -3.8 mEq/L | Laktat: 2.8 mmol/L"},
            "IDRAR_TAHLILI": {"name": "Tam İdrar Tahlili (Urinalysis)", "keywords": ["idrar", "urinalysis", "dansite", "protein"], "content": "Dansite: 1.032 | pH: 7.2 | Protein: ++ | Glikoz: Negatif | Keton: Negatif | Bilirubin: Hafif Pozitif | Hemoglobin: Negatif | Sediment: Lökosit ve epitel hücreleri"},
            "GORUNTULEME_MIKROBIYOLOJI": {"name": "Görüntüleme, Mikrobiyoloji & PCR", "keywords": ["pcr", "mikroskop", "biyopsi", "virüs"], "content": "Nodül Biyopsisi PCR: Capripoxvirus DNA'sı pozitif. Histopatolojide vaskülit ve intrastoplazmik inklüzyon cisimcikleri."}
        },
        "egitmen_bilgisi": {
            "kesin_tani": "Lumpy Skin Disease (LSD / Sığırların Yumrulu Deri Hastalığı / Çiçek).",
            "patofizyoloji": "Capripoxvirus kan emici vektörlerle bulaşarak vaskülit, perivaskülit ve lenfanjite yol açar. Dermis ve alt dokularda iskemik nekroz gelişerek 'sitno' karakterize nodüller oluşur.",
            "ayirici_tani": "Pseudo-LSD (Herpesvirus 2) ve Papillomatosis'ten yüksek ateş, nekrotik sitno oluşumu ve vaskülit ile ayrılır.",
            "tedavi_protokolu": "Spesifik antiviral tedavisi yoktur. Sekonder bakteriyel enfeksiyonlara karşı Parenteral Antibiyotik (Florfenikol / Penisilin), NSAİİ (Fluniksut Meglumin) ve sıvı desteği uygulanır.",
            "koruma_biyogüvenlik": "İhbarı mecburidir! Canlı LSD/Capripox aşısı uygulanmalı, vektör mücadelesi yapılmalı ve karantina önlemleri alınmalıdır."
        }
    },
    "Vaka 3 (Kınalı)": {
        "kod": "VAKA_3",
        "gorsel_adi": None,
        "sikayet": "Hocam, yeni sütten kestiğimiz kuzuların dudaklarının kenarlarında ve burun etrafında kabuklu, kanamalı çirkin yaralar oluştu. Yem yiyemiyorlar, anasını emmeye çalışırken canları yanıyor, ağızları şiş...",
        "categories": {
            "RASYON_YEM": {"name": "Rasyon & Yemleme Öyküsü", "keywords": ["rasyon", "yem", "kuzu", "süt"], "content": "Kuru ot ve kuzu büyütme yemi verilmektedir ancak dudaklardaki ağrı nedeniyle yem tüketimi düşmüştür."},
            "LOKASYON_RAKIM": {"name": "Lokasyon & Coğrafi Öykü", "keywords": ["lokasyon", "mera", "çalı"], "content": "Dikenli otların yoğun olduğu merada otlatılmaktadır."},
            "GECMIS_HASTALIK": {"name": "Geçmiş Hastalık & Sağlık Geçmişi", "keywords": ["geçmiş", "aşı"], "content": "Sürüye yeni kuzu katılımı olmuş, ektima aşısı uygulanmamış."},
            "ISTAH_DURUMU": {"name": "İştah & Yutma / Çiğneme Durumu", "keywords": ["iştah", "ağrı", "emme"], "content": "Ağızdaki yaralar nedeniyle emme ve çiğneme refleksleri ağrılıdır."},
            "VITAL_BULGULAR": {"name": "Genel Muayene & Vital Bulgular", "keywords": ["ateş", "sıcaklık", "nabız", "dudak", "kabuk", "yara"], "content": "Vücut Sıcaklığı: 39.8 °C | Nabız: 110 atım/dk | Solunum: 32 nefes/dk | Dudak bileşim yerlerinde, burun deliklerinde siğilimsi, siyanotik kanamalı kabuklu lezyonlar."},
            "OSKULTASYON": {"name": "Kalp, Akciğer & Göğüs Oskültasyonu", "keywords": ["kalp", "akciğer"], "content": "Kalp ve akciğer sesleri normal."},
            "AGRI_TESTLERI": {"name": "Retikulum, Perküsyon & Ağrı Testleri", "keywords": ["ağrı"], "content": "Dudak lezyonları muayenesinde şiddetli ağrı ve kanama."},
            "HEMOGRAM": {"name": "Tam Hemogram (CBC) Tahlili", "keywords": ["hemogram", "cbc", "kan", "lökosit"], "content": "RBC: 10.2 x10^6/µL | Hb: 11.8 g/dL | PCV: %36 | MCV: 35.3 fL | MCH: 11.5 pg | MCHC: 32.7 g/dL | RDW: %15.8 | PLT: 410 x10^3/µL | WBC: 12.4 x10^3/µL | Çomak: %3 | Segmenter: %62 | Lenfosit: %30 | Monosit: %3 | Eozinofil: %2 | Bazofil: %0 | Fibrinojen: 4.8 g/L | PP/F: 16.2"},
            "BIYOKIMYA_PANELI": {"name": "Bütünsellikli Serum Biyokimyası & Enzim Paneli", "keywords": ["biyokimya", "ast", "ggt", "alt", "üre", "kreatinin", "protein"], "content": "AST: 88 U/L | GGT: 32 U/L | ALT: 22 U/L | ALP: 140 U/L | CK: 130 U/L | LDH: 680 U/L | BUN: 22 mg/dL | Kreatinin: 1.2 mg/dL | Glikoz: 55 mg/dL | Total Protein: 6.8 g/dL | Albümin: 3.1 g/dL | Globülin: 3.7 g/dL | A/G: 0.84 | Na: 138 mEq/L | K: 4.4 mEq/L | Cl: 100 mEq/L | Ca: 9.2 mg/dL | P: 6.2 mg/dL | Mg: 2.1 mg/dL | Fe: 95 µg/dL | Cu: 88 µg/dL | Zn: 90 µg/dL | Se: 65 µg/L"},
            "KAN_GAZI": {"name": "Venöz / Arteriyel Kan Gazı Analizi", "keywords": ["kan gazı", "ph", "po2", "pco2"], "content": "pH: 7.38 | pO2: 40 mmHg | pCO2: 42 mmHg | HCO3-: 23 mEq/L | BE: -0.8 mEq/L | Laktat: 1.6 mmol/L"},
            "IDRAR_TAHLILI": {"name": "Tam İdrar Tahlili (Urinalysis)", "keywords": ["idrar", "urinalysis"], "content": "Dansite: 1.022 | pH: 7.5 | Protein: Negatif | Glikoz: Negatif | Keton: Negatif | Sediment: Temiz"},
            "GORUNTULEME_MIKROBIYOLOJI": {"name": "Görüntüleme, Mikrobiyoloji & PCR", "keywords": ["pcr", "elektron mikroskobu", "virüs"], "content": "Kabuk Biyopsisi PCR: Parapoxvirus DNA'sı pozitif. Histopatolojide epitel hücrelerinde balonsu dejenerasyon."}
        },
        "egitmen_bilgisi": {
            "kesin_tani": "Bulaşıcı Ektima / Orf (Parapoxvirus).",
            "patofizyoloji": "Parapoxvirus mukoza ve derideki mikrotravmalardan girerek epitel hücrelerinde balonlaşma, vesikül, pustül ve kalın kabuklu kanamalı siğil benzeri lezyonlara yol açar.",
            "ayirici_tani": "Çiçek ve Şap hastalıklarından lezyonların dudak bileşiminde lokalize olması ve sistemik ağır paralizi yapmaması ile ayrılır.",
            "tedavi_protokolu": "Lezyonlar %3'lük iyotlu antiseptiklerle temizlenir. Ağız içi Gliserin İyode sürülür. Sekonder enfeksiyonlar için sprey antibiyotik ve sistemik NSAİİ uygulanır.",
            "koruma_biyogüvenlik": "ZOONOZDUR! İnsanlara bulaşır (ellerde ağrılı nodüller). Mümkünse canlı scarification aşısı uygulanmalı, eldivensiz müdahale edilmemelidir."
        }
    },
    "Vaka 4 (Gül)": {
        "kod": "VAKA_4",
        "gorsel_adi": None,
        "sikayet": "Hocam, merada çalıya takılıp böğrünü çizdiren ineğin yarasını dün fark ettik. Yaranın içi delik delik olmuş, içine bakınca beyaz beyaz kurtların hareket ettiğini gördük. Yaranın etrafı kötü kokuyor...",
        "categories": {
            "RASYON_YEM": {"name": "Rasyon & Yemleme Öyküsü", "keywords": ["rasyon", "yem"], "content": "İştah hafif düşmüş, su tüketimi normaldir."},
            "LOKASYON_RAKIM": {"name": "Lokasyon & Coğrafi Öykü", "keywords": ["lokasyon", "mera", "sinek"], "content": "Sıcak ve nemli merada otlatma. Wohlfahrtia magnifica ve Lucilia sericata sinekleri yoğundur."},
            "GECMIS_HASTALIK": {"name": "Geçmiş Hastalık & Sağlık Geçmişi", "keywords": ["geçmiş", "yara"], "content": "1 hafta önce böğür bölgesinde travmatik cilt kesiği öyküsü var."},
            "ISTAH_DURUMU": {"name": "İştah & Yutma / Çiğneme Durumu", "keywords": ["iştah"], "content": "Ağrı nedeniyle hafif hiporeksi."},
            "VITAL_BULGULAR": {"name": "Genel Muayene & Vital Bulgular", "keywords": ["ateş", "sıcaklık", "nabız", "yara", "kurt", "koku"], "content": "Vücut Sıcaklığı: 39.1 °C | Nabız: 82 atım/dk | Solunum: 28 nefes/dk | Sağ böğürde nekrotik, kötü kokulu, içinde hareketli 1-1.5 cm boyunda sinek larvaları (maggots) bulunan geniş yara kaverni."},
            "OSKULTASYON": {"name": "Kalp, Akciğer & Göğüs Oskültasyonu", "keywords": ["kalp", "akciğer"], "content": "Normal akciğer ve kalp sesleri."},
            "AGRI_TESTLERI": {"name": "Retikulum, Perküsyon & Ağrı Testleri", "keywords": ["ağrı"], "content": "Yara çevresi palpasyonunda lokal şiddetli reaksiyon ve ağrı."},
            "HEMOGRAM": {"name": "Tam Hemogram (CBC) Tahlili", "keywords": ["hemogram", "cbc", "kan", "eozinofil", "lökosit"], "content": "RBC: 6.2 x10^6/µL | Hb: 10.5 g/dL | PCV: %32 | MCV: 51.6 fL | MCH: 16.9 pg | MCHC: 32.8 g/dL | RDW: %16.8 | PLT: 290 x10^3/µL | WBC: 13.2 x10^3/µL | Çomak: %4 | Segmenter: %58 | Lenfosit: %24 | Monosit: %4 | Eozinofil: %10 | Bazofil: %0 | Fibrinojen: 5.2 g/L | PP/F: 14.8"},
            "BIYOKIMYA_PANELI": {"name": "Bütünsellikli Serum Biyokimyası & Enzim Paneli", "keywords": ["biyokimya", "ast", "ggt", "alt", "ck", "üre", "kreatinin"], "content": "AST: 92 U/L | GGT: 28 U/L | ALT: 24 U/L | ALP: 70 U/L | CK: 210 U/L | LDH: 710 U/L | BUN: 18 mg/dL | Kreatinin: 1.1 mg/dL | Glikoz: 68 mg/dL | Total Protein: 7.6 g/dL | Albümin: 3.0 g/dL | Globülin: 4.6 g/dL | A/G: 0.65 | Na: 139 mEq/L | K: 4.2 mEq/L | Cl: 99 mEq/L | Ca: 9.4 mg/dL | P: 5.2 mg/dL | Mg: 2.1 mg/dL | Fe: 85 µg/dL | Cu: 102 µg/dL | Zn: 82 µg/dL | Se: 68 µg/L"},
            "KAN_GAZI": {"name": "Venöz / Arteriyel Kan Gazı Analizi", "keywords": ["kan gazı", "ph", "po2", "pco2"], "content": "pH: 7.40 | pO2: 41 mmHg | pCO2: 39 mmHg | HCO3-: 24 mEq/L | BE: +0.4 mEq/L | Laktat: 1.3 mmol/L"},
            "IDRAR_TAHLILI": {"name": "Tam İdrar Tahlili (Urinalysis)", "keywords": ["idrar", "urinalysis"], "content": "Dansite: 1.024 | pH: 7.8 | Protein: Negatif | Glikoz: Negatif | Keton: Negatif | Sediment: Temiz"},
            "GORUNTULEME_MIKROBIYOLOJI": {"name": "Görüntüleme, Mikrobiyoloji & Parazitoloji", "keywords": ["mikroskop", "larva", "parazit"], "content": "Larva İncelemesi: Wohlfahrtia magnifica L3 larvası. Posterior spirakulumda peritrem yapısı ve 3 adet düz solunum yarığı izlendi."}
        },
        "egitmen_bilgisi": {
            "kesin_tani": "Miyasis / Traumatik Yara Kurtlanması (Wohlfahrtia magnifica larvası).",
            "patofizyoloji": "Diptera sinekleri yumurtalarını açık yara ve mukoza kenarlarına bırakır. Yumurtadan çıkan L1-L3 larvaları ürettiği proteolitik enzimlerle canlı dokuları eriterek derin nekrotik kavernler oluşturur.",
            "ayirici_tani": "Apselerden ve flegmondan yara içerisinde canlı sinek larvalarının gözle görülmesi ve koku ile ayrılır.",
            "tedavi_protokolu": "1. Larvaların pens ile mekanik olarak temizlenmesi.\n2. Yaranın %3 Oksijenli Su ve Antiseptikler ile yıkanması.\n3. Sistemik veya lokal İvermektin / Doramektin uygulaması.\n4. Antibakteriyel spray ve sistemik antibiyotik.",
            "koruma_biyogüvenlik": "Yaz aylarında travmatik yaralar derhal antiseptiklerle kapatılmalı, sinek kovucu dökme (pour-on) insektisitler uygulanmalıdır."
        }
    },
    "Vaka 5 (Karabaş)": {
        "kod": "VAKA_5",
        "gorsel_adi": None,
        "sikayet": "Hocam, dün akşam sapasağlam olan tosun sabah kalkamadı. Sol arka kalçası kocaman şişmiş, dokununca çıtır çıtır gaz sesi geliyor ve içi sıcak. Hayvanın ateşi çok yüksek, inleyip duruyor...",
        "categories": {
            "RASYON_YEM": {"name": "Rasyon & Yemleme Öyküsü", "keywords": ["rasyon", "yem", "besi"], "content": "Yüksek protein ve enerji içerikli besi rasyonu uygulanmaktadır."},
            "LOKASYON_RAKIM": {"name": "Lokasyon & Coğrafi Öykü", "keywords": ["lokasyon", "toprak", "mera"], "content": "Mera dönüşü kapalı besi alanına alınmış. Toprakla yoğun temas var."},
            "GECMIS_HASTALIK": {"name": "Geçmiş Hastalık & Sağlık Geçmişi", "keywords": ["geçmiş", "aşı"], "content": "Clostridium aşısı (karma aşı) yapılmamıştır."},
            "ISTAH_DURUMU": {"name": "İştah & Yutma / Çiğneme Durumu", "keywords": ["iştah", "anoreksi"], "content": "Şiddetli anoreksi, adinamya ve inleme."},
            "VITAL_BULGULAR": {"name": "Genel Muayene & Vital Bulgular", "keywords": ["ateş", "sıcaklık", "nabız", "kalça", "şişlik", "gaz", "krepütasyon"], "content": "Vücut Sıcaklığı: 41.5 °C | Nabız: 115 atım/dk | Solunum: 52 nefes/dk | Sol uyluk/kalça bölgesinde önce sıcak ve ağrılı, sonra soğuk ve ağrısız emfizematöz şişlik. Palpasyonda gaz krepütasyonu (çıtırtı sesi) var."},
            "OSKULTASYON": {"name": "Kalp, Akciğer & Göğüs Oskültasyonu", "keywords": ["kalp", "akciğer"], "content": "Şiddetli taşikardi, boğuk kalp sesleri, hızlı solunum."},
            "AGRI_TESTLERI": {"name": "Retikulum, Perküsyon & Ağrı Testleri", "keywords": ["ağrı"], "content": "Lezyonlu kas grubuna basılınca başlangıçta aşırı ağrı, nekroz geliştikçe ağrısızlaşma."},
            "HEMOGRAM": {"name": "Tam Hemogram (CBC) Tahlili", "keywords": ["hemogram", "cbc", "kan", "lökosit", "çomak", "fibrinojen"], "content": "RBC: 5.8 x10^6/µL | Hb: 9.2 g/dL | PCV: %30 | MCV: 51.7 fL | MCH: 15.8 pg | MCHC: 30.6 g/dL | RDW: %19.2 | PLT: 110 x10^3/µL | WBC: 18.6 x10^3/µL | Çomak: %12 | Segmenter: %65 | Lenfosit: %15 | Monosit: %6 | Eozinofil: %2 | Bazofil: %0 | Fibrinojen: 9.6 g/L | PP/F: 8.8"},
            "BIYOKIMYA_PANELI": {"name": "Bütünsellikli Serum Biyokimyası & Enzim Paneli", "keywords": ["biyokimya", "ast", "ck", "ldh", "üre", "kreatinin", "protein", "laktat"], "content": "AST: 420 U/L | GGT: 35 U/L | ALT: 48 U/L | ALP: 85 U/L | CK: 8500 U/L | LDH: 2400 U/L | BUN: 38 mg/dL | Kreatinin: 2.4 mg/dL | Glikoz: 110 mg/dL | Total Bilirubin: 1.2 mg/dL | Total Protein: 8.2 g/dL | Albümin: 2.5 g/dL | Globülin: 5.7 g/dL | A/G: 0.44 | Na: 132 mEq/L | K: 5.8 mEq/L | Cl: 92 mEq/L | Ca: 7.8 mg/dL | P: 6.8 mg/dL | Mg: 1.8 mg/dL | Fe: 55 µg/dL | Cu: 110 µg/dL | Zn: 65 µg/dL | Se: 45 µg/L"},
            "KAN_GAZI": {"name": "Venöz / Arteriyel Kan Gazı Analizi", "keywords": ["kan gazı", "ph", "po2", "pco2", "hco3", "be", "laktat"], "content": "pH: 7.22 | pO2: 32 mmHg | pCO2: 52 mmHg | HCO3-: 16 mEq/L | BE: -9.2 mEq/L | Laktat: 6.4 mmol/L (Metabolik Asidoz + Doku Hipoksisi)"},
            "IDRAR_TAHLILI": {"name": "Tam İdrar Tahlili (Urinalysis)", "keywords": ["idrar", "urinalysis", "miyoglobin"], "content": "Dansite: 1.028 | pH: 6.5 | Protein: +++ | Glikoz: Negatif | Keton: Negatif | Bilirubin: Pozitif | Hemoglobin/Miyoglobin: Koyu Kahverengi Miyoglobinüri | Sediment: Hücre birikintileri"},
            "GORUNTULEME_MIKROBIYOLOJI": {"name": "Görüntüleme, Mikrobiyoloji & Gram Boyama", "keywords": ["gram", "kas", "froti", "bakteri"], "content": "Kas İğne Aspirasyon Frotisi: Gram-Pozitif, uçları yuvarlak, sporsuz veya santral/subterminal sporlu tekli/çiftli çomaklar (Clostridium chauvoei). Kas dokusu siyah-kırmızı renkte ve acı yağ kokusunda."}
        },
        "egitmen_bilgisi": {
            "kesin_tani": "Yanıkara / Blackleg (Clostridium chauvoei).",
            "patofizyoloji": "Topraktan alınan Cl. chauvoei sporları kas dokusuna yerleşir. Travma veya anoksi durumunda çimlenerek alpha ve beta toksinleri salgılar. Şiddetli miyonekroz, gaz emfizemi ve toksik şok gelişir.",
            "ayirici_tani": "Malign Ödem (Cl. septicum) ve Travmatik yaralanmalardan acı yağ kokusu, masif CK yüksekliği (>5000 U/L) ve Gram-pozitif sporlu basiller ile ayrılır.",
            "tedavi_protokolu": "Erken safhada masif yüksek doz Kristalize Penisilin G (20.000-40.000 IU/kg İV/İM) ve lezyon çevresine Penisilin infiltrasyonu. Şişliklere drenaj kesileri açılması. İV Sıvı (Ringer Laktat) ve NSAİİ.",
            "koruma_biyogüvenlik": "Ölen hayvanlar asla açılmamalı (otopsi yapılmamalı), kireçlenerek derin gömülmelidir! Sürü Polyvalent Clostridium aşıları ile aşılanmalıdır."
        }
    },
    "Vaka 6 (Benekli)": {
        "kod": "VAKA_6",
        "gorsel_adi": "Hipoderma Bovis",
        "sikayet": "Hocam, kışın sırtında fındık büyüklüğünde şişlikler vardı önemsemedik. Şimdi bahar geldi, sırtındaki şişlikler ceviz kadar oldu ve ortalarında delik var. Bastırınca içinden irin ve kurt çıkacak gibi duruyor...",
        "categories": {
            "RASYON_YEM": {"name": "Rasyon & Yemleme Öyküsü", "keywords": ["rasyon", "yem"], "content": "Besleme normal, kaba ve yoğun yem verilmektedir."},
            "LOKASYON_RAKIM": {"name": "Lokasyon & Coğrafi Öykü", "keywords": ["lokasyon", "mera", "sineklik"], "content": "Yaz aylarında merada otlatılmıştır. Hypoderma bovis sineklerinin yoğun olduğu bölge."},
            "GECMIS_HASTALIK": {"name": "Geçmiş Hastalık & Sağlık Geçmişi", "keywords": ["geçmiş", "parazit"], "content": "Sonbahar ayında sistemik ivermektin/parazit ilacı uygulanmamış."},
            "ISTAH_DURUMU": {"name": "İştah & Yutma / Çiğneme Durumu", "keywords": ["iştah"], "content": "İştah ve süt verimi hafif düşmüştür."},
            "VITAL_BULGULAR": {"name": "Genel Muayene & Vital Bulgular", "keywords": ["ateş", "sıcaklık", "nabız", "sırt", "nodül", "delik", "kurt"], "content": "Vücut Sıcaklığı: 38.8 °C | Nabız: 72 atım/dk | Solunum: 24 nefes/dk | Sırt ve bel bölgesi vertebra yanlarında 15-20 adet ortası delikli sert nodüller (warbles)."},
            "OSKULTASYON": {"name": "Kalp, Akciğer & Göğüs Oskültasyonu", "keywords": ["kalp", "akciğer"], "content": "Normal akciğer ve kalp sesleri."},
            "AGRI_TESTLERI": {"name": "Retikulum, Perküsyon & Ağrı Testleri", "keywords": ["ağrı"], "content": "Sırt nodüllerine basılınca hafif ağrı reaksiyonu."},
            "HEMOGRAM": {"name": "Tam Hemogram (CBC) Tahlili", "keywords": ["hemogram", "cbc", "kan", "eozinofil"], "content": "RBC: 6.5 x10^6/µL | Hb: 10.8 g/dL | PCV: %33 | MCV: 50.8 fL | MCH: 16.6 pg | MCHC: 32.7 g/dL | RDW: %16.0 | PLT: 310 x10^3/µL | WBC: 11.2 x10^3/µL | Çomak: %2 | Segmenter: %50 | Lenfosit: %32 | Monosit: %4 | Eozinofil: %12 | Bazofil: %0 | Fibrinojen: 3.8 g/L | PP/F: 17.1"},
            "BIYOKIMYA_PANELI": {"name": "Bütünsellikli Serum Biyokimyası & Enzim Paneli", "keywords": ["biyokimya", "ast", "ggt", "alt", "ck", "üre", "kreatinin"], "content": "AST: 85 U/L | GGT: 26 U/L | ALT: 20 U/L | ALP: 68 U/L | CK: 140 U/L | LDH: 640 U/L | BUN: 16 mg/dL | Kreatinin: 1.0 mg/dL | Glikoz: 64 mg/dL | Total Protein: 7.4 g/dL | Albümin: 3.2 g/dL | Globülin: 4.2 g/dL | A/G: 0.76 | Na: 141 mEq/L | K: 4.5 mEq/L | Cl: 101 mEq/L | Ca: 9.6 mg/dL | P: 5.4 mg/dL | Mg: 2.2 mg/dL | Fe: 102 µg/dL | Cu: 92 µg/dL | Zn: 98 µg/dL | Se: 70 µg/L"},
            "KAN_GAZI": {"name": "Venöz / Arteriyel Kan Gazı Analizi", "keywords": ["kan gazı", "ph", "po2", "pco2"], "content": "pH: 7.41 | pO2: 41 mmHg | pCO2: 40 mmHg | HCO3-: 25 mEq/L | BE: +1.0 mEq/L | Laktat: 1.2 mmol/L"},
            "IDRAR_TAHLILI": {"name": "Tam İdrar Tahlili (Urinalysis)", "keywords": ["idrar", "urinalysis"], "content": "Dansite: 1.023 | pH: 8.0 | Protein: Negatif | Glikoz: Negatif | Keton: Negatif | Sediment: Temiz"},
            "GORUNTULEME_MIKROBIYOLOJI": {"name": "Görüntüleme, Mikrobiyoloji & Parazitoloji", "keywords": ["mikroskop", "larva", "hypoderma"], "content": "Nodül Ekstraksiyonu: Delikten sıkılarak çıkarılan 2.5 cm boyunda kahverengi dikenli Hypoderma bovis L3 larvası."}
        },
        "egitmen_bilgisi": {
            "kesin_tani": "Hypoderma Bovis / Sığır Bükelegi (Nöf / Nokra).",
            "patofizyoloji": "Sineğin ayak kıllarına bıraktığı yumurtalardan çıkan L1 larvaları deriyi delip omurilik kanalına (H. bovis) veya özofagusa (H. lineatum) göç eder. Baharda sırta ulaşarak L3 larva haline gelir ve solunum deliği açar.",
            "ayirici_tani": "Deri altı apselerinden ve kistlerden nodülün ortasında solunum deliği bulunması ve L3 larvasının çıkarılması ile ayrılır.",
            "tedavi_protokolu": "L3 larvaları sırttayken SIKILARAK PATLATILMAMALIDIR! (Anafilaktik şok riski!). Sonbaharda göç aşamasında sistemik İvermektin / Doramektin dökme veya enjeksiyon uygulanır.",
            "koruma_biyogüvenlik": "Sonbaharda (Ekim-Kasım) tüm sürüye rutin dökme makrosiklik lakton uygulanarak larvalar göç yolundayken imha edilmelidir."
        }
    },
    "Vaka 7 (Duman)": {
        "kod": "VAKA_7",
        "gorsel_adi": None,
        "sikayet": "Hocam, bizim domuzların yanındaki dana birden çıldırdı sanki! Bacaklarını ve böğrünü duvara, çite öyle bir sürtüyor ki derisi soyuldu kan içinde kaldı. Durmadan böğürüyor, ağzından köpükler saçıyor...",
        "categories": {
            "RASYON_YEM": {"name": "Rasyon & Yemleme Öyküsü", "keywords": ["rasyon", "yem"], "content": "Besleme durmuştur."},
            "LOKASYON_RAKIM": {"name": "Lokasyon & Coğrafi Öykü", "keywords": ["lokasyon", "domuz", "barınak"], "content": "Sığırlar ile evcil/yaban domuzları aynı barınak/çiftlik alanında yetiştirilmektedir."},
            "GECMIS_HASTALIK": {"name": "Geçmiş Hastalık & Sağlık Geçmişi", "keywords": ["geçmiş", "aşı"], "content": "Aujeszky aşısı uygulanmamıştır."},
            "ISTAH_DURUMU": {"name": "İştah & Yutma / Çiğneme Durumu", "keywords": ["iştah", "salya"], "content": "Ağızdan yoğun salya akışı, yutma güçlüğü ve kriz hali."},
            "VITAL_BULGULAR": {"name": "Genel Muayene & Vital Bulgular", "keywords": ["ateş", "sıcaklık", "nabız", "kaşıntı", "sürecek", "kan", "salya"], "content": "Vücut Sıcaklığı: 40.8 °C | Nabız: 120 atım/dk | Solunum: 60 nefes/dk | Lokal durdurulamayan şiddetli pruritus (Mad Itch), arka bacak ve flank bölgesinde derinin kemiğe kadar soyulduğu otomutilasyon. Kas kasılmaları ve salya."},
            "OSKULTASYON": {"name": "Kalp, Akciğer & Göğüs Oskültasyonu", "keywords": ["kalp", "akciğer"], "content": "Şiddetli taşikardi, takipne."},
            "AGRI_TESTLERI": {"name": "Retikulum, Perküsyon & Ağrı Testleri", "keywords": ["ağrı"], "content": "Lokal dokunmada aşırı irritabilite ve saldırganlık."},
            "HEMOGRAM": {"name": "Tam Hemogram (CBC) Tahlili", "keywords": ["hemogram", "cbc", "kan", "lökosit"], "content": "RBC: 7.2 x10^6/µL | Hb: 12.0 g/dL | PCV: %38 | MCV: 52.7 fL | MCH: 16.6 pg | MCHC: 31.5 g/dL | RDW: %16.5 | PLT: 280 x10^3/µL | WBC: 15.6 x10^3/µL | Çomak: %5 | Segmenter: %72 | Lenfosit: %18 | Monosit: %4 | Eozinofil: %1 | Bazofil: %0 | Fibrinojen: 6.2 g/L | PP/F: 13.8"},
            "BIYOKIMYA_PANELI": {"name": "Bütünsellikli Serum Biyokimyası & Enzim Paneli", "keywords": ["biyokimya", "ast", "ck", "ldh", "üre", "kreatinin", "glikoz"], "content": "AST: 210 U/L | GGT: 32 U/L | ALT: 35 U/L | ALP: 90 U/L | CK: 1450 U/L | LDH: 1120 U/L | BUN: 32 mg/dL | Kreatinin: 1.8 mg/dL | Glikoz: 145 mg/dL (Stres) | Total Bilirubin: 0.6 mg/dL | Total Protein: 7.8 g/dL | Albümin: 3.2 g/dL | Globülin: 4.6 g/dL | A/G: 0.69 | Na: 142 mEq/L | K: 4.8 mEq/L | Cl: 100 mEq/L | Ca: 9.0 mg/dL | P: 5.6 mg/dL | Mg: 2.0 mg/dL | Fe: 90 µg/dL | Cu: 105 µg/dL | Zn: 85 µg/dL | Se: 60 µg/L"},
            "KAN_GAZI": {"name": "Venöz / Arteriyel Kan Gazı Analizi", "keywords": ["kan gazı", "ph", "po2", "pco2"], "content": "pH: 7.31 | pO2: 38 mmHg | pCO2: 46 mmHg | HCO3-: 20 mEq/L | BE: -4.2 mEq/L | Laktat: 3.8 mmol/L"},
            "IDRAR_TAHLILI": {"name": "Tam İdrar Tahlili (Urinalysis)", "keywords": ["idrar", "urinalysis"], "content": "Dansite: 1.026 | pH: 7.0 | Protein: + | Glikoz: Pozitif (Stres Glukozürisi) | Keton: Negatif | Sediment: Temiz"},
            "GORUNTULEME_MIKROBIYOLOJI": {"name": "Görüntüleme, Mikrobiyoloji & PCR", "keywords": ["pcr", "beyin", "virüs", "inklüzyon"], "content": "Beyin Kökü ve Serebellum PCR: Suid Herpesvirus 1 (Pseudorabies) DNA'sı pozitif. Nöronlarda intranükleer inklüzyon cisimcikleri."}
        },
        "egitmen_bilgisi": {
            "kesin_tani": "Yalancı Kuduz / Aujeszky Hastalığı (Suid Herpesvirus 1).",
            "patofizyoloji": "Domuzlar rezervuardır. Virus sığırlara solunum/sindirimsiz temasla geçer, periferik sinirlerden SSS'ye ulaşır. Şiddetli gangliyonöronitis ve refleks ark irritasyonu ile lokomotor pruritus (çıldırtan kaşıntı) oluşturur.",
            "ayirici_tani": "Gerçek Kuduz (Rabies) hastalığından patognomonik lokal çılgınca kaşıntı (Mad Itch) olması ile ayrılır. Kuduzda lokal kaşıntı görülmez.",
            "tedavi_protokolu": "Tedavisi yoktur! Ölüm oranı %100'dür. Semptomatik sedatifler (Ksilazin/Apromazin) ve antihistaminikler geçici rahatlama sağlar ancak hayvan prognozsuz olduğu için uyutulur/itlaf edilir.",
            "koruma_biyogüvenlik": "Sığırlar ve koyunlar kesinlikle domuz barınakları ile temas ettirilmemelidir!"
        }
    },
    "Vaka 8 (Alaca)": {
        "kod": "VAKA_8",
        "gorsel_adi": None,
        "sikayet": "Hocam, meradan gelen ineğin ateşi tavan yaptı. Gözlerinin akı ve damağı sapsarı oldu. En korktuğumuz şey oldu, hayvan koyu çay gibi, kanlı idrar yapmaya başladı! Çok halsiz, sallanarak yürüyor...",
        "categories": {
            "RASYON_YEM": {"name": "Rasyon & Yemleme Öyküsü", "keywords": ["rasyon", "yem"], "content": "Mera otlaması. İştah tamamen kesilmiş."},
            "LOKASYON_RAKIM": {"name": "Lokasyon & Coğrafi Öykü", "keywords": ["lokasyon", "mera", "kene"], "content": "Rhipicephalus (Boophilus) microplus ve Annulatus kenelerinin çok yoğun olduğu mera alanı."},
            "GECMIS_HASTALIK": {"name": "Geçmiş Hastalık & Sağlık Geçmişi", "keywords": ["geçmiş", "kene"], "content": "Sürüye yeni kene banyosu/dökme insektisit yapılmamış."},
            "ISTAH_DURUMU": {"name": "İştah & Yutma / Çiğneme Durumu", "keywords": ["iştah", "anoreksi"], "content": "Şiddetli anoreksi ve depresyon."},
            "VITAL_BULGULAR": {"name": "Genel Muayene & Vital Bulgular", "keywords": ["ateş", "sıcaklık", "nabız", "idrar", "sarılık", "ikter", "hemoglobinüri"], "content": "Vücut Sıcaklığı: 41.8 °C | Nabız: 118 atım/dk | Solunum: 50 nefes/dk | Mukozalar limon sarısı ikterik ve aşırı soluk. İdrar koyu kırmızı/kahverengi (Hemoglobinüri)."},
            "OSKULTASYON": {"name": "Kalp, Akciğer & Göğüs Oskültasyonu", "keywords": ["kalp", "akciğer"], "content": "Taşikardi, anemiye bağlı kardiyak üfürüm (anemic murmur), sert akciğer sesleri."},
            "AGRI_TESTLERI": {"name": "Retikulum, Perküsyon & Ağrı Testleri", "keywords": ["ağrı"], "content": "Ağrı testleri negatif, dalak palpasyonunda splenomegali."},
            "HEMOGRAM": {"name": "Tam Hemogram (CBC) Tahlili", "keywords": ["hemogram", "cbc", "kan", "mcv", "hct", "rbc", "anemi"], "content": "RBC: 2.1 x10^6/µL | Hb: 4.2 g/dL | PCV: %12 | MCV: 57.1 fL | MCH: 20.0 pg | MCHC: 35.0 g/dL | RDW: %22.4 | PLT: 85 x10^3/µL (Trombositopeni) | WBC: 16.2 x10^3/µL | Çomak: %8 | Segmenter: %65 | Lenfosit: %20 | Monosit: %5 | Eozinofil: %2 | Bazofil: %0 | Fibrinojen: 5.8 g/L | PP/F: 10.3"},
            "BIYOKIMYA_PANELI": {"name": "Bütünsellikli Serum Biyokimyası & Enzim Paneli", "keywords": ["biyokimya", "ast", "ggt", "alt", "alp", "bilirubin", "idrar"], "content": "AST: 280 U/L | GGT: 42 U/L | ALT: 52 U/L | ALP: 110 U/L | CK: 190 U/L | LDH: 1850 U/L | BUN: 34 mg/dL | Kreatinin: 1.9 mg/dL | Glikoz: 82 mg/dL | Total Bilirubin: 6.8 mg/dL | İndirekt Bilirubin: 5.2 mg/dL | Total Protein: 5.8 g/dL | Albümin: 2.2 g/dL | Globülin: 3.6 g/dL | A/G: 0.61 | Na: 132 mEq/L | K: 3.6 mEq/L | Cl: 94 mEq/L | Ca: 8.0 mg/dL | P: 3.2 mg/dL | Mg: 1.8 mg/dL | Fe: 180 µg/dL | Cu: 95 µg/dL | Zn: 75 µg/dL | Se: 50 µg/L"},
            "KAN_GAZI": {"name": "Venöz / Arteriyel Kan Gazı Analizi", "keywords": ["kan gazı", "ph", "po2", "pco2"], "content": "pH: 7.28 | pO2: 28 mmHg (Ağır Hipoksi) | pCO2: 44 mmHg | HCO3-: 18 mEq/L | BE: -6.8 mEq/L | Laktat: 4.8 mmol/L"},
            "IDRAR_TAHLILI": {"name": "Tam İdrar Tahlili (Urinalysis)", "keywords": ["idrar", "urinalysis", "hemoglobinüri"], "content": "Dansite: 1.020 | pH: 7.2 | Protein: +++ | Glikoz: Negatif | Keton: Negatif | Bilirubin: +++ | Hemoglobin: ++++ Koyu Kırmızı (Santrifüjde çökmez, berraklaşmaz!) | Sediment: Eritrosit Yok (Hemoliz)"},
            "GORUNTULEME_MIKROBIYOLOJI": {"name": "Görüntüleme, Mikrobiyoloji & Kan Frotisi", "keywords": ["mikroskop", "froti", "giemsa", "babesia", "kene"], "gorsel_adi": "Babesiosis", "content": "Giemsa Boyalı İnce Kan Frotisi: Eritrositlerin içinde çeperde veya merkezde ikili armut şeklinde (trofomerozoit) Babesia bigemina merozoitleri tespit edildi."}
        },
        "egitmen_bilgisi": {
            "kesin_tani": "Sığır Babesiosis / Piroplasmoz (Babesia bigemina).",
            "patofizyoloji": "Akar (kene) ısırığı ile eritrositlere giren Babesia sporozoitleri çoğalarak masif İNTRAVASKÜLER HEMOLİZ oluşturur. Serbest hemoglobin böbrek eşiğini aşarak HEMOGLOBİNÜRİ, anemi ve indirekt hiperbilirubinemi (ikter) yapar.",
            "ayirici_tani": "Anaplasmosis'ten koyu kırmızı/çay rengi HEMOGLOBİNÜRİ bulunması ile ayrılır (Anaplazmozda idrar berraktır, hemoliz ekstravaskülerdir!).",
            "tedavi_protokolu": "1. Spesifik İlaç: İmidokarb Dipropionat (1.2 mg/kg SC/İM) veya Diminazen Aseturat (3.5 mg/kg İM).\n2. Ağır anemide (PCV <%12) Tam Kan Transfüzyonu (4-8 Litre).\n3. Parenteral Sıvı (Ringer Laktat) ve Demir/B12 takviyesi.",
            "koruma_biyogüvenlik": "Kenelerle stratejik mücadele yapılmalı (dökme Flumethrin/Deltamethrin). İmidokarb koruyucu dozda (2.5 mg/kg) meraya çıkışta uygulanabilir."
        }
    },
    "Vaka 9 (Sarımsak)": {
        "kod": "VAKA_9",
        "gorsel_adi": None,
        "sikayet": "Hocam, meralar kuruyunca keneler arttı. Bizim inek 3 gündür aşırı halsiz, gözlerinin içi porselen gibi sapsarı oldu. Ama garip olan idrarı dipberrak, kanlı değil. Nefes nefese kalıyor, yerinden kalkamıyor...",
        "categories": {
            "RASYON_YEM": {"name": "Rasyon & Yemleme Öyküsü", "keywords": ["rasyon", "yem"], "content": "İştah kapalı, mera otlaması."},
            "LOKASYON_RAKIM": {"name": "Lokasyon & Coğrafi Öykü", "keywords": ["lokasyon", "mera", "kene"], "content": "Kuru yaz merası, kene ve kan emici sinek popülasyonu."},
            "GECMIS_HASTALIK": {"name": "Geçmiş Hastalık & Sağlık Geçmişi", "keywords": ["geçmiş", "aşı"], "content": "Geçmişte ektoparazit uygulaması yok."},
            "ISTAH_DURUMU": {"name": "İştah & Yutma / Çiğneme Durumu", "keywords": ["iştah", "anoreksi"], "content": "Depresyon ve iştahsızlık."},
            "VITAL_BULGULAR": {"name": "Genel Muayene & Vital Bulgular", "keywords": ["ateş", "sıcaklık", "nabız", "idrar", "sarılık", "ikter"], "content": "Vücut Sıcaklığı: 40.5 °C | Nabız: 110 atım/dk | Solunum: 46 nefes/dk | Mukozalar porselen sarısı aşırı ikterik. İDRAR TAMAMEN BERRAK VE SARI (Hemoglobinüri YOK!)."},
            "OSKULTASYON": {"name": "Kalp, Akciğer & Göğüs Oskültasyonu", "keywords": ["kalp", "akciğer"], "content": "Taşikardi, anemi üfürümü."},
            "AGRI_TESTLERI": {"name": "Retikulum, Perküsyon & Ağrı Testleri", "keywords": ["ağrı"], "content": "Dalak muayenesinde splenomegali."},
            "HEMOGRAM": {"name": "Tam Hemogram (CBC) Tahlili", "keywords": ["hemogram", "cbc", "kan", "anemi", "rbc", "mcv"], "content": "RBC: 2.4 x10^6/µL | Hb: 4.8 g/dL | PCV: %14 | MCV: 58.3 fL | MCH: 20.0 pg | MCHC: 34.2 g/dL | RDW: %21.0 | PLT: 105 x10^3/µL | WBC: 14.8 x10^3/µL | Çomak: %6 | Segmenter: %62 | Lenfosit: %24 | Monosit: %6 | Eozinofil: %2 | Bazofil: %0 | Fibrinojen: 5.2 g/L | PP/F: 11.1"},
            "BIYOKIMYA_PANELI": {"name": "Bütünsellikli Serum Biyokimyası & Enzim Paneli", "keywords": ["biyokimya", "ast", "ggt", "alt", "bilirubin"], "content": "AST: 240 U/L | GGT: 36 U/L | ALT: 44 U/L | ALP: 98 U/L | CK: 160 U/L | LDH: 1620 U/L | BUN: 28 mg/dL | Kreatinin: 1.6 mg/dL | Glikoz: 76 mg/dL | Total Bilirubin: 5.4 mg/dL | İndirekt Bilirubin: 4.1 mg/dL | Total Protein: 6.2 g/dL | Albümin: 2.4 g/dL | Globülin: 3.8 g/dL | A/G: 0.63 | Na: 135 mEq/L | K: 3.8 mEq/L | Cl: 96 mEq/L | Ca: 8.2 mg/dL | P: 3.6 mg/dL | Mg: 1.9 mg/dL | Fe: 165 µg/dL | Cu: 90 µg/dL | Zn: 80 µg/dL | Se: 52 µg/L"},
            "KAN_GAZI": {"name": "Venöz / Arteriyel Kan Gazı Analizi", "keywords": ["kan gazı", "ph", "po2", "pco2"], "content": "pH: 7.32 | pO2: 30 mmHg | pCO2: 42 mmHg | HCO3-: 19 mEq/L | BE: -5.4 mEq/L | Laktat: 4.1 mmol/L"},
            "IDRAR_TAHLILI": {"name": "Tam İdrar Tahlili (Urinalysis)", "keywords": ["idrar", "urinalysis"], "content": "Dansite: 1.022 | pH: 7.8 | Protein: + | Glikoz: Negatif | Keton: Negatif | Bilirubin: ++ | Hemoglobin: NEGATİF (Berrak Açık Sarı) | Sediment: Temiz"},
            "GORUNTULEME_MIKROBIYOLOJI": {"name": "Görüntüleme, Mikrobiyoloji & Kan Frotisi", "keywords": ["mikroskop", "froti", "giemsa", "anaplasma"], "content": "Giemsa Kan Frotisi: Eritrositlerin marjinal (kenar) sınırlarında küçük, koyu bazofilik yuvarlak Anaplasma marginale noktacıkları (%30 enjeksiyon oranı)."}
        },
        "egitmen_bilgisi": {
            "kesin_tani": "Sığır Anaplasmosis (Anaplasma marginale).",
            "patofizyoloji": "Anaplasma rickettsia'ları eritrositlere yerleşir. Dalak ve karaciğerdeki makrofajlar enfekte eritrositleri fagosite eder (EKSTRAVASKÜLER HEMOLİZ). İntravasküler lizis olmadığı için HEMOGLOBİNÜRİ GÖRÜLMEZ!",
            "ayirici_tani": "Babesiosis ve Leptospirozis'ten İDRARIN TAMAMEN BERRAK OLMASI (Hemoglobinüri olmaması) ile ayrılır.",
            "tedavi_protokolu": "1. Spesifik Antibiyotik: Oksitetrasiklin (20 mg/kg İM uzun etkili - LA, 3 gün arayla 2 doz) veya İmidokarb Dipropionat (2.5 mg/kg SC).\n2. Kan Transfüzyonu (PCV <%12 ise).\n3. Destekleyici sıvı ve vitaminler.",
            "koruma_biyogüvenlik": "Bulaşma keneler ve kanlı enjektör/dehorning aletleriyle olur. Her hayvana ayrı iğne ucu kullanılmalı, kene mücadelesi yapılmalıdır."
        }
    },
    "Vaka 10 (Efe)": {
        "kod": "VAKA_10",
        "gorsel_adi": None,
        "sikayet": "Hocam, meradan dönen dananın kulak altındaki ve kürek kemiğinin önündeki bezeri yumruk gibi şişti. Hayvanın gözünün bebeğinde beyaz bir perde oluştu, ateşi yükseldi ve yememeye başladı...",
        "categories": {
            "RASYON_YEM": {"name": "Rasyon & Yemleme Öyküsü", "keywords": ["rasyon", "yem"], "content": "İştahsızlık nedeniyle yem tüketimi durmuştur."},
            "LOKASYON_RAKIM": {"name": "Lokasyon & Coğrafi Öykü", "keywords": ["lokasyon", "mera", "kene"], "content": "Hyalomma anatolicum kenelerinin yoğun olduğu tropikal/subtropikal mera."},
            "GECMIS_HASTALIK": {"name": "Geçmiş Hastalık & Sağlık Geçmişi", "keywords": ["geçmiş", "aşı"], "content": "Theileria aşısı yapılmamış."},
            "ISTAH_DURUMU": {"name": "İştah & Yutma / Çiğneme Durumu", "keywords": ["iştah"], "content": "Anoreksi, depresyon ve gözlerde yaşarma."},
            "VITAL_BULGULAR": {"name": "Genel Muayene & Vital Bulgular", "keywords": ["ateş", "sıcaklık", "nabız", "lenf", "beze", "şişlik", "göz", "opak"], "content": "Vücut Sıcaklığı: 41.0 °C | Nabız: 105 atım/dk | Solunum: 44 nefes/dk | Lnn. prescapularis ve subillaris aşırı büyümüş (yumruk büyüklüğünde, ağrılı). Korneada bilateral opaklaşma (ak basma / korneal bulanıklık)."},
            "OSKULTASYON": {"name": "Kalp, Akciğer & Göğüs Oskültasyonu", "keywords": ["kalp", "akciğer"], "content": "Akciğerlerde akciğer ödemine bağlı krepitasyon sesleri, taşikardi."},
            "AGRI_TESTLERI": {"name": "Retikulum, Perküsyon & Ağrı Testleri", "keywords": ["ağrı"], "content": "Lenf nodları palpasyonunda şiddetli ağrı reaksiyonu."},
            "HEMOGRAM": {"name": "Tam Hemogram (CBC) Tahlili", "keywords": ["hemogram", "cbc", "kan", "lökopeni", "anemi"], "content": "RBC: 3.8 x10^6/µL | Hb: 6.2 g/dL | PCV: %18 | MCV: 47.3 fL | MCH: 16.3 pg | MCHC: 34.4 g/dL | RDW: %19.5 | PLT: 90 x10^3/µL | WBC: 3.2 x10^3/µL (Lökopeni) | Çomak: %2 | Segmenter: %30 | Lenfosit: %62 | Monosit: %4 | Eozinofil: %2 | Bazofil: %0 | Fibrinojen: 6.8 g/L | PP/F: 8.8"},
            "BIYOKIMYA_PANELI": {"name": "Bütünsellikli Serum Biyokimyası & Enzim Paneli", "keywords": ["biyokimya", "ast", "ggt", "alt", "bilirubin", "protein"], "content": "AST: 195 U/L | GGT: 32 U/L | ALT: 38 U/L | ALP: 105 U/L | CK: 150 U/L | LDH: 1450 U/L | BUN: 30 mg/dL | Kreatinin: 1.7 mg/dL | Glikoz: 70 mg/dL | Total Bilirubin: 3.8 mg/dL | Total Protein: 5.4 g/dL | Albümin: 1.9 g/dL | Globülin: 3.5 g/dL | A/G: 0.54 | Na: 134 mEq/L | K: 3.7 mEq/L | Cl: 95 mEq/L | Ca: 8.1 mg/dL | P: 3.8 mg/dL | Mg: 1.8 mg/dL | Fe: 130 µg/dL | Cu: 88 µg/dL | Zn: 72 µg/dL | Se: 48 µg/L"},
            "KAN_GAZI": {"name": "Venöz / Arteriyel Kan Gazı Analizi", "keywords": ["kan gazı", "ph", "po2", "pco2"], "content": "pH: 7.30 | pO2: 32 mmHg | pCO2: 45 mmHg | HCO3-: 18 mEq/L | BE: -6.0 mEq/L | Laktat: 4.2 mmol/L"},
            "IDRAR_TAHLILI": {"name": "Tam İdrar Tahlili (Urinalysis)", "keywords": ["idrar", "urinalysis"], "content": "Dansite: 1.021 | pH: 7.4 | Protein: ++ | Glikoz: Negatif | Keton: Negatif | Bilirubin: ++ | Hemoglobin: Negatif | Sediment: Lökositler"},
            "GORUNTULEME_MIKROBIYOLOJI": {"name": "Görüntüleme, Mikrobiyoloji & Lenf Punksiyonu", "keywords": ["mikroskop", "froti", "koch", "şizont", "lenf"], "content": "Lenf Düğümü Punksiyon Frotisi (Giemsa): Makrofaj ve lenfositler içerisinde halka/virgül şeklinde Koch Cisimcikleri (Şizontlar). Kan frotisinde eritirosit içi piroplazmlar."}
        },
        "egitmen_bilgisi": {
            "kesin_tani": "Tropikal Theileriosis (Theileria annulata).",
            "patofizyoloji": "Hyalomma keneleri ile bulaşan sporozoitler lenfositleri enfekte ederek kontrolsüz lenfoid proliferasyona (Koch cisimcikleri) ve takiben lenfoid yıkım/lökopeniye yol açar. Eritrositer evrede anemi ve korneal bulanıklık gelişir.",
            "ayirici_tani": "Babesiosis'ten yüzeyel lenf nodlarının masif büyümesi, korneal opaklaşma ve frotide Koch Cisimcikleri görülmesi ile ayrılır.",
            "tedavi_protokolu": "1. Spesifik İlaç: Buparvaquone (2.5 mg/kg İM, gerekirse 48 saat sonra 2. doz).\n2. İkinci seçenek: Oksitetrasiklin (20 mg/kg LA).\n3. Kornea için lokal atropin ve antibiyotikli göz damlaları, İV sıvı desteği.",
            "koruma_biyogüvenlik": "Attenuye canlı Theileria annulata aşısı (Aşvax) yapılmalı, Hyalomma keneleriyle barınak ve mera düzeyinde mücadele edilmelidir."
        }
    },
    "Vaka 11 (Nazlı)": {
        "kod": "VAKA_11",
        "gorsel_adi": None,
        "sikayet": "Hocam, yeni doğum yapan ineğimizin sütü aniden kanlı ve pembe renkte gelmeye başladı. Memeleri sarkık ve hamur gibi gevşek ama sıcak değil. Sürüde geçen hafta iki gebe düve de aniden yavru attı...",
        "categories": {
            "RASYON_YEM": {"name": "Rasyon & Yemleme Öyküsü", "keywords": ["rasyon", "yem"], "content": "Standart laktasyon rasyonu verilmektedir."},
            "LOKASYON_RAKIM": {"name": "Lokasyon & Coğrafi Öykü", "keywords": ["lokasyon", "su", "fare", "kemirgen"], "content": "Çiftlik çevresinde durgun su birikintileri ve yoğun kemirgen (fare/sıçan) popülasyonu var."},
            "GECMIS_HASTALIK": {"name": "Geçmiş Hastalık & Sağlık Geçmişi", "keywords": ["geçmiş", "abort", "yavru atma"], "content": "Geçen hafta sürüde 2 adet son trimester abort olgusu yaşanmış."},
            "ISTAH_DURUMU": {"name": "İştah & Yutma / Çiğneme Durumu", "keywords": ["iştah"], "content": "İştah hafif düşük, süt verimi aniden düşmüştür."},
            "VITAL_BULGULAR": {"name": "Genel Muayene & Vital Bulgular", "keywords": ["ateş", "sıcaklık", "nabız", "süt", "meme", "pembe", "kanlı", "sarkık"], "content": "Vücut Sıcaklığı: 40.2 °C | Nabız: 92 atım/dk | Solunum: 34 nefes/dk | Tüm meme lobları yumuşak, gevşek ve ağrısız (Flaccid Udder). Süt pembe/kırmızı pıhtılı, kanlı ve sarımsı."},
            "OSKULTASYON": {"name": "Kalp, Akciğer & Göğüs Oskültasyonu", "keywords": ["kalp", "akciğer"], "content": "Kalp ve akciğer sesleri normal."},
            "AGRI_TESTLERI": {"name": "Retikulum, Perküsyon & Ağrı Testleri", "keywords": ["ağrı"], "content": "Meme palpasyonunda yangı veya ağrı yok (sarkık gevşek meme)."},
            "HEMOGRAM": {"name": "Tam Hemogram (CBC) Tahlili", "keywords": ["hemogram", "cbc", "kan", "anemi"], "content": "RBC: 4.8 x10^6/µL | Hb: 7.8 g/dL | PCV: %24 | MCV: 50.0 fL | MCH: 16.2 pg | MCHC: 32.5 g/dL | RDW: %17.5 | PLT: 180 x10^3/µL | WBC: 13.8 x10^3/µL | Çomak: %4 | Segmenter: %64 | Lenfosit: %26 | Monosit: %4 | Eozinofil: %2 | Bazofil: %0 | Fibrinojen: 6.4 g/L | PP/F: 12.8"},
            "BIYOKIMYA_PANELI": {"name": "Bütünsellikli Serum Biyokimyası & Enzim Paneli", "keywords": ["biyokimya", "ast", "ggt", "alt", "üre", "kreatinin", "bilirubin"], "content": "AST: 185 U/L | GGT: 48 U/L | ALT: 32 U/L | ALP: 92 U/L | CK: 160 U/L | LDH: 920 U/L | BUN: 32 mg/dL | Kreatinin: 1.8 mg/dL | Glikoz: 68 mg/dL | Total Bilirubin: 2.8 mg/dL | Total Protein: 7.4 g/dL | Albümin: 2.8 g/dL | Globülin: 4.6 g/dL | A/G: 0.61 | Na: 136 mEq/L | K: 4.0 mEq/L | Cl: 98 mEq/L | Ca: 8.8 mg/dL | P: 4.2 mg/dL | Mg: 2.0 mg/dL | Fe: 80 µg/dL | Cu: 98 µg/dL | Zn: 82 µg/dL | Se: 58 µg/L"},
            "KAN_GAZI": {"name": "Venöz / Arteriyel Kan Gazı Analizi", "keywords": ["kan gazı", "ph", "po2", "pco2"], "content": "pH: 7.36 | pO2: 38 mmHg | pCO2: 42 mmHg | HCO3-: 22 mEq/L | BE: -2.0 mEq/L | Laktat: 2.1 mmol/L"},
            "IDRAR_TAHLILI": {"name": "Tam İdrar Tahlili (Urinalysis)", "keywords": ["idrar", "urinalysis", "hemoglobinüri"], "content": "Dansite: 1.022 | pH: 7.2 | Protein: ++ | Glikoz: Negatif | Keton: Negatif | Bilirubin: ++ | Hemoglobin: Pozitif (Kırmızımsı İdrar) | Sediment: Lökosit ve spiroketler"},
            "GORUNTULEME_MIKROBIYOLOJI": {"name": "Görüntüleme, Mikrobiyoloji & Karanlık Saha", "keywords": ["mikroskop", "karanlık saha", "spiroket", "leptospira", "idrar"], "content": "İdrar ve Süt Karanlık Saha Mikroskopisi: Aktif hareketli, kanca uçlu spiroket yapısında Leptospira interrogans (serovar Hardjo) bakterileri tespit edildi."}
        },
        "egitmen_bilgisi": {
            "kesin_tani": "Leptospirosis / Süt Düşme Sendromu (Leptospira Hardjo / Pomona).",
            "patofizyoloji": "Leptospiralar mukoza ve zedelenmiş deriden girerek bakteriyemi yapar. Meme dokusunda vaskülit ve vasküler lezyonlarla sütte kanlaşma ve memede sarkıklık (flaccid udder) oluşturur. Gebelerde plasentayı geçerek abort yaptırır.",
            "ayirici_tani": "Klasik Mastitislerden memede sıcaklık, ağrı ve sertlik olmaması (flaccid udder) ve tüm lopların birden etkilenip kanlı süt vermesi ile ayrılır.",
            "tedavi_protokolu": "1. Spesifik Antibiyotik: Streptomisin / Dihidrostreptomisin (25 mg/kg İM tek doz veya 3 gün) veya Oksitetrasiklin (20 mg/kg LA).\n2. Destekleyici NSAİİ ve İV sıvı sağaltımı.",
            "koruma_biyogüvenlik": "ZOONOZDUR! İdrarla bulaşır. Çiftlikte fare ve kemirgen mücadelesi yapılmalı, durgun sular kurutulmalı ve kombine Leptospira aşıları uygulanmalıdır."
        }
    },
    "Vaka 12 (Kudret)": {
        "kod": "VAKA_12",
        "gorsel_adi": None,
        "sikayet": "Hocam, işletmedeki 4 yaşındaki ineğimiz aylardır yavaş yavaş eriyor, ne versek kilo almıyor. Boynundaki ve kasığındaki bezeri ceviz gibi büyüdü. Gözleri dışarı fırlayacak gibi duruyor, nefes darlığı çekiyor...",
        "categories": {
            "RASYON_YEM": {"name": "Rasyon & Yemleme Öyküsü", "keywords": ["rasyon", "yem"], "content": "İştah normal olmasına rağmen sürekli zayıflama (kaşeksi)."},
            "LOKASYON_RAKIM": {"name": "Lokasyon & Coğrafi Öykü", "keywords": ["lokasyon", "sürü"], "content": "Enzootik lökoz geçmişi olan ticari süt işletmesi."},
            "GECMIS_HASTALIK": {"name": "Geçmiş Hastalık & Sağlık Geçmişi", "keywords": ["geçmiş", "kan nakli"], "content": "Geçmişte ortak enjektör kullanımı ve boynuz kesme operasyonu var."},
            "ISTAH_DURUMU": {"name": "İştah & Yutma / Çiğneme Durumu", "keywords": ["iştah", "zayıflama"], "content": "İştah var ancak kronik kaşeksi ve zayıflama."},
            "VITAL_BULGULAR": {"name": "Genel Muayene & Vital Bulgular", "keywords": ["ateş", "sıcaklık", "nabız", "lenf", "göz", "ekzoftalmus", "zayıflama"], "content": "Vücut Sıcaklığı: 38.9 °C | Nabız: 88 atım/dk | Solunum: 36 nefes/dk | Bilateral ekzoftalmus (gözlerin dışarı fırlaması). Tüm yüzeysel lenf nodları (lnn. prescapularis, retrofaryngealis, subillaris) asimetrik, sert ve ağrısız olarak büyümüş."},
            "OSKULTASYON": {"name": "Kalp, Akciğer & Göğüs Oskültasyonu", "keywords": ["kalp", "akciğer"], "content": "Sağ kalp oskültasyonunda retrograd venöz dolgunluk, üfürüm (Miyokardiyal lenfosarkom şüphesi)."},
            "AGRI_TESTLERI": {"name": "Retikulum, Perküsyon & Ağrı Testleri", "keywords": ["ağrı"], "content": "Rektal muayenede lnn. iliaci ve uterus çevresinde dev neoplastik kitleler palpasyonu."},
            "HEMOGRAM": {"name": "Tam Hemogram (CBC) Tahlili", "keywords": ["hemogram", "cbc", "kan", "lenfosit", "lökositoz", "blv"], "content": "RBC: 5.2 x10^6/µL | Hb: 8.4 g/dL | PCV: %26 | MCV: 50.0 fL | MCH: 16.1 pg | MCHC: 32.3 g/dL | RDW: %18.2 | PLT: 210 x10^3/µL | WBC: 48.5 x10^3/µL (Masif Lökositoz) | Çomak: %1 | Segmenter: %14 | Lenfosit: %82 (Persistan Lenfositoz) | Monosit: %2 | Eozinofil: %1 | Bazofil: %0 | Fibrinojen: 4.2 g/L | PP/F: 15.2"},
            "BIYOKIMYA_PANELI": {"name": "Bütünsellikli Serum Biyokimyası & Enzim Paneli", "keywords": ["biyokimya", "ast", "ggt", "alt", "ldh", "protein", "globülin"], "content": "AST: 165 U/L | GGT: 30 U/L | ALT: 28 U/L | ALP: 88 U/L | CK: 130 U/L | LDH: 2100 U/L (Çok Yüksek) | BUN: 24 mg/dL | Kreatinin: 1.4 mg/dL | Glikoz: 62 mg/dL | Total Bilirubin: 0.5 mg/dL | Total Protein: 9.2 g/dL | Albümin: 2.4 g/dL | Globülin: 6.8 g/dL (Hyperglobulinemi) | A/G: 0.35 | Na: 139 mEq/L | K: 4.2 mEq/L | Cl: 99 mEq/L | Ca: 9.2 mg/dL | P: 5.0 mg/dL | Mg: 2.1 mg/dL | Fe: 75 µg/dL | Cu: 105 µg/dL | Zn: 80 µg/dL | Se: 62 µg/L"},
            "KAN_GAZI": {"name": "Venöz / Arteriyel Kan Gazı Analizi", "keywords": ["kan gazı", "ph", "po2", "pco2"], "content": "pH: 7.39 | pO2: 40 mmHg | pCO2: 41 mmHg | HCO3-: 24 mEq/L | BE: +0.2 mEq/L | Laktat: 1.8 mmol/L"},
            "IDRAR_TAHLILI": {"name": "Tam İdrar Tahlili (Urinalysis)", "keywords": ["idrar", "urinalysis"], "content": "Dansite: 1.024 | pH: 7.8 | Protein: + | Glikoz: Negatif | Keton: Negatif | Sediment: Temiz"},
            "GORUNTULEME_MIKROBIYOLOJI": {"name": "Görüntüleme, Mikrobiyoloji & ELISA", "keywords": ["elisa", "mikroskop", "froti", "lenfosit", "blv"], "content": "Serum ELISA ve Agar Jel İmmünodifüzyon (AGID): Bovine Leukemia Virus (BLV) antikorları Pozitif. Kan frotisinde pleomorfik, atipik neoplastik B-lenfositler."}
        },
        "egitmen_bilgisi": {
            "kesin_tani": "Bovine Enzootic Leukosis / Sığır Lökozu (BLV - Retrovirus).",
            "patofizyoloji": "Retrovirus B-lenfositleri enfekte eder. B hücrelerinin neoplastik proliferasyonu ile lenfoid dokularda, abomazumda, sağ atriumda ve orbita arkasında malignant lenfosarkom tümörleri oluşur.",
            "ayirici_tani": "Tüberküloz ve Paratüberküloz'dan persistan masif lenfositoz (>30.000 WBC/µL) ve BLV ELISA pozitifliği ile ayrılır.",
            "tedavi_protokolu": "TEDAVİSİ YOKTUR! Sürü içi bulaşmayı önlemek için enfekte hayvanlar belirlenip kesime gönderilmeli (ayrılmalıdır).",
            "koruma_biyogüvenlik": "İhbarı mecburidir! Bulaşma kan yoluyla (enjektörler, dövme, boynuz kesme, veteriner eldivenleri) olur. Tüm medikal aletler dezenfekte edilmelidir."
        }
    },
    "Vaka 13 (Yıldız)": {
        "kod": "VAKA_13",
        "gorsel_adi": None,
        "sikayet": "Hocam, su borusu donmuştu, sütten kestiğimiz buzağılar gün boyu susuz kaldı. Akşam suyu açınca kovaya saldırıp litrelerce içtiler. Aradan iki saat geçti, buzağılar sallanmaya başladı, gözleri kör gibi sağa sola çarpıp kasılmaya başladılar...",
        "categories": {
            "RASYON_YEM": {"name": "Rasyon & Yemleme Öyküsü", "keywords": ["rasyon", "yem", "su", "susuz"], "content": "Uzun süreli tam su kısıtlaması sonrası sınırsız soğuk su içilmesi."},
            "LOKASYON_RAKIM": {"name": "Lokasyon & Coğrafi Öykü", "keywords": ["lokasyon", "don", "kış"], "content": "Kış şartlarında su tesisatının donduğu buzağı bölmesi."},
            "GECMIS_HASTALIK": {"name": "Geçmiş Hastalık & Sağlık Geçmişi", "keywords": ["geçmiş"], "content": "Daha önce bilinen enfeksiyöz hastalığı yok."},
            "ISTAH_DURUMU": {"name": "İştah & Yutma / Çiğneme Durumu", "keywords": ["iştah", "su"], "content": "Aşırı polidipsi (su içme arzusu) sonrası gelişen nörolojik kriz."},
            "VITAL_BULGULAR": {"name": "Genel Muayene & Vital Bulgular", "keywords": ["ateş", "sıcaklık", "nabız", "nöroloji", "körlük", "ataksi", "nöbet"], "content": "Vücut Sıcaklığı: 38.2 °C (Hipotermik) | Nabız: 110 atım/dk | Solunum: 42 nefes/dk | Bilateral nistagmus, kortikal körlük, ataksi, opistotonus ve tonik-klonik kasılmalar."},
            "OSKULTASYON": {"name": "Kalp, Akciğer & Göğüs Oskültasyonu", "keywords": ["kalp", "akciğer"], "content": "Taşikardi, akciğerlerde hafif ödem sesleri."},
            "AGRI_TESTLERI": {"name": "Retikulum, Perküsyon & Ağrı Testleri", "keywords": ["ağrı"], "content": "Nörolojik hiperestezi ve re refleks artışı."},
            "HEMOGRAM": {"name": "Tam Hemogram (CBC) Tahlili", "keywords": ["hemogram", "cbc", "kan", "hemoliz"], "content": "RBC: 4.2 x10^6/µL | Hb: 7.2 g/dL | PCV: %20 (İntravasküler Hemoliz) | MCV: 47.6 fL | MCH: 17.1 pg | MCHC: 36.0 g/dL | RDW: %18.8 | PLT: 220 x10^3/µL | WBC: 9.2 x10^3/µL | Çomak: %2 | Segmenter: %55 | Lenfosit: %35 | Monosit: %5 | Eozinofil: %3 | Bazofil: %0 | Fibrinojen: 3.4 g/L | PP/F: 18.2"},
            "BIYOKIMYA_PANELI": {"name": "Bütünsellikli Serum Biyokimyası & Enzim Paneli", "keywords": ["biyokimya", "na", "sodyum", "hiponatremi", "ast", "ck", "üre", "kreatinin"], "content": "AST: 110 U/L | GGT: 22 U/L | ALT: 25 U/L | ALP: 65 U/L | CK: 420 U/L | LDH: 820 U/L | BUN: 18 mg/dL | Kreatinin: 1.1 mg/dL | Glikoz: 72 mg/dL | Total Bilirubin: 1.8 mg/dL | Total Protein: 5.2 g/dL | Albümin: 2.6 g/dL | Globülin: 2.6 g/dL | A/G: 1.00 | Serum Sodyumu (Na): 112 mEq/L (AĞIR HİPONATREMİ!) | K: 3.8 mEq/L | Cl: 78 mEq/L | Ca: 8.6 mg/dL | P: 4.8 mg/dL | Mg: 1.9 mg/dL | Fe: 90 µg/dL | Cu: 85 µg/dL | Zn: 80 µg/dL | Se: 60 µg/L"},
            "KAN_GAZI": {"name": "Venöz / Arteriyel Kan Gazı Analizi", "keywords": ["kan gazı", "ph", "po2", "pco2"], "content": "pH: 7.35 | pO2: 40 mmHg | pCO2: 38 mmHg | HCO3-: 21 mEq/L | BE: -2.8 mEq/L | Laktat: 2.4 mmol/L"},
            "IDRAR_TAHLILI": {"name": "Tam İdrar Tahlili (Urinalysis)", "keywords": ["idrar", "urinalysis", "hemoglobinüri"], "content": "Dansite: 1.004 (Aşırı Hipostenüri) | pH: 7.0 | Protein: + | Glikoz: Negatif | Keton: Negatif | Hemoglobin: Pozitif (Hipotonik Hemoliz) | Sediment: Berrak"},
            "GORUNTULEME_MIKROBIYOLOJI": {"name": "Görüntüleme, Mikrobiyoloji & Beyin Ödemi", "keywords": ["mikroskop", "kan", "froti", "hayalet", "ghost"], "content": "Kan Frotisi: Hipotonik sıvı girişine bağlı patlamış eritrosit zarları (Ghost Cells / Hayalet Hücreler). MRG/Ultrason: Serebral ödem."}
        },
        "egitmen_bilgisi": {
            "kesin_tani": "Su Zehirlenmesi / Akut Su İntoksikasyonu (Water Intoxication / Su Hiponatremi Kriz).",
            "patofizyoloji": "Uzun susuzluk sonrası hızla alınan fazla miktardaki su, plazma ozmolalitesini aniden düşürür. Hipotonik hale gelen plazma eritrositlerin patlamasına (intravasküler hemoliz) ve suyun ozmozla beyin hücrelerine çekilerek SEREBRAL ÖDEM oluşturmasına yol açar.",
            "ayirici_tani": "Polioensefalomalazi (CCN) ve Kuduz'dan susuzluk öyküsü, ağır hiponatremi (Na <120 mEq/L) ve hemoglobinüri ile ayrılır.",
            "tedavi_protokolu": "1. SU DERHAL KISITLANIR!\n2. Serebral ödemi çözmek için Hipertonik NaCl (%3-5'lik Nöro-Solüsyon) veya Mannitol (%20'lik 1-2 g/kg İV).\n3. Deksametazon (Serebral ödem için) ve Furosemid.",
            "koruma_biyogüvenlik": "Susuz kalan hayvanlara su birden verilmemeli; ilk saatlerde azar azar (her 30 dakikada 1-2 Litre) ılık su verilmelidir."
        }
    },
    "Vaka 14 (Sürmeli)": {
        "kod": "VAKA_14",
        "gorsel_adi": None,
        "sikayet": "Hocam, koyunlara domuz besi yemi vermişler yanlışlıkla. İki gün sonra koyunlardan üç tanesi aniden yere serildi, gözlerinin akı sap sarı oldu. İdrarları simsiyah katran gibi çıkıyor, nefes alamıyorlar...",
        "categories": {
            "RASYON_YEM": {"name": "Rasyon & Yemleme Öyküsü", "keywords": ["rasyon", "yem", "bakır", "yem hatası"], "content": "Koyunlara yüksek miktarda bakır içeren sığır/domuz besi yemi veya tavuk gübresi bulaşıklı yem verilmiştir."},
            "LOKASYON_RAKIM": {"name": "Lokasyon & Coğrafi Öykü", "keywords": ["lokasyon", "otlatma"], "content": "Bakır sülfatlı meyve bahçesi altında otlatma öyküsü."},
            "GECMIS_HASTALIK": {"name": "Geçmiş Hastalık & Sağlık Geçmişi", "keywords": ["geçmiş", "stres"], "content": "Dün koyunların kırkılması ve nakliye stresi yaşanmış."},
            "ISTAH_DURUMU": {"name": "İştah & Yutma / Çiğneme Durumu", "keywords": ["iştah", "anoreksi"], "content": "Tam anoreksi, yatış ve inleme."},
            "VITAL_BULGULAR": {"name": "Genel Muayene & Vital Bulgular", "keywords": ["ateş", "sıcaklık", "nabız", "idrar", "siyah", "sarılık", "ikter"], "content": "Vücut Sıcaklığı: 40.8 °C | Nabız: 130 atım/dk | Solunum: 55 nefes/dk | Mukozalar safran sarısı şiddetli ikterik. İdrar simsiyah / katran renginde (Gunmetal Black Hemoglobinuria)."},
            "OSKULTASYON": {"name": "Kalp, Akciğer & Göğüs Oskültasyonu", "keywords": ["kalp", "akciğer"], "content": "Şiddetli taşikardi, kardiyak kolaps belirtileri."},
            "AGRI_TESTLERI": {"name": "Retikulum, Perküsyon & Ağrı Testleri", "keywords": ["ağrı"], "content": "Karaciğer bölgesinde sağ kaburga arkasında palpasyonda ağrı duyarlılığı."},
            "HEMOGRAM": {"name": "Tam Hemogram (CBC) Tahlili", "keywords": ["hemogram", "cbc", "kan", "hemoliz", "mcv"], "content": "RBC: 1.8 x10^6/µL | Hb: 3.5 g/dL | PCV: %10 | MCV: 55.5 fL | MCH: 19.4 pg | MCHC: 35.0 g/dL | RDW: %24.0 | PLT: 95 x10^3/µL | WBC: 18.2 x10^3/µL | Çomak: %8 | Segmenter: %68 | Lenfosit: %18 | Monosit: %4 | Eozinofil: %2 | Bazofil: %0 | Fibrinojen: 7.2 g/L | PP/F: 8.8"},
            "BIYOKIMYA_PANELI": {"name": "Bütünsellikli Serum Biyokimyası & Enzim Paneli", "keywords": ["biyokimya", "bakır", "cu", "ast", "ggt", "alt", "üre", "kreatinin", "bilirubin"], "content": "AST: 680 U/L (Masif Karaciğer Hasarı) | GGT: 120 U/L | ALT: 85 U/L | ALP: 240 U/L | CK: 310 U/L | LDH: 2800 U/L | BUN: 58 mg/dL | Kreatinin: 3.8 mg/dL (Hemoglobinürik Nefroz) | Glikoz: 88 mg/dL | Total Bilirubin: 12.4 mg/dL | İndirekt Bilirubin: 9.8 mg/dL | Total Protein: 5.4 g/dL | Albümin: 2.0 g/dL | Globülin: 3.4 g/dL | Serum Bakırı (Cu): 420 µg/dL (Çok Yüksek!) | Na: 130 mEq/L | K: 5.4 mEq/L | Cl: 90 mEq/L | Ca: 7.8 mg/dL | P: 6.2 mg/dL | Mg: 1.8 mg/dL | Fe: 210 µg/dL | Zn: 55 µg/dL | Se: 45 µg/L"},
            "KAN_GAZI": {"name": "Venöz / Arteriyel Kan Gazı Analizi", "keywords": ["kan gazı", "ph", "po2", "pco2"], "content": "pH: 7.18 | pO2: 26 mmHg | pCO2: 48 mmHg | HCO3-: 14 mEq/L | BE: -11.2 mEq/L | Laktat: 7.2 mmol/L (Ağır Laktik Asidoz + Doku Anoksisi)"},
            "IDRAR_TAHLILI": {"name": "Tam İdrar Tahlili (Urinalysis)", "keywords": ["idrar", "urinalysis", "günmetal", "siyah"], "content": "Dansite: 1.018 | pH: 6.8 | Protein: ++++ | Glikoz: Negatif | Keton: Negatif | Bilirubin: ++++ | Hemoglobin: ++++ Simsiyah/Katran İdrar | Sediment: Hemoglobin silindirleri"},
            "GORUNTULEME_MIKROBIYOLOJI": {"name": "Görüntüleme, Mikrobiyoloji & Karaciğer Biyopsisi", "keywords": ["mikroskop", "biyopsi", "bakır", "rhodanine"], "content": "Karaciğer Biyopsisi Histopatolojisi (Rhodanine Boyası): Hepatositlerde ve Kupffer hücrelerinde altın sarısı/kahverengi yoğun bakır birikim granülleri."}
        },
        "egitmen_bilgisi": {
            "kesin_tani": "Koyunlarda Kronik Bakır Zehirlenmesi (Bakır Hemolitik Krizi).",
            "patofizyoloji": "Karaciğerde aylarca biriken bakır, nakliye/kırkım stresiyle aniden kana salınır. Dolaşımdaki bakır eritrosit membranlarında lipid peroksidasyonuna ve Heinz cisimciği oluşumuna yol açarak Masif İntravasküler Hemoliz ve Katran İdrar (Gunmetal Kidney) oluşturur.",
            "ayirici_tani": "Babesiosis ve Kronik Gebelik Toksemisi'nden serum bakırının >300 µg/dL olması, böbreklerin metalik siyah renk alması ve Rhodanine boyama ile ayrılır.",
            "tedavi_protokolu": "1. Şelatör Madde: D-Penisilamin (26 mg/kg/gün Oral) veya Amonyum Molibdat (100 mg) + Sodyum Tiyosülfat (1 g) günlük oral drenç.\n2. Kan Transfüzyonu (Ağır anemide).\n3. Sodyum Bikarbonat İV infüzyonu (Böbrekleri hemoglobin çökmesinden korumak için).",
            "koruma_biyogüvenlik": "Koyunlara asla sığır/domuz yemi verilmemeli, rasyondaki Cu:Mo oranı 10:1 seviyesinde tutulmalıdır."
        }
    },
    "Vaka 15 (Kartal)": {
        "kod": "VAKA_15",
        "gorsel_adi": None,
        "sikayet": "Hocam, tayımız dün sapasağlam doğdu, anasını güzelce emdi. Bugün sabah bir baktık tay sapsarı olmuş, ayakta duramıyor, tir tir titriyor. İdrarı şarap gibi kırmızı renkte çıkıyor...",
        "categories": {
            "RASYON_YEM": {"name": "Rasyon & Yemleme Öyküsü", "keywords": ["rasyon", "yem", "kolostrum", "süt"], "content": "Doğum sonrası ilk 12 saatte ananın kolostrumunu tam ve bol miktarda emmiştir."},
            "LOKASYON_RAKIM": {"name": "Lokasyon & Coğrafi Öykü", "keywords": ["lokasyon", "hara"], "content": "At harası yetiştiriciliği."},
            "GECMIS_HASTALIK": {"name": "Geçmiş Hastalık & Sağlık Geçmişi", "keywords": ["geçmiş", "gebelik", "kısrak"], "content": "Kısrağın 4. doğumu. Daha önceki tayında da doğum sonrası sarılık gelişme öyküsü var."},
            "ISTAH_DURUMU": {"name": "İştah & Yutma / Çiğneme Durumu", "keywords": ["iştah", "emme"], "content": "Tay emmeyi bırakmış, yatmakta ve solumaktadır."},
            "VITAL_BULGULAR": {"name": "Genel Muayene & Vital Bulgular", "keywords": ["ateş", "sıcaklık", "nabız", "sarılık", "ikter", "idrar", "kırmızı", "tay"], "content": "Vücut Sıcaklığı: 38.8 °C | Nabız: 140 atım/dk | Solunum: 65 nefes/dk | Mukozalar şiddetli ikterik ve soluk. İdrar koyu kırmızı/şarap renginde. Tay ayakta duramıyor."},
            "OSKULTASYON": {"name": "Kalp, Akciğer & Göğüs Oskültasyonu", "keywords": ["kalp", "akciğer"], "content": "Sert takipne, kardiyak taşikardi ve sistolik üfürüm."},
            "AGRI_TESTLERI": {"name": "Retikulum, Perküsyon & Ağrı Testleri", "keywords": ["ağrı"], "content": "Klinik muayenede travma veya omurga hasarı yok."},
            "HEMOGRAM": {"name": "Tam Hemogram (CBC) Tahlili", "keywords": ["hemogram", "cbc", "kan", "anemi", "mcv", "rbc"], "content": "RBC: 2.0 x10^6/µL | Hb: 4.1 g/dL | PCV: %11 | MCV: 55.0 fL | MCH: 20.5 pg | MCHC: 37.2 g/dL | RDW: %22.0 | PLT: 150 x10^3/µL | WBC: 12.8 x10^3/µL | Çomak: %3 | Segmenter: %65 | Lenfosit: %28 | Monosit: %3 | Eozinofil: %1 | Bazofil: %0 | Fibrinojen: 4.5 g/L | PP/F: 12.2"},
            "BIYOKIMYA_PANELI": {"name": "Bütünsellikli Serum Biyokimyası & Enzim Paneli", "keywords": ["biyokimya", "ast", "ggt", "alt", "bilirubin"], "content": "AST: 210 U/L | GGT: 28 U/L | ALT: 30 U/L | ALP: 180 U/L | CK: 240 U/L | LDH: 1650 U/L | BUN: 26 mg/dL | Kreatinin: 1.5 mg/dL | Glikoz: 65 mg/dL | Total Bilirubin: 8.6 mg/dL | İndirekt Bilirubin: 7.2 mg/dL | Total Protein: 5.6 g/dL | Albümin: 2.6 g/dL | Globülin: 3.0 g/dL | A/G: 0.87 | Na: 136 mEq/L | K: 4.1 mEq/L | Cl: 98 mEq/L | Ca: 8.6 mg/dL | P: 4.0 mg/dL | Mg: 1.9 mg/dL | Fe: 175 µg/dL | Cu: 90 µg/dL | Zn: 82 µg/dL | Se: 55 µg/L"},
            "KAN_GAZI": {"name": "Venöz / Arteriyel Kan Gazı Analizi", "keywords": ["kan gazı", "ph", "po2", "pco2"], "content": "pH: 7.29 | pO2: 29 mmHg | pCO2: 43 mmHg | HCO3-: 17 mEq/L | BE: -6.2 mEq/L | Laktat: 5.1 mmol/L"},
            "IDRAR_TAHLILI": {"name": "Tam İdrar Tahlili (Urinalysis)", "keywords": ["idrar", "urinalysis", "hemoglobinüri"], "content": "Dansite: 1.020 | pH: 7.0 | Protein: +++ | Glikoz: Negatif | Keton: Negatif | Bilirubin: +++ | Hemoglobin: ++++ Koyu Kırmızı | Sediment: Berrak"},
            "GORUNTULEME_MIKROBIYOLOJI": {"name": "Görüntüleme, Mikrobiyoloji & Doğrulama", "keywords": ["aglütinasyon", "mikroskop", "kan", "maternal", "kolostrum"], "content": "Aglütinasyon Testi: Tayın washed eritrositleri ile kısrağın serumu/kolostrumu karıştırıldığında lam üstünde 30 saniyede Pozitif Makroskopik Aglütinasyon tespiti."}
        },
        "egitmen_bilgisi": {
            "kesin_tani": "Taylarda Neonatal İzoeritrolizis / Yenidoğan İzoeritrolizisi (NI - Hemolytic Disease of Newborn).",
            "patofizyoloji": "Kısrak tayın eritrosit antijenlerine (Aa / Qa antijenleri) karşı antikor geliştirir. Tay doğduğunda kolostrum emerek bu alloantikorları alır. Antikorlar tayın eritrositlerine bağlanarak şiddetli İntravasküler ve Ekstravasküler Hemoliz oluşturur.",
            "ayirici_tani": "Yenidoğan Sepsisinden ateş olmaması, semptomların emme sonrası 12-24. saatte başlaması ve maternal kolostrum ile direkt aglütinasyon pozitifliği ile ayrılır.",
            "tedavi_protokolu": "1. TAY ANASINI EMMEYİ DERHAL KESMELİDİR! (İlk 36-48 saat emzirilmez, başka kısrak sütü verilir).\n2. Ağır anemide Washed Maternal Erythrocytes (Yıkanmış Kısrak Eritrositi) veya Uygun Donör Kısraktan Kan Transfüzyonu.\n3. İV Sıvı desteği ve Deksametazon.",
            "koruma_biyogüvenlik": "Gebe kısrakların serumunda doğuma 1-2 hafta kala Alloantikor Taraması yapılmalı; riski kısrakların taylarına doğumda ağızlık takılarak ilk 48 saat kolostrum emmesi engellenmelidir."
        }
    }
}

# UI Layout for Case Selection
st.markdown("<div class='vaka-box'>", unsafe_allow_html=True)
selected_case_name = st.selectbox(
    "🔍 İncelemek İstediğiniz Vakayı Seçiniz (Öğrenci Görünümü - Hastalık İsimleri Gizlidir):",
    options=list(CASES.keys()),
    index=0
)
st.markdown("</div>", unsafe_allow_html=True)

active_case = CASES[selected_case_name]

# Session State Setup
if "history" not in st.session_state:
    st.session_state.history = {}

if selected_case_name not in st.session_state.history:
    st.session_state.history[selected_case_name] = []

# Display Student Anamnesis Card (Farmer Storytelling)
st.markdown(f"<div class='vaka-header'>📋 {selected_case_name} — Yetiştirici İlk Başvuru Şikayeti & Anamnez</div>", unsafe_allow_html=True)
st.info(f"**🗣️ Yetiştiricinin İfadesi:** '{active_case['sikayet']}'")

# Automatic Macroscopic Clinical Image Display (if exists)
if "gorsel_adi" in active_case and active_case["gorsel_adi"]:
    img_path = find_gorsel_2(active_case["gorsel_adi"])
    if img_path:
        st.markdown("### 📸 Hasta Klinik Makroskopik Görseli")
        st.image(img_path, caption=f"Klinik Lezyon Görseli: {active_case['gorsel_adi']}", use_column_width=True)

# Question Input Section
st.markdown("---")
st.markdown("### 💬 Sorunuzu veya İncelemek İstediğiniz Muayene / Tahlil Adını Yazınız:")

def match_query(user_text, categories_dict):
    text_clean = user_text.lower().strip()
    text_clean = text_clean.replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("ö", "o").replace("ç", "c")
    
    # Check for specific microscopy / froti / biopsy terms first
    micro_keywords = ["mikroskop", "froti", "frotis", "lam", "biyopsi", "pcr", "kültür", "gram", "giemsa", "karanlık saha", "spirakulum", "şizont", "koch", "spiroket", "aglütinasyon"]
    if any(mkw in text_clean for mkw in micro_keywords):
        if "GORUNTULEME_MIKROBIYOLOJI" in categories_dict:
            return ["GORUNTULEME_MIKROBIYOLOJI"]
            
    matched_cats = []
    for cat_key, cat_info in categories_dict.items():
        for kw in cat_info["keywords"]:
            kw_clean = kw.lower().replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("ö", "o").replace("ç", "c")
            if re.search(r'\b' + re.escape(kw_clean), text_clean) or kw_clean in text_clean:
                matched_cats.append(cat_key)
                break
    return matched_cats

col_input, col_button = st.columns([4, 1])

with col_input:
    user_query = st.text_input(
        "Klinik Sorunuzu Buraya Yazınız:",
        key=f"query_input_{active_case['kod']}",
        placeholder="Örn: Vital bulguları nedir?, Hemogram verisi verin, Biyokimya sonuçları?, İdrar tahlili, Kan frotisi bak..."
    )

with col_button:
    st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
    submit_btn = st.button("🔎 Sor ve Sorgula", type="primary", use_container_width=True)

if submit_btn and user_query:
    matches = match_query(user_query, active_case["categories"])
    if matches:
        new_disc = 0
        for cat_key in matches:
            cat_data = active_case["categories"][cat_key]
            already_in = any(item["cat_key"] == cat_key for item in st.session_state.history[selected_case_name])
            if not already_in:
                item_dict = {
                    "cat_key": cat_key,
                    "query": user_query,
                    "title": cat_data["name"],
                    "content": cat_data["content"]
                }
                if "gorsel_adi" in cat_data and cat_data["gorsel_adi"]:
                    item_dict["gorsel_adi"] = cat_data["gorsel_adi"]
                st.session_state.history[selected_case_name].append(item_dict)
                new_disc += 1
        if new_disc > 0:
            st.success(f"🎉 {new_disc} yeni klinik bulgu / tahlil verisi açığa çıkarıldı!")
    else:
        st.warning("⚠️ Eşleşen klinik bilgi bulunamadı. Lütfen sorunuzu farklı kelimelerle ifade ediniz.")

# Display Discovered Information
st.markdown("---")
st.markdown(f"### 📂 Keşfedilen Klinik İpuçları ve Tahlil Bulguları ({len(st.session_state.history[selected_case_name])} Bilgi Açıldı)")

if st.session_state.history[selected_case_name]:
    for item in reversed(st.session_state.history[selected_case_name]):
        st.markdown(f"""
            <div class='card-found'>
                <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;'>
                    <span class='badge-category'>{item['title']}</span>
                    <span style='font-size:12px; color:#7F7F7F;'>Sorulan Soru: "{item['query']}"</span>
                </div>
                <div class='card-content'><b>🩺 Bulgu / Tahlil Sonucu:</b> {item['content']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Display image in card if available
        if "gorsel_adi" in item and item["gorsel_adi"]:
            m_img_path = find_gorsel_2(item["gorsel_adi"])
            if m_img_path:
                st.markdown(f"#### 🔬 {item['gorsel_adi']} — Mikroskopik / Froti Görseli")
                st.image(m_img_path, caption=f"Mikroskopik İnceleme: {item['gorsel_adi']}", use_column_width=True)

    if st.button("🗑️ Bu Vakanın Sorgu Geçmişini Temizle"):
        st.session_state.history[selected_case_name] = []
        st.rerun()

# Teacher Portal in Sidebar
with st.sidebar:
    st.markdown("### 🏛️ ÇU Ceyhan Veteriner Fakültesi")
    st.markdown("**VET401 İç Hastalıkları I**")
    st.markdown("---")
    st.markdown("### 🔒 Eğitmen Portalı")
    teacher_login = st.checkbox("Eğitmen Anahtar Paneli")
    if teacher_login:
        pass_code = st.text_input("Giriş Şifresi:", type="password")
        if pass_code == "vet401":
            st.success("Eğitmen Erişimi Onaylandı!")
            eb = active_case["egitmen_bilgisi"]
            st.markdown(f"### 🔑 {selected_case_name} — Gizli Eğitmen Kartı")
            st.markdown(f"**🎯 Kesin Tanı:** {eb['kesin_tani']}")
            st.markdown(f"**🔬 Patofizyoloji:** {eb['patofizyoloji']}")
            st.markdown(f"**⚖️ Ayırıcı Tanı:** {eb['ayirici_tani']}")
            st.markdown(f"**💊 Tedavi Protokolü:**\n{eb['tedavi_protokolu']}")
            st.markdown(f"**🛡️ Koruma & Biyogüvenlik:**\n{eb['koruma_biyogüvenlik']}")
            st.markdown("---")
            st.markdown("#### 📜 Bu Vakanın Tüm Gizli Verileri:")
            for ck, cv in active_case["categories"].items():
                st.markdown(f"**• {cv['name']}:** {cv['content']}")
        elif pass_code:
            st.error("Hatalı Şifre!")
