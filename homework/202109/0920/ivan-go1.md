## Go新手教程

> https://learnku.com/go/t/24715

### hello world

```go
package main

import (
 "fmt"
)

func main(){
  fmt.Println("Hello World!")
}
```

fmt: 内置包，实现格式化IO

```go
export GOPATH=~/workspace
cd ~/workspace
go build main.go && ./main
go run main.go
```

### 变量

变量的定义与赋值

```go
var a int
var a = 1

message := "hello world"

var b, c int = 2, 3
```

### 数据类型

number 类型：int, int8, int16, int32, int64, uint, uint8, uint16, uint32, uint64, uintptr…

复数: complex64 和 complex128

```go
var a bool = true
var b int = 1
var c string = 'hello world'
var d float32 = 1.222
var x complex128 = cmplx.Sqrt(-5 + 12i)
```

**类型转化**

```go
a := 1.1
b := int(a)
fmt.Println(b)
//-> 1
```

### 数组与切片

```go
var a [5]int      // 不能拓展的数组
var mat [2][3]int	// 多维数组
```

切片包含三个组件：容量，长度和指向底层数组的指针

<img src="https://cdn.learnku.com/uploads/images/201902/27/1/GBYGX8ypGS.png!large" style="zoom:60%;" />

```go
// 切片，没有定义容量，可以随时拓展
var b []int				
// 定义了容量和长度的切片，初始长度为 5，容量为 10
numbers := make([]int,5,10)
				
// append 自动增加容量
numbers = append(numbers, 1, 2, 3, 4)

// 创建容量为15的切片number2
number2 := make([]int, 15)
// 将原始切片复制到新切片
copy(number2, numbers)
```

子切片可以用类似python的方式创建

```go
// 初始化长度为 4，以及赋值
number2 := []int{1,2,3,4}
fmt.Println(numbers) // -> [1 2 3 4]
// 创建子切片
slice1 := number2[2:]
fmt.Println(slice1) // -> [3 4]
slice2 := number2[:3]
fmt.Println(slice2) // -> [1 2 3]
slice3 := number2[1:4]
fmt.Println(slice3) // -> [2 3 4]
```

### map

```go
// 创建一个 string --> int 的 map 对象
m := make(map[string]int)
// 添加
m["clearity"] = 2
// 输出结果
fmt.Println(m["clearity"]) // -> 2
```







