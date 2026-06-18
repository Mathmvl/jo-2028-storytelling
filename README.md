
# 🏅 JO 2028 Los Angeles - Data Storytelling & Prédictions
Dashboard Streamlit — Machine Learning — Data Science


Ce projet consiste à analyser les performances des athlètes aux Jeux Olympiques 2024 et à prédire les résultats potentiels des Jeux Olympiques 2028 grâce à un modèle de machine learning. 

À partir d’un jeu de données historique enrichi, le travail inclut un important pipeline de préparation : nettoyage, normalisation, création de variables, sélection des athlètes récents et dédoublonnage par identifiant unique. Un modèle Random Forest a ensuite été entraîné pour estimer la probabilité qu’un athlète remporte une médaille ou une médaille d’or. 

L’ensemble est intégré dans une application Streamlit interactive composée de deux onglets : un premier dédié à l’analyse descriptive des JO 2024 (médailles, pays, sports, KPIs), et un second consacré aux prédictions 2028, incluant un classement des athlètes, des pays, un seuil ajustable de médaille et une comparaison entre les performances réelles de 2024 et les résultats prédits pour 2028. 

Ce projet offre ainsi un outil complet permettant d’explorer les dynamiques olympiques, d’anticiper les tendances futures et de visualiser les évolutions potentielles des nations et des athlètes.


## 👥 Équipe
* Imane Guarraz  
* Mathéo Morival  

---

## 📁 Ressources
* Présentation : https://www.canva.com/design/DAHDcOvILLU/_Ahb1pjapacgmycTzt4osw/edit


---

# 📘 1. Introduction

Ce projet propose une analyse complète des Jeux Olympiques ainsi qu’un système de prédiction des performances pour les JO 2028 à Los Angeles.  
Il combine :

- Data storytelling  
- Analyse exploratoire  
- Feature engineering avancé  
- Modélisation machine learning  
- Visualisations interactives  
- Dashboard Streamlit premium  

Objectif : comprendre les dynamiques historiques et anticiper les performances futures des athlètes, pays et sports.

---

# 📂 2. Données

## Dataset historique — `historique_jo.csv`

Contient les résultats des JO passés :

- Identité : `Name`, `Sex`, `Age`  
- Pays : `NOC`, `Team`  
- Sport : `Sport`  
- Année : `Year`  
- Médailles : `Medal`, `Medal_encode`, `has_medal`  
- Features dérivées :  
  - `particip_athlete`, `particip_country`  
  - `evol_medal_athlete`, `evol_medal_country`  
  - `nb_medal_country`, `nb_medal_athlete`  

Un mapping **NOC → pays** est intégré pour enrichir les analyses.


## Dataset prédictif — `predictions_2028.csv`

Contient les données préparées pour la prédiction :

- Variables démographiques  
- Variables sportives  
- Variables historiques  
- Features dérivées  
- Probabilités prédites :  
  - `P_medal` : probabilité d’obtenir une médaille  
  - `P_gold` : probabilité d’obtenir une médaille d’or  

---

# 🧹 3. Préparation et nettoyage des données

- **Contrôles initiaux**
  - Vérification des valeurs nulles (`df.isna().sum()`) et des doublons (`df.duplicated().sum()`).
  - Suppression de la colonne `Season` (valeur unique, non informative).

- **Filtrage des pays et des années**
  - Suppression des NOC obsolètes : `['URS', 'GDR', 'FRG', 'EUN']` (< 5 % des données).
  - Conservation uniquement des éditions `Year > 1960` pour un périmètre moderne et comparable.

- **Enrichissement avec les âges**
  - Chargement de `olympics_age.csv`.
  - Nettoyage des noms (`clean_name` via `unidecode`, minuscules, espaces normalisés).
  - Harmonisation des champs (`sex` → `Sex`, `noc` → `NOC`, `year` → `Year`).
  - Merge souple sur `["last_name", "Sex", "NOC", "Year"]`.
  - Taux de matching âge ≈ 87 %, imputation des `Age` manquants par la moyenne.

- **Normalisation des variables cibles**
  - Nettoyage de `Medal` (strip, lower, `fillna("no medal")`).
  - Encodage des médailles : `no medal=0`, `bronze=1`, `silver=2`, `gold=3` → `Medal_encode`.
  - Création d’un score cumulatif par athlète : `Medal_score` et `Medal_score_athlete_total`.
  - Indicateur binaire `has_medal` (athlète a-t-il déjà gagné une médaille ?).

- **Features athlètes**
  - `particip_athlete` : nombre de participations par athlète.
  - `nb_team` : nombre d’équipes distinctes par athlète/pays/année.
  - `nb_medal_athlete` : nombre total de médailles par athlète.
  - `evol_medal_athlete` : médailles cumulées avant l’édition courante.

