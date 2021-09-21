# 2. learn GO

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello World!")
}
```

**运行Go应用：**

```go
go run main.go
```

**生成可执行文件：**

```go
go build main.go
```

 `package main` 语句中告诉 Go，要创建的应用是一个可执行程序（可以运行的文件）。“Hello World!” 应用是 `main` 包的一部分。 包是一组常用的源代码文件。 每个可执行应用都具有此第一行，即使项目或文件具有不同的名称。

**自定义函数**

```go
package main

import (
    "os"
    "strconv"
)

func main() {
    sum := sum(os.Args[1], os.Args[2])
    fmt.Println("Sum:", sum)
}

func sum(number1 string, number2 string) int {
    int1, _ := strconv.Atoi(number1)
    int2, _ := strconv.Atoi(number2)
    return int1 + int2
}
```

**返回多个值**

```go
func calc(number1 string, number2 string) (sum int, mul int) {
    int1, _ := strconv.Atoi(number1)
    int2, _ := strconv.Atoi(number2)
    sum = int1 + int2
    mul = int1 * int2
    return
}
```

**更改函数参数数值（指针）**

Go 是**“按值传递”**编程语言。 这意味着每次向函数传递值时，Go 都会使用该值并创建本地副本（内存中的新变量）。 在函数中对该变量所做的更改都不会影响你向函数发送的更改。

```go
package main

func main() {
    firstName := "John"
    updateName(firstName)
    fmt.Println(firstName)
}

func updateName(name string) {
    name = "David"
}
```

## 包 package

**main包**

通常情况下，默认包是 `main` 包。 如果程序是 `main` 包的一部分，Go 会生成二进制文件。 运行该文件时，它将调用 `main()` 函数。当使用 `main` 包时，程序将生成独立的可执行文件。 但当程序非是 `main` 包的一部分时，Go 不会生成二进制文件。 它生成包存档文件（扩展名为 .a 的文件）。

**创建包**

```bash
src/
	calculator/
		sum.go
```

用包的名称初始化`sum.go`文件

 Go 不会提供 `public` 或 `private` 关键字，以指示是否可以从包的内外部调用变量或函数。 但 Go 须遵循以下两个简单规则：

- 如需将某些内容设为专用内容，请以小写字母开始
- 如需将某些内容设为公共内容，请以大写字母开始

```go
package calculator

var logMessage = "[LOG]"

// Version of the calculator
var Version = "1.0"

func internalSum(number int) int {
    return number - 1
}

// Sum two integer numbers
func Sum(number1, number2 int) int {
    return number1 + number2
}
```

## 模块

模块还有助于其他开发人员引用代码的特定版本，并更轻松地处理依赖项

若要为 `calculator` 包创建模块，在根目录 (`$GOPATH/src/calculator`) 中运行

```bash
go mod init github.com/myuser/calculator
```

运行此命令后，`github.com/myuser/calculator` 就会变成模块的名称。 在其他程序中，将使用该名称进行引用, 同时生成`go.md`文件

**引用本地包（模块）**

```bash
src/
  calculator/
    go.mod
    sum.go
  helloworld/
    main.go
```

```go
// /helloworld.go
package main

import "github.com/myuser/calculator"

func main() {
    total := calculator.Sum(3, 5)
    fmt.Println(total)
    fmt.Println("Version: ", calculator.Version)
}
```

通知go使用模块来应用其他包

```bash
go mod init helloworld
```

生成`go.mod`

```go
module helloworld

go 1.17
```

本地包不需要通知go远程位置，可以修改

```go
module helloworld

go 1.14

require github.com/myuser/calculator v0.0.0

replace github.com/myuser/calculator => ../calculator
```

`replace` 关键字指定使用本地目录，而不是模块的远程位置。

