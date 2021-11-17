# Lecture 07. Raft 2

### 7.1 日志恢复

一个例子：https://mit-public-courses-cn-translatio.gitbook.io/mit6-824/lecture-07-raft2/7.1

### 7.2 选举约束

为了保证系统的正确性，并非任意节点都可以成为Leader。

一个例子说明：https://mit-public-courses-cn-translatio.gitbook.io/mit6-824/lecture-07-raft2/7.2-xuan-ju-yue-shu-election-restriction

在处理别的节点发来的RequestVote RPC时，需要做一些检查才能投出赞成票。节点只能向满足下面条件之一的候选人投出赞成票：
- 候选人最后一条Log条目的任期号大于本地最后一条Log条目的任期号；或者，
- 候选人最后一条Log条目的任期号等于本地最后一条Log条目的任期号，且候选人的Log记录长度大于等于本地Log记录的长度

### 7.3 快速恢复

### 7.4 持久化

有且仅有三个数据是需要持久化存储的。它们分别是Log、currentTerm、votedFor。

### 7.5 日志快照

【Log压缩和快照（Log compaction and snapshots）在Lab3b中出现的较多】

对于一个长期运行的系统，例如运行了几周，几个月甚至几年，如果我们按照Raft论文图2的规则，那么Log会持续增长。最后可能会有数百万条Log，从而需要大量的内存来存储。快照就是为了解决这个问题的。

### 7.6 线性一致

【更偏概念性】