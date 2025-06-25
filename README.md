# LITRevu

Projet Openclassrooms : P9 Développez une application Web en utilisant Django

## Présentation du projet

LITRevu est une application web développée avec Django permettant aux utilisateurs de :
- publier des **tickets de lecture** (demandes de critique),
- poster des **critiques de livres** (réponses à un ticket ou critiques libres),
- **suivre** d'autres utilisateurs pour voir leurs publications dans un fil d’actualité personnalisé.

Ce projet a été réalisé dans le cadre de la formation “Développeur d'application Python” – OpenClassrooms.

---

## Installation et prérequis

### Prérequis

- Python 3.10.12
- pip
- virtualenv (facultatif mais recommandé)

### Installation

```bash
# Cloner le dépôt
git clone https://github.com/MagNott/P9_Developpez_application_web_django.git
cd litrevu

# Créer et activer un environnement virtuel
python -m venv env
source env/bin/activate  # ou env\Scripts\activate sous Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur local
python manage.py runserver

Accéder à l'application à l’adresse : http://localhost:8000
```

##  Style & CSS

Le projet utilise :

- Bootstrap 5 (personnalisé avec le thème Bootswatch United) intègre par défaut des bonnes pratiques en matière d’accessibilité, ce qui facilite la conformité aux normes WCAG.
- Des variables SCSS personnalisées (couleurs, contrastes, boutons…)
- Les fichiers CSS personnalisés sont situés dans static/css/custom.scss.

## Architecture du projet

```bash
litrevu/
├── authentication/        # Application de gestion des utilisateurs
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── templates/authentication
│
├── litrevu/               # Configuration principale du projet Django
│   ├── settings.py        # Paramètres globaux (BDD, apps, sécurité…)
│   └── urls.py            # Routage principal
│
├── reviews/               # App principale (tickets,critiques, feed...)
│   ├── models/            # A l'intérieur des dossiers suivants, il y a un fichier par entité
│   ├── views/
│   ├── forms/             # Un fichier pour review et un pour ticket pour la personnalisation du formualaire 
│   ├── templates/
│   ├── templatetags/      # Gestion de l'affichage des étoiles pour la notation
│
├── static/                # Fichiers statiques (CSS, images)
├── templates/             # Templates globaux (base.html, etc.)
│── db.sqlite3             # Base de données SQLite (fournie pour les tests)
├── manage.py
├── requirements.txt       # Liste des dépendances du projet
├── README.md              # Ce fichier
```

## Technologies utilisées & qualité du code

- Python 3.10.12
- Django 5.2.1
- SQLite (base intégrée pour test local)
- Bootstrap 5 + Bootswatch United
- Pillow (upload images)
- Flake8 pour la vérification PEP8
- Black pour le formatage automatique du code
- Lighthouse pour vérifier l’accessibilité (WCAG)

###  Qualité du code
- Formatage PEP8 automatisé avec black (line-length: 79)
- Vérification de conformité avec flake8
- Fichier setup.cfg pour paramétrer black et flacke8

##  Données de test

Une base de données est intégrée afin de permettre les tests, voici les utilisateurs : 
- magali (administrateur) : motpasseadmin1
- magnott : motpasse456
- magnott1 : motpasse4561
- magnott2 : motpasse4562
- magnott3 : motpasse4563
- magnott4 : motpasse4564


## Auteur
Projet réalisé par MagNott en juin 2025 dans le cadre du parcours développeur d'application Python chez OpenClassrooms.

