
# SSL 拒绝访问攻击


* thc-ssl-dos

## thc-ssl-dos
* 简介
> SSL 协商加密对性能开销增加，大量握手请求会导致 DOS  
  利用 SSL secure Renegotiation 特性，在单一 TCP 连接中生成数千个 SSL 重连接请求，造成服务器资源过载  
  与流量式拒绝访问攻击不同，thc-ssl-dos 可以利用 dsl 线路打垮 30G 带宽的服务器  
  服务器平均可以处理 300 次/秒 SSL 握手请求  
  对 SMTPS、POP3S 等服务同样有效  

* 用法
``` 
root@kali:~# thc-ssl-dos 10.10.10.132 80 --accept
```

* 对策
1. 禁用 SSL-Renegotiation、使用 SSL Accelerator
2. 通过修改 thc-ssl-dos，可以绕过以上两种对策
   
