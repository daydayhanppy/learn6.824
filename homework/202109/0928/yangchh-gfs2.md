## 4.7 系统交互

### 4.7.1  Leases and Mutation Order 

<img src="https://markdownimg-1255784639.cos.ap-shanghai.myqcloud.com/cpp_network/mit6.824/mutationOrder.png" style="zoom: 33%;" />

mutation 变动操作  : 改变chunk内容或者chunk的原数据的操作，比如改写或者增加操作。 每个变动都要对所有副本进行改动。使用租约(leases)来维持副本变更中顺序性的一致。 master  给副本中的一个chunk一个lease，这个副本就是primary副本。主chunk对更改操作序列化，其他chunk副本遵循这个序列执行变更操作。

每个lease的生存时间60s，通过master和chunkserver直接的心跳消息来维护。

如果应用的一个写入操作不止一个chunk或者是跨chunk的操作。GFS客户端代码把这个写入操作分解成为多个写入操作。每一个写操作都按照上边描述的控制流进行

### 4.7.2 数据流

## 4.8  Atomic Record Appends

GFS提供一种具有原子性的数据追加操作：记录追加。即Client只需指定要写入数据（而不用指定偏移值），GFS就保证至少有一次原子的写入操作执行成功，并返回偏移值的Client。 记录追加的引入是为了在分布式应用中，减少很多Client并行对同份数据写入的同步机制开销

## 4.9 快照 Snapshot

- Client快照请求的理解：对一个文件或者目录树做一次拷贝。 

- GFS使用copy-on-write技术来实现快照：收到快照请求时，Master并没有立即对指定Chunk拷贝，而只拷贝其元数据并对指定Chunk的引用计数增1。等到Client需要修改指定Chunk时，再在本地复制，并却保新Chunk拥有租约。

# 5. Master Operation

## 5.1 命名空间管理和锁

- 名字空间的组织：全路径和元数据映射关系的查找表，利用前缀压缩，高效存储在内存中
- 命名空间的每个节点都有一个读写锁，通过获取读写锁来实现对文件的正常操作
- 避免死锁方法：锁的获取依据全局一致的顺序，先按名字空间层次排序，同一层次按字典序排序

## 5.2 Chunk副本位置

两个原则：最大数据可靠性和可用性、最大网络带宽利用。

## 5.3 创建、重新复制、重新均衡

master创建chunk副本时考虑的因素：

- 新副本的磁盘利用率低于平均，随着时间推进趋于均匀
- 限制每个chunkserver上最新创建的数量
- 副本跨机架

当chunk的副本数小于一个用户指定的数量后，master尝试重新复制一个chunk副本，可以根据副本数量指定优先级。

master定期重新进行均衡副本，检查当前副本分布情况，逐渐渗透使用一个新的chunkserver，来均衡磁盘空间的使用。

## 5.4 GC

- 机制： 删除的文件被重新命名并添加一个删除时间戳，可以通过改名恢复被删除文件。 在chunkserver和master的心跳中，chunserver会报告自己的chunk集合，并且master回复在master元数据中已经不存在的chunk标记。  所有不被master知道的副本都是垃圾。  滞后删除的缺点：当存储紧张时，滞后删除会阻碍对磁盘均衡的效果。

## 5.5 过期副本删除

chunk副本可能会因为chunkserver失效期间丢失了对chunk的变动而导致过期。对于每一个chunk，master保持一个chunk的版本号码来区分最新的和过期的副本。

master给chunk  lease时，会增加chunk的版本号，并通知最新的副本。master和这些副本在他们的持久化状态中都记录最新的版本号码。

# 6. 容错和诊断

## 6.1 高可用

快速恢复与备份

- 快速恢复：master或chunkserver 关闭时，被设计为数秒内恢复状态并重启
- Chunk的复制：当ChunkServer关闭或Checksum校验出损坏的Chunk副本，Master都会通过复制已有Chunk副本来保障副本个数
- Master的复制：CheckPoint文件、操作日志完成Master的恢复。此外，GFS还有些“影子”Master，在Master宕机时提供GFS的只读访问

## 6.2 数据完整性

每个chunkserver使用checksum来检测存储数据的完整性，一个chunk被分为多个64KB的块，每个块对应一个32bit的checksum。

检测到错误时：chunkserver返回错误给client和master，client从其他副本读取，master复制其他chunk副本给当前副本，复制完后删除出错chunk。

读操作：chunkserver值检测相关数据的checksum

追加：只增量更新最后一个不完整chunk的checksum

写操作：读取和校验被写操作覆盖的第一个和最后一个chunk块，写操作完成后再重新计算和写入checksum

当ChunkServer空闲时，其会周期性扫描不活动的Chunk块，检验数据完整性

