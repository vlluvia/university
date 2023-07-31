

# switch 和 goto

* switch

* goto

## switch
```go 
package main

func main(){
    var n = 5
    
    switch n {
        case 1:
            fmt.Println("A")
        case 2:
            fmt.Println("B")
        default:
            fmt.Println("C")
    }
}

```
* 实例1
```go 
package main

func main(){
    
    switch n := 3; n {
        case 1, 2, 3:
            fmt.Println("A")
        case 4, 5, 6:
            fmt.Println("B")
        default:
            fmt.Println("C")
    }
}
```
* 实例2
```go 
package main

func main(){
    
    switch n := 3; n {
        case n > 10:
            fmt.Println("A")
        case n < 10:
            fmt.Println("B")
        default:
            fmt.Println("C")
    }
}
```

## goto
```go 
package main

import "fmt"

func main(){
    for i := 0 ; i < 10; i++ {
        if i == 3 {
            goto tag
        }
        fmt.Printf("%d", i)
    }
    return 
    tag:
        fmt.Print("结束", i)
}



```

