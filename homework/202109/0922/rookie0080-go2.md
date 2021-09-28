### 函数
```GO
func add(a int, b int) int {
    c := a + b;
    return c
}
func main() {
    fmt.Println(add(2, 1))
}
```
或者把返回值预先定义在函数中
```Go
func add(a int, b int) (c int) {
    c = a + b
    return
}
func main() {
    fmt.Println(add(2, 1))
}
```
单个函数可以返回多个返回值
```Go
func add(a int, b int) (int, string) {
    c := a + b
    return c, "successfully added"
}
func main() {
    sum, message := add(2, 1)
    fmt.Println(message)
    fnt.Println(sum)
}
```
### 方法、结构体、接口
Go不直接支持面向对象编程，但是支持结构体、接口、方法，具有面向对象的风格
结构体
```Go
type person struct {
    name string
    age int
    gender string
}
p := person{name: "Bob", age: 42, gender: "Male"}
person{"Bob", 42, "Male"}
p.name
p.age
p.gender
// 指针也可以这种直接访问结构体属性
pp = &person{name: "Bob", age: 42, gender: "Male"}
pp.name
```
方法
```Go
func (p *person) describe() {
    fmt.Printf("%v is %v years old.", p.name, p.age)
}
func (p *person) setAge(age int) {
    p.age = age
}
func (p person) setName(name string) {
    p.name = name
}
func main() {
    pp := &person{name: "Bob", age: 42, gender: "Male"}
    pp.describe()

    pp.setAge(45)
    pp.setName("Hari") // 不改变pp的Name
}
```
接口：Go的接口是一系列方法的集合
```Go
type animal interface {
    description() string
}
type cat struct {
    Type string
    Sound string
}
type snake struct {
    Type string
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
```
### 包
```shell
# 包的安装
go get github.com/satori/go.uuid
# 创建自定义包
mkdir person
cd person # 然后创建一个Go源文件
go install
```
### 错误处理
```Go
// 从函数返回自定义错误
func increment(n int) (int, error) {
    if n < 0 {
        return nil, errors.New("math: cannot process negative number")
    }
    return (n + 1), nil
}
func main() {
    num := 5
    if inc, err := increment(num); err != nil {
        fmt.Printf("Failed Number: %v, error message: %v", num, err)
    } else {
        fmt.Printf("incremented Number: %v", inc)
    }
}
```
panic和defer

