class Utilisateur:
    def __init__(self, id, nom, adresse, etablissements, mot_de_passe):
        self.id = id
        self.nom = nom
        self.adresse = adresse
        self.etablissements = etablissements
        self.mot_de_passe = mot_de_passe

    def afficher_user(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "adresse": self.adresse,
            "etablissements": self.etablissements,
            "mot_de_passe": self.mot_de_passe
        }