# Projet NSI 2026: nature et informatique 
## Overgrowth: The beginning of a new are 


**Établissement scolaire de l'équipe** : International french school of singapore (IFS)
**Membre de l'équipe :** Henri Zeman, homme et Lancelot Zeman, homme
**Niveau d’étude :**  première   
**Répartition filles/garçons dans la classe NSI premiere :** 15 garçons et 0 fille

## Résumé du projet :
L'annonce de ce projet NSI nous a très vite inspirés à créer un jeu unique qui se démarque. Après nous être mis d'accord sur le projet : un jeu horrifique avec un style dérangeant où il faut faire des choix pour essayer de survivre à une épidémie mondiale, est né. Nous nous sommes inspirés d'un jeu indépendant appelé « No I'm not human ».

### Naissance de l’idee
Dès l'annonce du projet nous nous sommes directement mit à trouver une idée de jeux vidéo car on savait déjà à l’avance qu’on voulait en faire un. Au debut nous etions pas d’accord sur qu’elle type de jeu faire. Un voulait faire un open world style Pokémon avec des animaux à attraper et sauver, l’autre disait que c'était compliqué et qu’il fallait voir plus petit. On a donc cherché un jeu qu’on avait tous les deux aimé et sur lequel on pouvait s’inspirer : “No I’m not human”. Nous avons ensuite écrit toute l’histoire avec chaque cinématique, chaque dialogues, chaque personnage et chaque morceau de l’environnement. Puis nous avons pu commencer à coder. 

### Problematique initial
Notre problématique initiale était de savoir comment faire un jeu seulement ou presque grâce à python. L’organisation, le temps, les graphismes etc.. Puisque avant ça, on ne savait pas que c'était possible a notre niveau de faire un jeu complet.

### Les objectifs
- Réussir à faire des dialogues qui collent ensemble et qui permettent d'aboutir à une histoire et une fin claire.
- Apprendre à coder un jeu en entier grâce à python.
- Réussir à créer une ambiance oppressante.
- Comment se déplacer dans l’environnement du jeu le plus simplement possible.

### Description 
Overgrowth: the beginning of a new era est donc un jeu horrifique et dérangeant. Sur une Terre devenue apocalyptique en 2174, le but est de survivre à une épidémie mondiale où une plante a pris le contrôle des humains et essaye de contaminer tout le monde pour reprendre le dessus sur notre planète trop polluée. Le  joueur doit survivre à cette épidémie très contagieuse mais qui attaque les humains seul. Le gouvernement met alors en place de la propagande pour que les familles non contaminées aillent voir les humains vivant seuls. Afin d'éviter le plus possible les contaminations. Il faut donc accueillir des gens affaiblis chez soi afin de sauver toi et les autres. 

### Inspiration
Afin de pouvoir faire un jeu de bonne qualité nous nous sommes inspirés des mécaniques du jeu indépendant “No I’m not human”. Grâce à ce jeu et à beaucoup d’imagination nous avons pu écrire tous les dialogues et inventer nos propres personnages humains et hybrides( les personnages contaminés). 


### Presentation de l’equipe

**Les membres:**
- Henri Zeman
- Lancelot Zeman

Nous sommes des élèves de première à l’international French school of singapore (IFS) et nous nous sommes engagés à participer au projet trophée NSI 2026. Avec notre ambition nous avons pu créer un jeu amusant et horrifique ou tout le monde peut s’amuser tout en faisant passer le message qu’il faut moins polluer notre planète.


## Répartition des tâches techniques

**Henri:**

**Création des personnages et de l'environnement (graphisme):**
Grâce à Piskel j’ai pu créer les personnages et l’environnement. Ce sont des graphismes assez simples malgré les détails grâce à l’utilisation de pixel. Tandis que pour l’environnement je me suis aidé de modèle déjà existant sur le site afin de faire une maison simple.

**Le cycle jour/nuit:**
C'est probablement la mécanique la plus importante. Elle utilise *time.time()* (l'horloge réelle de ton ordi) :
9h + 15 heures de jeu compressées en 7 minutes réelles. Quand heure >= 24.0, minuit est atteint.

**Le système de visites aléatoires:**
Chaque jour, 2 personnages sont tirés au sort sans répétition grâce à un set qui mémorise qui est déjà venu :
Ensuite une heure de visite aléatoire leur est assignée entre 10h et 22h. Le jeu vérifie en temps réel si l'heure est atteinte pour faire sonner.

