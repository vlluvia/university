
# dns

* socat

* ptunnle

* proxytunnle

* sslh

* stunnel4
## socat
```shell 
    socat - tcp:1.1.1.1:80
    socat - tcp-listen:22 / socat - tcp-l:333
    3. 发文件
        socat tcp4-listen:333 open:2.txt.creat,append
    4. 收文件
        cat 1.txt| socat - tcp:1.1.1.1:333
    5. 远程shell
        socat tcp-l:23 exec:sh,pty,stderr
    6. 端口转发
        socat tcp-listen:22,fork tcp4:1.1.1.1:22
    7. 远程执行命令
        服务器: socat - upd-l:2001
        客户端: echo "`id`" | socat - udp4-datagram:1.1.1.1:2001
    8. udp全端口任意内容发布
        for PORT in {1..65535}; do echo "aaaaa" | socat - UDP4-DATAGRAM:1.1.1.1:$PORT;sleep .1; done
    9. 二进制编辑器
        echo -e "\0\14\0\0\c" | socat -u - file:/usr/bin/squid.exe,seek,seek=0x00074420
```


## ptunnle
```shell 
    ping tunnel icmp隧道工具

    1. 服务器
        ptunnel -x 1234
    2. 客户端
        sudo ptunnel -p proxy -lp 2222 -da destination -dp 22 -x 1234
    3. 镶嵌ssh隧道
        ssh -CNfg -D 7000 root@127.0.0.1 -p 2222
```

## sslh

> 端口分配器  
> - 根据客户端第一个包检测协议类型
> - 根据协议检测结果将流量转发给不同目标
> - 支持HTTP, HTTPS, SSH, OPENVPN, tinc, XMPP 和 其他可基于正则表达式判断的人和协议类型
> - 使用于防火墙允许443端口入站访问流量的环境

* 配置文件
```
/etc/default/sslh
    # 需要修改的参数
    RUN=yes
    # --listem <change-me> 改成本机ip
    # --ssl 127.0.0.1      服务器ip
    DAEMON_OPTS="--user sslh --listen <change-me>:443 --ssh 127.0.0.1:22 --ssl 192.168.1.18:443 --http 127.0.0.1:80 --pidfile /var/run/sslh/sslh.pid"
```

* 安装https站点
    - 安装IIS服务、证书服务
    - 部署https站点

* 启动本地HTTP服务
* 防火墙映射TCP/443



## stunnel4
> - 无需修改源代码的情况下将TCP流量封装于SSL通道内
> - 适用于本身不支持加密传输的应用
> - 支持openssl安全特性
> - 跨平台
> - 性能优



* 安装内网stunnel4服务器

* 服务器端配置
    - 生成证书: openssl req -new –days 365 -nodes -x509 -out /etc/stunnel/stunnel.pem -keyout /etc/stunnel/stunnel.pem
    - 创建配置文件 /etc/stunnel/stunnel.conf
        - cert = /etc/stunnel/stunnel.pem
        - setuid = stunnel4
        - setgid = stunnel4
        - pid = /var/run/stunnel4/stunnel4.pid
        - [mysqls]
        - accept = 0.0.0.0:443
        - connect = 1.1.1.11:3306
    - stunnel4 自动生效
        - /etc/default/stunnel4
            - ENABLED = 1
            
    - 启动stunnel4服务端
        - service stunnel4 start
    
    - 防火墙规则
        - 端口映射TCP/443端口到stunnel4服务端TCP/443
    - stunnel4客户端
    

* 客户端配置
    - 安装stunnel4客户端
    - 客户端配置
        - 创建配置文件/etc/stunnel/stunnel.conf
            - client = yes
            - [mysqls]
            - accept = 3306
            - connect = 192.168.1.11:443\
    - 客户端自动启动
        - /etc/default/stunnel4
            - ENABLED = 1
    
    - 启动客户端服务
        - service stunnel4 stop / start
                
     
    