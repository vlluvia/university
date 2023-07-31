
# time 和 日志

* time

* 日志


## time

* 实例1
```go 
now := time.Now()
fmt.Println(now.Year())
fmt.Println(now.Month())
fmt.Println(now.Day())
fmt.Println(now.Hour())
```

* 实例2 - 时间戳
```go 
now := time.Now()
fmt.Println(now.Unix())
fmt.Println(noew.UnixNano())
```

* 实例3
```go 
fmt.Println(now.Add(24 * time.Hour))
```

* 实例4
```go
timer := time.Tick(time.Second)
for t:= range timer{
    fmt.Println(t)
}
```
* 实例5 - 格式化
```go 
fmt.Println(now.Format("2006-05-06"))
fmt.Println(now.Format("2006/01/02 15:04:05"))
fmt.Println(now.Format("2006/01/02 15:04:05.000"))
fmt.Println(now.Format("2006/01/02 03:04:05 PM"))
```

* 实例6 - 字符串转日期
```go 
to, err := now.parse("2006/01/02 15:04:05", "2000/12/15")
if err != nil {
    fmt.Printf("parse error")
    return
}

```

## 日志
```go
log.Println("日志信息"")
```


* 实例1
```go 
file, err := os.OpenFile("log.txt", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
if err ~!= nil {
    fmt.Printf("open file failed, err %v\n", err)
    return
}

log.SetOutput(file)
for{
    log.Println("这是一条测试日志")
    time.Sleep(timr.Second * 3)
}
```



