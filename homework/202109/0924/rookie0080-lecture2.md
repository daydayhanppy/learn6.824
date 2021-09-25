# Lecture 2. threads and RPC
### Why Go?
- 对于协程（goroutine）和RPC有很好的支持
- 垃圾回收
- 类型安全
- 简单
- 编译型语言
### Why threads（goroutines）?
表达并发
- IO 并发
- 多核并发
- 方便
### threads challenge
1）竞争条件：可以通过避免共享或者使用锁来解决竞争条件

2）协作（同步）：通道、条件变量

3）死锁

一般来说，不共享的情况下可以使用通道来解决；如果存在内存的共享，就需要使用锁+条件变量来解决 

go run -race vote-count-1.go 会检测竞争条件 

接下来讲了几个使用锁、条件变量、通道来解决竞争条件的例子，主要是体会Golang中这些同步工具的用法