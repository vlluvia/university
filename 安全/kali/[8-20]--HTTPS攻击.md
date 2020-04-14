

# HTTPS攻击

* HTTPS 简介
* openssl 用法
* sslscan 用法
* sslyze
* 在线检查


## HTTPS 简介
* HTTPS 作用
1. CIA
1. 解决的是信息传输付哦成数据被篡改、窃取
1. 解密：对称、非对称、单向

* HTTPS 攻击方法
1. 降级攻击
1. 解密攻击（明文、证书伪造）
1. 协议漏洞、实现方法的漏洞、配置不严格

* SSL/TLS 也被用于其他场景的传输通道加密
1. 邮件传输（SMTP和POP3都是明文传输，需要在服务器间、客户端和服务器之间进行传输加密）
1. 数据库服务器间
1. LDAP（轻量级目录访问协议 X.509）身份认证服务器间
1. SSL VPN
1. 远程桌面 RDP 通信过程中的加密和身份认证

* SSL弱点
1. SSL 是不同的对称、非对称、单向机密算法的组合加密实现（cipher suite）
1. 服务器端为提供更好的兼容性，选择大量过时的 cipher suite
1. 协商过程中强迫降级加密强度
1. 现代处理器计算能力可以再可接受时间呗破解过时加密算法
1. 购买云计算资源破解

* HTTPS 加密过程
1. 三次握手
1. 协商加密算法（对称加密算法）
1. 客户端获取服务器的公钥证书
1. 客户端在自己的根证书列表来验证服务器公钥证书，验证成功说明服务器公钥证书可信任
1. 客户端随机生成一次性会话密钥（对称密钥）
1. 客户端使用服务器的公钥加密一次性会话密钥，发给服务器
1. 服务器用自己的私钥解密，获取一次性会话密钥
1. 客户端对明文进行 Hash 计算，得到Hash值1
1. 客户端使用会话密钥加密明文和Hash值1，然后将密文1进行 Hash 计算生成 Hash值2
1. 客户端使用服务器公钥加密密文1和Hash值2，生成密文2，将密文2发送给服务器
1. 服务器解密密文2，获取密文1和Hash2，然后对密文1进行Hash计算，并比较解密得到的Hash2和计算得到的Hash值是否相同（完整性）
1. 用会话密钥解密密文1，得到明文和Hash值1，然后对明文进行Hash计算，并比较解密得到的Hash1和计算得到的Hash值是否相同（完整性）


## openssl 用法

> 直接调用 openssl 库识别目标服务器支持的 SSL/TLS cipher suite  
  openssl 需要大量密码学相关知识，命令复杂，结果可读性差


* 百度, 查看使用的安全协议信息
> root@kali:~# openssl s_client  -connect www.baidu.com:443

* 淘宝, 查看使用的安全协议信息
> root@kali:~# openssl s_client  -connect www.taobao.com:443

* 验证不安全的加密算法是否可以连接
``` 
root@kali:~# openssl s_client -tls1_2 -cipher 'ECDH-RSA-RC4-SHA' -connect www.taobao.com:443
```
* 验证不安全的加密套件是否可以连接
``` 
root@kali:~# openssl s_client -tls1_2 -cipher “NULL,EXPORT,LOW,DES” -connect www.taobao.com:443
```

* 可被破解的 cipher suite
``` 
root@kali:~# openssl ciphers -v "NULL,EXPORT,LOW,DES"
```

* 查看官网公布的安全的和不安全的加密算法信息
``` 
www.openssl.org/docs/manmaster/man1/ciphers
```

* openssl 使用帮助
``` 
root@kali:~# man openssl
```


## sslscan 用法
* 简介
> 自动识别 ssl 配置错误、过期协议、过时 cipher suite 和 hash 算法  
  默认会见擦汗 CRIME、heartbleed 漏洞  
  绿色表示安全、红色黄色需要引起注意  


* 使用
1. TLS 支持的 cipher suite
``` 
sslscan –tlsall www.taobao.com:443
```

2. 分析证书详细信息
``` 
sslscan –show-certificate –no-ciphersuites www.taobao.com:443
```

## sslyze
* 简介
> python 编写  
  检查 ssl 过时版本  
  检查存在弱点的 cipher suite  
  扫描多站点时，支持来源文件  
  检查是否支持会话恢复  

* 使用
``` 
root@kali:~# sslyze --regular www.taobao.com:443

```


## 在线检查
> 在线检查: www.ssllabs.com/ssltest/
