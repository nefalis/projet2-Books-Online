# librairies utilisées
import requests
from bs4 import BeautifulSoup
import urllib.request
import csv

# On récupère les infos de la page url visé
url = "http://books.toscrape.com/catalogue/charlie-and-the-chocolate-factory-charlie-bucket-1_13/index.html"
page = requests.get(url)
# Récupère les données à partir de HTML
soup = BeautifulSoup(page.text, 'lxml')

# On récupère le contenu html

# Je récupére d'abord ma balise , ensuite je lui demande toutes les class " star-rating" associée à cette balise .
# j'éxécute une méthode get pour lister toutes ma liste d'étoiles et une méthode pop pour me renvoyer le
# dernier élement de ma liste et savoir éxactement de combien d'étoile dispose mon livre
review_rating = soup.find('p', class_='star-rating').get('class').pop()

product_page_url = url
title = soup.find('h1').text
product_description = soup.find("article", {"class": "product_page"}).find_all("p")[3].text
category = soup.find("ul", {"class": "breadcrumb"}).find_all("a")[2].text

# On recherche tout les elements td de la page
list_table = soup.find_all('td')
# On recherche de l'element précis contenu uniquement dans les td
universal_product_code = list_table[0].text
price_including_tax = list_table[2].text
price_excluding_tax = list_table[3].text
number_available = list_table[5].text

# On récupère l'image - balise entière avec src et alt
image = soup.find('div', class_="item active").find('img')


# pour cibler la partie src
def recup_img(parse_img):
    target_link_img = parse_img.find('div', class_="item active").find('img')['src']
    base_url = "http://books.toscrape.com/"
    # base url + target link permet d'avoir l'adresse de l'image complete et on remplace le '../../' de devant
    # par rien
    complete_link = base_url + target_link_img
    return complete_link.replace("../../", '')


# pour enregistrer l'image
image_url = recup_img(soup)
name_img = "imageSave.jpg"
# urlretrieve va enregistré l'image avec son nom et l'image
urllib.request.urlretrieve(image_url, name_img)

# visualisation des données

# print("liste_table", list_table)
print("upc", universal_product_code)
print("titre", title)
print("prixinclu", price_including_tax)
print("prixexclu", price_excluding_tax)
print("nombre restant", number_available)
print("image", image_url)
print("page produit", product_page_url)
print("categorie", category)
print("description", product_description)
print("etoile", review_rating)


# Création fichier CSV
def write_csv():
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
        # Permet de boucler les élements
        writer.writerow([product_page_url,
                         universal_product_code,
                         title,
                         price_including_tax,
                         price_excluding_tax,
                         number_available,
                         product_description,
                         category,
                         review_rating,
                         image_url])


write_csv()
print("fichier csv fait")
