# librairies utilisées
import requests
from bs4 import BeautifulSoup

import csv

# On récupère les infos de la page url visé
url = "http://books.toscrape.com/catalogue/charlie-and-the-chocolate-factory-charlie-bucket-1_13/index.html"
page = requests.get(url)
# Récupère les données à partir de HTML
soup = BeautifulSoup(page.content, 'html.parser')

# On récupère le contenu html

product_page_url = url
title = soup.find('h1')
product_description = soup.find("div", {"id": "product_description"})
#review_rating = soup.find(class_="star-rating").find('p')
review_rating = soup.find(class_="star-rating").find_all("p")
image_url = soup.find(class_="item active").find('img')
category = soup.find("ul", {"class": "breadcrumb"}).find_all("a")[2]

# On recherche tout les elements td de la page
list_table = soup.find_all('td')
#list_p = soup.find_all('p')

# On recherche de l'element précis contenu uniquement dans les td
universal_product_code = list_table[0]
price_including_tax = list_table[2]
price_excluding_tax = list_table[3]
number_available = list_table[5]

# visualisation des données
"""

print("upc", universal_product_code)
print("titre", title)
print("prixinclu", price_including_tax)
print("prixexclu", price_excluding_tax)
print("nombre restant", number_available)
print("image", image_url)
print("page produit", product_page_url)
print("liste_table", list_table)
print("categorie", category)
"""
print("etoile", review_rating)
print("description", product_description)

#print("liste des p", list_p)

# Création fichier CSV

def charger(datas):
    # Création de l'en-tête pour le fichier CSV
    en_tete = ["product_page_url",
               "universal_ product_code",
               "title",
               "price_including_tax",
               "price_excluding_tax",
               "number_available",
               "product_description",
               "category",
               "review_rating",
               "image_url"]

    # Création d'un fichier pour écrire dans le fichier livre_data.csv
    with open('livre_data.csv', 'w') as fichier_csv:
        # Création objet writer (écriture) avec ce fichier
        writer = csv.writer(fichier_csv, delimiter=',')
        # Pour écrire la 1ere ligne
        writer.writerow(en_tete)
        # Permet de parcourir les élements
        for data in datas:
            writer.writerow(data)
