
# SNMP放大攻击 和 NTP放大攻击

* SNMP放大攻击

* NTP放大攻击

## SNMP放大攻击

> * 简单网络管理协议
>   - Simple Network Management Protocol
>   - 服务端口 UDP 161 / 162　　// 161是主动模式开放的端口，162是被动模式开放的端口
>   - 管理设备 ( manager / 客户端) 、被管理设备 ( agent / 服务端 )
>   - 管理信息数据库（MIB）是一个信息存储库，包含管理代理中的有关配置和性能的数据，按照不同分类，包含分属不同组的多个数据对象
>   - 每一个节点都有一个对象标识符（OID）来唯一的标识
>   - IETF定义标准的MIB库 / 厂家自定义MIB库
> * 攻击原理
>   - 请求流量小，查询结果返回流量大
>   - 结合伪造源地址实现攻击

* Scapy 


## NTP放大攻击

> * 网络时间协议
>   - Network Time Protocol
>   - 保证网络设备时间同步
>   - 电子设备互相干扰导致时钟差异越来越大
>   - 影响应用正常运行、日志审计不可信
>   - 服务端口 UDP 123
> * 攻击原理
>   - NTP 服务器 monlist（MON_GETLIST）查询功能
>       - 监控 NTP 服务器的状况
>   - 客户端查询时，NTP服务器返回最后同步时间的600个客户端 IP
>       - 每6个IP一个数据包，最多100个数据包（放大约100倍）

* 发现NTP服务
```
nmap -sU -p123 192.168.1.0/24     // 查询192.168.1.0/24网段内开放了123端口的服务器
```

* 发现漏洞
``` 
ntpdc -n -c monlist 192.168.1.125　　　　// -n 指不使用域名搜索，只用IP发现，-c 跟具体你要查询的IP
ntpq -c rv 192.168.1.125　　// 查询NTP服务器的服务端配置
ntpdc -c sysinfo 192.168.1.125　　// 查询其他的一些系统信息
```


* 配置文件 -  /etc/ntp.conf
``` 
// 注释这两行，即开启monlist查询功能，重启ntp服务
restrict -4 default kod nomodify notrap nopeer noquery　　
restrict -6 default kod nomodify notrap nopeer noquery
```




