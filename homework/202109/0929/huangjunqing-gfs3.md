# GFS
## Design Points
1、组件失效是正常的，而不被视为异常
2、文件更大，以GB计。
3、对于大多数文件来说，新增多于修改
4、与应用程序一起设计的文件系统api对于整个系统而言是更灵活的

## Assumptions
1、这个系统是建立在许多不昂贵的普通计算机上的，失效在所难免。
2、这个系统存储了大量的大文件
3、读取分为两类：大批量流式读取和小规模的随机读取
4、写入也分为两类：顺序写，一旦写入后很少修改；随机写，不需要做特别优化
5、系统必须高效支持多个客户端并发心中同一个文件
6、高、稳定的带宽比低延迟更重要

## Interface
create
delete
open
close
read
write
---
snapshot
record

## Architecture
chunk：存储在 GFS 中的文件分为多个 chunk，chunk 大小为 64M，每个 chunk 在创建时 master 会分配一个不可变、全局唯一的 64 位标识符(chunk handle)；
默认情况下，一个 chunk 有 3 个副本，分别在不同的 chunkserver 上；
master：维护文件系统的 metadata，它知道文件被分割为哪些 chunk、以及这些 chunk 的存储位置；它还负责 chunk 的迁移、重新平衡(rebalancing)和垃圾回收；此外，master 通过心跳与 chunkserver 通信，向其传递指令，并收集状态；
client：首先向 master 询问文件 metadata，然后根据 metadata 中的位置信息去对应的 chunkserver 获取数据；chunkserver：存储 chunk，client 和 chunkserver 不会缓存 chunk 数据，防止数据出现不一致；
https://pic4.zhimg.com/v2-a6c37fffa808aa88800bae22a891ad67_b.jpg

### read
https://pic4.zhimg.com/v2-a6c37fffa808aa88800bae22a891ad67_b.jpg
### write
https://pic2.zhimg.com/v2-6a7dbc6bdd0f4ddd67a3391c8c598bf1_b.jpg

## Consistency
弱一致性
master中的metedata：加锁
chunk file：写入失败client会重试...

## Interact
## Master Operation
## Fault Tolerance

...

FAQ
1、chunk是什么？为什么把文件分成chunk？chunk的大小（64MB）是怎么确定的？
每个文件被GFS分成若干个固定大小的chunk，每个chunk有三个分片（replicate），存储在不同的linux节点的磁盘中。
不知道
2、Master的作用是什么？Master节点只有一个，会出现什么问题？如何解决？
存储GFS的元信息，包括 文件的命名信息（/user/foo/bar）、文件名-chunk-chunk存储位置 映射、控制访问信息
读写都要首先询问master，IO压力大
单点故障问题 主从复制
IO压力大 master只提供元信息，不负责读写；client缓存元信息
3、GFS的读和写的控制流和数据流是怎么样的？

4、GFS如何平衡数据一致性和性能？

5、GFS的分区容错性和高可用性体现在哪里？

6、多个客户端同时追加（append）文件如何实现一致性？







