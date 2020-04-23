

# SOCAT

* 简介
* 操作
* socat 基本使用
## 简介
* 被称为 nc++（增强增强版的nc）
    * 双向数据流通道工具

## 操作


* 连接端口
``` 
Socat - tcp:1.1.1.1:80

```  

* 侦听端口（作为服务端）
``` 
socat - tcp4-listen:22 / socat - tcp-l:333

```

* 接收文件
``` 
socat tcp4-listen:333 open:2.txt,creat,append

```  

* 发送文件
``` 
cat 1.txt | socat - tcp4:1.1.1.1:333

```  

* 远程shell – 服务器端
``` 
socat tcp-l:23 exec:sh,pty,stderr

```  


* 端口转发
``` 
socat tcp4-listen:22,fork tcp4:1.1.1.1:22
fork：为新连接创建独立的进程
```  

* 远程执行命令
``` 
服务器：socat - udp-l:2001
客户端：echo “id” | socat - udp4-datagram:1.1.1.1:2001
```  

* UDP 全端口任意内容发包
``` 
for PORT in {1…65535}; do echo “aaaaa" | socat - UDP4-DATAGRAM:+
1.1.1.1:$PORT; sleep .1; done
```

* 二进制编辑器
``` 
echo -e "\0\14\0\0\c" | socat -u - file:/usr/bin/
squid.exe,seek,seek=0x00074420
```

* 简单的 web 服务器
``` 
  socat -T 1 -d -d TCP-L:10081,reuseaddr,fork,crlf SYSTEM:"echo -e \"\\\"HTTP/1.0 200 OK\\\nDocumentType: text/plain\\\n\\\ndate: \$\(date\)\\\nserver:\$SOCAT_SOCKADDR:\$SOCAT_SOCKPORT\\\nclient: \$SOCAT_PEERADDR:\$SOCAT_PEERPORT\\\n\\\"\"; cat; echo -e \"\\\"\\\n\\\"\""
```

## socat 基本使用

* 请求 80 端口
``` 
  root@kali:~# socat - tcp:192.168.1.1:80
  get / http 1.1/
```  

* 服务端打开侦听端口
``` 
  root@kali:~# socat - tcp4-listen:2222
```

* 客户端连接 2222 端口
``` 
  root@lamp:~# socat - tcp:192.168.1.14:2222
```  


* 服务器端接收客户端发来的文件
``` 
  # 服务端设置将接收到的信息保存到 2.txt
  root@kali:~# socat tcp4-listen:333 open:2.txt,creat,append

  # 客户端发送文件
  root@lamp:~# echo "I am xubuntu!" > 1.txt
  root@lamp:~# cat 1.txt | socat - tcp4:192.168.1.14:333

  # 服务端查看信息
  root@kali:~# cat 2.txt 
```

* 服务端侦听 23 端口
``` 
  root@kali:~# socat tcp-l:23 exec:sh,pty,stderr
```

* 客户端连接端口
``` 
  root@lamp:~# socat - tcp:192.168.1.14:23
```  


* 服务端设置端口转发
``` 
  当有流量访问本机8080端口，就转发到 192.168.1.1:80
  fork：为新连接创建独立的进程
  root@kali:~# socat tcp4-listen:8080,fork tcp4:192.168.1.1:80

```

* UDP 远程执行命令
``` 
服务器：
  root@kali:~# socat - udp-l:2000

客户端：
  root@lamp:~# echo "I am xubuntu!" | socat - udp4-datagram:192.168.1.14:2000

# 重启服务端重新开始
  root@lamp:~# echo "`id`" | socat - udp4-datagram:192.168.1.14:2000
# 重启服务端重新开始
  root@lamp:~# socat - udp-datagram:192.168.1.14:2000
```

* UDP 全端口任意内容发包
``` 
  root@lamp:~# for PORT in {1..65535}; do echo "I am xubuntu!" | socat - UDP4-DATAGRAM:192.168.1.14:$PORT; sleep .1; done
```

* 二进制编辑器
``` 
  echo -e "\0\14\0\0\c" | socat -u - file:/usr/bin、squid.exe,seek,seek=0x00074420
```


* 简单的 web 服务器
``` 
服务端开启监听端口：10081
  root@kali:~# socat -T 1 -d -d TCP-L:10081,reuseaddr,fork,crlf SYSTEM:"echo -e \"\\\"HTTP/1.0 200 OK\\\nDocumentType: text/plain\\\n\\\ndate: \$\(date\)\\\nserver:\$SOCAT_SOCKADDR:\$SOCAT_SOCKPORT\\\nclient: \$SOCAT_PEERADDR:\$SOCAT_PEERPORT\\\n\\\"\"; cat; echo -e \"\\\"\\\n\\\"\""


```

