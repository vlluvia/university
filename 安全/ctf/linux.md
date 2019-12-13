
# linux

* 命令

## 命令
```linux
    
pwd 显示当前所在的工作目录

cd 更改目录
    1. cd dir 进入一个目录dir
    2. cd . 可以验证"." 代表当前目录
    3. cd .. 进入当前目录的上一级目录
    4. cd - 回到刚才工作的目录

touch file  创建文件file

mkdir dir 创建目录dir

rm{
    -i 确认信息
    -r 地柜删除目录
    -f 强制删除
}

mv [option] file dst        移动、重命名文件或目录 


cp [option] file dst        
    
cat 显示文件的所有内容

more 查看文件内容，只可以往下查看不能往上查看

less 分页显示文件内容

head、tail 显示文件的首、尾（默认为10行）
    tail -num file 显示文件file的末尾10行 tail -20 /var/log/messages

ifconfig{
    ifconfig ethN   查看网卡N的信息
    ifconfig ethN ip/down
    ifconfig ethN 192.168.1.1. netmask 255.255.255.128
}

dhclient    重新获取IP地址
    -r  释放地址
    
 
```