
# Go环境

* 安装

* 目录结构

* Hello world

## 安装

* 安装网址

> https://golang.google.cn/dl/

* 查看版本
> ctrl+r -> cmd -> go version

* 配置GoPath
1. 环境变量中的用户变量里添加(修改)go存放项目的目录(GoPath)， 如: G:\\Go
2. G:\\Go目录下创建三个文件夹：bin、pkg、bin
3. 环境变量中的用户变量里Path添加(修改) G:\\Go\bin
4. cmd -> 端中输入 go env


## 目录结构
* bin: 存放编译后的二进制文件
* pkg: 存放编译后的库文件
* src: 存放代码文件
    - vlluvia.vom 项目组的网址
        - 前端
        - 后端
        - 基础架构
        
    - github.com

## hello world
* G:\Go\src\vlluvia.com\study1\helloworld\main.go 代码
```go
package main

import "fmt"

func main() {
	fmt.Printf("hello, world\n")
}
```

* G:\Go\src\vlluvia.com\study1\helloworld\ 下编译 main.go
> go build  
> go build -o hello.exe  
> go run  
> go install  先编译，拷贝执行文件到bin目录

* 跨平台编译
```go 
// 编译成在linux下可执行文件
SET CGO_ENABLED = 0
SET GOOS = linux
SET GOARCH=amd64
```