**Les images avec filtre vision nocturne:**
Quand tu fournis une image, elle passe par *appliquer_filtre_nocturne()* qui utilise NumPy pour manipuler chaque pixel :
C'est la formule classique de désaturation + recoloriage en vert. Si NumPy n'est pas installé, un fallback simple est utilisé.


### Lancelot:

**Architecture générale**
Le jeu tourne sur une boucle principale *(boucle_principale())* qui fait 3 choses à chaque frame :
1. Lit les événements (touches clavier)
2. Met à jour la logique (heure, visites, dialogues)
3. Dessine tout à l'écran

**Cinematique**
Grâce au point de vue de la caméra qui bouge et de simples mouvements des objets/personnages dans l'environnement, ça crée des cinématiques propres et simples qui permettent de mettre le joueur dans l’ambiance pesante.

**La génération sonore**
Nous n'avons ajouté aucun fichier audio. Tous les sons sont générés mathématiquement en créant des tableaux d'octets.


**Les effets post-process**
À chaque frame, 3 filtres sont appliqués par-dessus tout le reste :
Effet:
- Saclines = Dessine des rectangles noirs semi-transparents toutes les 4 lignes
- Grain = Place des pixels aléatoires lumineux un peu partout
- Vignette = Dessine des ellipses noires de plus en plus opaques vers les bords
- Glitch = Copie une bande de pixels et la redessine décalée horizontalement

**La navigation entre salles**
Très simple — juste une variable *salle_actuelle* qui change selon la touche :
Et *dessiner()* appelle la bonne fonction selon cette valeur. Chaque salle est redessinée entièrement à chaque frame (pas de cache).

**Le Traqueur de Minuit**
Sa logique est volontairement simple, il n'existe pas avant minuit. À exactement heure >= 24.0, le jeu vérifie une seule condition :
Sa silhouette est dessinée procéduralement avec des *sin()* pour faire bouger les racines et les câbles en temps réel.




**Temps passer:**
Environ 35 heures chacun


### Organisation du travail:
Travail principalement en classe. A chaque cours, nous procédons de cette
manière de séance : en début de cours nous définissons des objectifs
concrets. Et à chaque fois que nous finissons une tâche, nous le faisons savoir à l'autre. Si une partie restait incomplète ou inachevée, on l'indiquait par message sur une discussion prévue pour.


Les grandes étapes du projet
- **1er mois:** idée du jeu, histoire, répartition des tâches, organisation sur toute la période de création du projet.
- **2eme et 3eme mois:** avant de commencer le codage on a appris à coder certaines choses qu’on ne savait pas faire en se renseignant sur les compétences requises pour ce projet. Et création de tout les personnages et décors grâce à pixel
- **4ème et 5ème mois:** codage entier avec réglage des bugs et de l’apprentissage supplémentaire.
- **6eme mois:** vidéo de présentation et dossier technique.



## Les 4 défis techniques les plus complexes

**Lancelot:**
 La génération des sons sans fichiers externes
Le problème: Pygame ne génère pas de sons, il lit des fichiers. Il fallait créer de l'audio en mémoire, sans aucun fichier .mp3 ou .wav.
La solution: Construire manuellement des tableaux d'octets représentant des ondes sonores. Chaque son est une formule mathématique :
Le cri du Traqueur était le plus difficile : une fréquence qui monte progressivement de 200Hz à 1000Hz pendant que le volume descend, avec du bruit aléatoire par-dessus pour l'effet "glitch".

**Henri: Le cycle jour/nuit en temps réel**

Le problème: Compresser 15 heures de jeu (9h à minuit) en exactement 7 minutes réelles, de manière précise, sans que ça décroche ou saute.
La solution: Utiliser *time.time()* plutôt que de compter les frames. Les frames peuvent ralentir si le jeu rame, mais l'horloge système est toujours exacte.
Si on avait compté les frames *(frame × 0.01),* un ralentissement du jeu aurait décalé l'heure et le joueur pourrait "tricher" en surchargeant son ordi.

**Henri: Le filtre vision nocturne sur les images**

