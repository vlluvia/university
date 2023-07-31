
# if 和 for

* if

* for

## if

```Go
if 表达书1 {

}else if 表达式2 {

}else{

}
```
* 实例1
```go 
age := 18
if age > 18 {
    fmt.Println("A")
} else if age > 15 {
    fmt.Println("B")
} else {
    fmt.Println("C")
}
```


* 实例2
```go 
if age:=19 ; age > 18 {

} else {

}
```


## for
```go 
for 初始话语句 ; 条件表达式 ; 结束语句 {
    循环语句
}
```

* 实例1
```go
for i:= 0 ; i < 10 ; i++ {
    fmt.Println(i)
}
```
* 实例2
```go 
i:= 0
for ; i < 10 ; i++ {
    fmt.Println(i)
}
```
* 实例3

```go 
i:= 0
for i < 10 {
    fmt.Println(i)
    i++
}
```
* 实例4
```go 
str := "hello world"

for i,j := range str{
    fmt.Println("%d %c\n", i, j)
}

```
