
# DNS 协议隧道--dns2tcp

* 简介
* dns2tcp


## 简介
* 防火墙禁止 TCP 出战访问流量
    * SSH 隧道、端口转发全部失效
    * 使用基于UDP协议的隧道
    * DNS 的工作原理适合用于实现隧道
    * DNS TCP 53 端口主要用于 DNS 服务器之间进行数据同步（区域传输）
    * 用户提交的 DNS 查询请求，都是 UDP 53 端口的流量

* DNS 工作原理
    * DNS 隧道原理：注册受自己控制的 DNS 记录


* 重定向和 SSH 隧道 只能适用于 TCP 53 端口，对 UDP 53 端口无法使用。
  
  
## dns2tcp

* 描述
1. 利用合法 DNS 服务器实现 DNS 隧道
1. C/S （dns2tcp/dns2tcpd）结构
1. 通过 TXT 记录加密传输数据（A记录长度有限）
1. 隧道建立后保持连接
1. 默认记录生存时间 TTL 值为 3 秒

* 服务器配置文件
``` 
/etc/dns2tcpd.conf
.dns2tcprcd
资源可以是其他地址
```  


* 启动
``` 
dns2tcpd -F -d 1 -f /etc/dns2tcpd.conf
F:前端运行
d：debug level 1-3
f:指定配置文件
```


