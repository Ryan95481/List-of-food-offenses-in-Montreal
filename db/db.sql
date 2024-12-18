CREATE TABLE IF NOT EXISTS Violation(
    id_poursuite INTEGER PRIMARY KEY,
    business_id INTEGER NOT NULL,
    date_violation DATE NOT NULL,
    description TEXT NOT NULL,
    adresse TEXT NOT NULL,
    date_jugement DATE NOT NULL,
    etablissement TEXT NOT NULL,
    montant INTEGER NOT NULL,
    proprietaire TEXT NOT NULL,
    ville TEXT NOT NULL,
    statut TEXT NOT NULL,
    date_statut DATE NOT NULL,
    categorie TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Inspection(
    id INTEGER PRIMARY KEY,
    etablissement TEXT NOT NULL,
    adresse TEXT NOT NULL,
    ville TEXT NOT NULL,
    date_visite DATE NOT NULL,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Utilisateur(
    nom TEXT NOT NULL,
    adresse TEXT NOT NULL,
    liste TEXT NOT NULL,
    mot_de_passe TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS UtilisateurEtablissement(
    utilisateur_id INTEGER NOT NULL,
    etablissement TEXT NOT NULL,
    PRIMARY KEY(utilisateur_id, etablissement),
    FOREIGN KEY(utilisateur_id) REFERENCES Utilisateur(id)
);
