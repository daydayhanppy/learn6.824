#snapshot
GFS 通过 snapshot 来立即创建一个文件或者目录树的备份，它可以用于备份文件或者创建 checkpoint（用于恢复），同时 GFS 把写时复制技术（copy-on-write）引入到了快照操作中，原理与 Linux 进程中的写时复制基本相同。

当 master 收到 snapshot 操作请求后：

1. 废除所有的 lease，准备 snapshot（相当于暂停了所有写操作）
2. master 记录所有操作，并且将记录写入磁盘
3. master 将源文件和目录树的 metadata 进行复制，这样之前的记录就和当前的内存中所保存的状态对应起来了，新建的 snapshot 和源文件指向的会是同一个 chunk

#Master 职责
- 执行namespace相关的操作
- 管理chunk replicas
	- 决定chunk replicas的放置
	- 创建chunk replicas
	- 保障chunk被完全复制
	- 负载均衡
	- gc
#管理namespace
为了master在snapshot的时候还能继续工作，引入了namespace锁。
GFS将完整的路径名到元数据的映射表作为它的逻辑namespace。使用前缀压缩，这个表可以有效保存在内存中。namespace tree中的每个节点都有一个关联的读写锁。每个master操作在运行前都会获取一组锁。如果涉及到/d1/d2/../dn/leaf，它将获取目录名称/d1、/d1/d2、...、/d1/d2/.../dn上的读锁，完整路径/d1/d2/../dn/leaf的读锁或者写锁。leaf可以是文件或者目录。创建文件不需要对父级目录加锁，因为没有"目录"的概念不会修改它，而加读锁是防止它被删除、重命名或者snapshot。这种锁机制的好处是允许相同目录下并发的mutations。
#放置replicas
目的：

- 最大化数据可靠性和可用性
- 最大化网络带宽的利用

master在什么情况下会创建replicas

- 创建新的chunk
- 重新备份
- 负载均衡

如何选择将 replicas放置到哪台机器上呢？

- 优先选择磁盘利用率低的 chunkserver
- GFS 会限制每个 chunkserver【最近】创建的次数。换句话说，如果一个 chunkserver 近期创建 replicas 的操作比较频繁，就不会优先选择它（因为创建就意味着以后会进行读取，为了防止突然间大量的读取出现在同一台机器上）
- 保证可用性，尽可能跨机架进行创建操作

当有多个 chunk 需要备份时，GFS 如何决定先备份哪个呢？


- 优先选择可用备份少的
- 优先备份最近没有 delete 文件的
- 优先备份阻塞了 client 操作的
#gc
文件 delete 之后，GFS 并不会立即对空间进行回收，而是等待垃圾回收机制会空间进行释放。

当文件被删除之后，Master 会想其他操作一样，把删除操作记录下来，但是不进行空间的回收，而是将这块空间命名为 hidden（并且包含被删除时的时间戳），Master 会定期进行扫描，把隐藏了一定时间的文件空间进行回收（这个时间是可以进行配置的），在此期间可以对这块空间的文件进行恢复（直接通过重命名回原来的名称就可以）。

除此之外，垃圾回收机制还会扫描孤儿 chunk（所有的文件都没有用到的非空 chunk），然后对这块 chunk 的 metadata 进行清除。具体的做法是，在 master 于 chunkserver 的 heartbeat 信息中会携带关于 chunk 的信息，master 会把 metadata 中不存在的 chunk 发送给 chunkserver，chunkserver 会把它拥有的 chunk 发送给 master。
