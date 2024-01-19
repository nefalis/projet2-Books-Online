import requests
from bs4 import BeautifulSoup
import urllib.request
import csv
import os

# Récupération de la page d'acceuil. page number permet d'initialisé la page actuelle a 1.
base_url = "https://books.toscrape.com"
page_number = 1
next_page_url = base_url

page = requests.get(base_url)
soup = BeautifulSoup(page.content, 'lxml')

# Trouver le menu de navigation contenant les catégories
nav_menu = soup.find('div', class_='side_categories')

# Trouver toutes les catégories
categories = nav_menu.find_all('a')

print(categories)
# Afficher les catégories
#  la méthode .strip() est utilisée pour supprimer les espaces et les sauts de ligne éventuels autour du texte
for category in categories:
    print(category.text.strip())
