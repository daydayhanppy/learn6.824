## 数组

```go
package main

import "fmt"

func main() {
    var a [3]int
    a[1] = 10
    fmt.Println(a[0])
    fmt.Println(a[1])
    fmt.Println(a[len(a)-1])
    cities := [5]string{"New York", "Paris", "Berlin", "Madrid"}
    fmt.Println("Cities:", cities)
    cities1 := [...]string{"New York", "Paris", "Berlin", "Madrid"}
    fmt.Println("Cities:", cities1)
    var twoD [3][5]int
    for i:=0; i<3; i++{
        for j:=0; j<5; j++{
            twoD[i][j] = (i+1)(j+1)
        }
        fmt.Println("Row", i, twoD[i])
    }
    fmt.Println("\nAll at once:", twoD)
}
```

**切片**

<img src="https://markdownimg-1255784639.cos.ap-shanghai.myqcloud.com/cpp_network/go/%E6%95%B0%E7%BB%84%E5%88%87%E7%89%87.png" style="zoom: 33%;" />

```go
package main

import "fmt"

func main() {
	months := []string{"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"}
	quarter2 := months[3:6]
	quarter2Extended := quarter2[:1]
	quarter2Extended2 := quarter2[:5]
	quarter3 := quarter2[1:]
	fmt.Println(quarter2, len(quarter2), cap(quarter2))
	fmt.Println(quarter2Extended, len(quarter2Extended), cap(quarter2Extended))
	fmt.Println(quarter2Extended2, len(quarter2Extended2), cap(quarter2Extended2))
	fmt.Println(quarter3, len(quarter3), cap(quarter3))
}
```

```bash
[April May June] 3 9
[April] 1 9
[April May June July August] 5 9
[May June] 2 8
```

```go
// 没有删除，只能重新构建
package main

import "fmt"

func main() {
	letters := []string{"A", "B", "C", "D", "E"}
	remove := 2

	if remove < len(letters) {

		fmt.Println("Before", letters, "Remove ", letters[remove])

		letters = append(letters[:remove], letters[remove+1:]...)

		fmt.Println("After", letters)
	}
}
```

```bash
Before [A B C D E] Remove  C
After [A B D E]
```

**保存复本**

```go
package main

import "fmt"

func main() {
	letters := []string{"A", "B", "C", "D", "E"}
	fmt.Println("Before", letters)

	slice1 := letters[0:2]

	slice2 := make([]string, 3)
	copy(slice2, letters[1:4])

	slice1[1] = "Z"

	fmt.Println("After", letters)
	fmt.Println("Slice2", slice2)
}
```

```bash
Before [A B C D E]
After [A Z C D E]
Slice2 [B C D]
```

## map

```go
//使用项初始化
studentsAge := map[string]int{
        "john": 32,
        "bob":  31,
}
// 初始化空的
studentsAge := map(map[string]int)
// 删除项
delete(studentsAge, "john")
```

**循环**

```go
package main

import (
    "fmt"
)

func main() {
    studentsAge := make(map[string]int)
    studentsAge["john"] = 32
    studentsAge["bob"] = 31
    for name, age := range studentsAge {
        fmt.Printf("%s\t%d\n", name, age)
    }
}
```

## 结构

```go
package main

import "fmt"

type Employee struct {
    ID        int
    FirstName string
    LastName  string
    Address   string
}

func main() {
    employee := Employee{LastName: "Doe", FirstName: "John"}
    fmt.Println(employee)
    employeeCopy := &employee
    employeeCopy.FirstName = "David"
    fmt.Println(employee)
}
```

```bash
{0 John Doe }
{0 David Doe }
```

```go
package main

import "fmt"

type Person struct {
    ID        int
    FirstName string
    LastName  string
    Address   string
}

type Employee struct {
    Person
    ManagerID int
}

type Contractor struct {
    Person
    CompanyID int
}

func main() {
    employee := Employee{
        Person: Person{
            FirstName: "John",
        },
    }
    employee.LastName = "Doe"
    fmt.Println(employee.FirstName)
}
```

**json encoding**

