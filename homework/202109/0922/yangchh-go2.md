## 控制

**if**

```go
package main

import "fmt"

func givemeanumber() int {
    return -1
}

func main() {
    if num := givemeanumber(); num < 0 {
        fmt.Println(num, "is negative")
    } else if num < 10 {
        fmt.Println(num, "has only one digit")
    } else {
        fmt.Println(num, "has multiple digits")
    }
}
```

**switch**

```go
package main

import (
    "fmt"
    "math/rand"
    "time"
)

func main() {
    sec := time.Now().Unix()
    rand.Seed(sec)
    i := rand.Int31n(10)

    switch i {
    case 0:
        fmt.Print("zero...")
    case 1:
        fmt.Print("one...")
    case 2:
        fmt.Print("two...")
    default:
    	fmt.Print("no match...")
    }

    fmt.Println("ok")
}
```

使用多个表达式

```go
package main

import "fmt"

func location(city string) (string, string) {
    var region string
    var continent string
    switch city {
    case "Delhi", "Hyderabad", "Mumbai", "Chennai", "Kochi":
        region, continent = "India", "Asia"
    case "Lafayette", "Louisville", "Boulder":
        region, continent = "Colorado", "USA"
    case "Irvine", "Los Angeles", "San Diego":
        region, continent = "California", "USA"
    default:
        region, continent = "Unknown", "Unknown"
    }
    return region, continent
}
func main() {
    region, continent := location("Irvine")
    fmt.Printf("John works in %s, %s\n", region, continent)
}
```

使逻辑进入到下一个case

```go
package main

import (
    "fmt"
)

func main() {
    switch num := 15; {
    case num < 50:
        fmt.Printf("%d is less than 50\n", num)
        fallthrough
    case num > 100:
        fmt.Printf("%d is greater than 100\n", num)
        fallthrough
    case num < 200:
        fmt.Printf("%d is less than 200", num)
    }
}
```

**for**

```go
func main() {
    sum := 0
    for i := 1; i <= 100; i++ {
        sum += i
    }
    fmt.Println("sum of 1..100 is", sum)
}

func main() {
    var num int64
    rand.Seed(time.Now().Unix())
    for num != 5 {
        num = rand.Int63n(15)
        fmt.Println(num)
    }
}

func main() {
    var num int32
    sec := time.Now().Unix()
    rand.Seed(sec)

    for {
        fmt.Print("Writting inside the loop...")
        if num = rand.Int31n(10); num == 5 {
            fmt.Println("finish!")
            break
        }
        fmt.Println(num)
    }
}
```

### defer ,panic, recover

- `defer` 语句会推迟函数（包括任何参数）的运行，直到包含 `defer` 语句的函数完成。 通常情况下，当你想要避免忘记任务（例如关闭文件或运行清理进程）时，可以推迟某个函数的运行。

```go
package main

import "fmt"

func main() {
    for i := 1; i <= 4; i++ {
        defer fmt.Println("deferred", -i)
        fmt.Println("regular", i)
    }
}
```

```bash
regular 1
regular 2
regular 3
regular 4
deferred -4
deferred -3
deferred -2
deferred -1
```

**使用完文件后关闭**

```go
package main

import (
    "io"
    "os"
    "fmt"
)

func main() {
    newfile, error := os.Create("learnGo.txt")
    if error != nil {
        fmt.Println("Error: Could not create file.")
        return
    }
    defer newfile.Close()

    if _, error = io.WriteString(newfile, "Learning Go!"); error != nil {
        fmt.Println("Error: Could not write to file.")
        return
    }

    newfile.Sync()
}
```

- **panic** : 运行时错误会使 Go 程序崩溃，例如尝试通过使用超出范围的索引或取消引用 nil 指针来访问数组。 你也可以强制程序崩溃。内置 `panic()` 函数可以停止 Go 程序中的正常控制流。 当使用 `panic` 调用时，任何延迟的函数调用都将正常运行。 进程会在堆栈中继续，直到所有函数都返回。 然后，程序会崩溃并记录日志消息。 此消息包含错误信息和堆栈跟踪，有助于诊断问题的根本原因。

```go
package main

import "fmt"

func highlow(high int, low int) {
    if high < low {
        fmt.Println("Panic!")
        panic("highlow() low greater than high")
    }
    defer fmt.Println("Deferred: highlow(", high, ",", low, ")")
    fmt.Println("Call: highlow(", high, ",", low, ")")

    highlow(high, low + 1)
}

func main() {
    highlow(2, 0)
    fmt.Println("Program finished successfully!")
}
```

```bash
Call: highlow( 2 , 0 )
Call: highlow( 2 , 1 )
Call: highlow( 2 , 2 )
Panic!
Deferred: highlow( 2 , 2 )
Deferred: highlow( 2 , 1 )
Deferred: highlow( 2 , 0 )
panic: highlow() low greater than high

goroutine 1 [running]:
main.highlow(0x2, 0x3)
    /tmp/sandbox/prog.go:13 +0x34c
main.highlow(0x2, 0x2)
    /tmp/sandbox/prog.go:18 +0x298
main.highlow(0x2, 0x1)
    /tmp/sandbox/prog.go:18 +0x298
main.highlow(0x2, 0x0)
    /tmp/sandbox/prog.go:18 +0x298
main.main()
    /tmp/sandbox/prog.go:6 +0x37

Program exited: status 2.
```

- **recover**   :   有时，想要避免程序崩溃，改为在内部报告错误。 或者，想要先清理混乱情况，然后再让程序崩溃。 例如，想要关闭与某个资源的连接，以免出现更多问题 .。`recover`函数可以在程序崩溃之后重新获得控制权，只会在同时调用 `defer` 的函数中调用 `recover`

```go
package main

import "fmt"

func highlow(high int, low int) {
    if high < low {
        fmt.Println("Panic!")
        panic("highlow() low greater than high")
    }
    defer fmt.Println("Deferred: highlow(", high, ",", low, ")")
    fmt.Println("Call: highlow(", high, ",", low, ")")

    highlow(high, low + 1)
}

func main() {
    defer func() {
    handler := recover()
        if handler != nil {
            fmt.Println("main(): recover", handler)
        }
    }()
    
    highlow(2, 0)
    fmt.Println("Program finished successfully!")
}
```

```bash
Call: highlow( 2 , 0 )
Call: highlow( 2 , 1 )
Call: highlow( 2 , 2 )
Panic!
Deferred: highlow( 2 , 2 )
Deferred: highlow( 2 , 1 )
Deferred: highlow( 2 , 0 )
main(): recover from panic highlow() low greater than high

Program exited.
```

