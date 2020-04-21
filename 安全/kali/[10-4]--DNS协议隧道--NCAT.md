
# DNS 协议隧道--NCAT

* 简介

## 简介
* 被称为众多 NC 衍生版中最优的选择
  
* 代理功能
  
    * 默认侦听端口：31337
    * ncat -l 8080 --proxy-type http --proxy-auth user:pass
* broker 中介功能
  
    * AB 不同但AC、BC互通
    * 服务器：ncat -l 333 --broker
    * 客户端之间发送任何信息都会被 hub 到其他客户端
    * 批量执行命令：ncat 1.1.1.1 --sh-exec “echo ‘pwd’”
    * 批量传文件：ncat --send-only 1.1.1.1 < inputfile

