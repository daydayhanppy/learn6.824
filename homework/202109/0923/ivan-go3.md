## Go新手教程

> https://learnku.com/go/t/24715

### 包

一个最常见的包是 fmt 包

```go
package main
import (
  "fmt"
  "encoding/json"
)
```

### 错误处理

通过判断错误对象是否存在，以处理错误

```go
resp, err := http.Get("http://example.com/")
if err != nil {
  fmt.Println(err)
  return
}
```

写函数时要返回错误信息

```go
func Increment(n int) (int, error) {
  if n < 0 {
    return nil, errors.New("math: cannot process negative number")
  }
  return (n + 1), nil
}
```

**Panic**

`panic(执行的语句)`

未经处理的异常，panic后程序停止执行

**Defer**

`defer 执行的语句`

函数结束时执行，即使panic后也会执行

### 并发

#### go routine

可以与另一个函数并行或并发的函数

```go
func main() {
  go c()
  ...
}

func c() {}
```

#### 通道

在两个Go routine之间传递数据

```go
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

#### 单向通道

Go routine 通过通道接收数据但不发送数据

#### select

为 Go routine 处理多个通道

#### 缓冲通道

向一个通道发送多个数据





















