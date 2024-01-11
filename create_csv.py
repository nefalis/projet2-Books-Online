
import csv

# from main import title, review_rating

# Création fichier CSV
def write_csv():
    # Création de l'en-tête pour le fichier CSV
    en_tete = [
               "title",
               "review_rating"]

    # Création d'un fichier pour écrire dans le fichier livre_data.csv
    with open('book_data.csv', 'w') as fichier_csv:
        # Création objet writer (écriture) avec ce fichier
        writer = csv.writer(fichier_csv, delimiter=',')
        # Pour écrire la 1ere ligne
        writer.writerow(en_tete)
        # Permet de boucler les élements
        writer.writerow([
                         "title",
                         "review_rating"
                         ])


write_csv()
print("fichier csv fait")


