### 并发
```Go
package main
import(
    "fmt"
    "time"
)
func main() {
    go c()
    fmt.Println("I am main")
    time.Sleep(time.Second * 2)
}
func c() {
    time.Sleep(time.Second * 2)
    fmt.Println("I am concurrent")
}
```
### 通道
可以使用通道在两个goroutine之间传递数据，在创建通道时，必须指定通道接收的数据类型
```Go
package main
import "fmt"
func main() {
    c := make(chan string)
    go func() {c <- "hello"}()
    msg := <- c
    fmt.Println(msg)
}
```
单向通道


使用select为goroutine处理多个通道
```Go
package main

import (
 "fmt"
 "time"
)

func main() {
 c1 := make(chan string)
 c2 := make(chan string)
 go speed1(c1)
 go speed2(c2)
 fmt.Println("The first to arrive is:")
 select {
 case s1 := <-c1:
  fmt.Println(s1)
 case s2 := <-c2:
  fmt.Println(s2)
 }
}

func speed1(ch chan string) {
 time.Sleep(2 * time.Second)
 ch <- "speed 1"
}

func speed2(ch chan string) {
 time.Sleep(1 * time.Second)
 ch <- "speed 2"
}
```

缓冲通道：可以向一个通道发送多个数据，在缓冲区满之前，接收方不会收到任何消息
```Go
package main

import "fmt"

func main(){
  ch := make(chan string, 2)
  ch <- "hello"
  ch <- "world"
  fmt.Println(<-ch)
}
```