- **Features pays (NOC)**
  - `particip_pays` : nombre d’éditions distinctes par pays.
  - `nb_athlete_country` : nombre d’athlètes par pays/année.
  - `nb_sport_country` : nombre de sports distincts par pays/année.
  - `medal_score_country_total` et `nb_medal_country` : score et volume de médailles par pays/année.
  - Construction d’un dataframe `country_yearly` pour :
    - `evol_medal_country` : médailles cumulées dans le temps.
    - `nb_athletes`, `nb_medals`, `medal_rate` (taux de médailles).
    - `athlete_medal_ratio` : ratio athlètes / taux de médailles.

- **Contexte pays hôte**
  - Dictionnaire `host_countries` (Year → host_NOC).
  - Merge sur `Year`, création de `is_host_country` (binaire).

- **Filtre de récence**
  - `first_year_athlete` : première participation par `player_id`.
  - `years_since_first` : années depuis les débuts.
  - `recent_athlete` : athlètes avec `years_since_first <= 20`.

- **Nettoyage final**
  - Suppression de `Name` et `last_name`, renommage de `clean_name` en `Name`.
  - Suppression définitive de `Season`.

- **Réduction de la multicolinéarité (VIF)**
  - Sélection d’un sous-ensemble de features quantitatives (`cols_vif`).
  - Calcul du VIF (`variance_inflation_factor`) et suppression des variables redondantes.
  - Conservation d’un set de variables stable pour la modélisation (`has_medal` / `Medal_encode` exclues car cibles).

---

# 4. Sélection et évaluation des variables

Ce module réalise une analyse univariée complète pour mesurer la capacité prédictive de chaque variable numérique et catégorielle vis‑à‑vis des cibles :

- `has_medal` (binaire)
- `Medal_encode` (multiclasse : 0–3)

L’objectif est d’identifier les features réellement informatives avant la modélisation.

---

## 📌 1. AUC — Analyse univariée (binaire & multiclass)

- Modèle utilisé : `LogisticRegression`
- Pour chaque variable numérique :
  - entraînement d’un modèle 1‑variable → prédiction → calcul AUC
  - version binaire (`has_medal`)
  - version multiclasse (`Medal_encode`, OVR)

**Interprétation :**
- `AUC = 1.00` → prédiction parfaite  
- `AUC = 0.50` → aléatoire  
- `< 0.50` → variable inutile  

Les variables sont ensuite triées par importance décroissante.

---

## 📌 2. Mutual Information (MI) — Numérique

- Méthode : `mutual_info_classif`
- Mesure la dépendance **non linéaire** entre chaque variable et la cible.
- Calculée pour :
  - `has_medal`
  - `Medal_encode`

**Interprétation MI :**
- `> 0.25` → dépendance très forte  
- `0.05 – 0.10` → dépendance moyenne  
- `0.01 – 0.05` → faible  
- `< 0.01` → quasi inutile  

---

## 📌 3. Corrélation point‑bisériale (binaire uniquement)

- Méthode : `pointbiserialr`
- Mesure la corrélation entre une variable numérique et une cible binaire.

**Interprétation :**
- `> 0.30` → très forte dépendance  
- `0.10 – 0.30` → moyenne  
- `0.02 – 0.10` → faible  
- `< 0.02` → négligeable  

---

## 📌 4. Chi² — Variables catégorielles

- Sélection des colonnes catégorielles à faible cardinalité (`< 50 modalités`)
- Encodage via `OneHotEncoder(drop="first")`
- Calcul du Chi² pour :
  - `has_medal`
  - `Medal_encode`

**Attention :**
- Les colonnes dérivées de `Medal` (ex : `Medal_gold`, `Medal_silver`) explosent logiquement les scores → **fuite de cible**.
- Les colonnes `City_*` ont un Chi² très faible → **peu informatives**.
- `host_NOC` a un effet réel mais faible.

---

## 📌 5. Mutual Information — Catégoriel

- Encodage OHE identique au Chi²
- Calcul MI sur les variables catégorielles encodées
- Tri décroissant pour identifier les catégories les plus informatives

---

## 📌 6. Définition du dataframe final pour la modélisation

### 🎯 Cible :
- `has_medal`
- `Medal_encode`

### ❌ Variables supprimées (faible valeur prédictive ou redondance) :
- `particip_athlete`
- `first_year_athlete`
- `years_since_first`
- `Year`
- `recent_athlete` (utile uniquement pour filtrer les athlètes actifs)
- `Sex`
- `City`
- `host_NOC`
- `Team`
- `Event`
- `Name`

### ✔ Variables conservées dans `df_model` :
- `player_id`, `Name`, `NOC`, `Sport`
- `Age`, `Sex_encoded`
- `nb_team`, `particip_pays`, `nb_athlete_country`
- `nb_sport_country`, `nb_athletes`, `nb_medals`
- `medal_rate`, `athlete_medal_ratio`
- `is_host_country`, `recent_athlete`
- `has_medal`, `Medal_encode`

