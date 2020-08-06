

# pwn

## 基本工具

### 逆向辅助类（分析程序）
1. IDA
2. gdb

### 漏洞利用类
1. pwntools
> https://github.com/Gallopsled/pwntools
2. zio
> https://github.com/zTrix/zio
3. Ropgadget
> https://github.com/JonathanSalwan/ROPgadget
4. checksec
5. one_gadget
6.seccomp-tools

## 保护机制
* NX
> 数据执行保护，即DEP，是指禁止程序在非可执行的内存区中执行指令。0表示允许执行代码，1表示禁止执行代码
* ASLR
> 地址空间的随机化，/proc/sys/kernel/randomize_va_space里的值可以控制系统的ASLR  
> 0： 关闭ASLR  
> 1：mmap base、stack、vdso page将随机化。这意味着“.so”文件将被加载到随即地址。  
> 2：在1的基础上增加了heap随机化

* PIE
> 代码段随机化

* RELRO
> 重定向，一般分为两种情况，即partial relro和full relro, 前者重定向信息可写，而后者不可写
* STACK CANARY
> 栈溢出保护，

## 常见的利用方法
* shellcode
> http://shell-storm.org/shellcode/

* rop

* MAgiv_Addr

* Return-to-dl_resolve

