### 1. Introduction
#### 什么是分布式系统
……
#### 为什么需要分布式系统？
1）最基本的：连接物理上分离的机器，实现数据共享

2）通过并行提高容量

3）提高容错性 

4）通过隔离提高安全性【待理解】
#### 分布式系统的历史发展
……
#### 这门课的挑战
1）许多的并行处理情景

2）处理局部错误

3）如何提高性能
#### 为何学习这门课？
有趣、实用、热门
#### 课程结构
- lectures：big ideas
- paperes： case study
- labs：mapreduce、replication using raft、replicated kv service、shared kv service（lab4可以用另一个团队合作的项目替代）
#### 重点：基础设施
存储、计算、通信（稍微少一点）
#### Main topics
- 容错性：可用性（冗余）、恢复能力（日志、事务、持久化存储）
- 一致性：
- 性能：吞吐量、时延
- 当然，还有如何实现
### 2. MapReduce
背景、目标

map和reduce之间的shuffle操作是非常花时间的！

文件会在map worker和reduce worker之间传输

mapReducer的语义和函数式编程很相似

同一个map任务可能被完整地执行2次，这会产生相同地在中间数据，但不会影响最后的结果
同样的，reduce也可能被执行两次【待理解】

coordinator不会faile，理论上可以做容错处理，但是一般不管，坏了就坏了

slow workers怎么办？ 

【总结：paper上关于架构、实现部分要再好好读一读】