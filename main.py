# librairies utilisées
import requests
from bs4 import BeautifulSoup
# import urllib.request
# import csv

#  recup la page de la categorie
page_category = f"http://books.toscrape.com/catalogue/category/books/childrens_11/"
response = requests.get(page_category)
soup = BeautifulSoup(response.text, 'lxml')

# recup les liens des livres
book_links = soup.find_all('h3')
print(book_links)

# boucle pour extraire les url des livres sur chaque page
for book_link in book_links:
    relative_url = book_link.a['href']
    final_url = f"http://books.toscrape.com/catalogue/category/books/childrens_11/{relative_url}"

    print(final_url)

books = soup.find_all(class_="product_pod")
# boucle pour extraire les données sur chaque elements
for book in books:
    print("book")
    title = book.find("h3").text
    print("titre", title)
    review_rating = book.find('p', class_='star-rating').get('class').pop()
    print("etoile", review_rating)

"""# initialise le numero de page à 1
numero_page = 1

# boucle pour lire les pages tant qu'il y a une page, tant que le status est 200
while True:
    #  recup la page de la categorie
    page_category = f"http://books.toscrape.com/catalogue/category/books/childrens_11/index_{numero_page}.html"
    response = requests.get(page_category)

    # pour verifier si la page existe
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')

        # recup les liens des livres
        book_links = soup.find_all('h3')
        print(book_links)

        # boucle pour extraire les url des livres sur chaque page
        for book_link in book_links:
            relative_url = book_link.a['href']
            final_url = f"http://books.toscrape.com/catalogue/category/books/childrens_11/{relative_url}"

            print(final_url)

        # pour passer à la page suivante
        numero_page += 1

    # pour sortir de la boucle
    else:
        print("Fin lecture. pas de page suivante")
        break"""

"""# fonction pour recup la page de la categorie
def url_category():
    page_category = requests.get("http://books.toscrape.com/catalogue/category/books/childrens_11/")
    soup = BeautifulSoup(page_category.content, 'lxml')
    return soup
print("debut")

# fonction pour regarder les urls des pages
def get_all_pages(soup):
    urls = []
    base_url_category = "http://books.toscrape.com/catalogue/category/books/childrens_11/"
    print("marcel")
    listing_books = soup.find_all(class_="product_pod")

    # boucle pour extraire les données sur chaque élément
    for listing in listing_books:
        print("milieu")
        target_link = listing.find("h3").a.get("href")
        final_link = base_url_category + target_link
        urls.append(final_link)
        print("pouet")

    return urls

print("fin")"""

"""# Création fichier CSV
def write_csv():
    # Création de l'en-tête pour le fichier CSV
    en_tete = [
               "title",
               "review_rating"]

    # Création d'un fichier pour écrire dans le fichier livre_data.csv
    with open('book_data.csv', 'w') as file_csv:
        # Création objet writer (écriture) avec ce fichier
        writer = csv.writer(file_csv, delimiter=',')
        # Pour écrire la 1ere ligne
        writer.writerow(en_tete)
        # Permet de boucler les élements
        writer.writerow([
                         "title",
                         "review_rating"
                         ])


write_csv()
print("fichier csv fait")"""

"""
# fonction pour regarder les urls des pages
def get_all_pages():
    urls = []
    page_number = 1
    for base_url_category in range(2):
        base_url_category = f"http://books.toscrape.com/catalogue/category/books/childrens_11/{page_number}.html"
        page_number += 1

        urls.append(base_url_category)
        print("final link", base_url_category)

    return urls


# fonction pour regarder les elements d'une page
def parse_book(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')

    books = soup.find_all(class_="product_pod")
    # boucle pour extraire les données sur chaque elements
    for book in books:
        print("book")
        title = book.find("h3").text
        print("titre", title)
        review_rating = book.find('p', class_='star-rating').get('class').pop()
        print("etoile", review_rating)

    return url


# fonction pour regarder les elements dans chaque page de la catégorie
def parse_all_book():
    pages = get_all_pages()

    # boucle pour passer sur chaque page
    for page in pages:
        parse_book(url=page)
        print("pouet")


parse_all_book()"""

"""def parse_category():
    # On récupère les infos des pages url
    page = requests.get("http://books.toscrape.com/catalogue/category/books/science-fiction_16/")
    # Récupère les données à partir de HTML
    soup = BeautifulSoup(page.text, 'lxml')
    return soup"""

# fonction pour lire plusieurs pages
"""def get_all_pages(soup):
    # variable pour parcourir les pages
    # pour recolter les url pour mettre dans une liste vide
    urls = []
    listing = soup.find_all(class_="product_prod")
    page_number = 1

    # boucle pour lire chaque page
    for base_url_category in listing:
        target_link = base_url_category.find("h3").get("href")

        base_url_category = f"http://books.toscrape.com/catalogue/category/books/science-fiction_16/{page_number}.html"
        page_number += 1
        # lien complet
        final_link = base_url_category + target_link
        # append permet de rajouter un element a la liste
        urls.append(final_link)
        print("base_url", base_url_category)
        return urls

print("test")


def extract_book(urls):
    print("debut extractbook")

    response_category = requests.get("http://books.toscrape.com/catalogue/category/books/science-fiction_16/index.html")
    soup = BeautifulSoup(response_category.content, "lxml")
    for book_link in urls:
        product_page_url = book_link
        print("product_page", product_page_url)
        title = soup.find('h1').text
        print("titre", title)

    extract_book(urls)"""

"""
review_rating = soup.find('p', class_='star-rating').get('class').pop()
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
complete_link_img = base_url + target_link_img
return complete_link_img.replace("../../", '')

# pour enregistrer l'image
image_url = recup_img(soup)
name_img = "imageSave.jpg"
# urlretrieve va enregistré l'image avec son nom et l'image
urllib.request.urlretrieve(image_url, name_img)"""

# visualisation des données


"""
print("page produit", product_page_url)
print("etoile", review_rating)
print("upc", universal_product_code)
print("prixinclu", price_including_tax)
print("prixexclu", price_excluding_tax)
print("nombre restant", number_available)
print("image", image_url)
print("categorie", category)
print("description", product_description)"""
