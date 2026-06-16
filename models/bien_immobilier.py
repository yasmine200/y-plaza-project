class BienImmobilier:
    def __init__(self, id, titre, description, prix, surface, ville, statut, image_url):
        self.id = id
        self.titre = titre
        self.description = description
        self.prix = prix
        self.surface = surface
        self.ville = ville
        self.statut = statut
        self.image_url = image_url  # <-- Nouvelle ligne pour stocker le chemin de la photo

    def prix_formate(self):
        return f"{self.prix:,.2f} €".replace(',', ' ')

    def to_dict(self):
        """Représentation sérialisable en JSON (utilisée par l'API REST)."""
        return {
            "id": self.id,
            "titre": self.titre,
            "description": self.description,
            "prix": self.prix,
            "surface": self.surface,
            "ville": self.ville,
            "statut": self.statut,
            "image_url": self.image_url,
        }