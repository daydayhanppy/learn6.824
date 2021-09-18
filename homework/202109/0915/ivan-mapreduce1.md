# MapReduce

## Abstract

通过map函数将一个KV集转化为另一个KV集；通过reduce函数，合并所有key相同的value值。

通过MapReduce编写的程序能自动在许多机器上运行。

系统自动维护程序的执行、错误处理、机器间通讯等工作。程序员不用懂分布式。

## 1 Introduction

- 许多分布式的计算有如下要求：并行计算、分发数据、错误处理等

- MapReduce启发自Lisp语言

- 本文的主要贡献：为分布式创造了一个简单的编程模型

内容简介

- sec2描述基本的编程模型并给出范例。
- sec3将MapReduce用于集群计算。
- sec4为对模型的优化、实用技巧。
- sec5是MapReduce应用中的表现。
- sec6为MapReduce在谷歌索引系统中的使用经验
- sec7相关工作。

## 2 Programming Model

- 原理：输入KV集合，输出KV集合。

- Map为用户编写的，将输入转化为中间结果KV。MapReduce 库将 Key 都为 I 的中间结果进行整合，接着传递给 Reduce。
- Reduce 同样由用户编写，输入 key 集合 I ，以及键I对应的值的集合。Reduce 将 I 对应的值合并，一般每次 Reduce 操作都只产生 0 或 1 个 value 值。

### 2.1 Example

计算文件中每个单词的出现次数

- map：将文件分割为单词，输出(w, 1)

- reduce：输出单词和对应的集合，输出单词出现的次数

<img src="../../../../learn6.824-local/images/image-20210912212805114.png" alt="image-20210912212805114" style="zoom:50%;" />

```
map(k1, v1) -> list(k2, v2)
reduce(k2, list(v2)) -> list(v2)
```

### 2.3 More Examples

计算URL访问频率：map将web的logs输出为(URL, 1)，reduce输出(URL, total count)

反转web链接：map将页面中的链接转化为(target, source)，reduce输出(target, list(source))

## 3 Inplementation

MapReduce可以有不同的实现，取决于环境（内存、处理器大小等）。

本节描述的MapReduce实现适用于由网络连接的、普通PC机组成的大型集群。

1. x86处理器Linux系统，2-4G内存
2. 商用网络，100MBPS or 1GBPS
3. 几百或几千台机器，因此机器故障很常见
4. 低级的存储设施，分布在每台机器上。需要分布式存储系统进行顶层设计，来提供可靠存储。
5. 用户将工作（job）提交到调度系统中，工作（job）由许多任务（task）组成，由调度程序将其分发到各台机器上。

### 3.1 Execution Overview

通过将输入数据分成M splits，可以将map进行分发，到不同的机器上并行执行。通过分发函数（如hash(key) mod R），将中间结果 key 的值分成 R 份，来将 reduce 操作分发。（R的值和分发公式由用户指定）

用户调用MapReduce后的步骤：

1. MapReduce 库将输入数据拆分成 M 份，每份 16-64MB
2. master 分发任务，共有 M 个 map 任务和 R 个 reduce 任务， master 将一个 Map 任务或 Reduce 任务分配给一个空闲的 worker。
3. 被分配了 map 任务的 worker 程序读取输入数据，解析出 KV 对，并传递给用户自定义的 Map 函数。map 函数生成中间值 KV 对，并保存在内存中。
4. 中间值 KV 对由分区函数分为 R 个区域，并定期写入本地磁盘。它们在磁盘中的位置会发送给 master，由 master 负责将这些位置发送给 reduce worker。
5. master 告知 reduce worker 中间值 KV 对的位置后，reduce worker 就从 map worker 主机磁盘中读取。读取完后，reduce worker 使用 key 对数据进行排序，将相同 key 的数据聚合在一起。若数据量太大无法放入内存，则在外部进行排序。
6. 对于每一个唯一的中间值 key，reduce worker 将该 key 和其相关的 value 传递给用户自定义的 reduce 函数。reduce 函数的结果追加输出到所属分区的输出文件。
7. 所有的 map 和 reduce task 执行完后，master 向用户返回结果。

执行结果为 R 个输出文件，通常用户不用自行合并这些 R 个结果，而是将其作为另一个MapReduce的输入，或使用分布式文件处理程序。

![image-20210912213844828](../../../../learn6.824-local/images/image-20210912213844828.png)

### 3.2 Master 节点 data structure

对每一个 map 任务和 reduce 任务，master存储其状态（空闲、运行 中、已完成），非空闲的任务存储执行它的机器。

master 像一个数据管道，将 中间值 KV 对的位置从 map 传到 reduce。因此，对每个已完成的 map 任务，master 存储 map 任务产生的 R 个中间值 KV 对的大小和位置，并将这些信息逐渐推送给 reduce 任务。

### 3.3 Fault Tolerance

#### worker failure

- master 周期性地 ping worker，一段时间没有返回信息则标记为fail。
- fail 的 worker 的task（已完成的 map 任务、正在运行的 map 和 reduce 任务）回到空闲状态，等待重新调度
  - 已完成的 reduce 输出存储在全局文件系统中
  - 已完成的 map 输出在本地存储中，worker fail 后本地存储无法访问
- task 从 worker A 调度到 worker B 后，会通知所有执行 reduce 任务的 worker，此后需要从 worker B 获取中间数据。

#### Master Failure

**解决1**：master 周期性地将 3.2 节的数据结构写入磁盘，master 失败后从检查点启动另一个 master 进程。

**实际解决**：master 失败后中止 MapReduce 运算，由用户重启。

#### 失效处理机制

上述机制的前提：map 和 reduce 函数是输入确定性函数，即相同的输入产生相同的输出。

### 3.4 存储位置

- 前提：网络带宽为匮乏的资源
- 输入文件保存在机器的本地，按 64MB 的 Block 进行分隔，每一份 Block 保存在多台机器（一般为 3 份拷贝）。
- master 尽可能在输入数据的机器上执行 map 任务

结果：大部分的输入数据都能从本地机器读取

### 3.5 任务粒度

前述将 map 拆分成 M 份，reduce 拆分成 R 份。

理想情况下，M、R >> worker数量

- master 节点由于调度需要，需要保存 O(M*R) 个状态
- R 由用户指定
- M 值选择后让任务处理的数据在 16-64M，能让数据本地存储优化策略最有效、
- 通常 M=200000, R=5000, worker=2000

### 3.6 备用任务

落伍者：一台机器花了 长的时间完成最后几个 Map 或 Reduce 任务

解决：

- 当一个 MapReduce 操作块完成后，master调用备用任务进程执行执行中的或未执行的任务。
- 无论是原先的还是备用的 worker 执行成功，即可将该 task 标记为已完成。
