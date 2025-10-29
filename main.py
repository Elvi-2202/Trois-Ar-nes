from dresseur import Dresseur
from pokemon import Pokemon, PokemonFeu, PokemonEau, PokemonPlante 
from arene import AreneFeu, AreneEau, ArenePlante
import random

XP_BASE_SAUVAGE = 15 

# Fonctions de Création
def creer_pokemon_sauvage(niveau_moyen: int) -> Pokemon:
    type_choisi = random.choice(["Feu", "Eau", "Plante"])
    nom = random.choice(["Feunnec", "Pikachu", "Rondoudou", "Chenipan", "Roucool"]) 
    niveau = max(2, niveau_moyen + random.randint(-2, 2)) 
    base_pv, base_atk = 50 + niveau*3, 10 + niveau
    
    if type_choisi == "Feu": return PokemonFeu(nom, niveau, base_pv, base_atk)
    elif type_choisi == "Eau": return PokemonEau(nom, niveau, base_pv, base_atk)
    else: return PokemonPlante(nom, niveau, base_pv, base_atk)

# Fonctions d'Interaction
def choisir_pokemon_actif(joueur: Dresseur) -> Pokemon | None:
    pokemons_vivants = joueur.get_pokemons_vivants()
    if not pokemons_vivants:
        print("Tu n'as aucun Pokémon vivant pour combattre !")
        return None
    
    print("\n--- CHOIX DU POKÉMON ACTIF ---")
    for i, p in enumerate(pokemons_vivants):
         print(f"    {i+1}. {p.nom} ({p.type}) - Niv {p.niveau} - PV: {p.points_de_vie}/{p.pv_max}")

    while True:
        try:
            choix_index = int(input(f"Quel Pokémon (1 à {len(pokemons_vivants)}) vas-tu envoyer au combat ? : ")) - 1
            if 0 <= choix_index < len(pokemons_vivants):
                poke_actif = pokemons_vivants[choix_index]
                print(f"-> Tu envoies {poke_actif.nom} !")
                return poke_actif
            else: print("Choix invalide. Veuillez entrer un numéro de la liste.")
        except ValueError: print("Entrée invalide. Veuillez entrer un nombre.")

def combat_sauvage(joueur: Dresseur):
    if not joueur.get_pokemons_vivants():
        print("Tu n'as plus de Pokémon disponibles pour un combat sauvage.")
        return

    niveau_moyen = sum(p.niveau for p in joueur.equipe) // len(joueur.equipe) if joueur.equipe else 10
    pokemon_sauvage = creer_pokemon_sauvage(niveau_moyen)
    print(f"\n! ! ! Un Pokémon sauvage apparaît ! ! !\nC'est un {pokemon_sauvage.nom} de Niveau {pokemon_sauvage.niveau} ({pokemon_sauvage.type}).")
    poke_actif = choisir_pokemon_actif(joueur) 
    if not poke_actif: return

    tour = 1
    while not poke_actif.est_ko() and not pokemon_sauvage.est_ko():
        print(f"\n--- Tour {tour} (Sauvage) ---\nTon Pokémon: {poke_actif}\nSauvage : {pokemon_sauvage}")
        action = input("Que veux-tu faire ? (1: Attaque, 2: Tenter Capture, 3: Fuir) : ")
        
        if action == "1":
            poke_actif.attaquer(pokemon_sauvage)
            if pokemon_sauvage.est_ko():
                xp_gagne = XP_BASE_SAUVAGE
                nouvelle_evolution = poke_actif.gagner_xp(xp_gagne)
                if nouvelle_evolution != poke_actif: joueur.gerer_evolution(poke_actif, nouvelle_evolution)
                print(f"Le Pokémon sauvage, {pokemon_sauvage.nom}, est K.O. ! Combat terminé.")
                if pokemon_sauvage.est_ko():
                    joueur.ajouter_pokemon(pokemon_sauvage)
                    print(f" Le Pokémon sauvage K.O. ({pokemon_sauvage.nom}) a été capturé et ajouté à ton équipe !")
                break
            
            pokemon_sauvage.attaquer(poke_actif)
            if poke_actif.est_ko():
                print(f" Ton Pokémon, {poke_actif.nom}, est K.O. ! Combat terminé."); break 

        elif action == "2":
            chance_capture = max(0.1, (pokemon_sauvage.pv_max - pokemon_sauvage.points_de_vie) / pokemon_sauvage.pv_max)
            if random.random() < chance_capture:
                print(f"\n Tu as capturé {pokemon_sauvage.nom} !")
                joueur.ajouter_pokemon(pokemon_sauvage); break
            else:
                print(" Le Pokémon sauvage s'est libéré de la Pokéball !")
                pokemon_sauvage.attaquer(poke_actif)
                if poke_actif.est_ko():
                    print(f" Ton Pokémon, {poke_actif.nom}, est K.O. ! Combat terminé."); break

        elif action == "3": print("Tu as réussi à fuir. Le combat est terminé."); break
        else: print("Action invalide. Choisis 1, 2 ou 3.")
        tour += 1
    print("Fin du combat sauvage.")

