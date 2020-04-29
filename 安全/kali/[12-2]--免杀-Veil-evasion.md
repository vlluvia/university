
# Veil-evasion

* 描述
> * 属于 Veil-framework 框架的一部分
> * 由 Python 语言编写
> * 用于自动生成免杀payload
>   - 集成msf paypload，支持自定义 payload
>   - 集成各种注入技术
>   - 集成各种第三方工具
>       - Hypersion、PEScrambler、BackDoor Factory
>   - 继承各种开发打包运行环境
>       - Python：pyinstaller / py2exe
>       - C# ：mono for .NET
>       - C：mingw32


* 安装地址
> github：https://github.com/Veil-Framework/Veil-evasion

1. 安装失败 - 修改 `/etc/apt/sources.list`
``` 
# Regular repositories
deb http://http.kali.org/kali sana main non-free contrib
deb http://security.kali.org/kali-security sana/updates main contrib non-free
# Source repositories
deb-src http://http.kali.org/kali sana main non-free contrib
deb-src http://security.kali.org/kali-security sana/updates main contrib non-free
然后
apt-get update&apt-get upgrade -y
```


* 可支持的payload有50多种
[*] 可支持生成payloads:
1) auxiliary/coldwar_wrapper
2) auxiliary/macro_converter
3) auxiliary/pyinstaller_wrapper
4) c/meterpreter/rev_http
5) c/meterpreter/rev_http_service
6) c/meterpreter/rev_tcp
7) c/meterpreter/rev_tcp_service
8) c/shellcode_inject/flatc
9) cs/meterpreter/rev_http
10) cs/meterpreter/rev_https
11) cs/meterpreter/rev_tcp
12) cs/shellcode_inject/base64_substitution
13) cs/shellcode_inject/virtual
14) go/meterpreter/rev_http
15) go/meterpreter/rev_https
16) go/meterpreter/rev_tcp
17) go/shellcode_inject/virtual
18) native/backdoor_factory
19) native/hyperion
20) native/pe_scrambler
21) perl/shellcode_inject/flat
22) powershell/meterpreter/rev_http
23) powershell/meterpreter/rev_https
24) powershell/meterpreter/rev_tcp
25) powershell/shellcode_inject/download_virtual
26) powershell/shellcode_inject/download_virtual_https
27) powershell/shellcode_inject/psexec_virtual
28) powershell/shellcode_inject/virtual
29) python/meterpreter/bind_tcp
30) python/meterpreter/rev_http
31) python/meterpreter/rev_http_contained
32) python/meterpreter/rev_https
33) python/meterpreter/rev_https_contained
34) python/meterpreter/rev_tcp
35) python/shellcode_inject/aes_encrypt
36) python/shellcode_inject/aes_encrypt_HTTPKEY_Request
37) python/shellcode_inject/arc_encrypt
38) python/shellcode_inject/base64_substitution
39) python/shellcode_inject/des_encrypt
40) python/shellcode_inject/download_inject
41) python/shellcode_inject/flat
42) python/shellcode_inject/letter_substitution
43) python/shellcode_inject/pidinject
44) python/shellcode_inject/stallion
45) ruby/meterpreter/rev_http
46) ruby/meterpreter/rev_http_contained
47) ruby/meterpreter/rev_https
48) ruby/meterpreter/rev_https_contained
49) ruby/meterpreter/rev_tcp
50) ruby/shellcode_inject/base64
51) ruby/shellcode_inject/flat
