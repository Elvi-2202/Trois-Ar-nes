import random
from abc import ABC, abstractmethod

class Pokemon(ABC):
    def __init__(self, nom: str, type_pokemon: str, niveau: int, pv_max: int, attaque_base: int):
        self.nom = nom
        self.type = type_pokemon
        self.niveau = niveau
        self.pv_max = pv_max
        self.points_de_vie = pv_max
        self.attaque_base = attaque_base
        self.experience = 0
        self.xp_pour_prochain_niveau = self.calculer_xp_necessaire()
        self.evolution_niveau = 0  
        self.prochain_nom = ""
        self.prochaine_classe = None

    def calculer_xp_necessaire(self) -> int:
        return self.niveau * 10 + 50

    def monter_niveau(self) -> 'Pokemon':
        self.niveau += 1
        print(f"\n✨ {self.nom} atteint le Niveau {self.niveau} !")
        
        pv_gain = random.randint(4, 6)
        atk_gain = random.randint(1, 3)
        self.pv_max += pv_gain
        self.attaque_base += atk_gain
        self.points_de_vie = self.pv_max
        print(f"Stats augmentées : PV +{pv_gain}, ATK +{atk_gain}.")
        
        self.xp_pour_prochain_niveau = self.calculer_xp_necessaire()
        self.experience = 0
        
        return self.verifier_evolution()

    def gagner_xp(self, xp_gagne: int) -> 'Pokemon':
        if self.niveau >= 100:
             return self
             
        self.experience += xp_gagne
        
        nouvelle_evolution = self
        while self.experience >= self.xp_pour_prochain_niveau:
            nouvelle_evolution = self.monter_niveau() 
            if nouvelle_evolution != self:
                return nouvelle_evolution 
                
        return nouvelle_evolution

    def evoluer(self, nouvelle_nom: str, nouveau_type_classe) -> 'Pokemon':
        """Effectue l'évolution du Pokémon."""
        print(f"\n🎉 Félicitations ! Votre {self.nom} est en train d'évoluer...")
        
        nouveau_pokemon = nouveau_type_classe(
            nouvelle_nom,
            self.niveau,
            self.pv_max + 10, 
            self.attaque_base + 5 
        )
        nouveau_pokemon.experience = self.experience
        nouveau_pokemon.points_de_vie = self.points_de_vie
        
        print(f"Il est devenu {nouveau_pokemon.nom} !")
        return nouveau_pokemon 

    def verifier_evolution(self):
        if self.prochaine_classe and self.niveau >= self.evolution_niveau:
            return self.evoluer(self.prochain_nom, self.prochaine_classe)
        return self
        
    def est_ko(self) -> bool:
        return self.points_de_vie <= 0
        
    @abstractmethod
    def calculer_degats_speciaux(self, autre_pokemon: 'Pokemon') -> float:
        pass
    
    def attaquer(self, autre_pokemon: 'Pokemon'):
        if self.est_ko():
            return

        degats_bruts = self.attaque_base + random.randint(1, 5)
        multiplicateur = self.calculer_degats_speciaux(autre_pokemon)
        degats_finaux = int(degats_bruts * multiplicateur)
        
        message_type = ""
        if multiplicateur > 1.0:
            message_type = " (Super efficace ! )"
        elif multiplicateur < 1.0:
            message_type = " (Pas très efficace... )"
            
        print(f"   {self.nom} ({self.type}) attaque {autre_pokemon.nom} et inflige {degats_finaux} dégâts{message_type}!")
        
        autre_pokemon.points_de_vie = max(0, autre_pokemon.points_de_vie - degats_finaux)
        
    def __str__(self):
        statut = "K.O." if self.est_ko() else f"{self.points_de_vie}/{self.pv_max}"
        return f"[{self.type}] {self.nom} - Niv {self.niveau} (XP: {self.experience}/{self.xp_pour_prochain_niveau}) - PV: {statut}"


class PokemonEvoFeu(Pokemon):
     def __init__(self, nom: str, niveau: int, pv_max: int, attaque_base: int):
        super().__init__(nom, "Feu", niveau, pv_max, attaque_base)
        self.evolution_niveau = 0 
        
     def verifier_evolution(self): return self 
     
     def calculer_degats_speciaux(self, autre_pokemon: Pokemon) -> float:
        if autre_pokemon.type == "Plante": return 2.0
        elif autre_pokemon.type == "Eau": return 0.5
        return 1.0


class PokemonEvoEau(Pokemon):
     def __init__(self, nom: str, niveau: int, pv_max: int, attaque_base: int):
        super().__init__(nom, "Eau", niveau, pv_max, attaque_base)
        self.evolution_niveau = 0 
        
     def verifier_evolution(self): return self 
     
     def calculer_degats_speciaux(self, autre_pokemon: Pokemon) -> float:
        if autre_pokemon.type == "Feu": return 2.0
        elif autre_pokemon.type == "Plante": return 0.5
        return 1.0

class PokemonEvoPlante(Pokemon):
     def __init__(self, nom: str, niveau: int, pv_max: int, attaque_base: int):
        super().__init__(nom, "Plante", niveau, pv_max, attaque_base)
        self.evolution_niveau = 0 
        
     def verifier_evolution(self): return self 
     
     def calculer_degats_speciaux(self, autre_pokemon: Pokemon) -> float:
        if autre_pokemon.type == "Eau": return 2.0
        elif autre_pokemon.type == "Feu": return 0.5
        return 1.0

class PokemonFeu(Pokemon):
    def __init__(self, nom: str, niveau: int, pv_max: int, attaque_base: int):
        super().__init__(nom, "Feu", niveau, pv_max, attaque_base)
        self.evolution_niveau = 15
        self.prochain_nom = "Pyroli" 
        self.prochaine_classe = PokemonEvoFeu

    def calculer_degats_speciaux(self, autre_pokemon: Pokemon) -> float:
        if autre_pokemon.type == "Plante": return 2.0
        elif autre_pokemon.type == "Eau": return 0.5
        return 1.0
        
class PokemonEau(Pokemon):
    def __init__(self, nom: str, niveau: int, pv_max: int, attaque_base: int):
        super().__init__(nom, "Eau", niveau, pv_max, attaque_base)
        self.evolution_niveau = 15
        self.prochain_nom = "Aquali"
        self.prochaine_classe = PokemonEvoEau 
        
    def calculer_degats_speciaux(self, autre_pokemon: Pokemon) -> float:
        if autre_pokemon.type == "Feu": return 2.0
        elif autre_pokemon.type == "Plante": return 0.5
        return 1.0

class PokemonPlante(Pokemon):
    def __init__(self, nom: str, niveau: int, pv_max: int, attaque_base: int):
        super().__init__(nom, "Plante", niveau, pv_max, attaque_base)
        self.evolution_niveau = 15
        self.prochain_nom = "Phyllali" 
        self.prochaine_classe = PokemonEvoPlante 

    def calculer_degats_speciaux(self, autre_pokemon: Pokemon) -> float:
        if autre_pokemon.type == "Eau": return 2.0
        elif autre_pokemon.type == "Feu": return 0.5
        return 1.0