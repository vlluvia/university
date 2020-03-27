
# aircrack-ng其他工具

* 基础

* airdecap-ng

* airserv-ng

* airtun-ng

* besside-ng

## 基础
``` 
service network-manager stop

airmon-ng    #列出驱动信息、芯片信息

airmon-ng check  #监测与该软件可能起冲突的进程，后面直接加kill就行!

airmon-ng check kill

-----------准备就绪，启动侦听----------

airmon-ng start wlan0

#airmon-ng stop wlan0mon

iwconfig

iwlist wlan0mon channel   #查看监听网口所在的channel
```



## airdecap-ng
> 被wep和wpa加密的数据包我们用wireshark只能看到802.11协议，里面我的数据都被加密了，用就这个命令就可解密里面的部分数据生成1-dec.cap，用抓包工具看起来更舒适

* 去除802.11头
``` 
airdecap-ng -b <AP MAC> 1.pcap
```

* 解密WEP加密数据(必须有与AP建立关联关系)
``` 
airdecap-ng -w <WEP key> -b <AP MAC> 1.pcap
```

* 解密WPA加密数据(必须含有4步握手信息)
``` 
airdecap-ng -e kifi -p <PSK> -b <AP MAC> 1.pcap
```


## airserv-ng

* 描述
> 可以将你的无线网卡作为远程服务器，远程监听这个网卡。就是使用网络提供无线网卡服务器（有的网卡不支持），启动无线侦听

* 使用场景
> 黑客将网卡放到企业内部，远程监听

* 服务器端
``` 
airserv-ng -p 3333 -d wlan0mon
```

* 客户端
``` 
airodunp-ng 192.168.1.1:3333
```


## airtun-ng
* 描述
> 无线入侵检测wIDS    
>> 无线密码和BSSID  
>> 需要获取握手信息

> snort开源ids,发现入侵的异常流量  
> 类似交换机的镜像接口，airtun-ng形成隧道端口，可以把无线的所有流量都镜像到隧道接口上，再在隧道接口连一个IDS系统（或者直接抓包重放到ids）

* 无线入侵检测wIDS(可支持多个AP监听)
``` 
WEP: airtun-ng -a <AP MAC> -w SKA wlan0mon
WPA: airtun-ng -a <AP MAC> -p PSK -e kifi wlan0mon
ifconfig at0 up
四步握手
				
入侵检测系统
snorby
squert
```

* 中继和重放

```shell 
Repeate
airtun-ng -a <AP MAC> --repeat --bssid <AP MAC> -i wlan0mon wlan1mon		(wlan0mon 收包的网卡，wlan1mon 发包网卡，-a 发包源，--bssid 过滤执法指定地址的包)

Replay(将抓到的cap文件重放到指定网卡)
airtun-ng -a <Source MAX> -r 1.cap <interface>
```



