# lab1

## 需求文档

## 技术方案

### 流程设计

[XiaoZhuo_Blog/lab1.jpg at main · XiaoZhuoOps/XiaoZhuo_Blog (github.com)](https://github.com/XiaoZhuoOps/XiaoZhuo_Blog/blob/main/docs/image/lab1.jpg)

### 数据结构

Task的有三种：①未分配的任务、②已分配未完成的任务、③已完成的任务

这里用map和channel分别存放①+②和①。

用map可以记录每个task分配给哪个worker，用于后续task完成时的确认；用channel代替链表实现FILI。

### 建模设计

Coordinator

Coordinator需要维护以下变量：

```
type Coordinator struct {
   lock sync.Mutex // 保护共享信息，避免并发冲突

   // Your definitions here.
   stage        string
   mapNum           int
   reduceNum          int
   unFinishedTask     map[string]Task
   unAssignedTask     chan Task
}
```

与Coordinator相关的操作有：

1、worker向coordinator请求时，从中channel弹出一个任务，并将map中该任务的workid设置为该worker的id

2、worker向coordinator反馈任务完成时，coordinator检查map中该task对应的worker是否未该worker，若是则从map删除该任务，否则说明该任务由于过期已经重新分配给了其他worker，忽略即可

3、coordinator会定时遍历map，若某个已经分配的任务超时未完成，则将其加入channel中等待重新分配，并设置其对应的workerId为nil

Worker

Worker不停地向Coordinator发送请求，反馈旧的任务已经完成，申请新任务。