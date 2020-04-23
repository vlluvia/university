
# 隧道工具--ptunnel

* 简介


## 简介

* ping tunnel icmp 隧道工具
    * 通过 icmp echo (ping requests)和reply(ping reply) 实现隧道
    * 适用于防火墙只允许ping出战流量的环境
    * 支持多并发连接、性能优
    * 支持身份验证
    * 需要root权限
    * 支持抓包
        * windows：winpcap
        * linux：libpcap
    * 工作过程
        * proxy、client、destination

* 服务器
``` 
ptunnel -x 1234
```

* 客户端
``` 
sudo ptunnel -p proxy -lp 2222 -da destination -dp 22 -x 1234

```  

* 嵌套 SSH 隧道
  
```
ssh -CNfg -D 7000 root@127.0.0.1 -p 2222
```

* ptunnel 直到目前的最新版仍存在拒绝服务漏洞
  

