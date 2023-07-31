

# ini配置文件

## ini配置文件
```go 
// conf.ini
[mysql]
address = 10.20.30.40
port = 3306
username = root
password = root

[redis]
host = 127.0.0.1
port = 6379
password = root
database = 0 

```

```go
// main 文件
package main

import "fmt"

type MysqlConfig struct{
    Address  string `ini:"address"`
    Port     int    `ini:"port"`
    Username string `ini:"username"`
    Password string `ini:"password"`
}

type RedisConfig struct{
    Host     string `ini:"host"`
    Port     int    `ini:"port"`
    Password string `ini:"password"`
    Database int    `ini:"database"`
}


func loadIni(fileName string, v interface{}) (err string){
    t := reflect.TypeOf(data)
    if t.Kind() != reflect.Ptr {
        err = errors.New("data param should be a pointer")
        return
    }
    
    if t.Elm().Kind() != reflect.Struct {
        err = errors.New("data param should be a struct")
        return
    }
    
    b, err := ioutil.ReadFile(fileName)
    if err != nil{
        return
    }
    
    lineSlice := strings.Split(tring(b), "\n")
    
    for idx, line := range lineSlice {
        
        line = strings.TrimSpace(line) 
        if strings.HasPrefix(line, ";") || strings.HasPrefix(line, "#") {
            continue
        }
        
        if line[0] != '[' && line[len(line) - 1] != ']') {
            err = fmt.Errorf("line:%d syntax error", idx+1)
            return
        }
        
        
        
    }
}
```

