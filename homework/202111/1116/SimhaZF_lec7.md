# 日志恢复
这里有一个潜在的规则：raft为了保持最终的一致性，当遇到不同的log条目时，怎么保证安全的删除这些log entry。这里安全的原因主要是这条错误的log就没有被commit。所以删除后也不会影响到客户端的请求。
# 选举约束
1. 候选人最后一条Log条目的任期号大于本地最后一条Log条目的任期号
2. 候选人最后一条Log条目的任期号等于本地最后一条Log条目的任期号，且候选人的Log记录长度大于等于本地Log记录的长度

> Raft更喜欢拥有更高任期号记录的候选人，或者说更喜欢拥有任期号更高的旧Leader记录的候选人。限制2说明，如果候选人都拥有任期号最高的旧Leader记录，那么Raft更喜欢拥有更多记录的候选人。

# 快速恢复
解决任期号快速匹配的问题。当遇到一条错误log，需要找到第一条不相同的log光靠一次一次发送rpc是很浪费资源的事。所以提出了增加XTerm，XIndex，XLen的要求。
# 持久化
哪些数据需要持久化？Log、currentTerm、votedFor。
# 日志快照
本质上，数据库就是对于多个操作的简化合并，所以只要储存这一个状态下的数据库。就等于对之前的所有操作进行了一个快照。
# 线性一致
定义什么是强一致性