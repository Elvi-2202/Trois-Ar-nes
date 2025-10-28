''' faire un rpg ou on affronte 3 arenes avec des personnages 
ou on fait des attanques un jeu en ligne de texte
'''
import random

class Pokemon:
    """Représente un Pokémon avec ses attributs essentiels."""
    def __init__(self, nom, type_p, pv, attaque, defense):
        self.nom = nom
        self.type_p = type_p
        self.pv_max = pv
        self.pv_actuel = pv
        self.attaque = attaque
        self.defense = defense
        self.attaques = {"Charge": 20, "Rugissement": 0} # Exemple d'attaques

    def est_ko(self):
        """Vérifie si le Pokémon est K.O."""
        return self.pv_actuel <= 0

    def prendre_degats(self, degats):
        """Déduit les dégâts des PV actuels."""
        self.pv_actuel -= degats
        if self.pv_actuel < 0:
            self.pv_actuel = 0
        print(f"{self.nom} subit {degats} dégâts. PV restants: {self.pv_actuel}/{self.pv_max}")

    def attaque_ennemi(self, cible, nom_attaque):
        """Effectue une attaque sur un Pokémon cible."""
        if nom_attaque not in self.attaques:
            print(f"{self.nom} ne connaît pas l'attaque {nom_attaque}!")
            return

        puissance = self.attaques[nom_attaque]
        print(f"\n{self.nom} utilise {nom_attaque}!")

        # Calcul de dégâts très simplifié (vous pouvez ajouter des facteurs de type ici)
        degats = int((((2 * 10 + 10) / 250) * (self.attaque / cible.defense) * puissance + 2) * random.uniform(0.85, 1.0))

        if degats < 1:
            degats = 1
        
        cible.prendre_degats(degats)
        return degats

    def __str__(self):
        return f"{self.nom} (Type: {self.type_p}, PV: {self.pv_actuel}/{self.pv_max})"

# --- 2. Fonction de combat ---
def combat(pokemon_joueur, pokemon_adversaire):
    """Gère un tour de combat textuel."""
    print("--- Début du Combat ---")
    print(f"Vous affrontez le Pokémon de l'Arène: {pokemon_adversaire.nom}!")

    while not pokemon_joueur.est_ko() and not pokemon_adversaire.est_ko():
        print(f"\n--- Votre Tour ---")
        print(pokemon_joueur)
        print(pokemon_adversaire)
        
        # Choix de l'attaque du Joueur
        print(f"Attaques disponibles: {', '.join(pokemon_joueur.attaques.keys())}")
        choix_attaque = input("Choisissez une attaque: ").strip().capitalize()

        if choix_attaque in pokemon_joueur.attaques:
            pokemon_joueur.attaque_ennemi(pokemon_adversaire, choix_attaque)
        else:
            print("Choix invalide. Vous perdez un tour!")
        
        if pokemon_adversaire.est_ko():
            print(f"\n{pokemon_adversaire.nom} est K.O. ! Vous avez gagné le combat!")
            break

        # Tour de l'Adversaire
        print(f"\n--- Tour de l'Adversaire ---")
        # L'adversaire choisit une attaque au hasard (simplifié)
        attaque_adv = random.choice(list(pokemon_adversaire.attaques.keys()))
        pokemon_adversaire.attaque_ennemi(pokemon_joueur, attaque_adv)

        if pokemon_joueur.est_ko():
            print(f"\nVotre {pokemon_joueur.nom} est K.O. ! Vous avez perdu le combat!")
            break
    
    print("--- Fin du Combat ---")
    return not pokemon_joueur.est_ko()

# --- 3. Initialisation et Lancement ---
if __name__ == "__main__":
    # Création des Pokémon pour la première arène (Eau)
    
    # Votre Pokémon de départ (Feu)
    votre_pokemon = Pokemon("Salameche", "Feu", 50, 15, 10) 
    
    # Le Champion d'Arène Eau
    champion_arene_eau = Pokemon("Carapuce", "Eau", 60, 12, 12) 

    # Lancement du test de combat (simulant la première arène)
    combat_gagne = combat(votre_pokemon, champion_arene_eau)

    if combat_gagne:
        print("\nFélicitations, vous avez battu le Champion de l'Arène Eau!")
    else:
        print("\nEssayez encore ! Entraînez votre Pokémon et revenez.")