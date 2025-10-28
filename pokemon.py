
class Pokemon:
    def __init__(self, nom, type, niveau, points_de_vie, attaque):
        self.nom = nom
        self.type = type
        self.niveau = niveau
        self.points_de_vie = points_de_vie
        self.attaque = attaque

    def attaquer(self, autre_pokemon):
        
        degats = self.attaque + random.randint(0, 5)
        print(f"{self.nom} attaque {autre_pokemon.nom} et inflige {degats} dégâts !")
        autre_pokemon.points_de_vie -= degats

    def est_ko(self):
        return self.points_de_vie <= 0

    def __str__(self):
        return f"{self.nom} ({self.type}) - Niveau {self.niveau} - PV: {self.points_de_vie}"

