# 分布式系统

## 1、MapReduce笔记

What：

Map/Reduce 是一种编程模式，也是一种在分布式环境下的处理和生成大规模数据的方法。

具体来说，Map/Reduce分为Map（映射）和Reduce（规约）两步。

![image-20210915222019470](C:\Users\XiaoZ\AppData\Roaming\Typora\typora-user-images\image-20210915222019470.png)

我所了解的M/R思想在java后端开发中的实践

- list.stream().map().collect() （单机）
- merge sort 归并排序（单机）
- elastic search inverted index 倒排索引 （分布式）

how：

不关心

conclusion：

首先，限制编程模型可以使并行计算和分布计算变得容易，并使这些计算容错。

其次，网络带宽是一种稀缺资源。因此，我们系统中的许多优化都是针对减少跨网络的数据量，本地优化允许我们从本地磁盘读取数据，将中间数据的单个副本写入本地磁盘可以节省网络带宽。

第三，可以使用冗余执行来减少慢速机器的影响，并处理机器故障和数据丢失。