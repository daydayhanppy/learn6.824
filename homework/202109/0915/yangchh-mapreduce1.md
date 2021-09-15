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