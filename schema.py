contravention_schema = {
    "type": "object",
    "properties": {
        "id_poursuite": {"type": "string"},
        "business_id": {"type": "string"},
        "date_violation": {"type": "string"},
        "description": {"type": "string"},
        "adresse": {"type": "string"},
        "date_jugement": {"type": "string"},
        "etablissement": {"type": "string"},
        "montant": {"type": "string"},
        "proprietaire": {"type": "string"},
        "ville": {"type": "string"},
        "statut": {"type": "string"},
        "date_statut": {"type": "string"},
        "categorie": {"type": "string"}
    },
    "required": ["id_poursuite", "business_id", "date_violation",
        "description", "adresse", "date_jugement", "etablissement",
        "montant", "proprietaire", "ville", "statut", "date_statut",
        "categorie"], "additionalProperties": False
}

nouveau_user_schema = {
    "type": "object",
    "properties": {
        "nom": {"type": "string"},
        "adresse": {"type": "string"},
        "liste": {"type": "array", "items": {"type": "string"}},
        "mot_de_passe": {"type": "string"}
    },
    "required": ["nom", "adresse", "liste", "mot_de_passe"],
    "additionalProperties": False
}

nouvel_inspection_schema = {
    "type": "object",
    "properties": {
        "etablissement": {"type": "string"},
        "adresse": {"type": "string"},
        "ville": {"type": "string"},
        "date_visite": {"type": "string"},
        "nom": {"type": "string"},
        "prenom": {"type": "string"},
        "description": {"type": "string"}
    },
    "required": ["etablissement", "adresse", "ville", "date_visite",
        "nom", "prenom", "description"],
    "additionalProperties": False
}