# Fonctions d'Initialisation et d'Arène
def initialiser_jeu() -> Dresseur:
    print("\n## Bienvenue dans la Région d'Avelia ! ##") 
    nom_joueur = input("Bienvenue ! Quel est ton nom de Dresseur ? : ")
    joueur = Dresseur(nom_joueur)
    
    base_niv, base_pv, base_atk = 10, 50 + 10*3, 15 + 10
    joueur.ajouter_pokemon(PokemonFeu("Salamèche", base_niv, base_pv, base_atk))
    joueur.ajouter_pokemon(PokemonEau("Carapuce", base_niv, base_pv, base_atk))
    joueur.ajouter_pokemon(PokemonPlante("Bulbizarre", base_niv, base_pv, base_atk))

    print("\n Parfait ! Ton équipe de départ est composée des 3 Starters.")
    print(joueur)
    return joueur


def selection_equipe_arene(joueur: Dresseur):
    pokemons_disponibles = joueur.get_pokemons_vivants()
    
    if len(pokemons_disponibles) < 3:
        print(f" Tu n'as que {len(pokemons_disponibles)} Pokémon vivants. Ils combattront tous.")
        joueur.selectionner_equipe_combat(pokemons_disponibles)
        return
        
    print("\n--- CHOIX DE L'ÉQUIPE DE COMBAT (3 Pokémon requis) ---")
    equipe_choisie = []
    
    while len(equipe_choisie) < 3:
        print("\nTon équipe complète (vivants) :")
        pokemons_restants = [p for p in pokemons_disponibles if p not in equipe_choisie]
        
        for i, p in enumerate(pokemons_restants):
             print(f"    {i+1}. {p.nom} ({p.type}) - Niv {p.niveau} - PV: {p.points_de_vie}/{p.pv_max}")
        
        try:
            choix_index = int(input(f"Choisis le Pokémon #{len(equipe_choisie) + 1} (1 à {len(pokemons_restants)}) : ")) - 1
            if 0 <= choix_index < len(pokemons_restants):
                poke_selectionne = pokemons_restants[choix_index]
                equipe_choisie.append(poke_selectionne)
                print(f"-> Ajouté : {poke_selectionne.nom}.")
            else: print("Choix invalide.")
        except ValueError: print("Entrée invalide. Entre le numéro du Pokémon.")
            
    joueur.selectionner_equipe_combat(equipe_choisie)
    print("\nÉquipe de combat confirmée : " + ", ".join(p.nom for p in equipe_choisie))


def lancer_aventure():
    joueur = initialiser_jeu() 
    arenes = [ArenePlante(), AreneFeu(), AreneEau()]
    
    for i, arene in enumerate(arenes):
        
        while True:
            peut_entrer = len(joueur.get_pokemons_vivants()) >= 3 or i == 0 
            print(f"\nStatut de l'équipe : {len(joueur.get_pokemons_vivants())}/6 Pokémon vivants.")
            action = input("Que veux-tu faire ? (1: Aller à l'Arène, 2: Se Balader (Capture/XP)) : ")
            
            if action == "2":
                joueur.soigner_equipe_complete()
                print("Tu te reposes, tes Pokémon sont soignés.")
                if random.random() < 0.8: combat_sauvage(joueur)
                else: print("Rien ne se passe... continuons la balade.")
                print("\n" + joueur.__str__())
            
            elif action == "1":
                if peut_entrer:
                    print("\n" + "~" * 60); print(f"DÉFI : Arène {arene.type_arene}"); print("~" * 60)
                    break 
                else: print("Tu dois avoir au moins 3 Pokémon vivants pour défier l'Arène. Entraîne-toi davantage !")
            
            else: print("Action invalide.")
        
        joueur.soigner_equipe_complete() 
        selection_equipe_arene(joueur)
        
        if len(joueur.equipe_combat) < 3:
            print("Défaite avant le combat d'Arène, car l'équipe de combat ne contient pas 3 Pokémon vivants."); break

        input("Appuyez sur Entrée pour défier le Champion de l'Arène...")
        victoire = arene.combat(joueur) 

        if victoire:
            joueur.victoires += 1
            print(f"\n--- Tu as gagné le Badge {arene.type_arene} ! ---")
        else:
            print("\n Défaite de l'Arène. Tu n'as pas réussi à vaincre les 3 niveaux.")
            
        while True:
            if joueur.victoires == len(arenes): break
            choix_post_arene = input("\nAprès ce combat, que veux-tu faire ? (1: Aller à l'Arène Suivante, 2: Se Balader) : ")
            if choix_post_arene == "2":
                joueur.soigner_equipe_complete()
                print("Tu te balades et tes Pokémon sont soignés.")
                if random.random() < 0.8: combat_sauvage(joueur)
                else: print("Rien ne se passe...")
                print("\n" + joueur.__str__())
            elif choix_post_arene == "1": break
            else: print("Choix invalide.")
            
    if joueur.victoires == len(arenes):
        print("\n" + "!"*50); print("!!! Félicitations, tu as obtenu les trois Badges et es prêt pour la Ligue !!!"); print("!"*50)

if __name__ == "__main__":
    lancer_aventure()