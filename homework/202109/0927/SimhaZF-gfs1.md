#什么是GFS？
Google File System，一个适用于大规模分布式数据处理相关应用的，可扩展的分布式文件系统。

#设计概览
- 系统构建在普通廉价机器上，容易发生故障
- 系统存储大容量文件
- 系统支持的读操作：大量顺序读取以及小规模随机读取
- 系统的写操作主要是顺序的追加写，而不是覆盖写
- 系统对于大量客户端并发写文件具有优化，而且是原子操作
- 系统看中稳定的带宽，而不需要低延时

#GFS架构
Master、chunkserver、client。GFS master任意时刻只有一个，而chunkserver和GFS client可能有多个。

1. GFS 存储的文件都被分割成固定大小的 Chunk（64MB），每个chunk有全局唯一的文件句柄 ： 一个64位的chunk ID，每一份chunk会被复制到多个chunkserver（默认值是3)
2. GFS master是系统的元数据服务器，维护的元数据包括：命令空间（GFS按层级目录管理文件）、文件到chunk的映射，chunk的位置。其中，前两者是会持久化的，而chunk的位置信息来自于Chunkserver的汇报。
3. GFS master还负责分布式系统的集中调度：chunk lease管理，垃圾回收，chunk迁移等重要的系统控制。master与chunkserver保持常规的心跳，以确定chunkserver的状态。

#GFS的读取流程
客户端向 Master 节点询问它应该联系的 Chunk 服务器（就近原则）。客户端将这些元数据信息缓存一段时间，后续的操作将直接和 Chunk 服务器进行数据读写操作。
1. 应用程序调用GFS client提供的接口，表明要读取的文件名、偏移量。

2. GFS Client将偏移按照规则翻译成chunk索引，发送给master

3. master将chunk id与chunk的副本位置告诉GFS client

4. GFS client向最近的持有副本的Chunkserver发出读请求，请求中包含chunk handle与字节范围

5. ChunkServer读取相应的文件，然后将文件内容发给GFS client。

#元数据
所有的元数据都保存在 Master 服务器的内存中，元数据有三种类型：
- 文件和 Chunk 的命名空间
- 文件和Chunk 的对应关系
- 每个 Chunk 副本的存放地点
前两个类型的数据不经保存在master的本地硬盘中，也以log的形式在远端机器上保存副本。
master并不是持久化保存Chunk位置信息的，而是启动的时候轮询每一个chunkserver询问它的chunk信息。这样方便Master 服务器和 Chunk 服务器数据同步的问题。

#操作日志
master在灾难恢复的时候，通过重演操作日志把文件系统恢复到最近状态，但是大量日志操作很久，当日志超过一个范围时，引入checkpoint。
这样master只需要恢复最新的checkpoint和后续的日志文件。旧的checkpoint和日志文件可以删除，但是为了应对严重的故障，会多保存一些历史文件。
