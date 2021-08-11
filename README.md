# LITReview

Openclassroom projet 9

Ce projet est une application web à but pédagogique à exécuter localement. Cette application permets de gérer un système de ticket et de review entre différent utilisateur.
Cette application est un MVP, la partie Front-end de l'application est donc présente uniquement pour présenter les différentes fonctionnalitées.

### Installation et exécution de l'application

1.  Cloner ce dépôt de code à l'aide de la commande  `$ git clone https://github.com/GuillaumeRobin10/ocp9.git`
2.  Rendez-vous dans le dossier ocp9 avec la commande `$ cd ocp9`
3.  Créer un environnement virtuel pour le projet avec  `$ python -m venv env`  sous Windows ou  `$ python3 -m venv env`  sous MacOS ou Linux.
4.  Activez l'environnement virtuel avec  `$ env\Scripts\activate`  sous Windows ou  `$ source env/bin/activate`  sous MacOS ou Linux.
5.  Installez les dépendances du projet avec la commande  `$ pip install -r requirements.txt`
6.  Lancer l'application depuis le dossier LITReview avec la commande `$ python3 manage.py runserver`

## Utilisation et documentation

Dans cette application vous avez la possibilité de vous créer un compte ou de vous connecté avec un compte déjà existant.
afin de connaître les comptes existants vous pouvez vous connecter en tant que superutilisateur à l'url `http://127.0.0.1:8000/admin`.
l'identifiant du compte superutilisateur est le suivant : `admin` et le mot de passse `admin`.

lorsque vous êtes connecté à la plateforme classique de l'application (`http://127.0.0.1:8000/home`) vous pouvez créer des critiques ou en demander.

Vous pouvez également suivre des utilisateurs afin de voir leurs critiques et leurs tickets.

La page Posts permet de voir vos posts. 

La page Flux permet de voir les tickets des utilisateurs que vous suivez ainsi que les réponses à vos tickets.

Enfin vous pouvez vous déconnecter.
