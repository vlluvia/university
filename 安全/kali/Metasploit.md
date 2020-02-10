
# Metasploit

* [基本使用](./Metasploit-基本使用.md)
* [Exploit模块](./Metasploit-Exploit模块.md)
* [payload](./Metasploit-payload.md)
* [Meterpreter](./Metasploit-Meterpreter.md)
* [信息收集](./Metasploit-信息收集.md)
* [弱点扫描](./Metasploit-弱点扫描.md)
* [客户端渗透](./Metasploit-客户端渗透.md)
* [后渗透测试阶段](./Metasploit-后渗透测试阶段.md)


---
## 介绍
* Rex
    - 基本功能库，用于完成日常基本任务，无需人工手动编码实现
    - 处理 socket 连接访问、协议应答（http/SSL/SMB等）
    - 编码转换（XOR、Base64、Unicode）
* Msf::Core
    - 提供 Msf 的核心基本API，是框架的核心能力实现库
* Msf::Base
    - 提供友好的 API接口，便于模块调用的库
* Plugin 插件
    - 连接和调用外部扩展功能和系统


## 目录
>  /usr/share/metasploit-framework/modules/

* Exploits 利用系统漏洞进行攻击的动作，此模块对应每一个具体漏洞的攻击方法（主动、被动）
* Payload 成功exploit之后，真正在目标系统执行的代码或指令
    - Shellcode或系统指令
    - 三种 Payload：/usr/share/metasploit-framework/modules/payloads/
    - Single：all-in-one
    - Stager：目标计算机内存有限时，先传输一个较小的payload用于建立连接
    - Stages：利用stager建立的连接下载的后续payload
    - Stager、Stages都是多种类型，适用于不同场景
    - Shellcode 是payload的一种，由于其建立正向 / 反向 shell 而得名
    
* Auxiliary：执行信息收集、枚举、指纹探测、扫描等功能的辅助模块（没有 payload 的 exploit 模块）
* Encoders：对payload进行加密，躲避AV检查的模块
*  Nops：提高 payload 稳定性及维持大小  
    
  