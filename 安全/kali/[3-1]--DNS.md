

# DNS

* 描述

* NSLOOKUP

* DIG

* DNS区域传输

* DNS字典爆破

* DNS注册信息


## 描述
> 域名解析成IP地址  
> 域名 与 FQDN的区别  
> 域名记录：A 、C nmae、NS、MX、ptr  


## NSLOOKUP
``` 
nslookup www.sina.com
server
type=a、mx、ns、any
nslookup -type=ns example.com 156.154.70.22
```

## DIG
``` 
dig @8.8.8.8 www.sina.com mx
dig www.sina.com any
反向查询：dig +noall +answer -x 8.8.8.8
bind版本信息： dig +noall +answer txt chaos VERSION.BIND @ns3.dnsv4.com
DNS追踪： dig +trace example.com
```

## DNS区域传输
``` 
dig @ns1.example.com example.com axfr
host -T -l sina.com 8.8.8.8
```

## DNS字典爆破
``` 
fierce -dnsserver 8.8.8.8 -dns sina.com.cn -wordlist a.txt
dnsdict6 -d4 -t 16 -x sina.com
dnsenum -f dnsbig.txt -dnsserver 8.8.8.8 sina.com -o sina.xml
dnsmap sina.com -w dns.txt
dnsrecon -d sina.com --lifetime 10 -t brt -D dnsbig.txt
dnsrecon -t std -d sina.com
```

## DNS注册信息 - Whois
``` 
whois -h whois.apnic.net 192.0.43.10
```

