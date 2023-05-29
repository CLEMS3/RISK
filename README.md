# RISK

[![python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)

Le jeu populaire **RISK** écrit en python.

## Sommaire

1. [Installation](#installation)
    - [Dépendances](#dependances)
    - [Utilisation](#utilisation)
2. [Comment jouer ?](#howto)
    - [Menu principal](#mmenu)
    - [Fenêtre de jeu](#gwindow)
    - [Phases de jeu](#gphases)
        - [Renforcement](#renforcement)
        - [Attaque](#attaque)
        - [Déplacement](#depl)
        - [Missions](#mission)
        - [Fin de partie](#endgame)
3. [Structure du projet](#struct)
4. [Auteurs](#auteurs)


<div id="installation"></div>

## 💽 Installation

<div id="dependances"></div>

### Dépendances

Le projet utilise `pygame`, ainsi que plusieurs librairies incluses dans python par défaut (qu'il n'est donc pas nécessaire d'installer).

Pour simplifier l'installation, l'utilisation d'un environnement virtuel est possible, [comme décrite ici](https://docs.python.org/fr/3/tutorial/venv.html).

<div id="utilisation"></div>

### Utilisation

Après décompression de l'archive, il suffit de lancer le fichier `/src/main.py` en étant dans le dossier `src` du projet :
```bash
$ cd ./src
$ python3 main.py
```

<div id="howto"></div>

## 🕹 Comment jouer ?

<div id="mmenu"></div>

### Menu principal

Le menu principal est composé de trois boutons.

Le joueur peut choisir de :
- Commencer une **nouvelle partie**, ce qui, après sélection et identification des joueurs, le conduira directement dans le fenêtre de jeu.
- Afficher le **classement**, menu contenant les noms des différents joueurs, classés en fonction de leur nombre de victoires.
- Lire les **règles du jeu**, affiche un texte contenant les règles du jeu RISK.

<div id="dependences"></div>

### Fenêtre de jeu

La fenêtre de jeu se compose de quatre zones.

La carte, élément principal du jeu, se trouve au centre-droit de la fenêtre. Elle est cliquable tout au long du jeu, et permet de sélectionner les régions.

En dessous se trouve une barre notifiant le joueur de toute information pertinente.

Sur la gauche se trouve le volet de commande, qui permet aux joueurs d'interagir avec le jeu.

<div id="gphases"></div>

### Phases de jeu

<div id="renforcement"></div>

#### Renforcement

Pendant le renforcement, les joueurs doivent chacun leur tour placer le nombre de troupes affiché dans le volet de commande sur leurs territoires, comme ils le souhaitent.

Pour ce faire, il faut sélectionner un pays et utiliser les boutons `+` et `-` situés en dessous du compteur.

Pour passer au joueur suivant, utiliser la flèche en bas à droite. Une fois toutes les troupes de tous les joueurs placées, la flèche permet de passer à la phase d'**Attaque**.

<div id="attaque"></div>

#### Attaque

La phase d'attaque demande au joueur attaquant de choisir le territoire attaquant et attaqué, et remplir les paramètres du volet. Le joueur qui défend fait de même pour le nombre de dés.

Volet :
> - Le joueur **attaquant** peut choisir jusqu'à trois **régiments** pour attaquer.
> - Il choisit ensuite le nombre de **dés** qu'il désire utiliser pour réaliser l'attaque. Ce nombre doit être inférieur ou égal au nombre de régiments mobilisés.
> - Le joueur défenseur peut choisir jusqu'à deux **régiments** pour défendre, et utilisera le nombre dés correspondant.

Quand tous les paramètres rentrés, le joueur clique sur les épées en bas à gauche pour attaquer une fois.
Lorsque l'attaque est terminée, le bouton flèche permet de passer à la phase suivante.

Le joueur peut attaquer le nombre de territoire qu'il souhaite, selon sa stratégie. Une fois qu'il conquit un pays, il doit y placer un certain nombre de troupe, le minimum étant le nombre de troupe qu'il a utilisé pour attaquer.

<div id="depl"></div>

#### Déplacement

Durant la phase de déplacement, le joueur sélectionne deux territoires, et peut déplacer les troupes à l'aide du bouton double-flèches en bas à droite.

Le déplacement n'est possible qu'entre deux territoires. Le pays selectionné en premier est celui qui donne les troupes et le deuxième est celui qui les reçoit.

Une fois la phase terminée, cliquer sur le bouton flèche pour passer à la phase suivante.

<div id="mission"></div>

#### Missions

Chaque joueur se voit attribué en début de partie une mission secrète qu'il va devoir accomplir pour gagner la partie. Cette mission est visible en cliquant sur le tampon "TOP SECRET" au dessus de la carte. Il ne faut pas dévoiler sa missions aux autres joueurs, cela leur donnerait un avantage sur vous.

Une fois qu'un joueur a rempli sa mission, la partie prend fin.

<div id="endgame"></div>

#### Fin de partie

Une fois la partie remportée par un joueur, il suffit de fermer la fenêtre de jeu pour retourner au **menu**. On peut alors recommencer une partie ou choisir d'arrêter de jouer. Le gagnant de la partie remporte un point de score, ce qui le fera peut-être gagner une place dans le classement général !

A vous de jouer maintenant ! N'hésitez pas à revenir sur cette fenêtre en cours de jeu si vous voulez verifier des détails.


<div id="struct"></div>

## 📁 Structure du projet

```
.
├── Rendu/                  # Fichiers de rendu
├── src/
│   ├── Fichiers/           # Divers fichier de données pour le jeu
│   ├── Fonts/              # Polices utilisées
│   ├── Images/             # Images utilisées pour l'interface
│   ├── Pictures/           # Images utilisées pour les composants du jeu
│   ├── main.py             # Fichier principal
│   ├── carte.py            # Affichage pygame du jeu
│   ├── Rules.py            # Définition des règles du jeu en python
│   └── widgets.py          # Widgets pygame utilisés en jeu
├── requirements.txt        # Fichier pour les dépendances dans le venv
└── README.md
```

<div id="auteurs"></div>

## ✨ Auteurs

<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/olmetaprogrammer"><img src="https://avatars.githubusercontent.com/u/128503773?v=4?s=100" width="100px;" alt="olmetaprogrammer"/><br /><sub><b>olmetaprogrammer</b></sub></a><br /></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/AntoinePscl"><img src="https://avatars.githubusercontent.com/u/128501984?v=4?s=100" width="100px;" alt="AntoinePscl"/><br /><sub><b>AntoinePscl</b></sub></a><br /></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/CLEMS3"><img src="https://avatars.githubusercontent.com/u/56449459?v=4?s=100" width="100px;" alt="CLEMS3"/><br /><sub><b>CLEMS3</b></sub></a><br /></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/vitto4"><img src="https://avatars.githubusercontent.com/u/128498605?v=4?s=100" width="100px;" alt="vitto4"/><br /><sub><b>vitto4</b></sub></a><br /></td>
    </tr>
  </tbody>
</table>

