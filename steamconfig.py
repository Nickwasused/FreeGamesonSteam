#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Nickwasused

class config:
    # Config /Example for Bot (asf) bot_names = ["asf"]
    # !Important please change the Settings here!
    bots = ['{"name": "YOUR_BOT_NAME", "steamid": "YOUR_STEAM_ID_64"}']

    # e.g multiple bots
    # bots = ['{"name": "YOUR_BOT_NAME", "steamid": "YOUR_STEAM_ID_64"}, {"name": "YOUR_BOT_NAME_2", "steamid": "YOUR_STEAM_ID_64_2"}']


    boturl = 'http://127.0.0.1:1242/Api/Command/'
    botip = '127.0.0.1'
    boturl = 'http://{}:1242/Api/Command/'.format(botip)

    # Log Default: true
    log = 'true'
    # Logfile Default: freegames-log
    logfile = 'freegames.log'
    # Proxys are disabled by default
    proxy = 'disabled'
    # Timeout for redeeming Keys: Default 2 Seconds
    timeout = 2

    #You dont need to change things here:
    links = ['https://steamdb.info/sales/?min_discount=95&min_rating=0', 'https://steamdb.info/upcoming/free/#live-promotions']
    basesteam = 'https://store.steampowered.com/app/'

    def getsteamapilink(self, steamid):
        steam_api_key = "YOUR_STEAM_API_KEY"
        return "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={}&steamid={}&format=json".format(steam_api_key, steamid)

    # You can change the User Agent here:
    # Default: Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail appname/appversion
    headers = {
        'User-Agent': 'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail appname/appversion'
    }
