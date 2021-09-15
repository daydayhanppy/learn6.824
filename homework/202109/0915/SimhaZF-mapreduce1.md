# MapReduce

在大规模数据集下简化处理数据的模型
----------
## Abstract
并行编程模型。含有用户自定义的Map以及Reduce函数。
系统运行只需要关心：如何分割输入数据，集群调度，处理机器故障以及通信。
## 1 Introduction
提供了一个简单的接口实现并行化计算
## 2 Programming Model
1. Map：输入一**个** *key/value pair*，输出一**组**中间*key/value pair*。
2. MapReduce将这一组中间*key/value pair*传递给Reduce函数。
3. Reduce：合并所有和中间*key*相同的中间value，形成一个更小的value集合。

实现过程中为了防止value集合过大无法放入内存，使用迭代器把中间value传递给Reduce函数。
### 2.1 Example
> WordCount的简单例子
> ![](https://upload-images.jianshu.io/upload_images/15959547-805d8f8e19375d86.png?imageMogr2/auto-orient/strip|imageView2/2/w/861)
### 2.2 Types
>![](https://upload-images.jianshu.io/upload_images/15959547-1d7b4d3e3a1fe7d2.png?imageMogr2/auto-orient/strip|imageView2/2/w/709)

中间*key/value pair*类型和输出*key/value pair*类型相同
### 2.3 More Examples
- 分布式 Grep(Distributed Grep):map匹配，reduce求和，和Wordcount类似。
- 计算 URL 访问频率(Count of URL Access Frequency):map处理日志中web页面请求输出〈URL, 1〉，reduce选取相同url的value求和。
- 反转 Web-Link 图(Reverse Web-Link Graph): map在source中找到target组合成键值对〈target, source〉，reduce将给定的target的source组成(target,list(source))。
- 每个主机的检索词向量:map将输入的文档输出他们的〈hostname, term vector〉。term vector是 〈word, frequency〉组成的。reduce计算相同word的频率，丢弃低频词汇。输出最终的〈hostname, term vector〉。
- 倒排索引(Inverted Index)：map分析每一个输入文档形成〈word, document ID〉。reduce将给定word的document ID排序，然后输出〈word, list(document ID)〉。形成倒排索引
- 分布式排序(Distributed Sort): 
## 3 Implementation
### 3.1 Execution Overview
MapReduce 执行流程

1. 将输入数据分为m个数据片段
2. 每个程序副本中都有一个master，其余都是worker。有M个map task和R个reduce task。master会分配map task或者reduce task给空闲的worker。
3. map worker读取分配的相关输入数据的片段，解析出*key/value pair* 。传递给用户自定义的map函数。生成中间*key/value pair*缓存在内存中。
4. 中间*key/value pair*会被分区函数分为R个区域，它们的本地储存位置会回传给mater，master会将储存位置传送给reduce worker。
5. reduce worker使用RPC从map worker的主机中获取缓存的数据。将它们按key排序，这样key相同的数据就会排列在一起。如果内存不够，就外部排序。
6. reduce worker会将每一个中间key队友的value集合传给用户自定义的reduce函数。
7. 所有map和reduce task结束后，MapReduce调用返回。
### 3.2 Master Data Structures
master存储每一个map和reduce任务的状态（空闲，工作中或完成）以及非空闲任务机器的标识。还需要存储R个中间文件存储区域的大小和位置。
### 3.3 Fault Tolerance
- **worker故障** 

master会周期性的ping每一个worker。如果在一定时间内worker没有返回信息，master会把这个worker标记为失效。这个worker的map和reduce task都会设置为空闲状态

周期性的将数据写入磁盘，如果失败就从上一个检查点开始。因为只有一个master。目前的做法是直接终止MapReduce。
### 3.4 Locality
输入数据存放在本地磁盘中，这样能节省网络带宽。
### 3.5 Task Granularity
内存中保存O(M*R)个状态。选择合适M使得每个task处理16-64MB的数据。R为机器数量的倍数。
### 3.6 Backup Tasks
调优机制：当 MapReduce 操作接近完成时，master 调用 backup task 处理 in-progress task。谁先处理完就标记为完成。