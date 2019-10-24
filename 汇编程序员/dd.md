

# dd 伪指令
define dword

* db (define byte) :    8位

* dw (define word):     16位

* dd (define dword):    32位


## 代码
```$xslt
assume cs:code,ds:data,ss:stack
    
data segment
    dd 1
    dw 1
    db 1
data ends
    
stack segment
    dw 0,0,0,0
    dw 0,0,0,0
    dw 0,0,0,0
    dw 0,0,0,0
stack ends
```
 