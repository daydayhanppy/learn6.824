# MapReduce

## Abstract

通过map将KV集转化为另一个KV集，通过reduce再进行整合。

## 2 Programming Model

输入KV，输出KV。

Map为用户编写的，将输入转化为中间结果KV。MapReduce library将Key都为I的中间结果进行整合，接着传递给Reduce。

Reduce同样由用户编写，输入key集合I，以及键I对应的值。Reduce将I对应的值整合并压缩，只输出一个结果。

- 计算文件中每个单词的出现次数

  map：将文件分割为单词，输出(w, 1)

  reduce：输出单词和对应的集合，输出单词出现的次数

- 计算URL访问频率：map将web的logs输出为(URL, 1)，reduce输出(URL, total count)

- 反转web链接：map将页面中的链接转化为(target, source)，reduce输出(target, list(source))

## 3 Inplementation

MapReduce可以有不同的实现，取决于环境（内存、处理器大小等）。

通过将输入数据分成M splits，可以将map进行分发，到不同的机器上并行执行。通过一个分发公式（如hash(key) mod R），将中间结果key分成R份，来将reduce操作分发。（R的值和分发公式由用户指定）

### 3.2 Master Data Structures

对每一个任务，master存储:

- 状态（空闲、运行中、已完成）
- 执行的机器（非空闲的任务存储）

master存储map任务输出的R份中间结果的位置和大小，并逐渐将其发送给执行reduce任务的节点。

### 3.3 Fault Tolerance

#### worker failure

- master定时ping工作节点已确定其是否fail
- 工作节点完成或失败tasks后，都回到空闲状态，等待调度
- map任务失败需要重新运行，因为存储在内存
- reduce任务失败不用，因为存储在global file system
- map任务失败后reduce worker会被通知新执行它的机器

#### Master Failure

- 新副本从checkpoint启动

### 3.4 Locality

GFS管理文件，尽量保存在本地，以节省网络带宽

