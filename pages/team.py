import streamlit as st
import pandas as pd

from core.utils import *
from pages.sidebar import sidebar

def teams(competitions_df: pd.DataFrame, matches_df: pd.DataFrame, players_df: pd.DataFrame) -> None:
    st.session_state["current_page"] = "team"
    
    # =======================================
    # SIDEBAR
    # =======================================
    sidebar(competitions_df, matches_df, players_df)


    # =======================================
    # DATASET FILTRADOS
    # =======================================
    filters = st.session_state.get("sidebar_filters", {})

    competition = filters.get("competition")
    season = filters.get("season")
    team = filters.get("team")

    filtred_matches_df = matches_df[
        (matches_df["competition"] == competition) &
        (matches_df["season"] == season) &
        (
            (matches_df["home_team"] == team) |
            (matches_df["away_team"] == team)
        )
    ]


    # =======================================
    # CÁLCULO DE MÉTRICAS
    # =======================================
    # -------- Total de jogos
    total_games = len(filtred_matches_df)

    # -------- Total de vitórias
    filtred_matches_df["result"] = filtred_matches_df.apply(lambda row: get_result(row, team), axis=1)

    wins = (filtred_matches_df["result"] == "Vitória").sum()

    # -------- Total de gols marcados
    home_goals = filtred_matches_df.loc[
        filtred_matches_df["home_team"] == team, "home_score"
    ].sum()

    away_goals = filtred_matches_df.loc[
        filtred_matches_df["away_team"] == team, "away_score"
    ].sum()

    total_goals = home_goals + away_goals

    # -------- Total de gols sofridos
    home_conceded = filtred_matches_df.loc[
        filtred_matches_df["home_team"] == team, "away_score"
    ].sum()

    away_conceded = filtred_matches_df.loc[
        filtred_matches_df["away_team"] == team, "home_score"
    ].sum()

    goals_conceded = home_conceded + away_conceded

    # -------- Taxa de aproveitamento
    draws = (filtred_matches_df["result"] == "Empate").sum()
    losses = (filtred_matches_df["result"] == "Derrota").sum()
    
    performance = calculate_performance(wins, draws, losses)

    # -------- Gols marcados e sofridos por equipe
    filtred_matches_df["opponent"] = filtred_matches_df.apply(
        lambda row: (
            row["away_team"]
            if row["home_team"] == team
            else row["home_team"]
        ),
        axis=1
    )

    filtred_matches_df["goals_for"] = filtred_matches_df.apply(
        lambda row: (
            row["home_score"]
            if row["home_team"] == team
            else row["away_score"]
        ),
        axis=1
    )

    filtred_matches_df["goals_against"] = filtred_matches_df.apply(
        lambda row: (
            row["away_score"]
            if row["home_team"] == team
            else row["home_score"]
        ),
        axis=1
    )
    

    # =======================================
    # EXIBIÇÃO DAS MÉTRICAS
    # =======================================
    col1, col2, col3, col4, col5= st.columns(5)

    with col1:
        plot_metrics("Total de jogos", total_games)

    with col2:
        plot_metrics("Vitórias", wins)

    with col3:
        plot_metrics("Gols marcados", total_goals)

    with col4:
        plot_metrics("Gols sofridos", goals_conceded)

    with col5:
        plot_metrics("Aproveitamento", f"{performance}%")
     

    # =======================================
    # GRÁFICOS
    # =======================================
    
    teams = pd.concat([filtred_matches_df["home_team"], filtred_matches_df["away_team"]]).dropna().unique()
    
    col1, col2 = st.columns(2)
    
    with col2:
        home_col, away_col = st.columns(2)


        # -------- home team
        
        home_wins, home_draws, home_losses = calculate_team_performance(
            filtred_matches_df,
            team
        )
        home_performance = calculate_performance(home_wins, home_draws, home_losses)
        
        # -------- away team
        away_team = away_col.selectbox(
            "Equipe para comparar",
            teams
        )
        away_wins, away_draws, away_losses = calculate_team_performance(
            filtred_matches_df,
            away_team
        )
        away_performance = calculate_performance(away_wins, away_draws, away_losses)

    col1, col2 = st.columns(2)

    with col1:
        labels = {
            "opponent": "Oponente",
            "goals_for": "Gols marcados",
            "goals_against": "Gols sofridos"
        }

        plot_vertical_bars(
            filtred_matches_df,
            "opponent",
            ["goals_for", "goals_against"],
            labels,
            "Gols marcados e sofridos por confronto"
        )

    with col2:
        labels = {
            "performance": "Aproveitamento",
            "teams": "Equipes"
        }

        plot_horizontal_bars(
            pd.DataFrame({
                "performance": [home_performance, away_performance],
                "teams": [team, away_team]
            }),
            "performance",
            "teams",
            labels,
            "Comparativo de aproveitamento por equipe"
        )

    with st.expander("Dataframe completo de partidas"):
        st.dataframe(
            filtred_matches_df, use_container_width=True
        )


competitions_df = st.session_state["competitions_df"]
matches_df = st.session_state["matches_df"]
players_df = st.session_state["players_df"]
teams(competitions_df, matches_df, players_df)