```go
package main

import (
    "encoding/json"
    "fmt"
)

type Person struct {
    ID        int
    FirstName string `json:"name"`
    LastName  string
    Address   string `json:"address,omitempty"`
}

type Employee struct {
    Person
    ManagerID int
}

type Contractor struct {
    Person
    CompanyID int
}

func main() {
    employees := []Employee{
        Employee{
            Person: Person{
                LastName: "Doe", FirstName: "John",
            },
        },
        Employee{
            Person: Person{
                LastName: "Campbell", FirstName: "David",
            },
        },
    }

    data, _ := json.Marshal(employees) //return the json encoding of employees
    fmt.Printf("%s\n", data)

    var decoded []Employee
    json.Unmarshal(data, &decoded)//parses the JSON-encoded data and stores the result in the value pointed to by v
    fmt.Printf("%v", decoded)
}
```

```bash
[{"ID":0,"name":"John","LastName":"Doe","ManagerID":0},{"ID":0,"name":"David","LastName":"Campbell","ManagerID":0}]
[{{0 John Doe } 0} {{0 David Campbell } 0}]
```

## 方法和接口

```go
func (variable type) MethodName(parameters ...) {
    // method functionality
}
```

结构`type`获得方法`MethodName`, 可以调用`type.MethodName()`

```go
package main

import "fmt"

type triangle struct {
	size int
}

type square struct {
	size int
}

type coloredTriangle struct {
	triangle
	color string
}

func (t triangle) perimeter() int {
	return t.size * 3
}

func (t *triangle) perimeter_1() {
	t.size *= 3
}

func (s square) perimeter() int {
	return s.size * 4
}

// 重载
func (t coloredTriangle) perimeter() int {
	return t.size * 3 * 2
}

func main() {
	t := triangle{3}
	s := square{4}
	fmt.Println("Perimeter (triangle):", t.perimeter())
	fmt.Println("Perimeter (square):", s.perimeter())
	t.perimeter_1()
	fmt.Println("Perimeter (size):", t.size)

	ct := coloredTriangle{triangle{3}, "blue"}
	fmt.Println("Size:", ct.size)
	fmt.Println("Perimeter (perimeter)", ct.perimeter())
	fmt.Println("Perimeter (perimeter)", ct.triangle.perimeter()) // 重载后调用基类方法
}
```

```bash
Perimeter (triangle): 9
Perimeter (square): 16
Perimeter (size): 9
Size: 3
Perimeter (perimeter) 18
Perimeter (perimeter) 9
```

**使用技巧为其他类型（如基本类型）创建方法**

```go
package main

import (
    "fmt"
    "strings"
)

type upperstring string
// 为基本类型string创建了方法
func (s upperstring) Upper() string {
    return strings.ToUpper(string(s))
}

func main() {
    s := upperstring("Learning Go!")
    fmt.Println(s)
    fmt.Println(s.Upper())
}
```

## 接口

```go
type Shape interface {
    Perimeter() float64
    Area() float64
}
```



## 并发

 Go 的方法：“不是通过共享内存通信，而是**通过通信共享内存**。”

### Goroutine

goroutine 是轻量线程中的并发活动，而不是在操作系统中进行的传统活动。

原程序

```go
package main

import (
	"fmt"
	"net/http"
	"time"
)

func main() {
	start := time.Now()

	apis := []string{
		"https://management.azure.com",
		"https://dev.azure.com",
		"https://api.github.com",
		"https://outlook.office.com/",
		"https://api.somewhereintheinternet.com/",
		"https://graph.microsoft.com",
	}

	for _, api := range apis {
		_, err := http.Get(api)
		if err != nil {
			fmt.Printf("ERROR: %s is down!\n", api)
			continue
		}

		fmt.Printf("SUCCESS: %s is up and running!\n", api)
	}

	elapsed := time.Since(start)
	fmt.Printf("Done! It took %v seconds!\n", elapsed.Seconds())
}
```

**改为并发**

