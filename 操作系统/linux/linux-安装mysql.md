
# linux - 安装mysql

* mysql 5.1

* mysql 5.7

* 添加用户，删除用户，用户权限

## mysql 5.1
* yum安装

> yum install mysql-server mysql

* 开启服务
```sbtshell
    service mysqld start
```

* 给root用户添加密码
```sbtshell
    mysql -u root -p
    > use mysql;
    > update user set authentication_string=password('你的密码') where user='root';
    > GRANT ALL PRIVILEGES ON . TO 'root'@'%' IDENTIFIED BY '你的密码' WITH GRANT OPTION;
    > flush privileges;
    > exit;
```



## mysql 5.7

* 下载tar包，这里使用wget从官网下载
```sbtshell
    wget https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-5.7.22-linux-glibc2.12-x86_64.tar.gz
```
* 解压
```sbtshell
    tar -xvf mysql-5.7.22-linux-glibc2.12-x86_64.tar.gz
```

* 移动/usr/local/mysql下
```sbtshell
    mv mysql-5.7.22-linux-glibc2.12-x86_64 /usr/local/mysql
```
* 新建data目录
```sbtshell
    mkdir /usr/local/mysql/data
```
* 新建mysql用户、mysql用户组( 不是硬性要求 )
```sbtshell
    groupadd mysql
    useradd mysql -g mysql
    chown -R mysql.mysql /usr/local/mysql
    /usr/local/mysql/bin/mysqld --user=mysql --basedir=/usr/local/mysql/ --datadir=/usr/local/mysql/data --initialize
```
* 安装( 创建过用户选第一条命令，root用第二条 )
```sbtshell
    # 用户为mysql时
    /usr/local/mysql/bin/mysqld --user=mysql --basedir=/usr/local/mysql/ --datadir=/usr/local/mysql/data --initialize
    # 用户为root时
    /usr/local/mysql/bin/mysqld --user=root --basedir=/usr/local/mysql/ --datadir=/usr/local/mysql/data --initialize
```

* 编辑/etc/my.cnf
```sbtshell
    [mysqld]
    datadir=/usr/local/mysql/data
    basedir=/usr/local/mysql
    socket=/tmp/mysql.sock
    user=mysql
    port=3306
    character-set-server=utf8
    # 取消密码验证
    skip-grant-tables
    # Disabling symbolic-links is recommended to prevent assorted security risks
    symbolic-links=0
    # skip-grant-tables
    [mysqld_safe]
    log-error=/var/log/mysqld.log
    pid-file=/var/run/mysqld/mysqld.pid
```

* 将mysql加入服务
```sbtshell
    cp /usr/local/mysql/support-files/mysql.server /etc/init.d/mysql
```
* 添加快捷方式
```sbtshell
    ln -s /usr/local/mysql/bin/mysql /usr/bin
```

* 开启服务
```sbtshell
    service mysql start
```
* 给root用户添加密码
```shell
    /usr/local/mysql/bin/mysql -u root -p
    > use mysql;
    > update user set authentication_string=password('你的密码') where user='root';
    > GRANT ALL PRIVILEGES ON . TO 'root'@'%' IDENTIFIED BY '你的密码' WITH GRANT OPTION;
    > flush privileges;
    > exit;
```

* 将/etc/my.cnf中的skip-grant-tables删除
```sbtshell

```



## 添加用户，删除用户，用户权限

* 添加用户
> 查看全部的用户
```shell
    SELECT DISTINCT CONCAT('User: ''',user,'''@''',host,''';') AS query FROM mysql.user;
```
> 新建用户
```shell
    CREATE USER '用户名'@'localhost' IDENTIFIED BY '密码';
```

* 为用户授权
> 格式
```shell
    grant 权限 on 数据库.* to 用户名@登录主机 identified by "密码";
    grant 权限 on *.* to username@登录主机 identified by "password";
    flush privileges;
```

> 授予一个用户全部数据库的某些权限
```shell 
    grant select,delete,update,create,drop on 数据库.* to 用户名@localhost identified by '密码';
```

* 删除用户
> 删除用户
```shell 
    Delete FROM user Where User='用户名';
```
> 删除账户及权限
```shell 
    drop user 用户名@'%';
    drop user 用户名@ localhost;
```



