import pandas
import numpy
import streamlit
from datetime import datetime


def imsakiye(sehir):
    tables = pandas.read_html(f'https://www.haberturk.com/ramazan/imsakiye/{sehir}',flavor='bs4')[0]  # Pandas ile sitede bulunan 1. tabloyu çekelim
    tables = tables.iloc[0:-1]  # En alt satırda olan gereksiz satırı tablodan çıkaralım
    tables = tables.drop(26, axis=0)  # 26. satırda olan gereksiz satırı tablodan çıkaralım
    T = tables['Tarih'].str.split("-", expand=True)
    tables['TARİH'] = T[0] + "/" + T[1] + "/" + T[2]
    tables['TARİH'] = pandas.to_datetime(tables['TARİH'])
    tables.drop("Tarih", axis=1, inplace=True)

    return tables


def TimeLeftForIftar(sehir):
    df = imsakiye(sehir)
    today = datetime.today().date().strftime("%Y/%m/%d")
    currentTime = datetime.now().time().strftime("%H:%M")
    iftarVakti = df[df['TARİH'] == today]['AKŞAM'].values[0]
    remainingTime = pandas.Timedelta(pandas.to_datetime(iftarVakti) - pandas.to_datetime(currentTime))

    return remainingTime


def Today(sehir):
    df = imsakiye(sehir)
    today = datetime.today().date().strftime("%Y/%m/%d")
    iftarVakti = df[df['TARİH'] == today]

    return iftarVakti

streamlit.header("Hoşgeldin Ramazan 2025")

Citys = ["Adana", "Adıyaman", "Afyon", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın",
        "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı",
        "Çorum", "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir",
        "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Isparta", "Mersin", "İstanbul",
        "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya",
        "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir",
        "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat",
        "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt",
        "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük",
        "Kilis", "Osmaniye", "Düzce"]

pickCity = streamlit.sidebar.selectbox("Şehirler",Citys)

pickCity = pickCity.replace("İ","i")
pickCity = pickCity.lower()
pickCity = pickCity.replace("ı","i")
pickCity = pickCity.replace("ç","c")
pickCity = pickCity.replace("ü","u")
pickCity = pickCity.replace("ğ","g")
pickCity = pickCity.replace("ö","o")
pickCity = pickCity.replace("ş","s")

streamlit.subheader("İftara Kalan Süre")
S = TimeLeftForIftar(pickCity)
streamlit.markdown(f'<h1 style="color:green;">{S}</h1>', unsafe_allow_html=True)

streamlit.subheader("Bugün")
streamlit.table(Today(pickCity))

streamlit.subheader("İmsakiye")
streamlit.table(imsakiye(pickCity))
