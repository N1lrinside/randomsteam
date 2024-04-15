import requests
import random
import time
from deep_translator import GoogleTranslator
class GameSteam:
    def __init__(self, user_id: str) -> None:
        self.user_id = user_id
        self.api_key = 'A841CD672B51AB7D6C82A7CDA8B28E86'
        try:
            self.urltoid64 = f'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={self.api_key}&vanityurl={self.user_id}'
            response = requests.get(self.urltoid64).json()
            self.id64 = response.get('response', {}).get('steamid', self.user_id)
        except Exception as e:
            self.id64 = user_id
        self.session = requests.Session()

    def random_games(self) -> str:
        self.url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={self.api_key}&steamid={self.id64}&format=json'
        response = self.session.get(self.url).json()
        games = response.get('response', {}).get('games', [])
        game_ids = [game_id['appid'] for game_id in games if game_id['appid'] != '878760']
        return random.choice(game_ids)

    def get_state_about_achievements(self, game_id: str = '730') -> None:
        self.url = f'http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={game_id}&key={self.api_key}&steamid={self.id64}'
        self.url_game = f'https://store.steampowered.com/api/appdetails?appids={game_id}'
        self.url_hours = f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={self.api_key}&steamid={self.id64}&format=json'
        response_hours = self.session.get(self.url_hours).json()
        response_game = self.session.get(self.url_game).json()
        response = self.session.get(self.url).json()
        if response_game.get(str(game_id), {}).get('success'):
            self.name = response_game[str(game_id)]['data']['name']
        elif response.get('playerstats', {}).get('success'):
            self.name = response['playerstats']['gameName']
        else:
            self.name = "Не получилось получить информацию об игре"
        try:
            self.stats_achievement = len([i for i in requests.get(self.url).json()['playerstats']['achievements'] if i['achieved'] == 1])
        except KeyError as err:
            phrase = requests.get(self.url).json().get('playerstats', {}).get('error', '')
            self.stats_achievement = GoogleTranslator(source='en', target='ru').translate(phrase)
        self.hours = response_hours.get('response', {}).get('games', )