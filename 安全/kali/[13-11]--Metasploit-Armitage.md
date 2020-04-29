

# Armitage


* 描述
> * 开源免费图形前端
>   - 作者自称是众多不会使用metasploit的安全专家之一（命令行）
>   - MSF基于命令行，缺少直观的GUI图形用户接口
> * Armitage 只是调用MSF的漏洞利用能力
>   - Armitage 的每一个GUI操作都可以对应MSF中一条命令
> * 红队团队合作模拟对抗
>   - 分为客户端（armitage）和服务器（msfrpcd）两部分
>   - /usr/share/armitage/teamserver ip password
> * 可脚本化
 
 
 
 * 启动方式
``` 
service postgresql start
```
``` 
Teamserver
// 服务器端：teamserver 服务器IP 连接密码
// 户端：armitage
```
``` 
// 单机启动
Armitage
GUI 启动
127.0.0.1:55553
```


* 发现主机
> - 手动添加IP地址
> - 扫描结果导入（nmap、nessus、openvas、appscan、nexpose、awvs）
> - 直接扫描发现（nmap、msf）
> - DNS 枚举发现


* 扫描端口及服务

* 工作区 workspace

> - 个人视角的目标动态显示筛选，同一team的队员自定义工作区  
> - 基于地址的工作区划分  
> - 基于端口的工作区划分
> - 基于操作系统的工作区划分
> - 基于标签的工作区划分

* 生成payload

* 主动获取目标
> Ms08_067

* 被动获得目标
> Browser_autopwn2


* Meterpreter shell 能力展示

* 菜单功能

* Cortana 脚本
> Veil-Evasion?/use/share/veil-evasion/tools/cortana/veil_evasion.cna  
> https://github.com/rsmudge/cortana-scripts

* 别无他法的最后选择
``` 
Attacks
    - Find Attacks 　　　　　　   # 自动分析匹配漏洞利用模块
    - Hali Mary 　　　　　　　　# 上帝啊！赐予我力量吧！
    - 洪水式漏洞利用代码执行，流量及特征明显，容易被发现
```

* Armitage 现状

> 维护不及时，传言此项目已荒废  
> 仍然是目前唯一开源免费的 metasploit 图形前端

