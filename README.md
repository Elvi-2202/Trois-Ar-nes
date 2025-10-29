Le projet est organisé autour de plusieurs fichiers Python, chacun jouant un rôle crucial dans le  du jeu.

main.py: Le Moteur Central de l'Aventure
Ce fichier est le point d'entrée de toute l'application. Son rôle principal est d'orchestrer le succès global du jeu, depuis l'accueil du Dresseur jusqu'à la fin de la série des Arènes.
*Démarrage et Flux Principal : C'est ici que le programme commence son exécution ( if __name__ == "__main__":). Il initialise l'objet Dresseur, définit la séquence des Arènes à défier, et gère la boucle principale où le joueur choisit constamment entre Aller à l'Arène et Se Balader .
*Logique des Interactions : Il contient les fonctions de haut niveau, telles que combat_sauvage()qui gèrent les rencontres aléatoires, choisir_pokemon_actif()pour sélectionner le combattant, et selection_equipe_arene()pour préparer le défi du Champion.
*Création d'Adversaires : La fonction creer_pokemon_sauvage()est hébergée ici. Elle assure que les Pokémon sauvages générés ont un niveau de difficulté adapté, basé sur le niveau moyen actuel de l'équipe du joueur.

dresseur.py: Le Module du Joueur
Ce module définit tout ce qui concerne le personnage du joueur et la gestion de ses ressources.
*Gestion d'Inventaire et d'Équipe : Il définit la classe Dresseur. Cette classe stocke l'équipe complète du joueur ( self.equipe), tient le compte des victoires d'Arène, et maintient l'équipe de combat spécifique ( self.equipe_combat) sélectionnée pour les défis majeurs.
*Mécanismes de Vie et d'Équipe : Ce fichier fournit toutes les méthodes essentielles pour interagir avec l'équipe : ajouter_pokemon()pour les captures, soigner_equipe_complete()pour la guérison, get_pokemons_vivants()pour filtrer les Pokémon disponibles, et gerer_evolution()pour mettre à jour l'équipe après une transformation.

pokemon.py: Le Modèle des Créatures
Ce module est le cœur de la logique de combat et de la progression des créatures.
*Classe de Base et Attributs : Il définit la classe mère Pokemon qui sert de modèle pour toutes les créatures. Elle définit les attributs fondamentaux comme les Points de Vie (PV), l'Attaque, le Niveau et l'Expérience (XP).
*Héritage et Types Élémentaires : Il contient les classes filles ( PokemonFeu, PokemonEau, PokemonPlante). Ces classes héritent des caractéristiques de base, mais intègrent la logique des faiblesses et résistances de type , essentielles pour le calcul des dégâts en combat.
*Progression et Combat : Les méthodes gagner_xp()(pour la progression de niveau) et attaquer()(pour l'exécution des dégâts) sont centrales à ce module, régissant la mécanique de combat.

arene.py: Les Défis de Badge
Ce module structure les épreuves majeures du jeu que sont les Arènes.
*Définition des Champions : Il définit la classe de base Areneainsi que ses sous-classes spécifiques ( AreneFeu, AreneEau, ArenePlante).
*Logique de Champion : Chaque classe d'Arène est préconfigurée pour proposer trois Champions/Dresseurs successifs (appelés Niveaux), chacun présentant une difficulté croissante pour obtenir le badge.
*Moteur de l'Arène : La fonction principale combat()gère la séquence des trois duels d'Arène. La victoire n'est déclarée qu'après avoir vaincu ces trois niveaux. Le système prévoit une courte phase de soin et un nouveau choix de Pokémon entre chaque niveau.

1. Démarrage de l'Aventure
*Lancer le Jeu : Exécutez le fichier main.pyà partir de votre terminal.
*Initialisation : Le jeu vous accueillera et vous demandera d'entrer votre Nom de Dresseur .
*Obtention des Starters : Après avoir entré votre nom, vous recevez immédiatement vos trois Pokémon de départ : Salamèche (Feu), Carapuce (Eau), et Bulbizarre (Plante) .

2. Le Cycle de Jeu (Menu Principal)
À chaque étape, le jeu vous présentera les deux options principales pour progresser ou vous préparer :
Option 1 : Aller à l'Arène : Déclenchez le processus de défi de l'Arène en cours.
Option 2 : Se Balader (Capture/XP) : Soignez entièrement votre équipe, puis déclenchez une rencontre aléatoire avec un Pokémon sauvage (pour gagner de l'expérience et réaliser capturer).

3. Les Combats Sauvages (Option 2)
Si vous choisissez de vous balader, une rencontre aura lieu.
Choix du Combattant : Vous devrez d'abord choisir activement quel Pokémon de votre équipe vivante vous voulez envoyer combattre.
Actions de Combat : Une fois en combat, trois options s'offrent à vous :

*Attaque : Votre Pokémon inflige des dégâts.
Capture par KO : Si le Pokémon sauvage est mis KO par cette attaque, il est automatiquement capturé et ajouté à votre équipe, en plus de donner de l'XP à votre attaquant.
*Tenter Capture : Vous utilisez une Pokéball. La chance de succès est directement liée aux PV restants du Pokémon sauvage (plus il est faible, plus la capture à de chances de réussir).
*Fuir : Vous quittez le combat immédiatement.

Retour au Menu : Après la fin du combat (capture, KO, ou fuite), vous retournez au menu principal où vous aurez de nouveau le choix entre l'Arène et la Balade.

4. Le Défi des Arènes (Option 1)
Pour défier une Arène, vous devez avoir au moins 3 Pokémon vivants .
*Sélection de l'Équipe : Le jeu vous demandera de sélectionner 3 Pokémon vivants de votre équipe pour lancer votre équipe de combat.
*Séquence des Duels : Pour remporter le badge de l'Arène, vous devez réussir à battre les 3 niveaux (Champions/Dresseurs) consécutifs de l'Arène.

*Résultat et Poursuite :
Victoire : Si vous gagnez les 3 duels, vous remportez le Badge de l'Arène.
Défaite : Si vous perdez, vous êtes renvoyé au menu de progression.
Après le défi d'Arène (victoire ou défaite), le jeu vous demandera à nouveau :

Option 1 : Aller à l'Arène Suivante (si vous avez gagné ou non).
Option 2 : Se Balader (pour entraîner ou capturer de nouveaux Pokémon).