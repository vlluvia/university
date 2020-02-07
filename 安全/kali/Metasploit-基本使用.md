

# 基本使用

* 升级
```
//shell
apt update; 
apt install metasploit-framework
```
* Msfcli 使用接口
* Msfconsole 使用接口
    - 最流行的用户接口
    - 几乎可以使用全部MSF功能
    - 控制台命令支持 TAB 自动补齐
    - 支持外部命令的执行（系统命令等）
    - 点击鼠标启动  / msfconsole -h -q -r -v / exit
    - help / ? / help vulns


## MSF控制台命令
* 常用命令
1. Banner、Color、connect -h
2. show auxiliary / exploits / payloads / encoders / nops　　
3. search usermap_script / help search
    - search name:mysql / path:scada / platform:aix / type:aux /author:aaron /cve:2011 / 　　　　　　　　　　//  可多条件同时搜索
4. use dos/windows/smb/ms09_001_write　　　　　　　　　　　　　　　　　　　　　　
    - show options / payloads / targets / advanced / evasion　　　　　　
    - info edit
5. Check 、back

6. db_status / db_rebuild_cache
7. db_nmap　　　　　　　　　　// 这个是MSF内置加载了nmap，和操作系统的nmap完全等同
    - Hosts / host 1.1.1.1 / hosts -u / hosts -c address,os_flavor -S Linux　　　　　　// 下面的都是从数据库里面匹配数据筛选，比如host是1.1.1.1的，操作系统是linux的
    - services -p 80 / services -c info,name -p 1-1000
    - vulns / creds （mysql_login）/ loot （hashdump）
8. db_disconnect / db_connect
    - /usr/share/metasploit-framework/config/database.yml
9. db_import / db_export
    - db_import /root/nmap.xml
    - db_export -f xml /root/bak.xml
10. set / unset / setg / unsetg / save　　　　　　//set和setg的区别一个是临时设置，一个是全局设置，save保存设置
11. Run / exploit　　　　　　
12. jobs / kill 0
13. load / unload /loadpath　　　　　　　　　　// load是加载MSF的第三方模块功能，比如Nessus，openvas等等
14. Session　　　　　　　　　　　　　　　　
    - session -l / -i（Shell 、Meterpreter session、VNC）
15. route 通过指定 session 路由流量　　　　　　// 后渗透阶段如果进入了内网可以通过其来设置路由
16. irb （Framework::Version）
17. Resource （msfconsol -r a.rc）　　　　　　// 通过导入文件的方式将预定义的配置直接导入进行攻击，格式如下：
    

