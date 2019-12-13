

# windows缓存区溢出

* fuzzer


## fuzzer

* 服务器: windows xp

* 目标软件: SLMail 5.5.0 Mail Server 

* 测试工具: immunityDebugger_1_85_setup.exe 

* mona.py
```python

```

* SLMail 5.5.0 Mail Server 
1. POP3 PASS 命令存在缓存区溢出漏洞 
2. 无需身份验证实现远程代码执行
3. DEP: 阻止代码从数据也被执行
4. ASLR: 随机内存地址加载执行程序和DLL， 每次重启地址变化



