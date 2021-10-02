#### 存储系统

应用一般是无状态的，大部分状态信息存储在后台，所以需要专门的存储系统。

#### Why hard？

  - 数据太多，需要分布在多台服务器上
  - 机器一多，错误就很常见，需要容错
  - 容错需要冗余，副本需要保持一致性。
  - 强一致性和高性能是矛盾的。

#### 一致性

理想状态：所有的机器表现得像一个单一的系统。 

#### 案例：GFS

具备了分布式存储系统应该考虑的特性。而且是一个成功的系统，作为mapReduce的文件系统。

GFS存在一些不一致性！

#### GFS特性

- Big：大数据集
- Fast：自动分片
- Gloal：所有的应用看见的是同一个文件系统
- Fault tolerant：也是自动的

#### 设计

见paper架构图

#### master

- 映射：文件名 => chunk句柄的数组
- chunk句柄：版本 + chunkservers列表（主、从）
- log、检查点，形成稳定的存储

问题：哪些数据需要持久化存储，哪些只需要存在内存中？
- chunk句柄数组、log、checkpoint需要持久化
- chunkserver列表、主从节点信息、lease只需要存储在内存中，在master启动时像所有chunkserver询问即可
- 另外，master需要持久化chunk句柄的版本（否则的化，比如有些chunkserver如果fail了就不能得到最新的版本了）【待理解】

#### Read a file

1. client给出文件名 + 偏移到master
2. master返回chunk handle + chunk server列表 + version
3. client缓存下这些信息
4. 从最近的chunkserver读出数据
5. chunkserver检查版本号，如果版本号在正确就发送数据给client

#### write a file：append

以下是paper中的一个例子：
1. client询问master哪一个chunkserver持有chunk的当前lease，以及其它副本位置。如果没有任何chunkserver持有lease，master会选择一个并赋予它lease。
2. master回复持有lease的主节点的身份，以及其它从节点的位置。client缓存下这些数据。只有当在主节点不可访问或者主节点声明自己不再持有lease之后，client才需要再次询问master。
3. client将数据推到所有副本，节点的推送可以以任意顺序进行。此时，每一个chunkserver都只将数据存储在LRU缓存上。（这是实现数据流和控制流的解耦）
4. 当所有的副本都收到数据之后，client告诉primary可以开始写入更改了。
5. primary接着又通知其它所有从节点写入更改。
6. 从节点回复主节点写入完毕
7. 主节点回复client所有节点写入完毕，回复的信息中可能会报错，由client去处理错误信息。

#### 一致性

举了一个例子，说明版本号可以保持一致性。 






 

