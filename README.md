# TARTOMIEL

## Fonctions
Permet de gérer un calendrier des créneaux de jeux de rôles sur discord

## Commandes

Si le paramètre est entre [], alors il doit être remplacé par une valeur.
Si le paramètre est entre <>, alors il est optionnel.

### `!quest generate -max [NbDeJour] <-NoEmpty ou -NonVide>`
Ajoute une table de quete de longueur nbDeJour, cachant ou non les jours vide si -NoEmpty ou  est ajouté -NonVide
Exemple: `!quest generate -max 15 -NoEmpty`
* NbDeJour: nombre entre 1 et 365. Par défaut: 30

### `!quest remove`
Supprime une table de quete

### `!quest +event [date] [heure] -name ["nom"] -max [nbPersonne] -mj [MJ]`
Ajoute un évènement.
Exemple: `!quest +event 25/06/2020 19h30 Naheulbeuk -max 5 -mj @Harrygiel`
         `!quest +e 25/06 19h30 "Un JdR" -max 5 -mj @Harrygiel`
* date: date sous le format dd/mm/aa ou dd/mm
* heure: heure sous le format hh:mm ou hhhmm
* nom: Nom du JdR. Si il contient un espace, mettre entre guillemet. pas de "\"
* nbPersonne: nombre entre 1 et 100.
* MJ: Nom de l'utilisateur, sous le format discord

### `!quest -event [date] <heure> <-mj MJ>`
supprime un event
Exemple: `!quest -event 25/06/2020 19h30 @Harrygiel`
Exemple: `!quest -e 25/06`
* date: date sous le format dd/mm/aa
* heure: heure sous le format h:mm
* MJ: Nom de l'utilisateur, sous le format discord

### `!quest +play date <heure> <-mj MJ> <Joueur1 ...>`
Ajoute un joueur à un évènement. Si plusieurs événement sont prévu le même jour, ajoutez l'heure et le MJ.
Les administrateurs peuvent ajouter d'autres joueurs.
Exemple: `!quest +play 25/06 `
         `!quest +p 25/06/2020 19h30 -mj @Harrygiel`
         Si admin: `!quest +play 25/06/2020 @foetus @BLabla @JeanMiphel`
* date: date sous le format dd/mm/aa
* heure: heure sous le format h:mm
* MJ: Nom de l'utilisateur, sous le format discord

### `!quest -play date <heure> <-mj MJ> <Joueur1 ...>`
Supprime un joueur à un évènement. Si plusieurs événement sont prévu le même jour, ajoutez l'heure et le MJ.
Les administrateurs peuvent supprimer d'autres joueurs dans la commande complete uniquement.
Exemple: `!quest -play 25/06 `
         `!quest -p 25/06/2020 19h30 -mj @Harrygiel`
         Si admin: `!quest -play 25/06/2020 @foetus @BLabla @JeanMiphel`

## Planned features

1) corriger l'affichage des noms 									- FAIT
2) améliorer le système de paramètre 								- FAIT
3) ajouter des sécurités anti bug									
4) un channel log
5) notifier les joueurs quelques jours avant la partie en MP  		- FAIT (manuellement)
6) prévenir le MJ quand un joueurs rejoint ça partie 				- FAIT
7) faire une notif dans préparation quand un MJ rajoute un evenement
8) ajouter un compteur du nombre de joueur déjà présent
9) homogénéiser les heures

## BUG