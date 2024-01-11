# librairies utilisées
import requests
from bs4 import BeautifulSoup
import urllib.request
import csv

# Récupération de la page catégorie Children. page number permet d'initialisé la page actuelle a 1.
base_url = "http://books.toscrape.com/catalogue/category/books/childrens_11/"
page_number = 1
next_page_url = base_url

# boucle pour parcourir les pages
while next_page_url:
    # obtenir le contenu HTML de la page actuelle et beautiful pour analyser l'HTML
    response = requests.get(next_page_url)
    soup = BeautifulSoup(response.text, 'lxml')

    # Récupération des liens des livres sur la page actuelle
    book_links = soup.find_all('h3')
    for book_link in book_links:
        # boucle sur les liens pour construire url final
        relative_url = book_link.a['href']
        final_url = f"http://books.toscrape.com/catalogue/category/books/childrens_11/{relative_url}"

        # extraction des donnes sur la page de chaque livre
        # 2eme requete pour acceder à la page specifique  du livre
        response_book = requests.get(final_url)
        # utilisation de beautiful soup pour analyse de la page du livre
        soup_book = BeautifulSoup(response_book.text, 'lxml')

        product_page_url = final_url
        print("livre url", final_url)
        title = soup_book.find("h3").text
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

        # On récupère l'image - balise entière avec src et alt
        image = soup_book.find('div', class_="item active").find('img')

        # pour cibler la partie src
        def recup_img(parse_img):
            target_link_img = parse_img.find('div', class_="item active").find('img')['src']
            base_url_img = "http://books.toscrape.com/"
            # base url + target link permet d'avoir l'adresse de l'image complete et on remplace le '../../' de devant
            # par rien
            complete_link_img = base_url_img + target_link_img
            return complete_link_img.replace("../../", '')

        # pour enregistrer l'image
        image_url = recup_img(soup_book)
        name_img = "imageSave.jpg"
        # urlretrieve va enregistré l'image avec son nom et l'image
        urllib.request.urlretrieve(image_url, name_img)

    # Chercher le lien vers la page suivante
    # Mise à jour de next_page_url si une page suivante existe, sinon, le définir sur None pour arrêter la boucle.
    next_page = soup.find('li', class_='next')
    if next_page:
        next_page_url = base_url + next_page.a['href']
        page_number += 1
    else:
        next_page_url = None

# Après chaque boucle affichage du nombre total total de pages traitées
print(f"Extraction terminée. Nombre total de pages traitées : {page_number}")

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
    with open('book_data.csv', 'w') as file_csv:
        # Création objet writer (écriture) avec ce fichier
        writer = csv.writer(file_csv, delimiter=',')
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
