改一下代理 不然科学上网也没用
> go env -w GOPROXY=https://goproxy.io,direct
---
> import "fmt"

fmt包实现了格式化　I / O　的功能，类似iostream

---

> fmt.Println("Hello world！")

Println是打印函数

---
> a := "zf"

:= 是声明并赋值，并且系统自动推断类型，不需要var关键字

---

> var b, c int = 2, 3

可以这么声明变量

---

go 有切片的数据类型（slices）.
切片存储一系列元素，可以随时扩展。
切片有三个组件，长度，容量，指向底层数组的指针。
长度和容量有什么差别？
长度是初始长度，容量是定义了超过多少的限度才会增加切片长度。预定义有助于内存分配。

>func make([]T, len, cap) []T
>s := make([]int, 5, 10) //make创建切片 

---
>b := []byte{'g', 'o', 'l', 'a', 'n', 'g'}
// b[1:4] == []byte{'o', 'l', 'a'}, sharing the same storage as b  b[1:4]取到的是下标1-3,第一项不变，第二项要减1。

切片是引用型的，所以是共享内存的。

---

>s = append(s, 1, 2, 3) //append可以在末尾增加值
---

>copy(number2, numbers) //将numbers的指拷贝到number2 注：会覆盖
---
>m := make(map[string]int) //map是<key,value>型的数据结构
---
>a := 1.1
b := int(a) //类型转换

---
if-else
>if num := 9; num < 0 {            //花括号需要和if else在一行，分号代表一段代码的结束。这里相当于先把num赋值了9
 fmt.Println(num, "is negative")
} else if num < 10 {
 fmt.Println(num, "has 1 digit")
} else {
 fmt.Println(num, "has multiple digits")
}
---
switch case
>i := 2
switch i {
case 1:
 fmt.Println("one")
case 2:
 fmt.Println("two")
default:
 fmt.Println("none")
}
---
用for实现循环

>i := 0
sum := 0
for i < 10 { //类似while
 sum += 1
  i++
}
fmt.Println(sum)


>sum := 0
for i := 0; i < 10; i++ { 
  sum += i
}
fmt.Println(sum)

>for{
    //无限循环
}