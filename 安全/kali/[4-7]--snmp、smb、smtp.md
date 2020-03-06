

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

* 描述
> 基于SNMP，进行网络设备监控，如：交换机、防火墙、服务器，CPU等其系统内部信息，基本都可以监控到。  
  信息的金矿，经常被管理员配置错误  
  community：登录证书，默认值为public。容易被管理员遗忘修改其特征字符。两个默认的community strings，一个是public（可读），另一个是private（可写）  
  服务器：161端口，客户端：162端口（UDP）

> MIB Tree：
> * SNMP Management Information Base（MIB）
> * 树形的网络设备管理功能数据库

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

* 描述
> server message block 协议  
> * 是微软历史上出现安全问题最多的协议
> * 实现复杂
> * 系统默认开放
> * 文件共享
> * 空会话未身份认证访问（SMB1.0漏洞）
>  * 通过这个漏洞可获得密码策略，用户名，组名，机器名，用户、组SID


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
