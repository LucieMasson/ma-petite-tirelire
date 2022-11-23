## Description du projet
Il s'agit de réaliser une application de tirelire, sous forme d'une API Django.

Comme il s'agit d'un exercice de style en temps limité, certains choix ont été faits qui ne correspondent pas forcément toujours à l'état de l'art.

En particulier:
- L'application n'est pas sécurisée. Django est en mode DEBUG, des paramètres sont en clair ici ou là, le SECRET_KEY est dans un fichier déposé sur le repos GIT. Ce sont des mauvaises pratiques.
- L'URL pour la création du moteur SQLAlchemy est récupéré sous la forme de variables d'environnement au milieu du code. Ici encore c'est par manque de temps pour trouver une meilleure solution.
- L'image Docker de l'API lance directement le runserver Django. Il faudrait configurer un nginx ou guvicorn pour respecter les standards.
- Dans l'idéal il faudrait une doc auto-générée de l'API sous forme de documentation OpenAPI

L'application utilise PostgreSQL comme BDD. La BDD a sa propre image Docker, avec un fichier d'initialisation pour pré-remplir en partie la base.

## Utilisation de l'application
Dans le répertoire racine de l'application, lancer la commande suivante pour construire et lancer les images Docker:

`docker-compose -f build/docker-compose.yml up --build --exit-code-from api`

## Routes disponibles:
- "tirelires" (GET): liste des tirelires existantes, et de leur statut (broken)
  - exemple: `curl -X 'GET' 'http://127.0.0.1:8000/tirelires'`
- "tirelires/create" (POST): création d'une tirelire, en lui donnant un nom. Retourne l'ID de la tirelire
  - exemple: `curl -X 'POST' 'http://127.0.0.1:8000/tirelires/create?name=ours'`
- "tirelires/*ID*/save" (POST): épargne dans une tirelire, en billets et pièces
  - exemple: `curl -X 'POST' 'http://127.0.0.1:8000/tirelires/4/save?coins=1&coins=2&coins=2&notes=100'`
- "tirelires/*ID*/shake" (GET): secoue une tirelire
  - exemple: `curl -X 'GET' 'http://127.0.0.1:8000/tirelires/4/shake'`
- "tirelires/*ID*/smash" (POST): casse une tirelire, la tirelire devient inutilisable
  - exemple: `curl -X 'POST' 'http://127.0.0.1:8000/tirelires/4/smash'`

## Implémentation
Les données persistantes sont stockées dans une BDD PostgreSQL.
Il y a trois éléments:
- *Change*: la liste des pièces et billets existants
- *Piggybank*: les tirelires. Elles ont deux attributs
  - name: le nom de la tirelire
  - broken: si la tirelire est brisée
- *Wealth*: la richesse. C'est simplement une table d'association entre Change et Piggybank

Les modèles sont manipulés par le *PiggyBankManager* (app/service/manager.py) qui est le point central de l'application.

Pour épargner on va ajouter autant de lignes dans *Wealth* qu'il y a de pièces et de billets à ajouter.
Pour secouer et connaitre le contenu d'une tirelire, on somme les valeurs des éléments de *Wealth* pour la tirelire sélectionnée.

Petite subtilité, pour éviter les erreurs d'arrondi liées au stockage de valeurs flottantes, les pièces et billets ont leur
valeur enregistrée en centimes d'euros, sous forme d'entiers. Le *PiggyBankManager* se charge de la conversion en euros
qui est transparente pour le controlleur.


## Arborescence de fichiers
L'application est écrite de façon assez différente de l'arborescence Django standard.

On essaie ici de découpler le plus possible le controlleur (l'API Django) de la partie "intelligente" du système (la gestion des tirelires), qui serait le métier dans un milieu professionnel. On essaie ainsi de dépendre au minimum de frameworks tiers.

C'est aussi pour ça que l'ORM SQLAlchemy a été choisi pour faire persister les données dans une BDD indépendemment de Django, comme une sorte de cas d'école.

Les tests ont été sortis de l'arborescence de l'app afin de ne pas être déployés avec l'applicatif.

 - app: l'application en elle-même, celle qui sera déployée dans l'image Docker
     - controller: l'interface utilisateur, ici avec django_restframework
     - service: le domaine métier
 - build: les fichiers pour préparer le déploiement Docker
 - tests: les tests, TU et TF, du projet. L'arborescence est la même que pour app.


## Lancer les tests
Tests unitaires:

`docker-compose -f build/docker-compose-tests-ut.yml up --build --exit-code-from ut`


Tests fonctionnels:

`docker-compose -f build/docker-compose-tests-ft.yml up --build --exit-code-from ft`
