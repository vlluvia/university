
# mkdir、touch

## mkdir

* 功能说明
> mkdir命令是u make directories"中每个单词的粗体字母组合而成，其功能是创建目 录，默认情况下，如果要创建的目录已存在，则会提示此文件已存在；而不会继续创建目录。

* 语法格式
``` 
mkdir [option] [directory] 
mkdir ［选项］ ［目录］
```

* 选项说明
``` 
参数选项	解释说明（带※的为重点）
-P      1.递归创建目录，递归的意思是父目录及其子目录及子目录的子目录……淤
        2. 即使要创建的目录事先已存在也不会报错提示目录已存在
-m      设置新创建目录的默认目录对应的权限
-V      显示创建目录的过程

```

* 实例
``` 
mkdir test1

# 递归创建文件
mkdir -p package/file1

# 显示创建过程
mkdir -pv package2/files

# 创建时给默认权限
mkdir -m 333 test

# 同时创建多个同级目录
mkdir -pv package/{dir1, dir2}/{dir3, dir4}
tree -d package/

mkdir -p package/test{1..5} package2/test{a..g}

```

## touch

* 功能说明
> touch命令有两个功能：一是创建新的空文件；二是改变已有文件的时间戳属性。

* 语法格式
``` 
touch ［option］ ［file］
touch ［选项］	［文件］

```

* 选项说明
``` 
参数选项	解释说明
-a      只更改指定文件的最后访问时间
-d      STRING	使用字符串STRING代表的时间作为模板设置指定文件的时间属性
-m      只更改指定文件的最后修改时间
-r      file	将指定文件的时间属性设置为与模版文件file的时间属性相同
-t      STAMP	使用［［CC］YY］MMDDhhmm［.ss］格式的时间设置文件的时间属性。格式的含义从左 到右依次为：世纪、年、月、日、时、分、秒

```

* 实例
``` 
# 创建文件
touch file.txt      
touch file1. txt file2.txt
touch file{01..06}

# stat 查看文件的时间戳
stat file
# 更改文件最后访问时间
touch -a file
touch -m file

# 指定创建后文件的修改时间
touch -t 20200101 file

# 修改文件时间属性, file文件的时间戳和a.txt一致
touch -r a.txt file




```
