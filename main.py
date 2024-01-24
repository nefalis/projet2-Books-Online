import requests
from bs4 import BeautifulSoup
# import urllib.request
import csv
import os


# Récupération de la page d'acceuil. page number permet d'initialisé la page actuelle a 1.
base_url = "https://books.toscrape.com/"
page_number = 1

# Création fichier CSV
def write_csv(file_name, data):
    # Création d'un fichier pour écrire dans le fichier book_data.csv
    with open(file_name, 'a', encoding='utf-8', newline='') as file_csv:
        # Création objet writer (écriture) avec ce fichier
        writer = csv.writer(file_csv, delimiter=',')
        # Permet de boucler les éléments
        writer.writerow(data)

# Supprimer le fichier CSV s'il existe déjà
csv_file_name = 'book_data.csv'
if os.path.exists(csv_file_name):
    os.remove(csv_file_name)

# Écrire l'en-tête une seule fois avant la boucle
header = ["product_page_url",
          "universal_ product_code",
          "title",
          "price_including_tax",
          "price_excluding_tax",
          "number_available",
          "product_description",
          "category",
          "review_rating"]

write_csv('book_data.csv', header)

# obtenir le contenu HTML de la page actuelle et beautiful pour analyser l'HTML
response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'lxml')
link_category = []

# Trouver le menu de navigation contenant les catégories
nav_menu = soup.find('div', class_='side_categories')
# Trouver toutes les catégories
categories = nav_menu.find_all('a')
print(categories)

# Afficher les catégories
#  la méthode .strip() est utilisée pour supprimer les espaces et les sauts de ligne éventuels autour du texte
for category in categories:
    category_name = category.text.strip()
    category_url = base_url + category['href']
    link_category.append(category_url)
    print(f"Category: {category_name}")
    print("url", category_url)

    # boucle pour parcourir les pages de chaque catégorie
    while category_url:
        book_links = soup.find_all(category_url)

        for book_link in book_links:
            # boucle sur les liens pour construire url final
            relative_url = book_link.find('a')['href']
            final_url = base_url + relative_url

            # extraction des donnes sur la page de chaque livre
            try:
                response_book = requests.get(final_url)
                # utilisation de beautiful soup pour analyse de la page du livre
                soup_book = BeautifulSoup(response_book.content, 'lxml')

                product_page_url = final_url
                print("livre url", final_url)
                title = soup_book.find("h1").text
                print("titre", title)
                review_rating = soup_book.find('p', class_='star-rating').get('class').pop()
                print("etoile", review_rating)
                product_description = soup_book.find("article", {"class": "product_page"}).find_all("p")[3].text
                print("description", product_description)
                category = soup_book.find("ul", {"class": "breadcrumb"}).find_all("a")[2].text
                print("categorie", category)
                # On recherche tout les elements td de la page
                list_table = soup_book.find_all('td')
                # On recherche de l'element précis contenu uniquement dans les td
                universal_product_code = list_table[0].text
                print("upc", universal_product_code)
                price_including_tax = list_table[2].text
                print("prix avec taxe", price_including_tax)
                price_excluding_tax = list_table[3].text
                print("prix sans tax", price_excluding_tax)
                number_available = list_table[5].text
                print("dispo", number_available)

                # Ajouter les données du livre à la liste
                data = [product_page_url,
                        universal_product_code,
                        title,
                        price_including_tax,
                        price_excluding_tax,
                        number_available,
                        product_description,
                        category,
                        review_rating]

                # Appeler la fonction pour écrire dans le fichier CSV
                write_csv('book_data.csv', data)

            except Exception as e:
                print(f"Erreur lors de l'extraction des données pour {final_url}: {e}")

    # Chercher le lien vers la page suivante
    # Mise à jour de next_page_url si une page suivante existe, sinon, le définir sur None pour arrêter la boucle.
    next_page = soup.find('li', class_='next')
    if next_page:
        category_url = base_url + next_page.a['href']
        page_number += 1
    else:
        category_url = None
