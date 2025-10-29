from abc import ABC, abstractmethod
from dresseur import Dresseur
from pokemon import Pokemon, PokemonFeu, PokemonEau, PokemonPlante 

XP_BASE_ARENE = 40 

class Arene(ABC):
    
    def __init__(self, nom: str, type_arene: str):
        self.nom = nom
        self.type_arene = type_arene

    @abstractmethod
    def creer_champion_niveau(self, niveau: int) -> Dresseur:
        
        pass

    def _executer_duel(self, poke_joueur: Pokemon, poke_champion: Pokemon) -> bool:
        
        while not poke_joueur.est_ko() and not poke_champion.est_ko():
            
            
            poke_joueur.attaquer(poke_champion)
            
            if poke_champion.est_ko():
                return True 
                
            poke_champion.attaquer(poke_joueur)
            
            if poke_joueur.est_ko():
                return False 
                
        return not poke_joueur.est_ko()

    def _executer_combat_vs_champion(self, dresseur_joueur: Dresseur, champion: Dresseur) -> bool:
        
        
        victoires_joueur = 0
        
        print("\n--- Début des Duels (3 Duels pour le Niveau) ---")
        
        for i in range(3): 
            
            try:
                poke_joueur = dresseur_joueur.equipe_combat[i]
                poke_champion = champion.equipe_combat[i]
            except IndexError:
                print(f"    Il n'y a pas assez de Pokémon pour le Duel #{i+1} ! (Duel perdu par forfait)")
                continue

            if poke_joueur.est_ko():
                print(f"    {poke_joueur.nom} est K.O. et perd le Duel #{i+1} par forfait.")
                continue
                
            resultat_duel = self._executer_duel(poke_joueur, poke_champion)
            
            if resultat_duel:
                victoires_joueur += 1
                
                xp_gagne = XP_BASE_ARENE
                nouvelle_evolution = poke_joueur.gagner_xp(xp_gagne) 
                
                if nouvelle_evolution != poke_joueur:
                     dresseur_joueur.gerer_evolution(poke_joueur, nouvelle_evolution)
                     dresseur_joueur.equipe_combat[i] = nouvelle_evolution
                     
                print(f"    {poke_joueur.nom} gagne le Duel #{i+1} et gagne de l'XP !")
            else:
                 print(f"    {poke_joueur.nom} perd le Duel #{i+1} et ne gagne pas d'XP.")
                 
    
        return victoires_joueur == 3 


    def combat(self, dresseur_joueur: Dresseur) -> bool:
        print(f"\n Début de l'Arène {self.nom} ! Objectif: Vaincre les 3 Niveaux.")
        
        for niveau_arene in range(1, 4): 

            dresseur_joueur.soigner_equipe_complete() 
            
            champion = self.creer_champion_niveau(niveau_arene)
            champion.selectionner_equipe_combat(champion.equipe) 
            
            print(f"\n--- Niveau {niveau_arene}/3 : {champion.nom} te défie ! ---")
            
            
            print(f"Ton Équipe de Combat ({len(dresseur_joueur.equipe_combat)}): " + ", ".join(p.nom for p in dresseur_joueur.equipe_combat))
            print(f"Équipe Champion ({len(champion.equipe_combat)}): " + ", ".join(p.nom for p in champion.equipe_combat))
            
            victoire_niveau = self._executer_combat_vs_champion(dresseur_joueur, champion)
            
            if victoire_niveau:
                print(f"\n Niveau {niveau_arene} Gagné ! (3 Duels remportés)")
            else:
                print(f"\n Niveau {niveau_arene} Perdu. Retour à la ville. Entraîne-toi davantage !")
                return False 

            if niveau_arene < 3:
                 input("\n[Appuyez sur Entrée pour passer au niveau suivant de l'Arène...]")
        
        print("\n Victoire de l'Arène ! Les 3 niveaux ont été vaincus !")
        return True 


class AreneFeu(Arene):
    def __init__(self): super().__init__("Arène du Feu", "Feu")
    def creer_champion_niveau(self, niveau: int) -> Dresseur:
        base_niv = 14 + niveau * 2; base_pv = 80 + base_niv * 3; base_atk = 15 + base_niv
        champion = Dresseur(f"Pyra la Brûlante (Niv {niveau})")
        champion.ajouter_pokemon(PokemonFeu("Feurisson", base_niv, base_pv, base_atk))
        champion.ajouter_pokemon(PokemonFeu("Caninos", base_niv + 1, base_pv + 5, base_atk + 2))
        champion.ajouter_pokemon(PokemonFeu("Pyroli", base_niv, base_pv, base_atk))
        return champion

class AreneEau(Arene):
    def __init__(self): super().__init__("Arène de l’Eau", "Eau")
    def creer_champion_niveau(self, niveau: int) -> Dresseur:
        base_niv = 16 + niveau * 2; base_pv = 80 + base_niv * 3; base_atk = 15 + base_niv
        champion = Dresseur(f"Nereo le Marin (Niv {niveau})")
        champion.ajouter_pokemon(PokemonEau("Carabaffe", base_niv, base_pv, base_atk))
        champion.ajouter_pokemon(PokemonEau("Léviator", base_niv + 1, base_pv + 5, base_atk + 2))
        champion.ajouter_pokemon(PokemonEau("Aquali", base_niv, base_pv, base_atk))
        return champion

class ArenePlante(Arene):
    def __init__(self): super().__init__("Arène de la Plante", "Plante")
    def creer_champion_niveau(self, niveau: int) -> Dresseur:
        base_niv = 12 + niveau * 2; base_pv = 80 + base_niv * 3; base_atk = 15 + base_niv
        champion = Dresseur(f"Flora la Sage (Niv {niveau})")
        champion.ajouter_pokemon(PokemonPlante("Empiflor", base_niv, base_pv, base_atk))
        champion.ajouter_pokemon(PokemonPlante("Herbizarre", base_niv + 1, base_pv + 5, base_atk + 2))
        champion.ajouter_pokemon(PokemonPlante("Phyllali", base_niv, base_pv, base_atk))
        return champion