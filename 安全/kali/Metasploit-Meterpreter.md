
# Meterpreter

* 介绍
> * 高级、动态、可扩展的Payload
>   - 基于meterpreter上下文利用更多漏洞发起攻击
>   - 后渗透测试阶段一站式操作界面
> * 完全基于内存的DLL注入式 payload（不写硬盘）
>   - 注入合法进程并建立stager
>   - 基于Stager上传和预加载DLL进行扩展模块的注入（客户端API）
>   - 基于stager建立的socket连接建立加密的TLS/1.0通信隧道
>   - 利用TLS隧道进一步加载后续扩展模块（避免网络取证）
> * 服务端使用C语言编写
> * 客户端提供基于ruby的全特性API（支持任何语言）





