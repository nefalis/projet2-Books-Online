
import csv
import os

# Création fichier CSV
def write_csv(file_name, data):
    # création du dossier data_file s'il n'existe pas
    if not os.path.exists('../data_file'):
        os.makedirs('../data_file')

    # Création d'un fichier pour écrire dans le fichier book_data.csv
    with open('data_file/' + file_name, 'a', encoding='utf-8', newline='') as file_csv:
        # Création objet writer (écriture) avec ce fichier
        writer = csv.writer(file_csv, delimiter=',')
        # Permet de boucler les éléments
        writer.writerow(data)

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