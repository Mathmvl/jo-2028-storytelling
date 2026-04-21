"""
🏅 JO 2028 LOS ANGELES - DASHBOARD DE PRÉDICTIONS
Application Streamlit pour explorer les données olympiques et prédictions JO 2028
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# ============================
# CONFIG & SETUP
# ============================
st.set_page_config(
    page_title="JO 2028 Dashboard",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #032361;
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-card {
        background: linear-gradient(135deg, #032361 0%, #1e5a96 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin: 10px;
    }
    .prediction-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        margin: 5px 0;
    }
    .medal {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ============================
# CHARGEMENT DES DONNÉES
# ============================
@st.cache_data
def load_data():
    """Charger les données de prédictions"""
    predictions_path = "./data/data clean/predictions_JO28.csv"
    
    if os.path.exists(predictions_path):
        return pd.read_csv(predictions_path)
    else:
        st.error(f"❌ Fichier non trouvé: {predictions_path}")
        st.info("Assurez-vous d'avoir exécuté le notebook complet pour générer les prédictions.")
        return None

df = load_data()

if df is not None:
    # Compatibilite: certaines versions du pipeline exportent moins de colonnes.
    if "nb_medal_athlete" not in df.columns:
        df["nb_medal_athlete"] = 0
    if "particip_athlete" not in df.columns:
        df["particip_athlete"] = 0

    # ============================
    # HEADER
    # ============================
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h1 class="main-header">🏅 JO 2028 - DASHBOARD PRÉDICTIONS</h1>', unsafe_allow_html=True)
    
    st.markdown("**Los Angeles 2028 - Predictions & Analytics**")
    st.divider()
    
    # ============================
    # SIDEBAR - FILTRES
    # ============================
    st.sidebar.header("🎛️ FILTRES & PARAMÈTRES")
    
    # Sélection des pays
    all_countries = sorted(df["NOC"].unique())
    selected_countries = st.sidebar.multiselect(
        "🌍 Sélectionner les pays",
        all_countries,
        default=["USA", "CHN", "GBR", "FRA", "JPN"],
        key="countries_filter"
    )
    
    # Sélection des sports
    all_sports = sorted(df["Sport"].unique())
    selected_sports = st.sidebar.multiselect(
        "⚽ Sélectionner les sports",
        all_sports,
        key="sports_filter"
    )
    
    # Seuil de médaille
    prob_threshold = st.sidebar.slider(
        "🎯 Seuil de probabilité de médaille",
        0.0, 1.0, 0.5, 0.05,
        help="Probabilité minimale pour classer comme 'médaillable'"
    )
    
    # Genre
    genders = st.sidebar.multiselect(
        "👥 Genre",
        df["Sex"].unique(),
        default=df["Sex"].unique(),
        key="gender_filter"
    )
    
    # Filtre d'âge
    age_range = st.sidebar.slider(
        "📊 Âge de l'athlète",
        int(df["Age"].min()), int(df["Age"].max()),
        (int(df["Age"].min()), int(df["Age"].max())),
        key="age_filter"
    )
    
    # ============================
    # APPLICATION DES FILTRES
    # ============================
    filtered_df = df.copy()
    
    if selected_countries:
        filtered_df = filtered_df[filtered_df["NOC"].isin(selected_countries)]
    
    if selected_sports:
        filtered_df = filtered_df[filtered_df["Sport"].isin(selected_sports)]
    
    filtered_df = filtered_df[
        (filtered_df["Age"] >= age_range[0]) & 
        (filtered_df["Age"] <= age_range[1])
    ]
    
    filtered_df = filtered_df[filtered_df["Sex"].isin(genders)]
    
    # Prédictions
    filtered_df["prediction"] = (filtered_df["jo28_medal_proba"] >= prob_threshold).astype(int)
    
    # ============================
    # KPIs PRINCIPAUX
    # ============================
    st.subheader("📊 INDICATEURS CLÉS")
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)
    
    with kpi_col1:
        st.metric(
            "👥 Athlètes",
            len(filtered_df),
            delta=f"Total: {len(df)}"
        )
    
    with kpi_col2:
        medalists = filtered_df["prediction"].sum()
        st.metric(
            "🥇 Prédits médaillés",
            medalists,
            delta=f"{100*medalists/max(len(filtered_df), 1):.1f}%"
        )
    
    with kpi_col3:
        avg_proba = filtered_df["jo28_medal_proba"].mean()
        st.metric(
            "📈 Proba moyenne",
            f"{avg_proba:.1%}",
            delta=f"Min: {filtered_df['jo28_medal_proba'].min():.1%}"
        )
    
    with kpi_col4:
        countries = filtered_df["NOC"].nunique()
        st.metric(
            "🌍 Pays",
            countries,
            delta=f"Total: {df['NOC'].nunique()}"
        )
    
    with kpi_col5:
        sports = filtered_df["Sport"].nunique()
        st.metric(
            "🏅 Sports",
            sports,
            delta=f"Total: {df['Sport'].nunique()}"
        )
    
    st.divider()
    
    # ============================
    # ONGLETS
    # ============================
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🥇 Top Athlètes",
        "🌍 Classement Pays",
        "⚽ Classement Sports",
        "📊 Analyses",
        "📋 Données Brutes"
    ])
    
    # ============================
    # TAB 1: TOP ATHLÈTES
    # ============================
    with tab1:
        st.header("🥇 TOP ATHLÈTES - PRÉDICTIONS JO28")
        
        # Trier et afficher
        top_athletes = filtered_df.nlargest(30, "jo28_medal_proba")
        
        col_rank, col_data = st.columns([1, 4])
        
        with col_data:
            display_cols = ["Name", "NOC", "Sport", "Age", "nb_medal_athlete", "jo28_medal_proba"]
            display_df = top_athletes[display_cols].copy()
            display_df.columns = ["Athlète", "Pays", "Sport", "Âge", "Médailles", "Proba JO28"]
            display_df["Proba JO28"] = display_df["Proba JO28"].apply(lambda x: f"{x:.1%}")
            
            st.dataframe(
                display_df,
                width="stretch",
                hide_index=True,
                column_config={
                    "Athlète": st.column_config.TextColumn(),
                    "Pays": st.column_config.TextColumn(width="small"),
                    "Sport": st.column_config.TextColumn(),
                    "Âge": st.column_config.NumberColumn(format="%d"),
                    "Médailles": st.column_config.NumberColumn(format="%d"),
                    "Proba JO28": st.column_config.TextColumn(),
                }
            )
        
        # Distribution des probabilités
        st.subheader("Distribution des probabilités")
        fig = px.histogram(
            filtered_df,
            x="jo28_medal_proba",
            nbins=30,
            color_discrete_sequence=["#032361"],
            labels={"jo28_medal_proba": "Probabilité de médaille"}
        )
        fig.add_vline(x=prob_threshold, line_dash="dash", line_color="red",
                     annotation_text=f"Seuil: {prob_threshold:.0%}")
        st.plotly_chart(fig, width="stretch")
    
    # ============================
    # TAB 2: CLASSEMENT PAYS
    # ============================
    with tab2:
        st.header("🌍 CLASSEMENT DES PAYS")
        
        # Agrégation par pays
        country_rank = filtered_df.groupby("NOC").agg({
            "jo28_medal_proba": ["sum", "mean", "count"]
        }).reset_index()
        
        country_rank.columns = ["NOC", "Score_Total", "Proba_Moyenne", "Nb_Athletes"]
        country_rank = country_rank.sort_values("Score_Total", ascending=False)
        country_rank["Rank"] = range(1, len(country_rank) + 1)
        
        # Affichage tableau
        st.subheader("Tableau du classement")
        st.dataframe(
            country_rank[["Rank", "NOC", "Score_Total", "Proba_Moyenne", "Nb_Athletes"]],
            width="stretch",
            hide_index=True
        )
        
        # Graphique top 15
        top_15_countries = country_rank.head(15)
        fig = px.bar(
            top_15_countries,
            x="NOC",
            y="Score_Total",
            color="Proba_Moyenne",
            color_continuous_scale="RdYlGn",
            labels={"NOC": "Pays", "Score_Total": "Score Total", "Proba_Moyenne": "Proba Moyenne"},
            title="Top 15 Pays - Score Total de Médailles (JO28)"
        )
        st.plotly_chart(fig, width="stretch")
        
        # Carte géographique (si possible)
        st.subheader("Distribution par continent")
        continent_map = {
            "USA": "Amérique", "CAN": "Amérique", "BRA": "Amérique", "MEX": "Amérique",
            "CHN": "Asie", "JPN": "Asie", "IND": "Asie", "KOR": "Asie",
            "FRA": "Europe", "GBR": "Europe", "GER": "Europe", "ITA": "Europe",
            "AUS": "Océanie", "NZL": "Océanie"
        }
        country_rank["Continent"] = country_rank["NOC"].map(continent_map).fillna("Autre")
        continent_agg = country_rank.groupby("Continent")["Score_Total"].sum().sort_values(ascending=False)
        
        fig_pie = px.pie(
            values=continent_agg.values,
            names=continent_agg.index,
            title="Distribution des prédictions de médailles par continent",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_pie, width="stretch")
    
    # ============================
    # TAB 3: CLASSEMENT SPORTS
    # ============================
    with tab3:
        st.header("⚽ CLASSEMENT DES SPORTS")
        
        # Agrégation par sport
        sport_rank = filtered_df.groupby("Sport").agg({
            "jo28_medal_proba": ["mean", "sum", "count"]
        }).reset_index()
        
        sport_rank.columns = ["Sport", "Proba_Moyenne", "Score_Total", "Nb_Athletes"]
        sport_rank = sport_rank.sort_values("Score_Total", ascending=False)
        
        st.subheader("Sports par niveau de compétition")
        st.dataframe(
            sport_rank,
            width="stretch",
            hide_index=True
        )
        
        # Graphique
        fig_sports = px.bar(
            sport_rank.head(20),
            x="Sport",
            y="Score_Total",
            color="Proba_Moyenne",
            color_continuous_scale="Viridis",
            labels={"Sport": "Sport", "Score_Total": "Score Total"},
            title="Top 20 Sports - Potentiel de Médailles"
        )
        fig_sports.update_xaxes(tickangle=-45)
        st.plotly_chart(fig_sports, width="stretch")
    
    # ============================
    # TAB 4: ANALYSES
    # ============================
    with tab4:
        st.header("📊 ANALYSES DÉTAILLÉES")
        
        # Sous-onglets
        analysis_col1, analysis_col2 = st.columns(2)
        
        with analysis_col1:
            st.subheader("Analyse par Âge")
            
            # Distribution par âge
            age_dist = filtered_df.groupby("Age").agg({
                "jo28_medal_proba": ["mean", "count"]
            }).reset_index()
            age_dist.columns = ["Age", "Proba_Moyenne", "Nb_Athletes"]
            
            fig_age = px.line(
                age_dist,
                x="Age",
                y="Proba_Moyenne",
                markers=True,
                color_discrete_sequence=["#bae133"],
                title="Probabilité de médaille par âge",
                labels={"Age": "Âge", "Proba_Moyenne": "Proba Moyenne"}
            )
            st.plotly_chart(fig_age, width="stretch")
        
        with analysis_col2:
            st.subheader("Analyse par Genre")
            
            gender_stats = filtered_df.groupby("Sex").agg({
                "jo28_medal_proba": ["mean", "sum", "count"]
            }).reset_index()
            gender_stats.columns = ["Genre", "Proba_Moyenne", "Score_Total", "Nb_Athletes"]
            
            fig_gender = px.bar(
                gender_stats,
                x="Genre",
                y=["Score_Total"],
                color_discrete_sequence=["#032361"],
                title="Score de prédictions par genre",
                labels={"Genre": "Genre", "Score_Total": "Score Total"}
            )
            st.plotly_chart(fig_gender, width="stretch")
        
        # Palmarès exceptionnels
        st.subheader("🏆 Athlètes avec l'historique le plus impressionnant")
        
        top_history = filtered_df.nlargest(10, "nb_medal_athlete")[
            ["Name", "NOC", "Sport", "nb_medal_athlete", "particip_athlete", "jo28_medal_proba"]
        ]
        top_history.columns = ["Athlète", "Pays", "Sport", "Médailles", "Participations", "Proba JO28"]
        top_history["Proba JO28"] = top_history["Proba JO28"].apply(lambda x: f"{x:.1%}")
        
        st.dataframe(top_history, width="stretch", hide_index=True)
    
    # ============================
    # TAB 5: DONNÉES BRUTES
    # ============================
    with tab5:
        st.header("📋 DONNÉES BRUTES - EXPORT")
        
        # Affichage
        st.subheader("Données filtrées complètes")
        st.dataframe(
            filtered_df.sort_values("jo28_medal_proba", ascending=False),
            width="stretch",
            height=600
        )
        
        # Téléchargement CSV
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Télécharger les données filtrées (CSV)",
            data=csv,
            file_name=f"jo28_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    # ============================
    # FOOTER
    # ============================
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown("""
        <div style='text-align: center; color: #666;'>
            <small>🏅 JO 2028 Predictions Dashboard | Projet YPerf</small><br>
            <small>Données à titre indicatif | Dernière mise à jour: 2028</small>
        </div>
        """, unsafe_allow_html=True)

else:
    st.error("Impossible de charger les données. Veuillez exécuter le notebook complet d'abord.")
