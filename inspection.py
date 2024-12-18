class Inspection:
    def __init__(self, id, etablissement, adresse, ville, date_visite, nom, prenom, description):
        self.id = id
        self.etablissement = etablissement
        self.adresse = adresse
        self.ville = ville
        self.date_visite = date_visite
        self.nom = nom
        self.prenom = prenom
        self.description = description

    def afficher_inspection(self):
        return {
            "id": self.id,
            "etablissement": self.etablissement,
            "adresse": self.adresse,
            "ville": self.ville,
            "date_visite": self.date_visite,
            "nom": self.nom,
            "prenom": self.prenom,
            "description": self.description
        }