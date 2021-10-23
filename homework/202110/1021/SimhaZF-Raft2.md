# Raft

- leader election
- log replication
- safety

# leader election
follower 在election timeout内没有收到leader的心跳（没有选出leader；leader挂了；leader和follower网络故障）则会主动发起选举。
1. 增加自身的current term，切换到candidate
2. 给自己投一票
3. 并行给其他节点发送 RequestVote RPCs
4. 等待其他节点回复：
    1. 受到大多数人的投票，成为leader
    2. 被告知其他人已经当选，转换为follower
    3. 平票，重新发起选举

投票约束：
- 一个任期内，一个节点只能投一票
- 候选人的信息不能比自己少
- 先到先得

为了防止多个follower超时成为candidate导致选票平分的情况，Raft采用随机选举超时时间的方法，选举超时时间在一个固定区间内随机选择。这样就不会有许多个candidate同时瓜分选票的情况。同时节点数目是奇数。

# log replication
复制状态机用来保持最终一致性。leader需要大多数节点回复可用就会commit。
# safety
防止脑裂问题，raft：
- 一个节点一个任期最多只能投一票
- 只有获得大多数投票的节点才会成为leader。

所以某一个任期内只会有一个leader。