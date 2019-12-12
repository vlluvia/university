

# 主动信息收集 - snmp、smb、smtp

* snmp
    - onesixtyone
    - snmapwalk
    
* smb扫描
    - nmap
    - nbtscan
    - enum4linux
    
* smtp
    - nc
    - nmap
## snmp

* onesixtyone
```sbtshell
    onesixtyone 1.1.1.1 public

    onesixtyone -c client.txt -i hosts -o my.log -w 100
```
* snmapwalk
```sbtshell
    snampwalk 192.168.20.199 -c public -v 2c 
    snampwalk -c public -v 2c 192.168.20.199
    snampcheck -t 192.168.20.199
    snampcheck -t 192.168.20.199 -c private -v 2
    snampcheck -t 192.168.20.199 -w 
```

## smb

* nmap
```sbtshell
    nmap -v -p 139,445 192.168.60.1-20
    nmap 192.168.60.4 -p 139,445 --script=smb-os-discovery.me 
    nmap -v -p 139,445 --script=smb-check-vulns --script-args=unsafe=1 1.1.1.1
```

* nbtscan
```sbtshell
    nbtscan -r 192.168.60.0/24
```

* enum4linux
```sbtshell
    enum4linux -a 192.168.60.10
```

## smtp

* nc
```sbtshell
    nc -nv 1.1.1.1 
```

* nmap
```sbtshell
    nmap smtp.163.com -p25 --script=smtp-enum-users.nse --script-args=smtp-enum-users.methods={VRFY}
    nmap smtp.163.com -p25 --script=smtp-open-relay.nse 
```
