# 条件变量 Cond
条件锁
新建：
> cond := sync.NewCond(&sync.Mutex{})

使用：
> go func() {
            cond.L.Lock()
            defer cond.L.Unlock()
            cond.Wait()
            // 临界区.....
}()

唤醒：
- cond.Signal()：唤醒当前等待队列里第一个
- cond.Broadcast()：顺序唤醒当前等待队列里所有阻塞函数，唤醒期间阻塞的函数无法加入阻塞队列

大致用法
1. 首先声明一个mutex，这里sync.Mutex/sync.RWMutex可根据实际情况选用
2. 调用sync.NewCond(l Locker) *Cond 使用1中的mutex作为入参 注意 这里传入的是指针 为了避免c.L.Lock()、c.L.Unlock()调用频繁复制锁 导致死锁
3. 根据业务条件 满足则调用cond.Wait()挂起goroutine
4.  cond.Broadcast()唤起所有挂起的gorotune 另一个方法cond.Signal()唤醒一个最先挂起的goroutine 






# channel
go channel是通过通信来实现 共享内存，以及线程同步的，而不是通过共享内存来实现线程通信的.
# go语言代码编写的一些规范
RPC的调用不要太过频繁，有些通信是没有必要的，另外数据结构的声明可以放在一起。
