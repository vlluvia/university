
# reverse

## 逆向分析的主要方法
* 静态分析法
* 动态分析法
 
## 汇编指令体系结构
### x86
#### x86指令体系结构寄存器具体如下
```
通用寄存器:：EAX、EBX、ECX、EDX、ESI、EBP、ESP
指令指针寄存器：指向当前要执行的指令
状态标志寄存器：根据状态标志寄存器中状态的值控制程序的分支跳转
段寄存器：CS、DS、SS、ES、FS、GS。在当前的操作系统中，CS、DS、SS和ES的段寄存器的基地址通常为0
特殊寄存器：包括DR0-DR7，用于设置硬件断点
```
#### 汇编指令集
* 描述
> x86汇编代码有两种语法记法：Intel和AT&T。常用的逆向分析工具 IDA Pro、Ollydbg和MASM通常用Intel记法，而UNIX系统上通常用AT&T记法。

* 语法格式
> 操作项 目的操作数， 源操作数

* 分类
1. 数据传送指令
> MOV DEST, SRC

2. 栈操作与函数调用
> PUSH 、POP

3. 算数、逻辑运算指令
> add、sub、mul、div、and、or、xor等

4. 控制转移指令
> cmp ：对两个操作书执行减法操作， 修改状态标志寄存器    
> test  ：对两个操作数执行与操作，修改状态标志寄存器    
> jmp  ：强制跳转指令  
> jcc    ：条件跳转指令，包括jz、jnz

5. 特殊指令

### x64

* 寄存器组
> RAX、RBX、RDX、RCX、RBP、RDI、RSI、RSP、R8-R15

* 系统调用指令
> syscall/sysret

* x64应用程序二进制接口
1. Microsoft's x64 ABI
2. SysV x64 ABI

