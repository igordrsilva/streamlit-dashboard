import streamlit as st
import pandas as pd

from core.utils import *
from pages.sidebar import sidebar

def players(competitions_df: pd.DataFrame, matches_df: pd.DataFrame, players_df: pd.DataFrame) -> None:
    st.session_state["current_page"] = "player"
    
    # =======================================
    # SIDEBAR
    # =======================================
    sidebar(competitions_df, matches_df, players_df)


    # =======================================
    # DATASET FILTRADOS
    # =======================================
    filters = st.session_state.get("sidebar_filters", {})

    season = filters.get("season")
    team = filters.get("team")

    players_df["season"] = (
        players_df["season"]
        .astype(str)
        .str.strip()
    )

    players_df["team_name"] = (
        players_df["team_name"]
        .astype(str)
        .str.strip()
    )


    filtred_players_df = players_df[
        (players_df["season"] == season) &
        (players_df["team_name"] == team)
    ].drop_duplicates(
        subset=["player_id", "team_name", "season"]
    )


    # =======================================
    # CÁLCULO DE MÉTRICAS
    # =======================================
    # -------- Posição dos jogadores
    filtred_players_df["position"] = (
        filtred_players_df["positions"]
        .apply(get_position)
    )

    # -------- Goleiros
    total_gk = filtred_players_df["position"].isin(["Goalkeeper"]).sum()

    # -------- Defensores
    total_def = filtred_players_df["position"].isin([
        "Right Center Back",
        "Left Center Back",
        "Right Back",
        "Left Back"
    ]).sum()

    # -------- Meio campistas
    total_mid = filtred_players_df["position"].isin([
        "Right Defensive Midfield",
        "Left Defensive Midfield",
        "Right Midfield",
        "Left Midfield"
    ]).sum()

    # -------- Atacantes
    total_atk = filtred_players_df["position"].isin([
        "Right Center Forward",
        "Left Center Forward"
    ]).sum()

    # -------- Não informados
    no_info = filtred_players_df["position"].isin([
        "Não informado"
    ]).sum()


    # =======================================
    # EXIBIÇÃO DAS MÉTRICAS
    # =======================================
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        plot_metrics("Goleiros", total_gk)

    with col2:
        plot_metrics("Defensores", total_def)

    with col3:
        plot_metrics("Meio-campostas", total_mid)

    with col4:
        plot_metrics("Atacantes", total_atk)

    with col5:
        plot_metrics("Não informados", no_info)

    
    # =======================================
    # DATABASE
    # =======================================
    
    posicao = st.selectbox(
        "Posição",
        filtred_players_df["position"].dropna().unique(),
        width=450
    )

    filtred_players_df = filtred_players_df[filtred_players_df["position"] == posicao]

    st.dataframe(
        filtred_players_df,
        column_config={
            "player_id": None,
            "player_name": st.column_config.TextColumn(
                "Nome completo"
            ),

            "player_nickname": st.column_config.TextColumn(
                "Apelido"
            ),

            "jersey_number": st.column_config.NumberColumn(
                "Camisa",
                format="%d"
            ),

            "team_name": st.column_config.TextColumn(
                "Equipe"
            ),

            "position": st.column_config.TextColumn(
                "Posição"
            ),

            "season": st.column_config.NumberColumn(
                "Edição",
                format="%d"
            ),

            "positions": None,
            "cards": None
        },
        hide_index=True,
        use_container_width=True
    )

    


competitions_df = st.session_state["competitions_df"]
matches_df = st.session_state["matches_df"]
players_df = st.session_state["players_df"]
players(competitions_df, matches_df, players_df)