import mysql.connector
from app.GameSteam import GameSteam

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="2005",
  database="databasename"
)

def random(id_steam: str) -> str:
    User = GameSteam(id_steam)
    game_id = User.random_games()
    User.get_state_about_achievements(game_id)
    return (f'Название игры: {User.name}\n'
            f'Кол-во выполненных достижений: {User.stats_achievement}\n'
            f'https://store.steampowered.com/app/{game_id}')