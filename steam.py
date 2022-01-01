#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Nickwasused 2022
# Python 3.9

from steamconfig import config

class account():
    def __init__(self, steam_id):
        from urllib3 import PoolManager
        self.pool = PoolManager()
        self.steam_api_key = config.steam_api_key
        self.steam_id = steam_id

    def get_games(self):
        from json import loads
        games = []
        url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={}&steamid={}&format=json".format(self.steam_api_key, self.steam_id)
        response = self.pool.request('GET', url, preload_content=False)
        response.release_conn()

        apijson = loads(response.data)
        for item in apijson["response"]["games"]:
            games.append(item["appid"])

        return games

class gamefetcher:
    def __init__(self):
        from urllib3 import PoolManager
        self.pool = PoolManager()

    def getfreegames(self):
        from json import loads
        response = self.pool.request('GET', config.fetch_games_url, preload_content=False)
        response.release_conn()
        return response.data

    def filtergames(self, text, games_owned):
        from bs4 import BeautifulSoup
        from re import compile

        apps = []

        soup = BeautifulSoup(text, 'html.parser')
        links = soup.find_all("a", href=True)
        regexraw = r"^https:\/\/store.steampowered.com\/app\/[0-9]{1,}"
        regex = compile(regexraw)
        for link in links:
            result = regex.match(link["href"])
            if (result != None):
                app_id = result.group(0).replace("https://store.steampowered.com/app/", "")
                if app_id not in games_owned:
                    apps.append(app_id)

        return apps

class bot:
    def __init__(self, name):
        from urllib3 import PoolManager
        self.pool = PoolManager()
        self.name = name
        self.steam_id = self.get_steam_id()

    def get_steam_id(self):
        from json import loads
        response = self.pool.request('GET', "{}/api/bot/{}".format(config.boturl, self.name), preload_content=False)
        response.release_conn()

        apijson = loads(response.data)
        steam_id = apijson["Result"]["main"]["SteamID"]
        return steam_id

    def redeem_games(self, games):
        from urllib3 import exceptions
        from json import dumps
        error_message_api = 'Cant connect to Archisteamfarm Api. {}'
        error_message_redeem = 'Cant redeem appid: {} for bot: {}, because: "{}"'

        print("Trying to redeem {} Games.".format(len(games)))
        
        for app_id in games:
            try:
                data = {'Command': 'addlicense {} {}'.format(self.name, app_id)}
                print(data)
                response = self.pool.request('POST', "{}/api/command".format(config.boturl), body=dumps(data), headers={'accept': 'application/json', 'Content-Type': 'application/json'}, timeout=30)
                if response.status == 200:
                    if "Fail" in response.data.decode('utf-8'):
                        print(error_message_redeem.format(app_id, self.name, response.data.decode('utf-8')))
                    else:
                        print('Redeemed appid: {} for bot: {}'.format(app_id, self.name))
                elif response.status == 400:
                    print(error_message_redeem.format(app_id, self.name, response.data.decode('utf-8')))
                elif response.status == 401:
                    print('Wrong IPC password/auth faliure')
                elif response.status == 403:
                    print('Blocked by asf try again in a few hours')
                elif response.status == 500:
                    print('unexpected error while redeeming appid: {}'.format(app_id))
                elif response.status == 503:
                    print('third-party resource error while redeeming appid: {}'.format(app_id))
                else:
                    print('Cant Reddem code: {} on bot: {}'.format(self.name, app_id))
            except exceptions.ConnectionError:
                print(error_message_api.format(config.boturl))
            except exceptions.MaxRetryError:
                print(error_message_api.format(config.boturl))
            except exceptions.ConnectTimeoutError:
                print(error_message_api.format(config.boturl))
            except Exception as e:
                print(e)

# fetch the Games here
api = gamefetcher()
new_games = api.getfreegames()

for config_bot in config.bots:
    bot = bot(config_bot)
    accounthandler = account(bot.steam_id)
    owned_games = accounthandler.get_games()
    games_to_redeem = api.filtergames(new_games, owned_games)
    bot.redeem_games(games_to_redeem)