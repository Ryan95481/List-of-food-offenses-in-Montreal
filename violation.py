class Violation:
    def __init__(self, id_poursuite, business_id, date_violation, description, adresse, date_jugement, etablissement, montant, proprietaire, ville, statut, date_statut, categorie):
        self.id_poursuite = id_poursuite
        self.business_id = business_id
        self.date_violation = date_violation
        self.description = description
        self.adresse = adresse
        self.date_jugement = date_jugement
        self.etablissement = etablissement
        self.montant = montant
        self.proprietaire = proprietaire
        self.ville = ville
        self.statut = statut
        self.date_statut = date_statut
        self.categorie = categorie


    def afficher_info(self):
        return {
            "id_poursuite": self.id_poursuite,
            "business_id": self.business_id,
            "date_violation": self.date_violation,
            "description": self.description,
            "adresse": self.adresse,
            "date_jugement": self.date_jugement,
            "etablissement": self.etablissement,
            "montant": self.montant,
            "proprietaire": self.proprietaire,
            "ville": self.ville,
            "statut": self.statut,
            "date_statut": self.date_statut,
            "categorie": self.categorie
        }