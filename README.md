# JO 2028 - Prédictions de médailles avec ML

Un projet où on essaie de prédire qui va médailler aux Jeux Olympiques de Los Angeles 2028. On a fouillé 60 ans de données olympiques pour entraîner un modèle XGBoost qui fait du vrai du boulot (AUC ~0.82, c'est pas mal).

**Mathéo & Imane** | Ynov B3 - Spécialité Data & IA

---

## Structure

```
b3-projet-jo-2028/
├── PORJET_FIL_ROUGE_MachineLearning_JO2028.ipynb  ← Le gros du travail
├── app.py                                          ← Dashboard interactif
├── Investigations.ipynb                            ← Analyse des features
├── requirements.txt
├── data/
│   ├── data brut/
│   └── data clean/                                 ← predictions_JO28.csv (sortie)
└── models/
```

## Démarrage rapide

### 1. Installation

```bash
# Clone & setup env
git clone https://github.com/Mathmvl/jo-2028-storytelling.git
cd b3-projet-jo-2028

python -m venv venv
venv\Scripts\activate  # Windows
# ou: source venv/bin/activate

pip install -r requirements.txt
```

### 2. Exécuter le notebook ML

```bash
jupyter notebook PORJET_FIL_ROUGE_MachineLearning_JO2028.ipynb
```

Ça prend 20-30 min. À la fin tu as `predictions_JO28.csv` avec les prédictions.

### 3. Lancer le dashboard

```bash
streamlit run app.py
```

S'ouvre sur `localhost:8501`. Tu peux filter par pays, sport, âge, etc.
## Comment ça marche

1. **Préparation des données** — Fusion 300k+ lignes d'athlètes + données d'âge. Énorme boulot de matching sur les noms (94% de succès, pas mal).

2. **Exploratory Analysis** — Distribution des médailles, corrélations, patterns bizarres (genre l'âge a quasi aucun effet direct).

3. **Feature engineering** — On crée 10 features: combien de médailles tu as gagnées avant, dans quel pays tu es, quel sport, etc. Les historiques > tout.

4. **Modèle XGBoost** — Split temporel: train sur ≤2016, test sur 2020+2024. Scale pos_weight pour gérer que 85% des athlètes ne médaillent jamais. AUC ~0.82.

5. **Prédictions 2028** — On prend le dernier snapshot de chaque athlète (2016/2020/2024), on prédit, et voilà.

**Top features qui comptent vraiment:**
- Combien de médailles tu as gagnées avant
- Combien de fois t'es allé aux JO
- La force du sport en général
- Le nombre d'athlètes du pays (oui, c'est un signal)

(L'âge? Franchement pas grand chose. Les gens médaillent à peu près au même âge qu'ils participent non-médaillés.)
**Performance**: ROC-AUC = 0.82 ✅

---

## 🎨 Dashboard Streamlit

### 5 Onglets principaux

| Onglet | Contenu |
|--------|---------|
| **🥇 Top Athletes** | Athlètes prédits médaillés, ranking, distribution probabilités |
| **🌍 Countries** | Classement pays, top 15 bar chart, distribution continents |
| **⚽ Sports** | Ranking des sports, performances par discipline |
| **📊 Analytics** | Âge vs probabilité, genre, tendances historiques |
| **📋 Raw Data** | Données filtrées + export CSV |

### Filtres disponibles
## Dashboard

5 onglets pour explorer les prédictions:

- **Top Athlètes** — Les prédictions top, classées par probabilité
- **Par pays** — Top 15 pays, combien de médailles attendues
- **Par sport** — Hockey, natation, etc. qui a le plus de shots
- **Analytics** — Âge vs proba, répartition genre, tendances
- **Données brutes** — Filter ce que tu veux, export CSV

Filtres: pays, sport, âge, genre, seuil de probabilité.

## Trucs intéressants qu'on a découvert

- **85% ne médaillent jamais** — C'est brutal. Participer c'est déjà cool mais les médailles c'est rare.
- **USA domine évidemment** — 3500+ participations médaillées. GBR, FRA loin derrière.
- **Hockey = money** — Plus de médaillés prédits que natation ou athlétisme (parce que les pools sont petits mais denses).
- **L'âge c'est pas ça** — Même corrélation entre médaillés et non-médaillés. C'est l'expérience qui compte, pas les bougies.
- **Gender gap** — 70% d'hommes. Les femmes arrivent mais t'as des sports où c'est encore très déséquilibré.

## Fichiers principaux

- `PORJET_FIL_ROUGE_MachineLearning_JO2028.ipynb` — Tout le ML (données→modèle→prédictions). Exécute ça en premier.
- `Investigations.ipynb` — Deep dive sur chaque feature. Pourquoi telle feature marche ou pas.
- `app.py` — Dashboard Streamlit. Visualisation interactive des prédictions.
- `requirements.txt` — Dépendances (pandas, xgboost, streamlit, etc.)

## Dépendances

```
pandas, numpy, scikit-learn, xgboost, matplotlib, seaborn, streamlit, scipy, jupyter
```

```bash
pip install -r requirements.txt
```

## Petit guide

**Le notebook est long?** Ouais, 20-30 min. Va prendre un café, une barre de progression s'affiche.

**Où sont les prédictions?** Dans `./data/data clean/predictions_JO28.csv` après que le notebook ait fini.

**Je veux tester d'autres modèles?** Modifie la cellule "Modèle principal" du notebook.

**Ça marche pas?** Vérifie que:
1. Tu as bien lancé le notebook complet
2. Tes versions des packages sont à jour (`pip list`)
3. Les dossiers data/ et models/ existent

---

Fait par **Mathéo** & **Imane** | Ynov B3 2026 
