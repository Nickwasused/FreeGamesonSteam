#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Nickwasused

class config:
    # Config /Example for Bot (asf) bot_names = ["asf"]
    # !Important please change the Settings here!
    bot_names = ['PUT_YOU_BOT_NAME_HERE_1', 'PUT_YOU_BOT_NAME_HERE_2']
    boturl = 'http://127.0.0.1:1242/Api/Command/'
    botip = '127.0.0.1'

    # By default the log output gets translated to the System Language
    # Default: true
    translateoutput = 'true'
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

    # You can change the User Agent here:
    # Default: Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail appname/appversion
    headers = {
        'User-Agent': 'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail appname/appversion'
    }
