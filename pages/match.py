import streamlit as st
import pandas as pd

from core.utils import *

def matches(matches_df: pd.DataFrame) -> None:
    st.session_state["current_page"] = "match"

    # =======================================
    # AVISO DA PÁGINA
    # =======================================
    st.info("Filtros não estão habilitados nesta página!", title="Atenção")


    # =======================================
    # CÁLCULO DE MÉTRICAS
    # =======================================
    # -------- Soma total de gols
    total_goals = (matches_df["home_score"].astype(int)).sum() + (matches_df["away_score"].astype(int)).sum()

    # -------- Total (único) de equipes participantes
    all_teams = pd.concat([matches_df["home_team"], matches_df["away_team"]])
    total_unique_teams = all_teams.nunique()

    # -------- Total de partidas
    total_matches = len(matches_df)

    # -------- Total (único) de partidas
    all_matches = matches_df["home_team"] + " x " + matches_df["away_team"]
    total_unique_matches = all_matches.nunique()

    # -------- Total de edições
    total_unique_seasons = (matches_df["season"].astype(int)).nunique()
    
    # -------- Evolução de gols por edições
    matches_df["total_goals"] = (matches_df["home_score"] + matches_df["away_score"])
    goals_per_season = matches_df.groupby("season")["total_goals"].sum().reset_index()

    # -------- Top 5 times com mais gols marcados
    home_goals = matches_df.groupby("home_team")["home_score"].sum()
    away_goals = matches_df.groupby("away_team")["away_score"].sum()

    goals_by_team = home_goals.add(away_goals, fill_value=0).sort_values(ascending=False)
    top_5_teams = (
        goals_by_team
        .head(5)
        .sort_values(ascending=True)
        .reset_index()
    )

    top_5_teams.columns = ["team", "goals"]


    # =======================================
    # EXIBIÇÃO DAS MÉTRICAS
    # =======================================
    col1, col2, col3, col4, col5= st.columns(5)

    with col1:
        plot_metrics("Total de gols", total_goals)

    with col2:
        plot_metrics("Número de equipes", total_unique_teams)

    with col3:
        plot_metrics("Quantidade de partidas", total_matches)

    with col4:
        plot_metrics("Quantidade de partidas únicas", total_unique_matches)

    with col5:
        plot_metrics("Total de edições", total_unique_seasons)


    # =======================================
    # GRÁFICOS
    # =======================================
    col1, col2 = st.columns([4, 3])
    
    with col1:
        labels = {
            "season": "Edições", 
            "total_goals": "Total de gols"
        }
        plot_graph(goals_per_season, "season", "total_goals", labels, "Total de gols por edição")
    
    with col2:   
        labels = {
            "goals": "Gols", 
            "team": "Equipes"
        }
        plot_horizontal_bars(top_5_teams, "goals", "team", labels, "Top 5 equipes com mais gols marcados")
    
    with st.expander("Dataframe completo de partidas"):
        st.dataframe(
            matches_df,
            use_container_width=True
        )

matches_df = st.session_state["matches_df"]
matches(matches_df)