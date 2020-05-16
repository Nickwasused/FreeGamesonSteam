# FreeGamesonSteam
Searching SteamDB for Free Games and Activating them using  ArchiSteamFarm 

# Important!
You need to enable the IPC interface.

Put this in your ASF.json:
```
{
	"IPC": true
}
```

and

You need to enter your bot name in the script file!
```
...
# Config
bot_name = "PUT_YOU_BOT_NAME_HERE"
...
```

# Setup for Raspberry-Pi

1. You need ArchiSteamFarm running on ``` 127.0.0.1:1242 ```
2. Download the Script: ``` wget https://raw.githubusercontent.com/Nickwasused/FreeGamesonSteam/master/steam.py ```
3. Install Dependencies ```  sudo pip3 install beautifulsoup4 ```
4. Create the Service and timer file:
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
	ExecStart=/usr/bin/python3 /home/pi/steam.py
	WorkingDirectory=/home/pi/

	[Install]
	WantedBy=multi-user.target
	```
				
	- Path: ``` /etc/systemd/system/steam.timer```
	- Content : 
	```
	[Unit]
	Description=Execute Steam

	[Timer]
	OnCalendar=*-*-* 0,6,12,18:00:00
	Unit=steam.service

	[Install]
	WantedBy=multi-user.target
	```
	
5. Enable and Start the Services:
	- ``` sudo systemctl enable steam.service ```
	- ``` sudo systemctl enable steam.timer ```
	- ``` sudo systemctl start steam.service ```
	- ``` sudo systemctl start steam.timer ```

# Notice

The Service assumes that the Script is located here: ``` /home/pi/steam.py ```
