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
3. [Auteurs](#auteurs)
4. [License](#license)


## 💽 Installation <div id="installation"></div>

### Dépendances <div id="dependances"></div>

Le projet utilise `pygame`, ainsi que plusieurs librairies incluses dans python par défaut (qu'il n'est donc pas nécessaire d'installer).

Pour simplifier l'installation, l'utilisation d'un environnement virtuel est possible, [comme décrite ici](https://docs.python.org/fr/3/tutorial/venv.html).

### Utilisation <div id="utilisation"></div>

Après décompression de l'archive, il suffit de lancer le fichier `./src/main.py` en étant dans le dossier `src` racine du projet :
```bash
$ cd ./src
$ python3 src/main.py
```

## 🕹 Comment jouer ? <div id="howto"></div>

### Menu principal <div id="mmenu"></div>

Le menu principal est composé de trois boutons.

Le joueur peut choisir de :
- Commencer une **nouvelle partie**, ce qui, après sélection et identification des joueurs, le conduira directement dans le fenêtre de jeu.
- Afficher le **classement**, menu contenant les noms des différents joueurs, classés en fonction de leur nombre de victoires.
- Lire les **règles du jeu**, affiche un texte contenant les règles du jeu RISK.

### Fenêtre de jeu <div id="dependences"></div>

La fenêtre de jeu se compose de quatre zones.

La carte, élément principal du jeu, se trouve au centre-droit de la fenêtre. Elle est cliquable tout au long du jeu, et permet de sélectionner les régions.

Au dessous se trouve une barre notifiant le joueur de toute information pertinente.

Sur la gauche se trouve le volet de commande, qui permet aux joueurs d'interagir avec le jeu.

Il est possible d'afficher les missions en utilisant la touche `m` du clavier.


### Phases de jeu <div id="gphases"></div>

#### Renforcement <div id="renforcement"></div>

Pendant le renforcement, les joueurs doivent chacun leur tour placer le nombre de troupes affiché dans le volet de commande sur leurs territoires, comme ils le souhaitent.

Pour ce faire, il faut sélectionner un pays et utiliser les boutons `+` et `-` situés en dessous du compteur.

Pour passer au joueur suivant, utiliser la flèche en bas à droite. Une fois toutes les troupes de tous les joueurs placées, la flèche permet de passer à la phase d'**Attaque**.

#### Attaque <div id="attaque"></div>

La phase d'attaque demande au joueur attaquant de choisir le territoire à attaquer, et remplir les paramètres du volet. Le joueur qui défend fait de même pour le nombre de dés.

Quand tous les paramètres rentrés, le joueur clique sur les épées en bas à gauche pour attaquer une fois.
Lorsque l'attaque est terminée, le bouton flèche permet de passer à la phase suivante.

#### Déplacement <div id="depl"></div>

Durant la phase de déplacement, le joueur sélectionne deux territoires, et peut déplacer les troupes à l'aide du bouton double-flèches en bas à droite.

Une fois la phase terminée, cliquer sur le bouton flèche pour passer à la phase suivante.

## 📁 Structure du projet

```
.
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

## ✨ Auteurs <div id="auteurs"></div>

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

