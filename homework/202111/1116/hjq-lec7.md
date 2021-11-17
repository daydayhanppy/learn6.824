# lec7

## 日志恢复

Leader只会在commit之后回复给客户端

## **选举约束**

投票的条件

------

候选人最后一条Log条目的任期号**大于**本地最后一条Log条目的任期号；

或者，候选人最后一条Log条目的任期号**等于**本地最后一条Log条目的任期号，且候选人的Log记录长度**大于等于**本地Log记录的长度

## **快速恢复**

让Follower返回足够的信息给Leader，这样Leader可以以任期（Term）为单位来回退，而不用每次只回退一条Log条目。所以现在，在恢复Follower的Log时，如果Leader和Follower的Log不匹配，Leader只需要对每个不同的任期发送一条AppendEntries，而不用对每个不同的Log条目发送一条AppendEntries。

## **持久化**

需要持久化的数据：Log、currentTerm、votedFor

## 日志快照

把应用程序的状态作为一种快照存下来

## 线性一致