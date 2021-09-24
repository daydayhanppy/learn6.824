#并发

Go 中的并发可以通过轻量级线程的 Go routine 来实现。
##Go routine
>package main
import (
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
//=> I am main
//=> I am concurrent

Go routine 之间共享资源的方法：通过 Go 语言的通道。
##通道
 在创建通道时，必须指定通道接收的数据类型。
 >c := make(chan string) //这是一个string类型的通道
```
package main
import "fmt"
func main(){
  c := make(chan string)
  go func(){ c <- "hello" }()
  msg := <-c
  fmt.Println(msg)
}
//=>"hello"
```
接收方通道将会一直等待发送方向通道发送数据。

通道可以定义为单向的
select case 可以处理程序中的多个通道
使用缓冲通道， 在缓冲区满之前接受方不会收到任何消息
```
package main

import "fmt"

func main(){
  ch := make(chan string, 2)
  ch <- "hello"
  ch <- "world"
  fmt.Println(<-ch)
}
```