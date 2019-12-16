
# 字典

* crunch

* cupp

* cewl

* john

* hydra

* medusa

* hash

## crunch
```shell 
    0. crunch <min-len> <max-len> [<charset string>] [options]
    1. crunch 6 6 0123456789 -o START -d 2 -b 1mb / -c 100
        -b 按大小分割文件(kb/kib、mb/mib、gb/gib)
        -c 字典行数
        以上两个参数必须与-o START 结合使用
        -d 同一个字符连贯出现数量

    2. 字符集
        crunch 4 4 -f /usr/share/crunch/charset.lst lalpha-sv -o 1.txt

    3. 无重复字符
        crunch 1 1 -p 1234567890 | more

    4. 读取文件中每行内容作为基本字符生成字典
        crunch 1 1 -q read.txt

    5. 字典组成规则
        crunch 6 6 -t @,%%^^ | more
        @ : 小写字母 lalpha
        , : 大写字母 ualpha
        % : 数字 numeric
        ^ : 符号 symbols
		
    6. 输出文件压缩
        crunch 4 4 -t @,%^ -o 1.txt -z 7z
```

## cupp
```shell 
    git clone https://github.com/Mebus/cupp.git
    python cupp.py -i
```

## cewl
> 收集网站信息生成字典
```shell 
    cewl 1.1.1.1 -m 3 -d -e -c -v -w a.txt
        -m : 最小单词长度
        -d : 爬网深度
        -e : 收集email地址信息
        -c : 每个单词出现次数
```
## john
```shell
    vi /etc/john/john.conf
```
## hydra
```shell 
    a. windows密码破解
        hydra -l administrator -P pass.lst smb://1.1.1.1 -vVd
        hydra -l administrator -P pass.lst rdp://1.1.1.1 -t 1 -vV

    b. linux密码破解
        hydra -l root -P pass.lst ssh://1.1.1.1 -vV

    c. 其他服务器密码破解
        hydra -L user.lst -P pass.lst ftp:1.1.1.1 -s 2121 -e nsr -o p.txt -t 64

    d. 图形化界面
        xhydra
```

## medusa
```shell 
    medusa -d
    a. 破解windows密码
        medusa -M smbnt -h 1.1.1.1 -u administrator -P pass.lst -e ns -F
    b. 破解linux ssh密码
        medusa -M ssh -h 192.168.20.10 -u root -P pass.lst -e ns -F
    c. 其他服务器破解
    medusa -M mysql -h 1.1.1.1 -u root -P pass.lst -e ns -F
```

## hash
```shell 
    hashid{
        hashid <hash>
    }

    hash-identifier{

    }

    hashcat{
			
    }

    oclhashcat{
        基于gpu
    }
    
    rainbowcrack{
        https://www.freerainbowtables.com/en/download/
    }

    ophcrack{
        http://ophcrack.sourceforge.net/tables.php
    }
    1. windows 
```