## 📦 Résultat

Un dataframe final propre, réduit, non redondant et optimisé pour l’entraînement du modèle prédictif, basé sur une analyse univariée complète (AUC, MI, Chi², corrélation).

---

## 🤖 5. Modélisation — Construction, entraînement et évaluation du modèle

La modélisation repose sur un pipeline supervisé visant à prédire :

- `has_medal` (probabilité de remporter une médaille)
- `Medal_encode` (type de médaille : 0 = aucune, 1 = bronze, 2 = argent, 3 = or)

### 🔧 1. Préparation des données pour le modèle
- Sélection du dataframe final `df_model` contenant :
  - variables athlètes : âge, nb_team, nb_medals, medal_rate…
  - variables pays : nb_athletes, nb_sport_country, athlete_medal_ratio…
  - contexte : is_host_country, recent_athlete
  - cibles : `has_medal`, `Medal_encode`
- Suppression des colonnes non informatives ou redondantes :
  - `Year`, `City`, `Team`, `Event`, `Sex`, `recent_athlete`, `first_year_athlete`, etc.
- Normalisation et encodage :
  - `Sex_encoded` (M=1, F=0)
  - Variables catégorielles traitées via OneHotEncoder si nécessaire.

### 🧪 2. Split & équilibrage
- Séparation train/test (80/20).
- Vérification de l’équilibre des classes (fort déséquilibre → beaucoup de "no medal").
- Possibilité d’utiliser :
  - `class_weight="balanced"`
  - ou un sur-échantillonnage (SMOTE) selon les tests.

### 🌲 3. Modèle utilisé : Random Forest Classifier
- Justification :
  - robuste aux non‑linéarités,
  - gère bien les interactions,
  - peu sensible au scaling,
  - interprétable via feature importance.
- Hyperparamètres principaux :
  - `n_estimators`
  - `max_depth`
  - `min_samples_split`
  - `class_weight`

### 📈 4. Évaluation du modèle
- Métriques utilisées :
  - AUC (binaire et multiclass)
  - F1‑score
  - Accuracy
  - Matrice de confusion
- Analyse des performances :
  - Très bon AUC sur `has_medal`
  - AUC multiclass plus faible (normal : classes déséquilibrées)
  - Importance des variables cohérente :
    - `medal_rate`, `athlete_medal_ratio`, `nb_medals`, `Age`, `is_host_country`

### 🔮 5. Génération des prédictions
- Le modèle produit :
  - `P_medal` : probabilité de médaille
  - `P_gold` : probabilité d’or
- Ajout d’un seuil ajustable dans le dashboard :
  - `P_medal >= seuil` → 1 médaille prédite
- Filtrage final :
  - uniquement `recent_athlete == 1`
  - dédoublonnage par `player_id`

---

## 📊 6. Dashboard Streamlit — Architecture & fonctionnalités

L’application Streamlit est organisée en **deux onglets principaux** : Analyse (2024) et Prédiction (2028).


### 🟦 1. Onglet Analyse — Résultats réels JO 2024

#### 🔍 Filtres interactifs
- Année
- Sport
- Pays
- Genre

#### 📌 Indicateurs clés (KPIs)
- Total médailles
- Nombre de pays représentés
- Taux de médailles
- Nombre de sports

#### 📊 Visualisations
- Top 10 pays (bar chart)
- Top 10 sports (bar chart)
- Distribution des médailles
- Analyse dynamique selon les filtres

👉 **Aucune prédiction dans cet onglet.**


### 🟧 2. Onglet Prédiction — JO 2028

#### 🎛 Filtres prédiction
- Genre
- Sport
- Pays
- Top N athlètes
- Seuil médaille (slider)

#### 🥇 Top pays (prédictions)
- Moyenne des probabilités `P_medal`
- Classement dynamique selon les filtres

#### 🧍 Top athlètes
- Triés par `P_medal`
- Affichage des 10/20/50 meilleurs selon le paramètre Top N

#### 🔄 Comparaison JO 2024 vs JO 2028
- Basée sur :
  - `recent_athlete == 1`
  - `drop_duplicates("player_id")`
  - seuil médaille
- Tableau final :
  - `Medals_2024`
  - `Pred_2028`
  - `Évolution`

#### 📈 Visualisations supplémentaires
- Évolution par pays
- Répartition des probabilités
- Analyse par sport

---

## 🧩 Résultat final

Le projet combine :

- un pipeline de préparation de données complet,
- une modélisation robuste basée sur Random Forest,
- un système de scoring probabiliste,
- un dashboard interactif permettant :
  - d’explorer les JO 2024,
  - de prédire les JO 2028,
  - de comparer les deux éditions.

Le tout dans une architecture claire, modulaire et adaptée à une utilisation métier.

