# 🏅 JO 2028 Los Angeles - Data Storytelling & Prédictions
Dashboard Streamlit — Machine Learning — Data Science

## 👥 Équipe
* Imane Guarraz 
* Mathéo Morival


📂 1. Introduction

Ce projet propose une analyse complète des Jeux Olympiques ainsi qu’un système de prédiction des performances pour les JO 2028.
Il combine :

préparation et nettoyage de données

feature engineering avancé

modélisation machine learning

visualisations interactives

un dashboard Streamlit premium

un comparateur de pays


L’objectif : comprendre les dynamiques historiques et anticiper les performances futures.


## 📁 Ressources
* Présentation : https://www.canva.com/design/DAHDcOvILLU/_Ahb1pjapacgmycTzt4osw/edit

## ✅ To Do

- [x] Définition du besoin (ce que l'on cherche à faire dans ce projet)
- [x] Mise en place de l'orga (Share point, Repo git...)
- [x] Choix des technos/outils(collaboration, langages,modèle de llm...)
- [x] Diapo de présentation (mi parcours)
- [x] Trouver les dataset les plus intéressants sur Kaggle
- [x] Nettoyage, normalisation et structuration des données
- [x] Analyse exploratoire (tendances & visualisation globale) - R
- [x] Choix du modèle et Entraînement du LLM - Python
- [x] Création du dashboard dynamique avec différentes visualisations
- [x] Documentation complète du projet
- [x] Diapo de présentation final


## 🛠️ Installation
1. Cloner ce dépôt : `git clone https://github.com/Mathmvl/jo-2028-storytelling.git`
2. Créer un environnement virtuel et l'activer.
3. Installer les dépendances : `pip install -r requirements.txt`



📂 2. Données
2.1. Dataset historique — historique_jo.csv
Les données proviennent de Kaggle et sont opensource.


Contient les résultats des JO passés :

Athlète : Name, Sex, Age

Pays : NOC, Team

Sport : Sport

Année : Year

Médailles : Medal, Medal_encode, has_medal

Features dérivées :

particip_athlete, particip_country

evol_medal_athlete, evol_medal_country

nb_medal_country, nb_medal_athlete

Un mapping NOC → pays est intégré pour enrichir les analyses.

2.2. Dataset prédictif — predictions_2028.csv
Contient les données préparées pour la prédiction :

Variables démographiques

Variables sportives

Variables historiques

Features dérivées

Probabilités prédites :

P_medal : probabilité d’obtenir une médaille

P_gold : probabilité d’obtenir une médaille d’or

🧹 3. Préparation des données
3.1. Nettoyage
suppression des doublons

harmonisation des sports et pays

gestion des valeurs manquantes

correction des incohérences (âge, années, participations)

3.2. Feature Engineering
Création de variables clés :

ratio de médailles par athlète

évolution des performances

participation cumulée

performance du pays

nombre de sports pratiqués

âge normalisé

années depuis la première participation

3.3. Encodage
Sex_encoded

Medal_encode

one-hot encoding pour les sports

3.4. Split & préparation modèle
séparation Homme / Femme

normalisation

sélection de features

train/test split

🤖 4. Modélisation
Le modèle utilisé est un RandomForestClassifier, optimisé via :

GridSearchCV

validation croisée

tuning d’hyperparamètres

Cibles :
P_medal

P_gold

Métriques :
AUC

F1-score

Recall (prioritaire pour détecter les athlètes prometteurs)

📊 5. Analyse des données (Dashboard)
L’onglet Analyse propose :

5.1. Filtres interactifs
Genre

Sport

Pays (NOC)

5.2. Indicateurs globaux
nombre d’athlètes

nombre de pays

taux de médaillés

5.3. Visualisations
Top 10 sports

Top 10 pays

Évolution des performances

Top 20 athlètes

5.4. Comparateur de pays
Comparaison de 2 à 5 pays sur :

nombre total de médailles

taux de médailles

nombre d’athlètes

🔮 6. Prédiction JO 2028 (Dashboard)
L’onglet Prédiction affiche :

6.1. Filtres
Genre

Sport

Pays

Top N

6.2. Indicateurs
nombre d’athlètes

nombre de pays

probabilité moyenne de médaille

6.3. Classements
Top pays (moyenne P_medal)

Top sports

Top athlètes

6.4. Médailles prédites par pays
Méthode utilisée :

somme des probabilités P_medal par pays
(plus réaliste qu’un seuil binaire)

🖥️ 7. Lancement du dashboard
Installation des dépendances
bash
pip install -r requirements.txt
Lancement de l’application
bash
streamlit run app.py
L’application s’ouvre automatiquement dans votre navigateur.

🏗️ 8. Architecture du projet
Code
📁 projet_jo/
│── app.py
│── historique_jo.csv
│── predictions_2028.csv
│── README.md
│── requirements.txt
│── models/
│     └── random_forest.pkl
│── utils/
      └── preprocessing.py
🚧 9. Limites
dépendance à la qualité des données historiques

modèle non spécifique à chaque sport

pas de prise en compte des blessures / actualités récentes

pas de données sur les qualifications réelles 2028

🚀 10. Améliorations possibles
modèles par sport

intégration des JO 2024

simulation de médailles par pays

ajout d’un module de scouting athlètes

prédiction du nombre exact de médailles

🎉 11. Conclusion
Ce projet combine :

Data Engineering

Machine Learning

Visualisation avancée

UX premium

Il constitue une base solide pour analyser les performances olympiques et anticiper les tendances futures.
