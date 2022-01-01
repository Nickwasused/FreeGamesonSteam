# FreeGamesonSteam <br>
[![Build Status](https://travis-ci.org/Nickwasused/FreeGamesonSteam.svg?branch=master)](https://travis-ci.org/Nickwasused/FreeGamesonSteam) 

Searching SteamDB for Free Games and Activating them using ArchiSteamFarm 

# Status
A Workaround is being implemented.
(Currently broken See: https://github.com/Nickwasused/FreeGamesonSteam/issues/41)

# Requirements

* Steam Web Api Key [here](https://steamcommunity.com/dev/apikey)
* ArchiSteamFarm running with IPC Enabled

# Info

Python: 3.9<br>
CPU-Tested: AMD64, ARM64

# Important!
You need to enable the IPC interface.

Put this in your ASF.json:
```
{
	"IPC": true
}
```

and

You need to edit the Config file: ```mv steamconfig.py.example steamconfig.py```<br>``` nano steamconfig.py ```
```
class config:
    boturl = 'http://127.0.0.1:1242'
    botip = '127.0.0.1'

    bots = ["main"]

    fetch_games_url = "https://store.steampowered.com/search/?specials=1&maxprice=free"

    # Get your Key here: https://steamcommunity.com/dev/apikey
    steam_api_key = "ADD YOUR STEAM API KEY HERE"
```

# Setup for Raspberry-Pi

1. You need ArchiSteamFarm running on ``` 127.0.0.1:1242 ```
2. Download the Script and Config: ```git clone git@github.com:Nickwasused/FreeGamesonSteam.git steam```
3. Go into the Directory ```cd steam```
4. Install Dependencies ```pip3 install -r requirements.txt```
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
	ExecStart=/usr/bin/python3 /home/pi/steam/steam.py
	WorkingDirectory=/home/pi/steam/

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

The Service assumes that the Script is located here: ``` /home/pi/steam/steam.py ``` <br>
And the Service assumes that the Config is located here: ``` /home/pi/steam/steamconfig.py ```
