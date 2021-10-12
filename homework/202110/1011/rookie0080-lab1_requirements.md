#### 目标

实现一个worker进程，调用Map和Reduce函数，处理文件读写；
实现一个coordinator(master)进程，将任务派发给woker，并处理失败的worker节点

#### 配置环境

#### Job

在lab中，多个worker进程运行在一台机器上（和真实环境不同）。worker通过RPC和coordinator通信。

coordinator和worker主例程在main/mrcoordinator.go和main/mrworker.go中，不要修改这两个文件。我们在mr/coordinator.go，mr/worker.go和mr/rpc.go中添加代码

#### 一些规则和提示（重要）