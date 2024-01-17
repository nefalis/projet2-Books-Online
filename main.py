# librairies utilisées
import requests
from bs4 import BeautifulSoup
import urllib.request
import csv

#  recup toute les catégories
htmlResponse = requests.get('http://books.toscrape.com/index.html')
soup = BeautifulSoup(htmlResponse.text, 'lxml')


"""
# Création fichier CSV
def write_csv(file_name, data):
    # Création d'un fichier
    with open(file_name, 'a', encoding='utf-8', newline='') as file_csv:
        # Création objet writer (écriture) avec ce fichier
        writer = csv.writer(file_csv, delimiter=',')
        # Permet de boucler les éléments
        writer.writerow(data)

# fonction pour recup toute les catégories
def get_category(base_url):
    response_category = requests.get(base_url)
    soup_category = BeautifulSoup(response_category.text, 'lxml')
    categories = soup_category.find('ul', {'class': "nav nav-list"}).find('ul').find_all('li')
    category_links = [base_url + category['href'] for category in categories]
    return category_links

# Écrire l'en-tête une seule fois avant la boucle
header = ["product_page_url",
          "title",
          "category"]

write_csv('book_data.csv', header)

# Récup de tous les liens categories
all_categories_links = get_category("http://books.toscrape.com/")

# boucle pour parcourir toutes les categories
for category_link in all_categories_links:
    base_url = category_link
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
            final_url = f"http://books.toscrape.com/catalogue{relative_url}"

            # extraction des donnes sur la page de chaque livre
            # 2eme requete pour acceder à la page specifique  du livre
            response_book = requests.get(final_url)
            # utilisation de beautiful soup pour analyse de la page du livre
            soup_book = BeautifulSoup(response_book.text, 'lxml')

            product_page_url = final_url
            print("livre url", final_url)
            title = soup_book.find("h3").text
            print("titre", title)
            category = soup_book.find("ul", {"class": "breadcrumb"}).find_all("a")[2].text
            print("categorie", category)

            # Ajouter les données du livre à la liste
            data = [product_page_url,
                    title,
                    category
                    ]

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
print("Extraction terminée.")
print("fichier csv fait")
"""
"""
# Récupération de toutes les catégories.
base_url = "http://books.toscrape.com"
next_category_url = base_url

# Création fichier CSV
# fonction pour faire l'entete
def write_header_csv(category_name):
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

    file_name = f'book_data.{category_name}.csv'
    # Création d'un fichier pour écrire dans le fichier book_data.csv
    with open(file_name, 'w', encoding='utf-8', newline='') as file_csv:
        # Création objet writer (écriture) avec ce fichier
        writer = csv.writer(file_csv, delimiter=',')
        # Permet de boucler les éléments
        writer.writerow(header)
    return file_name

# fonction pour ecrire dans le fichier CSV
def write_category_csv(file_name, data):
    with open(file_name, 'a', encoding='utf-8', newline='') as file_csv:
        writer = csv.writer(file_csv, delimiter=',')
        writer.writerow(data)

# Initialiser la variable category_number à 0
category_number = 0

# pour obtenir le nom des catégories
response = requests.get(next_category_url)
soup = BeautifulSoup(response.text, 'lxml')
# Récupération du nom de la categorie pour le fichier csv
category_name = soup.find('li', class_='side_categories').text
print("categorie", category_name)

# initialise un fichier CSV pour categorie
category_csv_file = write_header_csv(category_name)

# boucle pour parcourir les catégories
while next_category_url:
    # obtenir le contenu HTML de la page actuelle et beautiful pour analyser l'HTML
    response = requests.get(next_category_url)
    soup = BeautifulSoup(response.text, 'lxml')

    # Récupération des liens des livres sur la page actuelle
    book_links = soup.find_all('h3')

    for book_link in book_links:
        # boucle sur les liens pour construire url final
        final_url = book_link.a['href']

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
        write_category_csv(category_csv_file, data)

    # Chercher le lien vers la page suivante
    # Mise à jour de next_page_url si une page suivante existe, sinon, le définir sur None pour arrêter la boucle.
    next_page = soup.find('li', class_='next')
    if next_page:
        next_page_url = base_url + next_page.a['href']
    else:
        next_page_url = None

    # augmente de 1 à chaque irération
    category_number += 1

    # Afficher le nombre total de catégories traitées
    print(f"Catégorie traitée. Nombre total de catégories traitées : {category_number}")

# Après chaque boucle affichage du nombre total total de pages traitées
print(f"Extraction terminée.")

print("fichier csv fait")"""
