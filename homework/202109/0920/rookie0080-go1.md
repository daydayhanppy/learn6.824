差不多每半年发布一次新版本，2020年2月发布的1.14中加入了强抢占特性，目前最新版本是2021年8月2发布的1.17。

https://learnku.com/go/t/24715

### 快速入门
- Go是由包组成的，main包是应用程序的入口。
- 设置Go的工作区：export GOPATH = ~/workspace，Go将搜索GOPATH目录中的包，或者是从安装Go的目录搜索
- hello world
```Go
package main
import(
    "fmt"   // 格式化IO的包
)
func main() {
    fmt.Println("Hello World!)
}
```
### 变量
- Go是静态类型的语言。
```Go
var a int
var = 1 // 自动定义为了int类型
message := "hello world" // 更简短的语法
var b, c int = 2, 3 // 感觉有点反人类……
```
### 基本数据类型
- int int8 int16 int32 int64
- uint uint8 uint16 uint32 uint64 uintptr
- string
- bool
- 复数类型
### 数组、切片、Maps
```Go
// 数组
var a[5]int
var multiD [2][3]int
// 切片数组的抽象，使用数组作为底层数据结构
var b []int // 创建一个零容量和零长度的切片
numbers := make([]int, 5, 10)   // 定义了初始长度为5，容量为10的切片
numbers = append(numbers, 1, 2, 3, 4) // 增加切片的容量，在末尾增加值
number := make([]int, 15) // 创建一个更大容量的切片并使用copy
copy(number2, numbers) 
// 子切片
number2 := []int{1, 2, 3, 4}
fmt.Println(numbers)
slice1 := number2[2:]
slice2 := number2[:3] // [1 2 3]左闭右开
slice3 := number[1:4] // [2 3 4]
// map
m := make(map[string]int)
m["clearity"] = 2
m["simplicity"] = 3
```
### 类型转化
// 并不是所有类型都可以转为另一类型的
```Go
a := 1.1
b := int(a)
```
### 流程控制
```Go
// if else
if num := 9; num < 0 {
    fmt.Println(num, "is negative")
} else if num < 10 {
    fmt.Println(num, "has 1 digit")
} else {
    fmt.Println(num, "has multiple digits")
}
// switch
i := 2
switch i {
case 1:
    fmt.Println("one")
case 2:
    fmt.Println("two")
default:
    fmt.Println("none")    
}
// 循环
i := 0
sum := 0
for i < 10 {
    sum += 1
    i++
}
fmt.Println(sum)
sum := 0
for i:= 0; i < 10; i++ {
    sum += i;
}
fmt.Println(sum)
指针
var ap *int
a := 12
ap = &a
fmt.Println(*ap)
// 指针作为参数的例子
func increment(i *int) {
    *i++
}
func main() {
    i := 10
    increment(&i)
    fmt.Println(i)
}
```