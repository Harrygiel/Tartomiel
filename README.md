# TARTOMIEL

## Fonctions
Permet de gérer un calendrier des jeux de rôles sur discord

## Commandes

### `!quest generate NbDeJour <-NoEmpty ou -NonVide>`
Ajoute une table de quete de longueur nbDeJour, cachant ou non les jours vide si -NoEmpty ou  est ajouté -NonVide
Exemple: `!quest generate 15 -NoEmpty`
* NbDeJour: nombre entre 1 et 365. Par défaut: 20

### `!quest remove`
Supprime une table de quete

### `!quest +event date heure nom nbPersonne MJ`
Ajoute un évènement.
Exemple: `!quest +event 25/06/2020 19h30 Naheulbeuk 5 @Harrygiel`
* date: date sous le format dd/mm/aa
* heure: heure sous le format h:mm
* nom: Nom du JdR SANS ESPACE, ni \
* nbPersonne: nombre entre 1 et 100.
* MJ: Nom de l'utilisateur, sous le format discord

### `!quest -event date heure MJ`
supprime un event
Exemple: `!quest -event 25/06/2020 19h30 @Harrygiel`
* date: date sous le format dd/mm/aa
* heure: heure sous le format h:mm
* MJ: Nom de l'utilisateur, sous le format discord

### `!quest +play date <heure MJ> <Joueur1 ...>`
Ajoute un joueur à un évènement. Si plusieurs événement sont prévu le même jour, ajoutez l'heure et le MJ.
Les administrateurs peuvent ajouter d'autres joueurs dans la commande complete uniquement.
Exemple: `!quest +play 25/06/2020 `
         `!quest +play 25/06/2020 19h30 @Harrygiel`
         Si admin: `!quest +play 25/06/2020 19h30 @Harrygiel @foetus @BLabla @JeanMiphel`
* date: date sous le format dd/mm/aa
* heure: heure sous le format h:mm
* MJ: Nom de l'utilisateur, sous le format discord

### `!quest -play date heure MJ`
Supprime un joueur à un évènement. Si plusieurs événement sont prévu le même jour, ajoutez l'heure et le MJ.
Les administrateurs peuvent supprimer d'autres joueurs dans la commande complete uniquement.
Exemple: `!quest -play 25/06/2020 `
         `!quest -play 25/06/2020 19h30 @Harrygiel`
         Si admin: `!quest -play 25/06/2020 19h30 @Harrygiel @foetus @BLabla @JeanMiphel`
* date: date sous le format dd/mm/aa
* heure: heure sous le format h:mm
* MJ: Nom de l'utilisateur, sous le format discord
