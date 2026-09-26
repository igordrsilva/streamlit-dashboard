import pandas as pd
import plotly.express as px
import streamlit as st
import ast


def plot_horizontal_bars(df: pd.DataFrame, x: str, y: str, labels: dict, title: str) -> None:
    fig = px.bar(
        df, 
        x = x,
        y = y,
        orientation='h',
        labels = labels,
        title = title
    )
    
    st.plotly_chart(fig, use_container_width=True, height=450)


def plot_vertical_bars(df: pd.DataFrame, x: str, y: str, labels: dict, title: str) -> None:
    fig = px.bar(
        df, 
        x = x,
        y = y,
        barmode="group",
        labels = labels,
        title = title
    )

    fig.update_traces(
        texttemplate="%{y}",
        textposition="outside"
    )

    fig.for_each_trace(
        lambda trace: trace.update(
            name=labels.get(trace.name, trace.name)
        )
    )

    fig.update_layout(
        legend_title_text="",
        yaxis=dict(
            showticklabels=False,
            title_text=""
        )
    )
    
    st.plotly_chart(fig, use_container_width=True, height=450)


def plot_graph(df: pd.DataFrame, x: str, y: str, labels: dict, title: str) -> None:
    fig = px.line(
        df, 
        x = x,
        y = y, 
        markers=True, 
        labels = labels,
        title = title
    )
    
    st.plotly_chart(fig, use_container_width=True)


def plot_metrics(title: str, main_data: any, delta: any = None, delta_color: bool = False, border: bool = True) -> None:
    if delta_color:
        st.metric(title, main_data, delta=delta, border=True)
    else:
        st.metric(title, main_data, delta=delta, delta_color="off", border=border)


def get_result(row, team):
    if row["home_team"] == team:
        if row["home_score"] > row["away_score"]:
            return "Vitória"
        elif row["home_score"] == row["away_score"]:
            return "Empate"
        return "Derrota"

    else:
        if row["away_score"] > row["home_score"]:
            return "Vitória"
        elif row["away_score"] == row["home_score"]:
            return "Empate"
        return "Derrota"
    

def calculate_team_performance(matches_df: pd.DataFrame, team: str) -> (int, int, int):
    results = matches_df.apply(
        lambda row: get_result(row, team),
        axis=1
    )

    wins = (results == "Vitória").sum()
    draws = (results == "Empate").sum()
    losses = (results == "Derrota").sum()

    return wins, draws, losses


def calculate_performance(wins: int, draws: int, losses: int) -> float:
    total_games = wins + draws + losses
    points = (wins * 3) + draws
    max_points = total_games * 3
    return round((points / max_points) * 100, 2)


def get_position(positions):
    if pd.isna(positions) or positions == "[]":
        return "Não informado"

    try:
        positions = ast.literal_eval(positions)
        if not positions:
            return "Não informado"
        return positions[0].get("position", "Não informado")
    except (ValueError, SyntaxError):
        return "Não informado"