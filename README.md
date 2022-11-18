## Description du projet
Il s'agit de réaliser une application de tirelire, sous forme d'une API Django.

Comme il s'agit d'un exercice de style en temps limité, certains choix ont été faits qui ne correspondent pas forcément toujours à l'état de l'art.

En particulier:
- L'application n'est pas sécurisée. Django est en mode DEBUG, des paramètres sont en clair ici ou là, le SECRET_KEY est dans un fichier déposé sur le repos GIT. Ce sont des mauvaises pratiques.
- L'URL pour la création du moteur SQLAlchemy est récupéré sous la forme de variables d'environnement au milieu du code. Ici encore c'est pas manque de temps pour trouver une meilleure solution.
- L'image Docker de l'API lance directement le runserver Django. Il faudrait configurer un nginx ou guvicorn pour respecter les standards.
- Dans l'idéal il faudrait une doc auto-générée de l'API sous forme de documentation OpenAPI

L'application utilise PostgreSQL comme BDD. La BDD a sa propre image Docker, avec un fichier d'initialisation pour pré-remplir en partie la base.

## L'utilisation de l'application
Dans le répertoire racine de l'application, lancer la commande suivante pour construire et lancer les images Docker:
`docker-compose -f build/docker-compose.yml up --build --exit-code-from api`


## Arborescence de fichiers
L'application est écrite de façon assez différente de l'arborescence Django standard.

On essaie ici de découpler le plus possible le controller (l'API Django) de la partie "intelligente" du système (la gestion des tirelires), qui serait le métier dans un milieu professionnel. On essaie ainsi de dépendre au minimum de frameworks tiers.

C'est aussi pour ça que l'ORM SQLAlchemy a été choisi pour faire persister les données dans une BDD indépendemment de Django, comme une sorte de cas d'école. On pourrait imaginer découpler aussi les fonctionnalités d'accès à la BDD du métier lui-même.

Les tests ont été sortis de l'arborescence de l'app afin de ne pas être déployés avec l'applicatif.

 - app: l'application en elle-même, celle qui sera déployée dans l'image Docker
     - controller: l'interface utilisateur, ici avec django_restframework
     - service: le domaine métier
 - build: les fichiers pour préparer le déploiement Docker
 - tests: les tests, TU et TF, du projet. L'arborescence est la même que pour app.
