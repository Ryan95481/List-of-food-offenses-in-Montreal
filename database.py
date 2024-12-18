import sqlite3
from violation import Violation
from utilisateur import Utilisateur
from inspection import Inspection
import requests
import csv
import datetime


class Database():
    def __init__(self):
        self.connection = None
        self.create_tables()

    def download_csv(self):
        csv_url = (
            "https://data.montreal.ca/dataset/"
            "05a9e718-6810-4e73-8bb9-5955efeb91a0/resource/"
            "7f939a08-be8a-45e1-b208-d8744dca8fc6/download/violations.csv")

        response = requests.get(csv_url)
        csv_reader = csv.DictReader(response.text.splitlines())

        for row in csv_reader:
            violation = Violation(
                int(row['id_poursuite']), int(row['business_id']),
                datetime.datetime.strptime(row['date'], '%Y%m%d'),
                row['description'], row['adresse'],
                datetime.datetime.strptime(row['date_jugement'], '%Y%m%d'),
                row['etablissement'], int(row['montant']),
                row['proprietaire'], row['ville'], row['statut'],
                datetime.datetime.strptime(row['date_statut'], '%Y%m%d'),
                row['categorie'])

            if self.id_existe(violation.id_poursuite):
                self.update_violation(violation)
            else:
                self.inserer_violation(violation)
        return "Téléchargement effectué avec succès !"

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/database.db',
                                              check_same_thread=False)
        return self.connection

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def create_tables(self):
        connection = self.get_connection()
        with open('db/db.sql') as f:
            commands = f.read().split(';')
            for command in commands:
                if command.strip() != '':
                    try:
                        connection.execute(command)
                    except sqlite3.Error as e:
                        print(f"An error occurred: {e.args[0]}")
        connection.commit()

    def get_violation_id(self, id_poursuite):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Violation WHERE id_poursuite = ?",
                       (id_poursuite,))
        row = cursor.fetchone()
        return row

    def inserer_violation(self, violation):
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO Violation "
            "(id_poursuite, business_id, date_violation, "
            " description, adresse, date_jugement, "
            "etablissement, montant, proprietaire, "
            "ville, statut, date_statut, categorie) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (
                violation.id_poursuite,
                violation.business_id,
                violation.date_violation,
                violation.description,
                violation.adresse,
                violation.date_jugement,
                violation.etablissement,
                violation.montant,
                violation.proprietaire,
                violation.ville,
                violation.statut,
                violation.date_statut,
                violation.categorie
            ))
        connection.commit()

    def afficher_violation(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Violation")
        violation = cursor.fetchall()
        return [Violation(*row) for row in violation]

    def rechercher_violation(self, keyword):
        """Recherche d'un article."""
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM Violation WHERE etablissement LIKE ? "
            "OR proprietaire LIKE ? OR adresse LIKE ?",
            ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%')
        )
        resultat = cursor.fetchall()
        return [Violation(*row) for row in resultat]

    def rechercher_violation_par_date(self, date_debut, date_fin):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM Violation WHERE date_violation BETWEEN ? AND ?",
            (date_debut, date_fin)
        )
        violation = cursor.fetchall()
        return [Violation(*row) for row in violation]

    def trier_par_nombre_infractions(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT business_id, etablissement, "
                       "COUNT(*) as nombre_violations FROM Violation"
                       " GROUP BY business_id ORDER BY nombre_violations DESC")
        violation = cursor.fetchall()
        return [(row[0], row[1], row[2]) for row in violation]

    def update_violation(self, violation):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE Violation SET business_id = ?, date_violation = ?,"
            " description = ?, adresse = ?, date_jugement = ?,"
            " etablissement = ?, montant = ?, proprietaire = ?,"
            " ville = ?, statut = ?, date_statut = ?"
            " WHERE id_poursuite = ?",
            (violation.business_id,
             violation.date_violation,
             violation.description,
             violation.adresse,
             violation.date_jugement,
             violation.etablissement,
             violation.montant,
             violation.proprietaire,
             violation.ville,
             violation.statut,
             violation.date_statut,
             violation.id_poursuite)
        )
        connection.commit()

    def delete_violation(self, id_poursuite):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM Violation WHERE id_poursuite = ?", (id_poursuite,)
        )
        connection.commit()

    def id_existe(self, id):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1 FROM Violation WHERE id_poursuite = ?", (id,))
        return cursor.fetchone() is not None

    def creer_inspection(self, inspection):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO Inspection "
            "(etablissement, adresse, ville, "
            "date_visite, nom, prenom, description) "
            "VALUES (?,?,?,?,?,?,?)", (
                inspection.etablissement,
                inspection.adresse,
                inspection.ville,
                inspection.date_visite,
                inspection.nom,
                inspection.prenom,
                inspection.description
            ))
        connection.commit()
        return inspection

    def read_inspections(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT rowid, etablissement, adresse,"
                       " ville, date_visite, nom, prenom,"
                       " description FROM Inspection")
        inspection = cursor.fetchall()
        return [Inspection(id, etablissement, adresse,
                           ville, date_visite, nom,
                           prenom, description)
                for id, etablissement, adresse,
                ville, date_visite, nom,
                prenom, description in inspection]

    def read_one_inspection(self, id):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT rowid, etablissement, adresse,"
                       " ville, date_visite, nom, prenom,"
                       " description FROM Inspection WHERE rowid = ?", (id,))
        inspections = cursor.fetchall()
        if len(inspections) == 0:
            return None
        else:
            inspection = inspections[0]
            return Inspection(inspection[0], inspection[1], inspection[2],
                              inspection[3], inspection[4], inspection[5],
                              inspection[6], inspection[7])

    def supprimer_inspection(self, inspection):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Inspection WHERE rowid = ?",
                       (inspection.id,))
        connection.commit()

    def sauvegarder_utilisateur(self, utilisateur):
        connection = self.get_connection()
        etablissements_str = "('{}')".format(utilisateur.etablissements)
        if utilisateur.id is None:
            connection.execute(
                "INSERT INTO Utilisateur "
                "(nom, adresse, liste, mot_de_passe) "
                "VALUES (?,?,?,?)", (
                    utilisateur.nom,
                    utilisateur.adresse,
                    etablissements_str,
                    utilisateur.mot_de_passe
                ))
            connection.commit()
            cursor = connection.cursor()
            cursor.execute("SELECT last_insert_rowid() FROM Utilisateur")
            resultat = cursor.fetchall()
            utilisateur.id = resultat[0][0]

            for etablissement in utilisateur.etablissements:
                connection.execute(
                    "INSERT INTO UtilisateurEtablissement "
                    "(utilisateur_id, etablissement) "
                    "VALUES (?,?)", (
                        utilisateur.id,
                        etablissement
                    ))
                connection.commit()
        else:
            connection.execute(
                "UPDATE Utilisateur SET "
                "nom = ?, adresse = ?, mot_de_passe = ? "
                "WHERE id = ?", (
                    utilisateur.nom,
                    utilisateur.adresse,
                    utilisateur.mot_de_passe,
                    utilisateur.id
                ))
            connection.commit()

            connection.execute(
                "DELETE FROM UtilisateurEtablissement "
                "WHERE utilisateur_id = ?",
                (utilisateur.id,))
            connection.commit()

            for etablissement in utilisateur.etablissements:
                connection.execute(
                    "INSERT INTO UtilisateurEtablissement "
                    "(utilisateur_id, etablissement) "
                    "VALUES (?,?)", (
                        utilisateur.id,
                        etablissement
                    ))
            connection.commit()
        return utilisateur

    def read_utilisateurs(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT rowid, nom, adresse, "
                       "liste, mot_de_passe FROM Utilisateur")
        utilisateurs = cursor.fetchall()
        return [Utilisateur(id, nom, adresse, liste.split(','), mot_de_passe)
                for id, nom, adresse, liste, mot_de_passe in utilisateurs]

    def __del__(self):
        self.close_connection()
