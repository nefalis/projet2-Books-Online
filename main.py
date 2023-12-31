# librairies utilisées
import requests
from bs4 import BeautifulSoup

import csv



#Récupère les infos de la page url visé
url = "http://books.toscrape.com/catalogue/charlie-and-the-chocolate-factory-charlie-bucket-1_13/index.html"
page = requests.get(url)
# Récupère les données à partir de HTML
soup = BeautifulSoup(page.content, 'html.parser')

# Récupérer le contenu html

product_page_url = url
title = soup.find('h1')
product_description = soup.find(class_='article.product_page').find('p')
review_rating = soup.find(class_="star-rating").find('p')
image_url = soup.find(class_="item active").find('img')
category = soup.find(class_="breadcrumb").find('a')

#recherche de tout les elements td de la page
list_table = soup.find_all('td')

# recherche de l'element précis contenu uniquement dans table
universal_product_code = list_table[0]
price_including_tax = list_table[2]
price_excluding_tax = list_table[3]
number_available = list_table[5]


"""print("upc", universal_product_code)
print("titre", title)
print("prixinclu", price_including_tax)
print("prixexclu", price_excluding_tax)
print("nombre restant", number_available)
print("image", image_url)
print("page produit", product_page_url)"""

print("etoile", review_rating)
print("description", product_description)
print("categorie", category)



