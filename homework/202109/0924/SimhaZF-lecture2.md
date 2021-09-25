#为什么要使用GO语言
例如c++这样的语言需要自行管理内存，在编程实现时会遇到许多困难。而Go语言自带许多特性，例如go routinue,locking,synchronization,RFC包。Go的垃圾回收机制也有助于内存管理。

#线程
go routines就是线程
#并发
使用线程，可以让其中一部分等待，一部分执行。所有线程不都是一直运行而是会休眠，所以总体带来的开销并不会增加太多。
Q：进程与线程的联系
#锁
线程共享内存，会发生bug。Go提供了锁机制。
方便线程之间交流协调，Go 提供了下面的工具

- channels：收发信息 (使用 Channel 而不是共享变量的形式，channel 是线程安全的)
- sync.Cond：条件锁，更好地知道是要条件性等待，还是继续执行线程
- wait group：lauch 一组线程并等待完成

Q：死锁
Go针对race问题，提供了优秀的工具，race 检测工具```go run -race```
，检测不同 routines 先读后写又无锁的情况。

