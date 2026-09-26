import streamlit as st
import pandas as pd

def sidebar(competitions_df:pd.DataFrame, matches_df: pd.DataFrame, players_df: pd.DataFrame) -> None:
    
    if st.session_state.get("current_page") == "match":
        return
    
    # =======================================
    # FILTROS
    # =======================================
    st.sidebar.title("Filtros")

    # -------- Competição
    competition = st.sidebar.selectbox("Competição", sorted(competitions_df["competition_name"].dropna().unique()))
    filtred_competition_df = competitions_df[competitions_df["competition_name"] == competition]

    # -------- Edição
    season = st.sidebar.selectbox("Edição", sorted(filtred_competition_df["season_name"].dropna().unique()))

    # -------- Equipes
    filtred_matches_df = matches_df[
        (matches_df["competition"] == competition) &
        (matches_df["season"] == season)
    ]

    filtred_matches_df = pd.concat([filtred_matches_df["home_team"], filtred_matches_df["away_team"]])
    team = st.sidebar.selectbox("Equipe", sorted(filtred_matches_df.dropna().unique()))

    # -------- Limpar filtros
    if st.sidebar.button("Limpar filtros"):
        st.session_state["sidebar_filters"] = {}
        st.rerun()

    # -------- Aplicar filtros
    st.session_state["sidebar_filters"] = {
        "competition": competition,
        "season": season,
        "team": team
    }
