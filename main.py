import os
import pandas as pd
import streamlit as st
from time import sleep

from core.extract_data import *
from core.utils import *


# =======================================
# FUNÇÕES PARA EXTRAÇÃO DOS DADOS
# =======================================
@st.cache_data(ttl=3600, show_spinner=False)
def load_competitions():
    return extract_competitions_info()

@st.cache_data(ttl=3600, show_spinner=False)
def load_matches(competitions_df):
    return extract_matches_info(competitions_df)

@st.cache_data(ttl=3600, show_spinner=False)
def load_players(matches_df):
    return extract_players_info(matches_df)


# =======================================
# CONFIGURAÇÕES DA PÁGINA
# =======================================
st.set_page_config(
    page_title="Soccer Dashboard Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "match"


# =======================================
# NAVEGAÇÃO
# =======================================
page_match = st.Page('./pages/match.py', title='Partidas', icon="🏟️")
page_team = st.Page('./pages/team.py', title='Equipes', icon="⚽️")
page_player = st.Page('./pages/player.py', title='Jogadores', icon="🧍🏽")
pg = st.navigation([page_match, page_team, page_player])


# =======================================
# CABEÇALHO DO DASHBOARD
# =======================================
with st.container():
    st.header("Soccer Dashboard Analytics")
    st.subheader("Welcome to FIFA World Cup dashboard!")
    st.text("Here we captured data from all FIFA World Cups and developed a dashboard that provides an in-depth look at the teams, their matches and their players. (All data was extracted from the Python lib StatsBombPy)")
    

# =======================================
# CARREGAMENTO DOS DADOS
# =======================================
status_container = st.empty()

with status_container.container():
    with st.status("Carregando dados...", expanded=True) as status:
        
        st.write("Carregando competições...")
        competitions_df = load_competitions()

        st.write("Carregando partidas...")
        matches_df = load_matches(competitions_df)
        
        st.write("Carregando jogadores...")
        players_df = load_players(matches_df)

        status.update(
            label="Dados carregados!",
            state="complete",
            expanded=False
        )
sleep(2)
status_container.empty()

st.session_state["competitions_df"] = competitions_df
st.session_state["matches_df"] = matches_df
st.session_state["players_df"] = players_df

pg.run()