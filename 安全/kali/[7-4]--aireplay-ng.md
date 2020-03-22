

# aireplay-ng

* 描述

* 参数

* 实例

## 描述
* 产生或者加速无线通信流量
    - 向无线网络中注入数据包
        - 伪造身份验证
        - 强制重新身份验证
        - 抓包重放
    - 用于后续WEP和WPA密码破解
    - 支持十种包注入
* 获取包的两种途径
    - 指定接口 (-i)
    - 抓包文件pacp (-r)


## 参数
* Filter 选项
> 常用于除了解除认证攻击和伪造认证攻击之外的所有攻击的参数，用于控制数据包。常用的选项为 –b.
``` 
-b bssid ：AP(接入点）的MAC地址
-d dmac：目的MAC地址
-s smac：源MAC地址
-m len：数据包最小长度
-n len：数据包最大长度
-u type：frame control, type field
-v subt：frame control, subtype field
-t tods：到目的地址的控制帧
-f fromds：从目的地址出发的控制帧
-w iswep：含有WEP数据的控制帧
```

* Replay 选项
> 当注入（injecting 或 replay)数据包时，常用于下面的选项(通常用部分，而不是全部）.
``` 
-x nbpps：设置每秒发送数据包的数目
-p fctrl：设置控制帧中包含的信息（16进制）
-a bssid：设置接入点的MAC地址 （access point mac address)
-c dmac：设置目的MAC地址  (destination mac address)
-h smac：设置源MAC地址 (sourse mac address)
-e essid：虚假认证攻击中，设置接入点名称.当接入点不是隐藏时，它可以省略，反过来，它可心攻击隐藏的接入点。（For fakeauth attack or injection test, it sets target AP SSID. This is optional when the SSID is not hidden.）
-j：arpreplay attack : inject FromDS pkts
-g value : change ring buffer size (default: 8)
-k IP : set destination IP in fragments
-l IP : set source IP in fragments
-o npckts : number of packets per burst (-1)
-q sec : seconds between keep-alives (-1)
-y prga : keystream for shared key auth
“-B” or “–bittest” : bit rate test (Applies only to test mode)
“-D” :disables AP detection. Some modes will not proceed if the AP beacon is not heard. This disables this functionality.
“-F” or “–fast” : chooses first matching packet. For test mode, it just checks basic injection and skips all other tests.
“-R” disables /dev/rtc usage. Some systems experience lockups or other problems with RTC. This disables the usage.
```


## 实例

* 基本测试
``` 
// 满足向网络中注包功能性要求(基本检测模式 只发probe包)
Aireplay -9 wlan0mon 
```

