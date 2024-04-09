# TP - Versus & Build - Data checker

Le présent projet sert à vérifier la conformité des données dans un fichier Excel donné, 
structuré selon le format de votre choix.

## Table of Contents
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)

## Installation

### Python 
Pour pouvoir executer notre projet ici présent, vous devriez avoir ou installer `python`.

Vous pouvez trouver leur page de téléchargement (du site officiel) [ici](https://www.python.org/downloads/).
* [Windows](https://www.digitalocean.com/community/tutorials/install-python-windows-10)
* [Linux](https://kinsta.com/knowledgebase/install-python/#linux)
* [MacOS](https://kinsta.com/knowledgebase/install-python/#mac)

### Dépendance
Notre projet requiere les packages suivants:

```bash
pip install pandas numpy json
```

### Télécharment du projet
Vous pouvez soit cloner avec la commande suivante:
```bash
git clone https://github.com/FanantenanaR/data-checker-excel.git
```
Soit télécharger avec la fonctionnalité de [download as zip](https://codeload.github.com/FanantenanaR/data-checker-excel/zip/refs/heads/master).

## Configuration et structure
Vous devriez mettre dans le dossier `data` votre fichier excel `.xlsx`.

### Fichier de Configuration
Le dossier config contient des fichiers JSON pour la configuration de chaque 
table de données (processeur, RAM, disque dur, etc.). 
Vous pouvez modifier ces fichiers selon vos besoins pour spécifier les colonnes, 
les types de données, les contraintes, etc.

### Structure du projet
Les deux dossiers importants sont les suivants:
* `config`: Ce dossier contient les fichiers de configuration pour chaque table de données, utilisés pour 
spécifier les colonnes, les types de données, les contraintes, etc.
* `data`: Ce dossier contient les fichiers de données nécessaires au projet, tels que les fichiers Excel à traiter.


## Utilisation
Pour lancer le projet, veuillez executer la commande suivante 
dans le répertoire du projet (même niveau que les dossier `data`, `config`, ...)

```bash
python main.py
```

## Licence
...
