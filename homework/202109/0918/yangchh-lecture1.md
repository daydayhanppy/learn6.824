# lecture 1 introduction

## 1.15 可拓展性 Scalability

希望可以通过增加机器的方式来实现扩展，但是现实中这很难实现，需要一些架构设计来将这个可扩展性无限推进下去。

## 1.16  可用性 Availability

为了实现可恢复，有很多工具。其中最重要的有两个：

- 非易失存储（non-volatile storage，类似于硬盘）
- 复制（replication）

## 1.17 一致性 Consistency

- 强一致性
- 最终一致性

## 1.18 MapReduce

MR很大的瓶颈在于数据的通信。
