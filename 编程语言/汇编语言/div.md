
# 除法

* 被除数 -> ax
* 除数-> 寄存器或者内存中，用8位寄存器(bl,cl,dl,dh,ch,bh)或者 byte ptr
* 商 -> al
* 余数 -> ah


## 代码

```
assume cs:code,ds:data,ss:stack
    
data segment
    db 16,0,0,0
    db 0FFH,0FFH,,FFGH,0FFH
    db 0,0,0,0
    db 0,0,0,0
data ends
    
stack segment
    dw 0,0,0,0
    dw 0,0,0,0
    dw 0,0,0,0
    dw 0,0,0,0
stack ends
    
code segment
    
    start:  mov ax,stack
            mov ss,ax
            mov sp,32
            
            mov ax,data
            mov ds,ax
            
;           mov ax,16
;           mov bl,3
            
;           div byte ptr ds:[0]

            mov ax,ds:[0]
            mov dx,ds:[2]
            
            mov bx,3
            
            div bx
               
    
```