### 5. The Raft consensus algorithm

通过leader方式，Raft将log的一致性问题分解为三个子问题
- leader选举
- log复制
- 安全性：只要有一台机器在状态机中应用了log中的某一项，那么任何其它机器必须对该项应用相同的指令

#### 5.1 Raft基础

一个典型的Raft集群可能有5台机器，这样可以允许两台机器宕机。每台机器可能有3种状态：leader、follower、candidate。正常情况下只会有1台leader且其余均是follower。

Raft将时间分成许多段，在每一段开始时都会选举leader，选举成功后执行normal operations。如果选举失败则稍后直接开启下一个时间段。

在不同的term之间，会有不同的server监控raft的转移。

不同的raft server通过rpc来通信。最基础的一致性算法只需要RequestVote和AppendEntries两种请求。

#### 5.2 leader选举

Raft通过心跳机制来出发leadr选举。正常情况下，leadr会不断向所有follower发送空的log，声明自己还在。如果某个follower发现一段时间没有收到声明了，就会发起新一轮选举。这个follower会增加自己的当前term，然后转移到candidate状态。如果产生多个candidate，选举有可能会失败。如果某个candidate收到来自其它server的AppendEntries，且该server的current term不小于自己，则会承认新的leader已经产生，自己乖乖转为follower状态。

Raft如何解决选举失败？让每台server的timeout随机设置，尽量避免多台follower同时成为candidate，而是有明显的先后顺序。如果选举真的失败了，，那么在开启下一轮选举之前，所有的server都会重新随机生成一个timeout，谁的超时时刻先到达，谁就先发起投票。这样能尽量避免再次选举失败。

（最开始准备使用一个排序系统，但发现引入的小问题非常多；另一方面，现在的选举方案要容易理解的多！）

#### 5.3 log replication

来自client的每一个请求都对应一个command，而一个command就对应一个log entry。leader收到来自client的请求后，会向所有follower发送log entry。正常情况下，当所有follower都复制了log后，leader就会在状态机上执行command，然后将结果返回给client。如果有follwer失败了或者网速太慢、丢包，leader可能会先响应client，但会坚持向未响应的follower发送log entry。

每一个entry包含一条command，以及对应的term。后者用来检测log的一致性。

leader会检测何时执行command是安全的。执行了command的entry称为已提交，Raft保证已提交的entry是持久的，且最终会被所有可访问的状态机执行。Raft始终会维持下面两条性质，由于满足这两条性质，所以当AppendEntries成功返回时，leader知道follower上的log与自己保持了一致。
- ……
- ……
【细节暂时没看】

有了前面的机制，在normal operation阶段一致性是能得到保证的，但是当leader更换时，一致性仍有可能出错。当新leader发现某个follower上的log与自己不一致时，会强制其以自己的为准并进行覆盖。leader需要找到follower与自己保持一致的最后一个entry是什么。【具体算法没看】

#### 5.4 safety