这次没有看视频，主要参考 https://mit-public-courses-cn-translatio.gitbook.io/mit6-824/lecture-06-raft1/6.1-split-brain

#### 脑裂

MapReduce、GFS和VMware FT都是多副本系统，但是它们又都使用一个额外的单节点来决定谁是primary/leader，而这些单节点本身存在单点故障问题的。

以VM FT的第三方test-and-set服务为例，如果第三方test-and-set服务是有两台副本的，那么这两台副本本身又会出现脑裂问题，等于为了解决primary和backup的脑裂风险，又引入了新的脑裂风险。单节点则没有这种风险。

如果要避免test-and-set服务的单点故障，则要想办法解决脑裂问题。
1. 构建一种不可能出现故障的网络
2. 人工解决问题，当客户端不能与任何一台服务器通信时，让运维人员去机房检查服务器
很长一段时间人们都使用上述方式来构建多副本系统。虽然贵或者麻烦，但至少是可行的。

#### 过半票决

随着技术的发展，人们发现可以实现自动完成故障切换的系统，而不再需要昂贵的网络或者人工干预。

由于任意两组过半服务器中都至少有一个是重叠的，所以Raft新leader的过半服务器必然至少有一个服务器包含了旧leader的所有操作，即这台服务器知道已经有一个leader在工作了。这是Raft能正确运行（不会出现脑裂）的一个重要因素。

#### log同步时序

客户端会将请求发送给Raft集群中的leader节点对应的应用程序。当Raft的Leader节点确认集群中过半的副本已经有了这个操作的拷贝之后，leader才会真正执行这个请求，然后将结果返回给客户端。当一个操作再leader节点被提交后，所有的副本节点都会执行相同的操作。

具体地，假设集群中有3台服务器，当Raft集群的leader收到client的消息后，它会向其它两台server发送AppendEntries消息，当leader收到某一台server的响应后，就会提交请求。之后，leader需要将操作同步到其它server，Raft不发送专门的commit消息，而是把commit信息夹带在下一次AppendEntries消息中

这样看来，其它server的操作同步其实是不及时的，事实上这个同步时间并不是很重要，因为没人在等待这个步骤。只需要保证Raft集群最终能够避免单点故障就可以了。

#### 关于log

- log是leader用来对操做排序的一种手段。
- log用来存储操作
  - 对于follower来说，log是用来临时存放操作的地方，直到follower知道leader已经提交了操作，它们才会进行同样的提交。这些操作也有可能会被丢弃。
  - 对于leader节点来说，log还可以用来把操作重传给follower，以应对某些follower丢失消息的状况。
  - 对于所有的节点来说，log都可以帮助重启的server恢复状态。

#### 应用层接口

【有时间再细读】

#### Leader选举

> 为什么需要leader？

可以没有leader，事实上， Paxos就没有。引入leader的原因是提高效率，同时也更容易理解系统是如何工作的。

Raft生命周期中可能会有不同的leader，使用任期号（term number）来区分不同的leader。follower只关注leader的term number，而不关注leader的id。

> leader选举的细节，见paper

> 如果一次选举成功了，整个集群的节点是如何知道的？

Raft规定，如果某个候选人赢得了选举，它应当立即向所有server发送一条Appendentries消息，并带上自己的任期号。其它server知道对于任期19有一次选举，或许它们不知道谁赢了，但现在收到了一条任期为19的AppendEntries，就知道选举已经成功了。

#### 选举定时器

任何一条AppendEntries消息都会重置所有Raft节点的选举定时器。只要Leader还在线，就不会有server因为定时器超时而发起新的选举。

分割选票问题，通过为每一台server设置随机的超时时间来避免。但显然，超时时间最小也要大于leader的心跳时间。最大超时时间影响了系统多久能从故障中恢复，如何设置取决于系统需要达到怎样的性能。

#### 可能的异常情况

> 如果旧leader故障了导致系统一致性被破坏，新leader如何恢复一致性？

【重要，下次课继续】



