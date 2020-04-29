

# Veil- catpult

* Payload 的投递
1. 集成veil-evasion 生成免杀payload 或自定义payload
2. 使用Impacket 上传二进制 payload 文件
3. 使用passing-the-hash 出发执行 payload


* Payload 直接在内存中运行
> 不向硬盘写入payload文件，避免文件型病毒查杀软件


* Powershell injector
　　– 适用于 windows 7 及以上版本系统
* Barebones python injector　　（最好用）
　　– 适用于powershell injector 失败的情况下使用
* Sethc backdoor　　　　（替换黏滞位）
　　– 用 cmd.exe 替换 C:\Windows\System32\sethc.exe
* Execute custom command　　　　// 执行自定义命令
* EXE delivery
　　– /etc/veil/settings.py
