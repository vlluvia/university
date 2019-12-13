
# aircrack-ng其他工具

* airdecap-ng

* airserv-ng

* airtun-ng

* besside-ng

## airdecap-ng
```shell 
    1. 去除802.11头
        airdecap-ng -b <AP MAC> 1.pcap
    2. 解密WEP加密数据(必须有与AP建立关联关系)
        airdecap-ng -w <WEP key> -b <AP MAC> 1.pcap
    3. 解密WPA加密数据(必须含有4步握手信息)
        airdecap-ng -e kifi -p <PSK> -b <AP MAC> 1.pcap
```

## airserv-ng
```shell 
    1. 通过网络提供无线网卡服务器
    2. 启动无线监听
    3. 服务器端
        airserv-ng -p 3333 -d wlan0mon
    4. 客户端
        airodunp-ng 192.168.1.1:3333
```

## airtun-ng
```shell 
    1. 无线入侵检测wIDS(可支持多个AP监听)
        WEP: airtun-ng -a <AP MAC> -w SKA wlan0mon
        WPA: airtun-ng -a <AP MAC> -p PSK -e kifi wlan0mon
        ifconfig at0 up
        四步握手
				
        入侵检测系统
        snorby
        squert
				
    2. 中继和重放
        Repeate
        airtun-ng -a <AP MAC> --repeat --bssid <AP MAC> -i wlan0mon wlan1mon		(wlan0mon 收包的网卡，wlan1mon 发包网卡，-a 发包源，--bssid 过滤执法指定地址的包)
				
        Replay(将抓到的cap文件重放到指定网卡)
        airtun-ng -a <Source MAX> -r 1.cap <interface>
```



