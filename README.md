
# 🏅 JO 2028 Los Angeles - Data Storytelling & Prédictions
Dashboard Streamlit — Machine Learning — Data Science

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

## 2.1. Dataset historique — `historique_jo.csv`

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

---

## 2.2. Dataset prédictif — `predictions_2028.csv`

Contient les données préparées pour la prédiction :

- Variables démographiques  
- Variables sportives  
- Variables historiques  
- Features dérivées  
- Probabilités prédites :  
  - `P_medal` : probabilité d’obtenir une médaille  
  - `P_gold` : probabilité d’obtenir une médaille d’or  

---

# 🧹 3. Préparation des données

## 3.1. Nettoyage

- suppression des doublons  
- harmonisation des sports et pays  
- gestion des valeurs manquantes  
- correction des incohérences (âge, années, participations)  

## 3.2. Feature Engineering

Création de variables clés :

- ratio de médailles par athlète  
- évolution des performances  
- participation cumulée  
- performance du pays  
- nombre de sports pratiqués  
- âge normalisé  
- années depuis la première participation  

## 3.3. Encodage

- `Sex_encoded`  
- `Medal_encode`  
- one-hot encoding pour les sports  

## 3.4. Préparation modèle

- séparation Homme / Femme  
- normalisation  
- sélection de features  
- train/test split  

---

# 🤖 4. Modélisation

Modèle utilisé : **RandomForestClassifier**, optimisé via :

- GridSearchCV  
- validation croisée  
- tuning d’hyperparamètres  

### Cibles :

- `P_medal`  
- `P_gold`  

### Métriques :

- AUC  
- F1-score  
- Recall  

---

# 📊 5. Analyse des données (Dashboard)

L’onglet **Analyse** propose :

## 5.1. Filtres interactifs

- Genre  
- Sport  
- Pays (NOC)  

## 5.2. Indicateurs globaux

- nombre d’athlètes  
- nombre de pays  
- taux de médaillés  

## 5.3. Visualisations

- Top 10 sports  
- Top 10 pays  
- Évolution des performances  
- Top 20 athlètes  

## 5.4. Comparateur de pays

Comparaison de 2 à 5 pays sur :

- nombre total de médailles  
- taux de médailles  
- nombre d’athlètes  

---

# 🔮 6. Prédiction JO 2028 (Dashboard)

L’onglet **Prédiction** affiche :

## 6.1. Filtres

- Genre  
- Sport  
- Pays  
- Top N  

## 6.2. Indicateurs

- nombre d’athlètes  
- nombre de pays  
- probabilité moyenne de médaille  

## 6.3. Classements

- Top pays (moyenne P_medal)  
- Top sports  
- Top athlètes  

## 6.4. Médailles prédites par pays

Méthode utilisée :

> somme des probabilités P_medal par pays  
> (plus réaliste qu’un seuil binaire)

---

# 🖥️ 7. Lancement du dashboard

## Installation des dépendances

```bash
pip install -r requirements.txt
