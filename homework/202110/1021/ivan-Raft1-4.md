# Raft

> https://pdos.csail.mit.edu/6.824/papers/raft-extended.pdf
>
> 中文版: https://github.com/maemual/raft-zh_cn/blob/master/raft-zh_cn.md
>
> 可视化界面：https://raft.github.io/raftscope/index.html

## 解读

> https://mp.weixin.qq.com/s/EkC0mLPeICyAFlSPxXFLxA

Raft算法：管理重复日志的一致性算法。

一致性：多个服务器状态达成一致。如即使两台服务器发生故障，五台服务器的集群也可以继续运行。

### 基础知识

5个服务器是Raft集群的典型形式，允许系统容忍两个故障。

每个服务器在三种状态之间转化：领导者（Leader），追随者（Follower）或候选人（Candidate）

![](../../../../../blog/docs/images/bb.jpeg)

### 选举Leader

心跳机制。

服务器启动时为Follower状态。Leader定时向所有Follower定时发送心跳包，以保持其权限。如果在一段时间内没有发送，则重新选举。

### 日志复制

1. 一旦Leader当选，它就开始为客户请求提供服务。
2. 每个客户端请求：包含需要由复制状态机执行的命令。
3. Leader将命令作为新条目附加到其日志，然后并行地向每个服务器发出AppendEntries RPC以复制条目。
4. 当条目被安全地复制时，Leader将条目应用于其状态机，并将该执行的结果返回给客户端。
5. 如果Follower崩溃或运行缓慢，或者网络数据包丢失，Leader将无限期地重试AppendEntries RPC（即使它已经响应客户端），直到所有Follower最终存储所有日志条目。

### 总结

- 强一致性：节点数据虽然不是实时一致，但Raft算法保证了Leader节点数据最全；所有请求都由Leader处理。
- 高可靠性：Raft算法保证了Committed的日志不会被修改，状态机只会应用Committed的日志。日志在大多数节点上冗余存储：少于一半的磁盘故障数据不会丢失。
- 高可用性：节点故障不会影响系统的可用性。但Leader故障时存在重复数据问题，需要业务去重或幂等性保证。
- 高性能：与必须将数据写到所有节点才能返回客户端成功的算法相比，Raft算法只需要大多数节点成功即可，少量节点处理缓慢不会延缓整体系统运行。

## 1 介绍

算法分解：Raft 主要被分成了领导人选举，日志复制和安全三个模块

减少状态机的状态：和 Paxos 相比，Raft 减少了非确定性

Raft 的独特性：

- 强领导者：日志条目只从领导者发给其他服务器
- 领导选举
- 成员关系调整

## 2 复制状态机

- 复制状态机：产生相同状态的副本，在部分部分服务器宕机时能继续运行。
- 常用于解决容错问题。
- 复制状态机一般基于复制日志实现，每个服务器获得相同的日志，就会有相同的状态。

## 3 Paxos算法的问题

- 难以理解(todo: read about Paxos)
- 没有具体实现

## 4 为了可理解性的设计

- 问题分解：将 Raft 分成领导人选举，日志复制，安全性和成员变更
- 减少状态的数量：使用随机化简化 Raft 中的领导人选举。

