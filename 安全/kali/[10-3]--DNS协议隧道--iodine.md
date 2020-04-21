
# DNS 协议隧道--iodine

* 简介

## 简介

* 基于 DNS 查询的隧道工具
* 与同类工具相比的优点
    * 对下行数据不进行编码，因此性能优
    * 支持多平台：Linux、BSD、Mac OS、Windows
    * 最大16个并发链接
    * 支持同网段隧道IP（不同于服务器、客户端网段）
    * 支持多种 DNS 记录类型
    * 丰富的隧道质量检测措施

* 运行服务器端
``` 
iodined -f -c 10.0.0.1 test.lab.com
-f：前段显示（可选）
-c：不检查客户端地址
IP：服务器端的隧道IP地址（不同于服务器主机IP和客户端主机IP，此IP仅用于隧道之间，在隧道的两道构成独立的网段）
```

* 运行客户端
``` 
指定IP：局域网内部的本地 DNS 服务器
iodine -f test.lab.com
curl --socks5-hostname 127.0.0.1:7001 http://www.sina.com
```

* 隧道网络接口
``` 
不基于资源的通用隧道，如同本网段内两台相邻的主机
隧道两端接口的IP地址应不同于客户端和服务器端网段
基于此隧道可嵌套其他隧道技术
    ssh -CfNg -D 7001 root@10.0.0.1
```

* 安装 TAP 网卡驱动
> https://openvpn.net/index.php/open-source/downloads.html

* Windows 客户端
  
> http://code.kryo.se/iodine/
```
iodine -f test.lab.com
```

* 建立 SSH 隧道
  




