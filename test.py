import requests
from bs4 import BeautifulSoup
import pandas as pd


url = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
all_country = soup.find_all("table", class_="wikitable")

# memilih table dari page country list yang sesuai jadi di dalam class wikitable ada beberapa table dan yang kami inginkan ini adalah table country populasi 
tb = all_country[0]
# mengambil tr dri tabel
tr = tb.find_all("tr")
# mengambil setiap th dalam bentuk text dan menghilangkan kolom kosong dengan strip()
hd = [header.text.strip() for header in tr[0].find_all("th")]

countries_data = []
for tro in tr[1:]:
    cols = tro.find_all("td")
   
    country_info = [col.text.strip() for col in cols]
    countries_data.append(country_info)

# Membuat DataFrame dengan kolom headers
df = pd.DataFrame(countries_data, columns=hd)


# print(df)
df.to_excel("country1.xlsx")