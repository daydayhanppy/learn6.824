### Introduction 

接下来的一系列实验将会实现一个键/值存储系统，lab2的Raft是第一个实验，后续将会在Raft之上构建键值存储服务。

有用的资料：
- a guide for students（写于几年前，注意有的地方如今已经不一样了）
- the advice about locking and structure for concurrency
  
### Getting started

### The code

### Part 2A: leader election

实现leader选举和心跳机制
- 选举
- 在没有错误发生的情况下，保持leader的权威性
- 如果old leadr宕机了，让新的leader可以顺利接管

