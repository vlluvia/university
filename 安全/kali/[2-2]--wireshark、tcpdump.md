
# wireshark、tcpdump

* wireshark
* tcpdump

## wireshark

* 描述

> 抓包嗅探协议分析  
> 安全专家必备的技能    
> 抓包引擎

> * Libpcap9—— Linux  
> * Winpcap10—— Windows 
 
> 解码能力


* 基本使用方法

1. 启动
2. 选择抓包网卡
3. 混杂模式
4. 实时抓包
5. 保存和分析捕获文件
6. 首选项

* 常见协议包

1. Arp
2. Icmp
3. Tcp——三次握手
4. Udp
5. Dns
6. http
7. ftp


* 信息统计
1. 节点数
2. 协议分布
3. 包大小分布
4. 会话连接
5. 解码方式
6. 专家系统
7. 抓包对比nc、ncat加密与不加密的流量


## tcpdump

> No-GUI的抓包分析工具
> Linux、Unix系统默认安装

* 抓包
``` 
// 抓包
tcpdump -i eth0 -s 0 -w file.pcap

// 读取抓包文件
tcpdump -r file.pcap

```

* 筛选
``` 
tcpdump -n -r http.cap | awk '{print $3}'| sort –u
tcpdump -n src host 145.254.160.237 -r http.cap
tcpdump -n dst host 145.254.160.237 -r http.cap
tcpdump -n port 53 -r http.cap
tcpdump -nX port 80 -r http.cap
```

* 高级筛选
``` 
tcpdump -A -n 'tcp[13] = 24' -r http.cap
```

