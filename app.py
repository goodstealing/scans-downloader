import tkinter as tk
import requests
from bs4 import BeautifulSoup
import os
from tkinter import filedialog
import random

image_paths = [
    "assets/hi.png",
    "assets/hatsune.png",
    "assets/kawiiMiku.png",
    "assets/onionMiku.png",
    "assets/hmm.png",
    "assets/hamm.png",
    "assets/airplane.png",
    "assets/01.png",
    "assets/02.png",
    "assets/03.png",
    "assets/03.png",
    "assets/04.png",
    "assets/05.png",
    "assets/06.png",
    # Add paths or remove paths to other images as needed
]
random_image_path = random.choice(image_paths)


def scrape_and_download():
    url = url_entry.get()
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "lxml")

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

    output_folder = filedialog.askdirectory(title="Select Output Folder")
    if output_folder:
        output_folder = os.path.join(output_folder, full_name)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for idx, url in enumerate(src_texts):
            response = requests.get(url)
            if response.status_code == 200:
                filename = os.path.join(output_folder, f"{idx}.jpg")
                with open(filename, "wb") as file:
                    file.write(response.content)
                status_label.config(text=f"Saved image - {idx} total")
            else:
                status_label.config(text=f"Error downloading image {url}")


app = tk.Tk()
app.title("Scans Downloader")
app.geometry('500x500')

icon_path = 'assets/icon.ico'
if os.path.exists(icon_path):
    app.iconbitmap(icon_path)

background_image = tk.PhotoImage(file=random_image_path)
background_label = tk.Label(app, image=background_image)
background_label.place(relwidth=1, relheight=1)

url_label = tk.Label(app, text="Enter URL:", font="Arial")
url_label.pack()

url_entry = tk.Entry(app, width=50, font="Arial")
url_entry.pack()

scrape_button = tk.Button(app, text="Scrape and Download", command=scrape_and_download, font="Arial")
scrape_button.pack()

status_label = tk.Label(app, text="", fg="red", font="Arial")
status_label.pack()

app.mainloop()
