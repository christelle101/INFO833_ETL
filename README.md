# INFO833 | Extract - Transform - Load


Un ETL est un logiciel permettant d'intégrer des grands volumes de données de différents types, en provenance de différentes sources. Il extrait les données brutes, les restructure et enfin les charge dans un Data Warehouse. Ces opérations sont réalisées en temps réel et permettent d'enrichir les données et de prendre en charge des milliards de transactions.

La finalité du TP est d'implémenter un système de gestion d'ETL à large échelle en fixant un certain nombre de tâches à traiter. Nous avons choisi d'implémenter 3 tâches dans le projet.

## 💭 Un ETL avec Redis
### 1️⃣ ETL de base
On construit un fichier tasks.py qui contient la définition de toutes les tâches. Connaissant les paramètres et le nom d'une tâche, on peut ainsi l'exécuter dans n'importe quel cluster. On suppose ensuite qu'on va exécuter une séquence de tâches : T1, suivi de T2, puis de T3, etc. Les paramètres d'entrée sont générés dans une file qu'on appelle task_queue, que le programme lit pour pouvoir instancier la prochaine tâche à faire. La file se vide quand le traitement est terminé.

Cette conception est implémentée dans le fichier **main_ETL.py**. 

### 2️⃣ Un ETL avec un cache Redis
On suppose que task_queue est mise en place sous Redis en tant que liste et on implémente le même système ETL qu'en première partie.
Sachant que nous avions déjà Redis sur nos machines, nous n'avons pas utilisé d'image Docker mais plutôt la commande *redis-server* dans le terminal.

Cette conception est implémentée dans le fichier **redis_ETL.py**.

### 3️⃣ Multiprocessing
> Python ne permet pas de faire du parallélisme au niveau thread à cause du GIL (Global Interpreter Lock) qui est une exclusion mutuelle destinée à intégrer plus facilement les librairies externes et à exécuter le code non-parallèle plus rapidement tout en sécurisant les threads. En effet, la gestion de la mémoire en Python n'est pas sûre au niveau thread. Le GIL permet donc d'éviter les conflits de concurrence, mais le prix à payer reste le parallélisme massif au niveau thread dans ce langage.

Dans cette partie, on tente d'appliquer le multiprocessing à notre ETL.

Cette conception est implémentée dans le fichier **multiprocessing_ETL.py**.

## 🧶 Un ETL avec MapReduce
L'objectif est ici de combiner MapReduce et l'aspect pubsub de Redis. Ce procédé est tout d'abord appliqué sur [Killer Queen du groupe Queen](https://raw.githubusercontent.com/christelle101/INFO833_ETL/main/MapReduce/tst.txt?token=GHSAT0AAAAAABROFS3BDP66ZKIUA2IXSN7QYUIAFCQ) pour tester, puis sur un plus gros fichier : [les sonnets de Shakespeare](https://raw.githubusercontent.com/christelle101/INFO833_ETL/main/MapReduce/t8.shakespeare.txt?token=GHSAT0AAAAAABROFS3AYLLUP7DPBEWPJPJOYUIAF6A).

L'objectif était d'écrire un fichier JSON avec les occurrences de chaque mot. Toutefois, nous ne sommes pas encore parvenus à réaliser cela à cause d'une erreur qui doit être présente dans le code. Pour le moment, nous avons le fichier **dumbp.rdb** qui a été généré par Redis.