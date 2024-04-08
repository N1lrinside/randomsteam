import requests
import random
class GameSteam:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.api_key = 'A841CD672B51AB7D6C82A7CDA8B28E86'
        self.url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={self.api_key}&steamid={self.user_id}&format=json'
        self.response = [game_id['appid'] for game_id in requests.get(self.url).json()['response']['games']]

    def random_games(self):
        return random.choice(self.response)

User = GameSteam('76561198821788610')
print(User.random_games())