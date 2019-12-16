
# 侦查、扫描

* 侦查
    - httrack
* 扫描
    - nikto
    - vega
    - skipfish
    - w3af
    - arachni
    - owasp-zap

## 侦查

* httrack
```shell 
    httrack http://topspeedsnail.com -O /tmp/topspeedsnail
```

## 扫描

* nikto
```shell 
    配置文件 /etc/nikto.conf
    nikto -list-plugins
        -host
        -port
        -ssl
        -output
        -vhost <域名>
    nikto -update
    nikto -host http://1.1.1.1 -port 8080
    nikto -host host.txt
    nmap -p80 192.168.1.0/24 -oG - |  nikto -host -
    nikto -host 192.168.1.1 -ssl -port 443
    nikto -host 192.168.1.1 -useproxy http://1.1.1.1:8081
```


* skipfish
```shell 
    -o 目录
    -I 只检查string的URL
    -X 不检查包含string的URL
    -D 跨站点扫描另外一个域
    -l 每秒最大请求数
    -m 每IP最大并发连接数
    --config 指定配置文件
    skipfish -o test http://1.1.1.1
    skipfish -o test @url.txt
    skipfish -o test -S complet.wl -W a.wl http://1.1.1.1
    1. 身份验证
        skipfish -A user:pass -o test http://1.1.1.1
        skipfish -C "name=val" -o test http://1.1.1.1
```


* w3af
```shell 
    1. 安装
        cd ~
        apt-get update	
        apt-get install -y python-pip w3af
        pip install -upgrade pip
        git clone git@github.com:andresriancho/w3af.git
        cd w3af
        ./w3af_console (./w3af_gui)
        apt-get build-dep python-lxml
        apt-get install libssl-dev
        ./tmp/w3af_dependency_install.sh
    2. 升级
        git pull

    3. console 指令
        help
        profiles/ 
            save test self=contained
```
