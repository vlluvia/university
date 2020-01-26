
# Syn-flood和IP地址欺骗

* Syn-flood

* IP地址欺骗

## Syn-flood

* Scapy
```python
i = IP()
i.dst = 1.1.1.1
i.display()
t = TCP()
sr1(i/t, verbose = 1, timeout=3)
sr1(IP(dst=1.1.1.1)/TCP())
```
<font color=red size=72>color=gray</font>