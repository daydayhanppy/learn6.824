# 6 Raft

> https://mit-public-courses-cn-translatio.gitbook.io/mit6-824/lecture-06-raft1

## 6.1 脑裂（Split-brain）

MapReduce、GFS、VMware FT 都存在一个主机，这种方式可以避免脑裂，但同样是一个单点故障的隐患。

方法：客户端总是要等待两个服务器响应，如果只有一个服务器响应，永远不要执行任何操作

## 6.2 过半票决（Majority Vote）

1. 服务器的数量是奇数，能使过半票决通过

过半的分母：所有服务器，而不是当前开机服务器

**如果系统有 2 \* F + 1 个服务器，那么系统最多可以接受F个服务器出现故障，仍然可以正常工作。**

## 6.3 Raft 初探

上层：应用程序代码，接收RPC或者其他客户端请求。Lab3 中即为 KV 数据库。上层KV数据库向Raft层进行函数调用，以传递状态。

下层：Raft库，帮助应用程序将其状态拷贝到其他副本节点。lab3 中即为 KV table。Raft本身也有状态，需要记录操作日志。

客户端：外部程序代码，使用服务，分布式对其透明。

**客户端步骤**

1. 客户端发送请求（get/put）给 leader 节点
2. leader 节点的上层将请求发送到Raft层
3. Raft层将操作提交到log中，并在节点间交互
4. 过半的节点将操作添加到日志，并通知了 leader 节点
5. leader 节点的 Raft 层发送通知给应用程序
6. 应用程序执行操作

## 6.4 同步时序

没有故障的情况下，处理普通操作的流程：

> AE：AppendEntries，添加日志请求

![ae](../images/ae.png)

在消息被 commit 之后，leader还需要通知其他副本该消息已被提交

在 Raft 中，这条消息被夹带在下一个AppendEntries消息的RPC中

![image-20211026230255423](../images/image-20211026230255423.png)

## 6.5 日志（Raft Log）

1. Log是Leader用来对操作排序的一种手段。复制状态机的副本需要执行相同的操作，且顺序相同。
2. follower 收到但未 commit 的操作会被临时存放，可以被丢弃
3. leader需要存储请求，才能向丢失连接的follower重传丢失的log消息
4. log被用来持久化存储，服务器可以依赖这些操作来恢复状态

QA:

leader的速度大于follower的速度时，follower可能会爆内存，因此需要额外的follower发向leader的消息来调节leader的速度

## 6.6 应用层和Raft层间接口

接口1：转发客户端请求的接口

该接口为函数调用，接收参数为客户端请求，KV层将客户端请求转发给Raft层，并要求Raft层将请求存放在Log中的某处

接口2：Raft层通知KV层，请求已经被commit

## 6.7 Leader选举（Leader Election）

Raft使用任期号来区分leader，在一个任期内有≤1个leader

leader创建：每个节点都有一个选举定时器，某个节点在一个周期内没有收到来自leader的消息，则认为leader失联，它会重新开启一轮选举

重新开始一轮选举，即开启一个新的任期号，该节点会发出请求投票（RequestVote）RPC给其他节点

**Raft协议存在没有考虑到的极端情况**

赢得选举的节点通过发送AppendEntries消息来通知其他节点

## 6.8 选举定时器（Election Timer）

相同的选举定时器时间可能会导致无限分隔选票，无限重试选举