```go
package main

import (
	"fmt"
	"net/http"
	"time"
)

func checkAPI(api string) {
	_, err := http.Get(api)
	if err != nil {
		fmt.Printf("ERROR: %s is down!\n", api)
		return
	}

	fmt.Printf("SUCCESS: %s is up and running!\n", api)
}

func main() {
	start := time.Now()

	apis := []string{
		"https://management.azure.com",
		"https://dev.azure.com",
		"https://api.github.com",
		"https://outlook.office.com/",
		"https://api.somewhereintheinternet.com/",
		"https://graph.microsoft.com",
	}

	for _, api := range apis {
		go checkAPI(api)
	}

	time.Sleep(3 * time.Second)

	elapsed := time.Since(start)
	fmt.Printf("Done! It took %v seconds!\n", elapsed.Seconds())
}
```

### channel 用作通信

`channel`只能发送`channel`支持类型的用于`goroutine`间通信的双向通道。

```go
// 声明
ch := make(chan int)

ch <- x //x发送到通道
x = <-ch //x接收通道ch收到的数据
<-ch // 通道接受数据，但数据被遗弃

// 关闭通道
close(ch)
```

无缓冲`channel`

```go
package main

import (
	"fmt"
	"net/http"
	"time"
)

func checkAPI(api string, ch chan string) {
	_, err := http.Get(api)
	if err != nil {
		ch <- fmt.Sprintf("ERROR: %s is down!\n", api)
		return
	}

	ch <- fmt.Sprintf("SUCCESS: %s is up and running!\n", api)
}

func main() {
	start := time.Now()

	apis := []string{
		"https://management.azure.com",
		"https://dev.azure.com",
		"https://api.github.com",
		"https://outlook.office.com/",
		"https://api.somewhereintheinternet.com/",
		"https://graph.microsoft.com",
	}

	ch := make(chan string)
	for _, api := range apis {
		go checkAPI(api, ch)
	}

	// 无缓冲channel会阻塞发送操作，直到有人准备好接收数据
	for i := 0; i < len(apis); i++ {
		fmt.Print(<-ch)
	}

	elapsed := time.Since(start)
	fmt.Printf("Done! It took %v seconds!\n", elapsed.Seconds())
}
```

```bash
ERROR: https://api.somewhereintheinternet.com/ is down!
SUCCESS: https://dev.azure.com is up and running!
SUCCESS: https://management.azure.com is up and running!
SUCCESS: https://api.github.com is up and running!
SUCCESS: https://graph.microsoft.com is up and running!
SUCCESS: https://outlook.office.com/ is up and running!
Done! It took 0.952523177 seconds!
```

**有缓冲的channel**

有缓冲 channel 在不阻塞程序的情况下发送和接收数据，因为有缓冲 channel 的行为类似于队列。每次向 channel 发送数据时，都会将元素添加到队列中。 然后，接收操作将从队列中删除该元素。 当 channel 已满时，任何发送操作都将等待，直到有空间保存数据。 相反，如果 channel 是空的且存在读取操作，程序则会被阻塞。

**无缓冲的buffer** 保证每次发送数据时，程序被阻塞，直到有人从`channel`中读取数据

**有缓冲的buffer** 将发送和接受操作解耦，不会阻塞程序



**Channel方向**

```go
// 定义channel方向
chan<- int // channel to only send data
<-chan int // channel to only receive data
```

```go
package main

import "fmt"

func send(ch chan<- string, message string) {
	fmt.Printf("Sending: %#v\n", message)
	ch <- message
}

func read(ch <-chan string) {
	fmt.Printf("Receiving: %#v\n", <-ch)
}

func main() {
	ch := make(chan string, 1)
	send(ch, "Hello World!")
	read(ch)
}
```



### 多路复用

```go
package main

import (
	"fmt"
	"time"
)

func process(ch chan string) {
	time.Sleep(3 * time.Second)
	ch <- "Done processing!"
}

func replicate(ch chan string) {
	time.Sleep(1 * time.Second)
	ch <- "Done replicating!"
}

func main() {
	ch1 := make(chan string)
	ch2 := make(chan string)
	go process(ch1)
	go replicate(ch2)

	for i := 0; i < 2; i++ {
		select {
		case process := <-ch1:
			fmt.Println(process)
		case replicate := <-ch2:
			fmt.Println(replicate)
		}
	}
}
```

