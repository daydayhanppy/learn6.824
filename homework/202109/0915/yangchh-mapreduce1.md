[TOC]

# 1. MapReduce

map: 产生中间值 k-v对

reduce：合并这些中间值k-v

**产生的背景**：一些概念简单的计算，输入数据量和计算量过大必须被分布到多台机器上以减少处理时间，如何简单地进行 并行计算、分布数据、处理错误、负载均衡。

## 1.1 编程模型

- **Map**:  接收输入数据产生中间值 **k-v对**     :   $(k1,v1) \rarr list(k2,v2)$
- **Reduce**：合并处理相同key的k-v对，产生数量更少的值集合  :  $(k2,list(v2)) \rarr list(v2)$

## 1.2 示例

- **distriburted grep** :

    - map: 输出匹配某一模式的一行
    - reduce：中间数据复制到输出

- **计算URL的访问频率**

    - map：处理日志得到 **<URL,1>**
    - reduce:  将url相同的累加得到 **<URL, total count>**

- **反转web-link图**

    - map：将source页面得到的所有target url生成 **<target , sorce>**
    - reduce:  将所有 target的source url 连接起来，得到 **<target, list(source)>**

- **Term-Vector per Host**

    term vector : 一个或多个文档中最重要的词组成的 <word ,frequency> 对

    hostname： 从文档url中提取出的

    - map:  产生**<hostname, term vector>**
    - reduce:  对于给定的hostname，reduce将term vector相加丢掉低频的

- **Inverted Index 倒排索引**

    - map：解析文档得到 **<word , document ID>**
    - reduce:  按documen ID排序聚合成**<word, list(document ID)>**

- **Distributed Sort 分布式排序**

    - map：从每个记录提取 key，输出 (key,record)
    - Reduce： 函数不改变任何的值。这个运算依赖分区机制(4.1)和排序属性(4.2)



## 1.3 MR的实现过程

![](https://markdownimg-1255784639.cos.ap-shanghai.myqcloud.com/cpp_network/mr%E6%89%A7%E8%A1%8C%E8%BF%87%E7%A8%8B.png)

MR library将数据分区划分为M片，主节点来分配M个 map tasks 和R个 reduce taks给节点

1. map任务节点从数据中解析出k-v, 执行map function, 生成中间k-v存储在内存缓冲区中
2. 周期性，缓冲区中的中间值k-v被分区函数划分到R个分区中，并存储在磁盘中，将存储位置告知主节点以便分配给reduce任务节点
3. reduce任务节点通过rpc读取中间数据，安装key进行排序、分组， 执行reduce function, 生成R个reduce output files 



## 1.4 Master Data Structures

map任务和reduce任务的状态

- idle
- in-progress
- completed

## 1.5 容错

- 工作节点错误： 主节点周期发送心跳消息。在失败worker上 **正在或已经**允许完的map任务会**重新**执行， 在失败worker上正在运行的reduce任务会重新执行，已经执行的reduce不会再执行，因为已经执行完并输出了。一个map任务被重新执行时，要通知所有在执行reduce任务的worker
- 主节点错误：客户发现后重新执行MR任务

## 1.6 存储位置

根据位置信息，将分配的数据包，安排在尽可能近的位置


