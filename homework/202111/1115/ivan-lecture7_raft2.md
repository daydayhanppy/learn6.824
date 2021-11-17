# Lecture 07 Raft2

> https://mit-public-courses-cn-translatio.gitbook.io/mit6-824/lecture-07-raft2

## 7.1 日志恢复（Log Backup）

| logID | 10   | 11   | 12   | 13   |
| ----- | ---- | ---- | ---- | ---- |
| S1    | 3    |      |      |      |
| S2    | 3    | 3    | 4    |      |
| S3    | 3    | 3    | 5    | 6    |

表格内的为节点保存的 log 对应的任期号

如图中S3当选，并添加log[13]，指定任期号为6，尝试发送AE RPC给S1和S2的流程：

**S2**

1. S3发送AE(prevLogIndex=12, prevLogTerm=5)给S2
2. S2接收到消息，但log[12]对应的prevLogTerm不对应，拒绝该请求
3. S3发送AE(prevLogIndex=11, prevLogTerm=3)给S2，该AE RPC包含log[11]及之后的所有log信息
4. S2接收消息，并更新log[11]之后的所有日志条目，与S3对齐

**S1**

1. S3发送AE(prevLogIndex=12, prevLogTerm=5)给S1
2. S1接收到消息，但prevLogTerm不对应(log[12]为空)，拒绝该请求
3. S3发送AE(prevLogIndex=11, prevLogTerm=3)给S1，被拒绝
4. S3发送AE(prevLogIndex=10, prevLogTerm=3)给S1，被接收

**S2覆写掉之前的log原因**

由于S3当选，则S3的log日志被大多数认同，S2与S3有冲突，则S2被覆写的log必然无法被大多数认同，也就无法提交。反之，如果被覆写的log提交过，则S3无法当选。

## 7.2 选举约束（Election Restriction）

其他的设计中：选择拥有最长记录的节点作为Leader

**Raft中**

1. 候选人最后一条Log条目的任期号**大于**本地最后一条Log条目的任期号；
2. 或者，候选人最后一条Log条目的任期号**等于**本地最后一条Log条目的任期号，且候选人的Log记录长度**大于等于**本地Log记录的长度

可能出现的情况如下表。

其中S1在某个节点的任期5结束后赢得选举，并在发出第一个AE之前，存放到自己的log之后故障。之后故障重启，再次赢得选举，同样的故障。

这种情况下，S2和S3知晓任期6和任期7的存在（由于RV RPC中包含了任期号），因此当S2或S3开启一个新的任期时，任期号为8。

| logID | 10   | 11   | 12   |
| ----- | ---- | ---- | ---- |
| S1    | 5    | 6    | 7    |
| S2    | 5    | 8    |      |
| S3    | 5    | 8    |      |

在上表的情况中，S1在第二次重启后无法赢得选举，且它的记录会被覆写

## 7.3 快速恢复（Fast Backup）

> 论文中表述的加强

原本为每次回退一条：Follower在离线重启后，Leader需要找到Follower中最后一条相匹配的Log

加速策略：以任期为单位进行匹配，Leader针对每个任期发送一条AE RPC

为了实现加速策略，Follower在回复Leader的AE RPC时，需要携带3个额外的信息来实现。

XTerm：这个是Follower中与Leader冲突的Log对应的任期号。在之前（7.1）有介绍Leader会在prevLogTerm中带上本地Log记录中，前一条Log的任期号。如果Follower在对应位置的任期号不匹配，它会拒绝Leader的AppendEntries消息，并将自己的任期号放在XTerm中。如果Follower在对应位置没有Log，那么这里会返回 -1。

XIndex：这个是Follower中，对应任期号为XTerm的第一条Log条目的槽位号。

XLen：如果Follower在对应位置没有Log，那么XTerm会返回-1，XLen表示空白的Log槽位数。



















