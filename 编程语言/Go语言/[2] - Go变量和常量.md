
# Go变量

* 变量声明
* 常量声明
* 基本数据类型

## 变量声明
* 声明变量
```go 
package main

import "fmt"
// 函数外只能 变量\常数\函数\类型 的声明
var name string
var age int
var isOk bool

func main() {
    name  = "hello"
    age = 17
    isOk = true
}
```
* 批量声明
```go
package main

import "fmt"
// 函数外只能 变量\常数\函数\类型 的声明
var(
	name string
	age int 
	isOk bool
)

func main() {
    name  = "hello"
    age = 17
    isOk = true
}
```

* 累型声明
```go 
package main

import "fmt"
// 函数外只能 变量\常数\函数\类型 的声明

func main() {
    var name = "hello"
    var age = 12
}
```

* 简短变量声明
```go 
package main

import "fmt"
// 函数外只能 变量\常数\函数\类型 的声明

func main() {
    name := "hello"
    age := 12
}
```

* 匿名变量声明
```go 
package main

import "fmt"
// 函数外只能 变量\常数\函数\类型 的声明
func foo()(int, string){
    return 10, "hello world"
}
func main() {
    x, _ := foo()
    _, y := foo()
}
```

## 常量声明

* 常量声明
```go 
package main

import "fmt"
// 常量定义之后不能修改
const pi = 3.1415926

func main() {

}
```
* 批量声明
```go 
package main

import "fmt"

const (
    pi = 3.1415926
    e = 2.7182818
)
// 没有赋值，与上一行一致
const (
    n1 = 100
    n2
    n3 
)
func main() {

}
```

## iota
```go 
package main

import "fmt"

// const出现时 iota初始化为0
// 每出现一行 iota 加一
const (
    a1 = iota // 0
    a2 = iota // 1
    a3 = iota // 2
)

const (
    a1 = iota   // 0
    a2          // 1
    _           // 2
    a3          // 3
)

const (
    a1 = iota   // 0
    a2 = 100    // 100
    a3 = iota   // 2
    a4          // 3
)
const (
    d1,d2 = iota +1, iota + 2 // d1:1  d2: 2
    d3,d4 = iota +1, iota + 2
)

func main() {

}
```

## 基本数据类型
* int
```go
// 有符号位 
int8
int16
int32
int64

// 无符号位
uint8
uint16
uint32
uint64

// 特殊整型
uint
int
uintptr         -- 无符号整型，用于存放一个指针   
```

* 浮点数
```go 
double32
double64
```

* 复数
```go 
complex64
complex128
```
 
 * 布尔值
 ```go 
bool
 ```
 
 * 字符串
 ```go 
 string
 
 // 多行字符串
 str := `
    第一行
    第二行
 `
 
 // 字符串拼接
 name := "hello"
 where := "beijin"
 str := name + where
 
 // 分割
 str := "nothing to do"
 str := strings.Split(str, "to")
// 包含
strings.Contains(str, "do")
// 前缀
strings.HasPrefix(str, "not")

// 后缀
strings.HasSuffix(str, "do")

// 字符串的位置
strings.Index(str, "c")
strings.LastIndex(str, "d")

// 拼接
strings.Join(str, "+") 


// 循环遍历
for i:=0 ; i < len(str) ; i++{
    fmt.Printf("%c", str[i])
}

for _, c := range s{
    fmt.Printf("%c", c)
}

// 字符串修改
str1 := "你好"
str2 := []rune(str1)
str2[0] = '我'
fmt.Println(string(str2))
 ```
 
 