from pokemon import Pokemon 

class Dresseur:
    def __init__(self, nom: str):
        self.nom = nom
        self.equipe: list[Pokemon] = [] 
        self.equipe_combat: list[Pokemon] = [] 
        self.victoires = 0

    def ajouter_pokemon(self, pokemon: Pokemon):
        if len(self.equipe) < 6:
            self.equipe.append(pokemon)
            print(f"Ajouté : {pokemon.nom} a rejoint l'équipe de {self.nom}. (Équipe actuelle: {len(self.equipe)}/6)")
        else:
            print(f"L'équipe de {self.nom} est pleine (max 6). {pokemon.nom} est envoyé dans la Boîte PC (ignoré).")

    def gerer_evolution(self, ancien_pokemon: Pokemon, nouveau_pokemon: Pokemon):
        try:
            index = self.equipe.index(ancien_pokemon)
            self.equipe[index] = nouveau_pokemon
            print(f"Le Dresseur {self.nom} a échangé {ancien_pokemon.nom} contre son évolution, {nouveau_pokemon.nom} dans son équipe complète.")
        except ValueError:
            pass

    def selectionner_equipe_combat(self, pokemons_selectionnes: list[Pokemon]):
        self.equipe_combat = pokemons_selectionnes
        self.equipe_combat = self.equipe_combat[:3] 

    def choisir_pokemon(self) -> Pokemon | None:
        for p in self.equipe_combat:
            if not p.est_ko():
                return p
        return None
    
    def a_des_pokemons_vivants(self) -> bool:
        return any(not p.est_ko() for p in self.equipe_combat)

    def soigner_equipe_complete(self):
        for p in self.equipe:
            p.points_de_vie = p.pv_max
            
    def get_pokemons_vivants(self) -> list[Pokemon]:
        return [p for p in self.equipe if not p.est_ko()]
    
    def __str__(self):
        equipe_str = "\n".join(f"  - {str(p)}" for p in self.equipe)
        return f"Dresseur {self.nom} (Victoires: {self.victoires})\nÉquipe ({len(self.equipe)}/6) :\n{equipe_str}"