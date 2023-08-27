import os
import requests
from bs4 import BeautifulSoup

# hello
username = os.getlogin()
print(f"Hello {username} ༼ つ ◕_◕ ༽つ")
url = input("Pls insert link:")


response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, "lxml")

# status
if response.status_code == 200:
    print("Страница успешно обработана")
else:
    print("Ошибка при получении страницы. Код состояния:", response.status_code)

# gets title of the chapter
title = soup.title.string
chapter_num = title.split(" - ")[-1]
a = title.split('Read Manga')[1]
title_name = a.split(" - ")
chapter_name = title_name[0].split(",")[0][0:]

full_name = f"{chapter_num}{chapter_name}"

# scrape the page looking for data-src
unsort_pages = soup.find_all("div", class_="page-break no-gaps")
src_texts = [soup.find('img')['data-src'] for soup in unsort_pages]

# downloader
output_folder = f"uploads/{full_name}"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for idx, url in enumerate(src_texts):
    response = requests.get(url)
    if response.status_code == 200:
        filename = os.path.join(output_folder, f"{idx}.jpg")
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"Сохранено изображение {filename}")
    else:
        print(f"Ошибка при загрузке изображения {url}")
