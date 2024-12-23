import requests
from bs4 import BeautifulSoup
import pandas as pd

# Karena Web menggunnakan limit untuk menampilkan datanya maka harus kita set agar data nya sampai 500
def scrape_manga_data(limit):
    url = f"https://myanimelist.net/topmanga.php?limit={limit}"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    all_manga = soup.find_all("table", class_="top-ranking-table")

    # [0]= maksudnya mengambil table dengan indeks 0 atau tabel pertama dalam page, ini untuk memastikan bahwa tidak salah table
    tb = all_manga[0]
    # ini untuk mencari tabel row dalam tabel
    tr = tb.find_all("tr")
    
    
    manga_data = []
    for tro in tr[1:]:
        cols = tro.find_all("td")
         # Len digunakan untuk menghitung Jumlah elemen pada objek, ini digunakan untuk mengecek bahwa kolom di tabel memiliki isi(lebih dari 1 kolom) agar tidak missing value
        if len(cols) > 1:  
            # Rank berada di index kolom 0 atau baris paling pertama
            rank = cols[0].text.strip()
            # Detail ada di kolom ke 2 di split \n untuk memisahkan per kalimatnya karna title year dan member didalam 1 div yang sama yang di pisahkan <br> doang
            details = cols[1].text.strip().split("\n")
            title = details[0]
            members = details[-1].strip()
            type_of_manga = details[2].strip().split(" ")[0]
            score = cols[2].text.strip()
            
            
            
            # Ambil tahun rilis dari details
            description = " ".join(details[1:-1]).strip()
            year = None
            if "-" in description:
                year_parts = description.split("-")
                if len(year_parts) > 0:
                    year = year_parts[0].strip()[-4:]  # Ambil 4 karakter terakhir dari tahun awal

            manga_data.append([rank, title,type_of_manga, score, year, members])
    return manga_data
    


# Menggabungkan data dari beberapa halamans
all_manga_data = []
    # Mengambil data dari limit 0 hingga 450 (500 data)
for limit in range(0, 500, 50): 
    all_manga_data.extend(scrape_manga_data(limit))

# Header untuk DataFrame
hd = ["Rank", "Title","Type", "Score", "Year_release", "Members"]


df = pd.DataFrame(all_manga_data, columns=hd)
df.to_excel("top_500_manga  .xlsx", index=False)
print("Data berhasil disimpan ke 'top_500_manga.xlsx'")
