# Raft
# 日志恢复
- AppendEntries RPC中包含的prevLogIndex字段和prevLogTerm字段是用来和follower确定之前的term和logindex是否正确，不正确就返回false，然后nextIndex会减少，相当于往前寻找匹配的日志记录。
- 找到匹配项后，会先删除follower内的日志项，然后将AppendEntries内的内容代替本地log。这样就保证最终一致性。
# 选举约束
1. 候选人最后一条Log条目的任期号大于本地最后一条Log条目的任期号；
2. 或者，候选人最后一条Log条目的任期号等于本地最后一条Log条目的任期号，且候选人的Log记录长度大于等于本地Log记录的长度
> Raft更喜欢拥有更高任期号记录的候选人，或者说更喜欢拥有任期号更高的旧Leader记录的候选人。限制2说明，如果候选人都拥有任期号最高的旧Leader记录，那么Raft更喜欢拥有更多记录的候选人。
# 快速恢复
可以以term为单位回退。

# 持久化
Log、currentTerm、votedFor需要持久化存储
# 日志快照
理论上上层key-value表单会比log小很多。（因为很多条log执行完才是key-value表单），那么可以设定当log超过多少时，保存key-value表单作为快照，同时将之前的log删除，这样可以压缩log。