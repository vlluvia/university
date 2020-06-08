
# Mysql基本知识

* 常见命令
* 基本语言
* 语法规范
## 常见命令
* 登录
``` 
mysql –h 主机名 –u用户名 –p密码
```

* 退出
``` 
exit
```


## 基本语言
* DML
> DML用于查询与修改数据记录，包括如下SQL语句
``` 
INSERT：添加数据到数据库中
UPDATE：修改数据库中的数据
DELETE：删除数据库中的数据
SELECT：选择（查询）数据
```

* DDL
> DDL用于定义数据库的结构，比如创建、修改或删除
  数据库对象，包括如下SQL语句

``` 
CREATE TABLE：创建数据库表
ALTER TABLE： 更改表结构、添加、删除、修改列长度
DROP TABLE：删除表
CREATE INDEX：在表上建立索引
DROP INDEX：删除索引
```

* DCL
> DCL用来控制数据库的访问，包括如下SQL语句

``` 
GRANT：授予访问权限
REVOKE：撤销访问权限
COMMIT：提交事务处理
ROLLBACK：事务处理回退
SAVEPOINT：设置保存点
LOCK：对数据库的特定部分进行锁定
```

## 语法规范
> 不区分大小写  
> 每句话用;或\g结尾  
> 各子句一般分行写  
> 关键字不能缩写也不能分行  
> 用缩进提高语句的可读性  

* 进入 mysql
> mysql –uroot –p####

*  查看 mysql 中有哪些个数据库
> show databases;
* 使用一个数据库
> use 数据库名称;

* 新建一个数据库
>  create database 名 数据库名

* 查看指定的数据库中有哪些数据表
> show tables;

* 查看表的结构
> desc 表名

*  删除表
> drop table 表名

* 查看表中的所有记录: 
> select * from 表名;

* 向表中插入记录：
> insert into 表名( 列名列表) values( 列对应的值的列表);

* 修改记录: 
> update 表名 set 列1 = 列1 的值, 列2 = 列2 的值 where …

* 删除记录: 
> delete from 表名 where ….

* 查询所有列: 
> select * from 表名

*  查询特定的列: 
> select 列名1, 列名2, … from 表名

* 对查询的数据进行过滤： 
> 使用 where 子句

* 运算符
``` 
+ - * /
>= <=
== !=
between .. and ..
in()
like '%a%'  # 查询 name 中有 a 的人的名字
like '__a%' # 查询 name 中 第 3 个字母是 a 的人的名字
is null     # 查询 email 为 空 的所有人的信息
is not null # 查询 email 为 非空 的所有人的信息
order by salary      # 查询所有客户信息, 且按 salary 升序排列
order by salary desc #  查询所有客户信息, 且按 salary 降序排列

```

