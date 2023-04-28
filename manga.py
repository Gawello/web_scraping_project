import requests
import os
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Funkcja pobierająca plik obrazu ze strony
def download_image(url, directory, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(os.path.join(directory, filename), 'wb') as f:
            for chunk in response:
                f.write(chunk)

# Funkcja pobierająca stronę komiksu i zapisująca pliki obrazów
def download_chapter():
    url = url_input.get()
    save_dir = filedialog.askdirectory()
    format_type = format_input.get()

    # Konfiguracja opcji przeglądarki
    options = Options()
    options.add_argument('--headless')  # Tryb bez okna przeglądarki
    options.add_argument('--disable-gpu')  # Wyłączenie akceleracji GPU
    options.add_argument('--no-sandbox')  # Wyłączenie izolacji procesów

    # Uruchomienie przeglądarki i pobranie strony
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Pobierz wszystkie obrazy z tagiem img
    img_tags = driver.find_elements_by_tag_name('img')

    for i, img in enumerate(img_tags):
        # Pobierz link do obrazu
        img_url = img.get_attribute('src')

        # Stwórz nazwę pliku
        filename = f"{i+1:03d}.{format_type}"

        # Pobierz obraz i zapisz go w podanym katalogu
        download_image(img_url, save_dir, filename)

    # Zamknij przeglądarkę
    driver.quit()

    # Wyświetl komunikat o zakończeniu pobierania
    messagebox.showinfo(title="Pobieranie zakończone", message="Pobieranie zakończone pomyślnie.")

# Stwórz okno Tkinter
root = Tk()
root.title("Pobieranie komiksu")

# Dodaj pola do wprowadzania danych
url_label = Label(root, text="Link do strony:")
url_label.pack()
url_input = Entry(root)
url_input.pack()

format_label = Label(root, text="Format pliku:")
format_label.pack()
format_input = Entry(root)
format_input.pack()

# Dodaj przycisk do rozpoczęcia pobierania
download_button = Button(root, text="Pobierz", command=download_chapter)
download_button.pack()

root.mainloop()
