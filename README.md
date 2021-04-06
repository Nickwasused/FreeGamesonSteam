# FreeGamesonSteam <br>
[![Build Status](https://travis-ci.org/Nickwasused/FreeGamesonSteam.svg?branch=master)](https://travis-ci.org/Nickwasused/FreeGamesonSteam) 
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Nickwasused_FreeGamesonSteam&metric=alert_status)](https://sonarcloud.io/dashboard?id=Nickwasused_FreeGamesonSteam) 

Searching SteamDB for Free Games and Activating them using  ArchiSteamFarm 

# Requirements

* Steam Web Api Key [here](https://danbeyer.github.io/steamapi/page1.html)

# Python Versions

| Version | Supported          |
| ------- | ------------------ |
|   3.9   | :white_check_mark: |
|   3.8   | :white_check_mark: |
|   3.7   | :white_check_mark: |
|   3.6   | :white_check_mark: |
| >=3.5   | :x:                |

# Cpu Architectures

|   Arch  | Supported          |
| ------- | ------------------ |
|  AMD64  | :white_check_mark: |
| ppc64le | :white_check_mark: |
|  s390x  | :white_check_mark: |
|  Arm64  | :white_check_mark: |
|  Other  | :x:                |

# Important!
You need to enable the IPC interface.

Put this in your ASF.json:
```
{
	"IPC": true
}
```

and

You need to edit the Config file: ``` nano steamconfig.py ```
```
...
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
...
	def getsteamapilink(self, steamid):
        steam_api_key = "YOUR_STEAM_API_KEY"
        return "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={}&steamid={}&format=json".format(steam_api_key, steamid)
...
```

# Setup for Raspberry-Pi

1. You need ArchiSteamFarm running on ``` 127.0.0.1:1242 ```
2. Make the Directory and change in it: ``` mkdir /home/pi/steambot && cd /home/pi/steambot ```
3. Download the Script and Config: ``` wget https://raw.githubusercontent.com/Nickwasused/FreeGamesonSteam/master/steam.py && wget https://raw.githubusercontent.com/Nickwasused/FreeGamesonSteam/master/steamconfig.py```
4. Install Dependencies ```  wget https://raw.githubusercontent.com/Nickwasused/FreeGamesonSteam/master/requirements.txt &&  pip3 install -r requirements.txt ```
5. Create the Service and timer file:
	- Path: ``` /etc/systemd/system/steam.service```
	- Content : 
	```
	[Unit]
	Description=Steam service
	After=network.target
	StartLimitIntervalSec=0

	[Service]
	Type=simple
	User=pi
	ExecStart=/usr/bin/python3 /home/pi/steambot/steam.py
	WorkingDirectory=/home/pi/steambot/

	[Install]
	WantedBy=multi-user.target
	```
				
	- Path: ``` /etc/systemd/system/steam.timer```
	- Content : 
	```
	[Unit]
	Description=Execute Steam

	[Timer]
	OnCalendar=*-*-* 18:00:00
	Unit=steam.service

	[Install]
	WantedBy=multi-user.target
	```
	
6. Enable and Start the Services:
	- ``` sudo systemctl enable steam.service ```
	- ``` sudo systemctl enable steam.timer ```
	- ``` sudo systemctl start steam.service ```
	- ``` sudo systemctl start steam.timer ```

# Notice

The Service assumes that the Script is located here: ``` /home/pi/steambot/steam.py ``` <br>
And the Service assumes that the Config is located here: ``` /home/pi/steambot/steamconfig.py ```