Le problème: Les images des personnages sont en couleurs normales. Il fallait les transformer en vert avec un effet vision nocturne sans perdre les détails, et sans que ça soit trop lent à chaque frame.
La solution en deux étapes :
- Étape 1:  appliquer le filtre une seule fois au chargement (pas à chaque frame, sinon c'est trop lent) avec NumPy :
- Étape 2: prévoir un fallback si NumPy n'est pas installé, avec une teinte verte simple moins précise mais qui fonctionne quand même. C'est la dégradation gracieuse : le jeu tourne toujours, juste moins bien.

**Henri et Lancelot: Les salles dessinées entièrement en code**

Le problème: Dessiner des pièces crédibles et détaillées (perspective, ombres, meubles, textures) uniquement avec les primitives de Pygame : rectangles, lignes, ellipses, polygones. Sans images, sans moteur 3D.
La solution, Trois techniques combinées :
- Dégradés simulés : dessiner des centaines de lignes horizontales dont la couleur change légèrement à chaque pixel pour imiter un éclairage
- Perspective manuelle : calculer les coordonnées des lignes de fuite à la main pour le couloir.
- Animations légères : utiliser *math.sin(timer)* pour faire pulser les halos lumineux, bouger la vapeur de la tasse, faire vaciller l'ampoule etc.. ce qui donne un coter plus 
réaliste sans animation réelle.


### 3 idées d'amélioration

**1. Un système de réputation/méfiance**

Actuellement le joueur accepte ou refuse sans conséquence. On pourrait ajouter une jauge de méfiance : refuser trop de monde la fait monter, et à partir d'un certain seuil des événements se déclenchent. Ex: voisins qui se plaignent, couvre-feu imposé, ou au contraire un bonus si tu as bien joué. Ça rendrait chaque décision plus difficile.

**2. Évolution des hybrides dans le temps**

Les hybrides hébergés pourraient se transformer progressivement si tu ne les détectes pas. Un Perso 8 "ordinaire" commencerait sans signe visible, puis après 2 jours une légère lueur rouge apparaîtrait dans son dos, puis au jour 4 ses ongles auraient de la terre. Ce serait plus angoissant qu'un signe présent/absent dès le départ.

**3. Journal de bord du joueur**

Une 5ème pièce (le bureau) où le joueur écrit ses observations sur chaque visiteur. Il pourrait noter "Perso 4 : pieds sales → humain ou hybride ?" et relire ses notes les jours suivants. Ça donnerait une dimension enquête/thriller, une meilleure immersion et aiderait les joueurs à ne pas se perdre sur 5 jours.

## Analyse critique

**Ce qui fonctionne bien:**
L'architecture en classes est solide. La séparation entre *Personnage, SalleManager, EtatJeu et DialogueBox* fait que chaque partie du code a une responsabilité. Ça sépare les responsabilités, et ça facilite beaucoup l'ajout de contenu.
Le choix de générer les sons mathématiquement est techniquement plus beau et rend le jeu entièrement portable : tu n'as pas besoin de distribuer des fichiers audio avec le .py. C'est pratique et bien exécuté.
Le système de fallback à deux niveaux (image réelle → portrait procédural, NumPy → teinte simple) c’est robuste parce que le jeu ne plantera jamais si un fichier manque.

**Les limites les plus “grave”:**
La vignette est très coûteuse en performance et en fait perdre beaucoup. Elle recalcule et redessine des centaines d'ellipses à chaque frame. Sur un ordi peu puissant, c'est elle qui va ralentir le jeu. La solution serait de la précalculer une seule fois au démarrage et de la stocker comme *Surface.*
Les cinématiques ont le même problème: placer 750 pixels aléatoires individuellement à chaque frame avec *surface.set_at()* est une des opérations les plus lentes en Pygame. Un tableau NumPy ou une surface pré-générée renouvelée toutes les 3 frames serait bien plus rapide.
La logique de jeu et le dessin sont mélangés dans certains endroits. Ex:  *_dessiner_couloir()* vérifie *jeu.visiteur_en_attente* pour décider quoi afficher . C'est la logique qui se mélange dans le rendu. Dans un projet plus grand, ça deviendrait difficile à maintenir.
Il n'y a pas de sauvegarde. Si tu fermes le jeu au jour 3, tu recommences depuis le début. Pour un jeu de 5 jours ce n'est pas grave car il se finit en 50 minutes max, mais c'est une limite si on faisait quelque chose de plus grand.


### Competences techniques developpé

Nous avons tout les deux presque tout appris sur le tas. A par les choses basiques que nous savions déjà faire grâce au cours de NSI. Les  tutos, l'aide du professeur et de nos camarades nous a permis d'apprendre et de découvrir beaucoup de nouvelles choses.