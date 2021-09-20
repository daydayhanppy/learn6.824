## Go新手教程 part2

> https://learnku.com/go/t/24715

### 流程控制

#### if else

```go
if num := 9; num < 0 {
 
} else if num < 10 {
 
} else {
 
}
```

#### switch case

```go
i := 2
switch i {
case 1:
 
case 2:
 
default:
 
}
```

#### for循环

类似while的实现

```go
i := 0
sum := 0
for i < 10 {
 sum += 1
  i++
}
```

真正的for

```go
sum := 0
for i := 0; i < 10; i++ {
  sum += i
}
```

### 指针

和C/C++的使用类似

```go
// 指向int的指针ap
var ap *int
// 获取变量的地址
a := 12
ap = &a
// *访问指针指向的值
fmt.Println(*ap)
// => 12
```

#### 例子

```go
func increment(i *int) {
  *i++
}
func main() {
  i := 10
  increment(&i)
  fmt.Println(i)
}
//=> 11
```

### 函数

```go
func add(a int, b int) int {
  c := a + b
  return c
}
func main() {
  fmt.Println(add(2, 1))
}
//=> 3
```

预先定义返回值

```go
func add(a int, b int) (c int) {
  c = a + b
  return
}
```

多个返回值

```go
func add(a int, b int) (int, string) {
  c := a + b
  return c, "success"
}
func main() {
  sum, message := add(2, 1)
}
```

### 面向对象

#### 结构体

结构体定义

```go
type person struct {
  name string
  age int
  gender string
}
```

对象创建

```go
//方式1：指定属性和值
p := person{name: "Bob", age: 42, gender: "Male"}
//方式2：指定值
person{"Bob", 42, "Male"}
```

对象访问

```go
p.name
//=> Bob
pp = &person{name: "Bob", age: 42, gender: "Male"}
pp.name
//=> Bob
```

#### 方法

特殊类型的带有返回值的函数

```go
func (p *person) setAge(age int) {
  p.age = age
}
func (p person) setName(name string) {
  p.name = name
}
```

调用setAge会改变对象内的age，调用setName不会

#### 接口

```go
type animal interface {
  description() string
}
```

**例子**

在cat实现animal接口时，并没有显式的表明，而是在创建对象时，以父类对象和子类实现的形式来体现

```go
package main

import (
  "fmt"
)

type animal interface {
  description() string
}

type cat struct {
  Type  string
  Sound string
}

type snake struct {
  Type      string
  Poisonous bool
}

func (s snake) description() string {
  return fmt.Sprintf("Poisonous: %v", s.Poisonous)
}

func (c cat) description() string {
  return fmt.Sprintf("Sound: %v", c.Sound)
}

func main() {
  var a animal
  a = snake{Poisonous: true}
  fmt.Println(a.description())
  a = cat{Sound: "Meow!!!"}
  fmt.Println(a.description())
}

//=> Poisonous: true
//=> Sound: Meow!!!
```













