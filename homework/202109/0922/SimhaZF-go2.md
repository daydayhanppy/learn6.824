# 指针
>var ap *int


#函数
>func add(a int, b int) int {    　　　//最后一个int是代表返回值类型
  c := a + b
  return c
}
func main() {
  fmt.Println(add(2, 1))
}
//=> 3

>func add(a int, b int) (c int) {   //可以预先定义返回值
  c = a + b
  return
}
func main() {
  fmt.Println(add(2, 1))
}
//=> 3

> func add(a int, b int) (int, string) {   　　//可以多个返回值，用空格隔开
  c := a + b
  return c, "successfully added"
}
func main() {
  sum, message := add(2, 1)
  fmt.Println(message)
  fmt.Println(sum)
}
#结构体
结构体定义
>type person struct {
  name string
  age int
  gender string
}

实例化p
>//方式1：指定属性和值
p := person{name: "Bob", age: 42, gender: "Male"}
//方式2：指定值
p:=person{"Bob", 42, "Male"}

go语言中，(.)运算符可以访问数据，结构体指针也使用的是(.)而不是(->)
>pp = &person{name: "Bob", age: 42, gender: "Male"}
pp.name
//=> Bob

#方法
方法是struct的一种属性,可以直接使用(.)调用
>type person struct {
  name   string
  age    int
  gender string
}

>// 方法定义
func (p *person) describe() {
  fmt.Printf("%v is %v years old.", p.name, p.age)
}
func (p *person) setAge(age int) {
  p.age = age
}

>func (p person) setName(name string) {
  p.name = name
}

>func main() {
  pp := &person{name: "Bob", age: 42, gender: "Male"}
  pp.describe()  　　／／直接使用(.)就可以调用方法
  // => Bob is 42 years old
  pp.setAge(45)
  fmt.Println(pp.age)
  //=> 45
  pp.setName("Hari")  　　//这里的setName无法修改p的值因为是值传递
  fmt.Println(pp.name)
  //=> Bob
}

#接口
接口是一系列方法的集合，接口有助于将类型的属性组合在一起。有利于实现多态。
>type animal interface {
  description() string
}
package main

```
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
snake和dog实现了animal接口

