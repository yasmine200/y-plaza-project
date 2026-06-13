class BienImmobilier:
    def __init__(self, id, titre, description, prix, surface, ville, statut):
        self.id = id
        self.titre = titre
        self.description = description
        self.prix = prix
        self.surface = surface
        self.ville = ville
        self.statut = statut

    def prix_formate(self):
        return f"{self.prix:,.2f} €".replace(',', ' ')