
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
<span style="color:red;">这是比font标签更好的方式。可以试试。</span>