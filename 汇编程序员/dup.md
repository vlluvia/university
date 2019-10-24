# dup 伪指令

* dd 100 dup ('1') -> 填充100次'1'
* dd 100 dup (1) -> 填充100次1


## 代码
```
assume cs:code,ds:data,ss:stack
    
data segment
    dd 100 dup ('1')
    dd 100010
    dw 100
    dw 0
data ends
    
stack segment
    db 120 dup (0)
stack ends

code segment
    start:  mov ax,stack
            mov ss,ax
            mov sp,128
            
            mov ax,4C00H
            int 21H
            
code ends

end start            

```