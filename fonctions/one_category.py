# librairies utilisées
import requests
from bs4 import BeautifulSoup
import urllib.request
import csv
import os


# Création fichier CSV
def write_csv(file_name, data):
    # création du dossier data_file s'il n'existe pas
    if not os.path.exists('data_file'):
        os.makedirs('data_file')

    # Création d'un fichier pour écrire dans le fichier book_data.csv
    with open('data_file/' + file_name, 'a', encoding='utf-8', newline='') as file_csv:
        # Création objet writer (écriture) avec ce fichier
        writer = csv.writer(file_csv, delimiter=',')
        # Permet de boucler les éléments
        writer.writerow(data)


# pour cibler la partie src
def recup_img(parse_img):
    target_link_img = parse_img.find('div', class_="item active").find('img')['src']
    base_url_img = "http://books.toscrape.com/"
    # base url + target link permet d'avoir l'adresse de l'image complete et on remplace le '../../' de devant
    # par rien
    complete_link_img = base_url_img + target_link_img
    return complete_link_img.replace("../../", '')


def one_category(base_url, file_name):

    # Supprimer le fichier CSV s'il existe déjà
    if os.path.exists(file_name):
        os.remove(file_name)

    # Écrire l'en-tête une seule fois avant la boucle
    header = ["product_page_url",
              "universal_ product_code",
              "title",
              "price_including_tax",
              "price_excluding_tax",
              "number_available",
              "product_description",
              "category",
              "review_rating",
              "image_url"]

    write_csv('book_data.csv', header)

    page_number = 1
    # Récupération de la page catégorie. page number permet d'initialisé la page actuelle a 1.

    next_page_url = base_url
    # boucle pour parcourir les pages
    while next_page_url:
        # obtenir le contenu HTML de la page actuelle et beautiful pour analyser l'HTML
        response = requests.get(next_page_url)
        soup = BeautifulSoup(response.content, 'lxml')

        # Récupération des liens des livres sur la page actuelle
        book_links = soup.find_all('h3')
        for book_link in book_links:
            # boucle sur les liens pour construire url final
            relative_url = book_link.a['href']
            final_url = base_url + relative_url

            # extraction des donnes sur la page de chaque livre
            # 2eme requete pour acceder à la page specifique  du livre
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

            # pour enregistrer l'image
            image_url = recup_img(soup_book)
            name_img = "imageSave.jpg"
            # urlretrieve va enregistré l'image avec son nom et l'image
            urllib.request.urlretrieve(image_url, name_img)
            print("image url", image_url)

            # Ajouter les données du livre à la liste
            data = [product_page_url,
                    universal_product_code,
                    title,
                    price_including_tax,
                    price_excluding_tax,
                    number_available,
                    product_description,
                    category,
                    review_rating,
                    image_url]

            # Appeler la fonction pour écrire dans le fichier CSV
            write_csv('book_data.csv', data)

        # Chercher le lien vers la page suivante
        # Mise à jour de next_page_url si une page suivante existe, sinon, le définir sur None pour arrêter la boucle.
        next_page = soup.find('li', class_='next')
        if next_page:
            next_page_url = base_url + next_page.a['href']
            page_number += 1
        else:
            next_page_url = None

    # Après chaque boucle affichage du nombre total total de pages traitées
    print(f"Extraction terminée.")
    print("fichier csv fait")


# programme principal

"""file_name = 'book_data.csv'

base_url = "https://books.toscrape.com/catalogue/category/books_1/"

one_category(base_url, file_name)"""
