# 3. RPC and Threads

- **为什么用go：**

RPC方便

GC

线程安全

- **多线程的挑战：**

数据共享，竞争问题

线程间的协作

死锁



- **爬虫**

抓取所有的web连接，其可能是个有环图。

 **挑战：**

i/o，在同一时间抓取更多的url

每个url只抓取一次

什么时候结束



基于`ConcurrentMutex`的爬虫

每个页面一个线程，使用`Mutex`, 防止两个页面包含一个url

```go
func ConcurrentMutex(url string, fetcher Fetcher, f *fetchState) {
	f.mu.Lock()
	already := f.fetched[url]
	f.fetched[url] = true
	f.mu.Unlock()

	if already {
		return
	}

	urls, err := fetcher.Fetch(url)
	if err != nil {
		return
	}
	var done sync.WaitGroup
	for _, u := range urls {
		done.Add(1)
		//u2 := u
		//go func() {
		// defer done.Done()
		// ConcurrentMutex(u2, fetcher, f)
		//}()
		go func(u string) {
			defer done.Done()
			ConcurrentMutex(u, fetcher, f)
		}(u)
	}
	done.Wait()
	return
}
```

