# INF-5170 Projet de session: Guide pour la correction

## 

### 1. Installation des dépendances
   1. Lancer un nouveau terminal
   2. Exécuter la commande pip `install -r requirements.txt`
### 2.  Génération du fichier raml et démarrage du serveur

   1. Lancer un nouveau terminal
   2. Exécuter la commande `make`

### 3. Correction des routes

#### A1

- Faire une simple recherche sur la page d’accueil

#### A2

- Faire une simple recherche sur la page d’accueil

#### A3

- Remplacer la dernière partie du code dans le fichier `app.py` par le code ci-dessous afin de mettre à jour la base de données à tout les deux minutes pour tester:

```python
if __name__ == "__main__":
    with app.app_context():
        scheduler.add_job(func=get_db().download_csv, trigger="interval", minutes=2)
        scheduler.start()
        app.run(debug=True, use_reloader=False)
```

#### A4

Il y a deux options

- Ajouter la route "/contrevenants?du=2022-05-08&au=2024-05-15" dans le lien de la page
- Sur POSTMAN ou YARC, faites "GET /contrevenants?du=2022-05-08&au=2024-05-15"

#### A5

- Faire une simple recherche par date sur la page d’accueil
- Si ça ne marche pas redémarrez le serveur

#### C1

Il y a deux options

- Ajouter la route "/infractions" dans le lien de la page
- Sur POSTMAN ou YARC, faites "GET /infractions"

#### C2

Il y a deux options

- Ajouter la route "/infractions-xml" dans le lien de la page
- Sur POSTMAN ou YARC, faites "GET /infractions-xml"

#### C3

Il y a deux options

- Ajouter la route "/infractions-csv" dans le lien de la page
- Sur POSTMAN ou YARC, faites "GET /infractions-csv"

Un fichier csv sera téléchargé dans votre ordinateur et vous pourrez l'ouvrir avec Excel

#### D1

Pour l'affichage des inspections il y a deux options

- Ajouter la route "/inspection" dans le lien de la page
- Sur POSTMAN ou YARC, faites "GET /inspection"

Pour acceder au formulaire de plainte

- Cliquez sur le bouton "Faire une plainte"
- Remplissez le formulaire et cliquez sur le bouton "Créer"

#### D2

- Sur POSTMAN ou YARC, faites "DELETE /inspection/{id à supprimer}"
- Refaites l'affichage mentionné dans D1

#### E1

Il y a deux options

- Ajouter la route "/utilisateur" dans le lien de la page
- Sur POSTMAN ou YARC, faites "GET /utilisateur"

#### E2 (partiellement fait)

- Sur la page d'accueil, appuyez sur le bouton "Authentification"
- Remplissez le formulaire (ctrl + click pour sélectionner plus qu'un établissement) et créer votre compte
