## lab1: MapReduce

> https://pdos.csail.mit.edu/6.824/labs/lab-mr.html
>
> https://pdos.csail.mit.edu/6.824/schedule.html
>
> https://pdos.csail.mit.edu/6.824/labs/guidance.html
>
> https://pdos.csail.mit.edu/6.824/labs/go.html

## intro

worker: 调用 Map 函数和 Reduce 函数，用以读写文件

coordinator（master in paper）: 分发任务、处理失效的 worker

src/main/mrsequential.go：单线程 MapReduce程序

mrapps/wc.go：单词数数

mrapps/indexer.go：text indexer

测试单词计数程序：

```sh
$ cd ~/6.824
$ cd src/main
$ go build -race -buildmode=plugin ../mrapps/wc.go
$ rm mr-out*
$ go run -race mrsequential.go wc.so pg*.txt
$ more mr-out-0
A 509
ABOUT 2
ACT 8
...
```

## job

### 目标

- 1 coordinator + workers in parallel
- worker 运行在同一台机器
- worker 和 coordinator 之间通过 RPC 通信
- worker 向 coordinator 请求任务，从一个或多个文件中读取任务的输入，并执行任务，最后将结果输出到一个或多个文件中
- coordinator 观察 worker 是否在规定时间内(10s)完成任务，若未完成则将同样的任务分配给另一个 worker

**代码**

- 主程序为 `main/mrcoordinator.go` and `main/mrworker.go` （不动）
- MapReduce 逻辑实现在  `mr/coordinator.go`, `mr/worker.go`, and `mr/rpc.go`

**程序运行**

```sh
$ cd src/main
$ go build -race -buildmode=plugin ../mrapps/wc.go
$ rm mr-out*
$ go run -race mrcoordinator.go pg-*.txt
# 在多个窗口中运行下列代码
$ go run -race mrworker.go wc.so
# 结果需要符合
$ cat mr-out-* | sort | more
A 509
ABOUT 2
ACT 8
...
```

**测试程序**

检查输入输出是否正确、 MapReduuce 的并行表现、worker crash 时的表现

```sh
$ cd ~/6.824/src/main
$ bash test-mr.sh
*** Starting wc test.
```



