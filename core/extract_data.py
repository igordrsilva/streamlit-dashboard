from statsbombpy import sb
import pandas as pd
import os


def extract_competitions_info(competition_id: int | None = 43) -> pd.DataFrame:
    """Acessa a API da StatsBomb e retorna as competições disponíveis.
    Se um ID for fornecido, filtra apenas as temporadas daquela competição.
    """

    os.makedirs("data", exist_ok=True)
    path = "data/raw_competitions.csv"

    if os.path.exists(path):
        competitions = pd.read_csv(path)
    else:
        competitions = sb.competitions()
        pd.DataFrame(competitions).to_csv(path, index=False)

    if competition_id is None:
        return competitions

    return competitions[competitions["competition_id"] == competition_id]


def extract_matches_info(competitions_df: pd.DataFrame) -> pd.DataFrame:
    """Recebe um DataFrame de competições (filtradas ou completas) e extrai 
    todas as partidas de cada temporada listada, identificando o ID do torneio dinamicamente.
    """

    if competitions_df.empty:
        return pd.DataFrame()

    os.makedirs("data", exist_ok=True)
    path = "data/raw_matches.csv"

    if os.path.exists(path):
        matches = pd.read_csv(path)
    else:
        matches_list = []

        for _, row in competitions_df.iterrows():
            competition_id = row['competition_id']
            season_id = row['season_id']

            try:
                match = sb.matches(competition_id=competition_id, season_id=season_id)
                matches_list.append(match)
            except Exception as e:
                print(f"Erro ao buscar partidas da competição {competition_id}, temporada {season_id}: {e}")

        if not matches_list:
            return pd.DataFrame()
        
        matches = pd.concat(matches_list,ignore_index=True)
        matches.to_csv(path, index=False)
    
    seasons_map = competitions_df.set_index("season_id")["season_name"].to_dict()
    competitions_map = competitions_df.set_index("competition_id")["competition_name"].to_dict()
    
    matches["season"] = matches["season_id"].map(seasons_map)
    matches["competition"] = matches["competition_id"].map(competitions_map)

    final_columns = ["match_id", "match_date", "home_team", "away_team", "home_score", "away_score", "season", "competition"]

    return matches[final_columns]


def extract_players_info(matches_df: pd.DataFrame) -> pd.DataFrame:
    """Recebe o DataFrame de partidas e extrai uma lista única de jogadores 
    que atuaram nelas, vinculando-os ao time e à respectiva temporada.
    """
    if matches_df.empty:
        return pd.DataFrame()

    os.makedirs("data", exist_ok=True)
    path = "data/raw_players.csv"

    if os.path.exists(path):
        players = pd.read_csv(path)
    else:
        players_list = []
        
        match_to_season_map = matches_df.set_index("match_id")["season"].to_dict()

        for match_id in matches_df["match_id"].unique():
            try:
                lineup = sb.lineups(match_id=match_id)
                
                for team_name, team_players in lineup.items():
                    team_players["team_name"] = team_name
                    team_players["season"] = match_to_season_map.get(match_id)
                    players_list.append(team_players)
            except Exception:
                continue

        if not players_list:
            return pd.DataFrame()

        players = pd.concat(players_list, ignore_index=True)
        players.to_csv(path, index=False)

    final_players_df = players

    return final_players_df