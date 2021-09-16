https://pdos.csail.mit.edu/6.824/papers/mapreduce.pdf

Jeffrey Dean and Sanjay Ghemawat From Google

### 0. 摘要
#### MapReduce是什么？
MapReduce是一个用于处理和产生大数据集的编程模型及其实现。
#### MapReduce带来什么好处？
用户只要按照MapReduce规定的函数风格来编写程序，程序就会自动在一个大规模的集群上并行执行。MapReduce的运行时来管理输入数据的分组、跨机器上的程序的调度、处理机器错误，以及机器之间的通信。简而言之就是为用户封装好了在集群上并行处理大规模数据的能力。

一个典型的MapReduce计算任务可以在上千台机器上处理数TB大小的数据。Google每天在集群上运行着超过上千个的MapReduce任务。

### 1. Introduction
- Section 2 描述了基本的编程模型以及几个例子
- Section 3 描述了MapReduce接口的一种实现
- Section 4 描述了一些对编程模型的改进方式
- Section 5 基于一些任务对我们的实现进行性能度量
- Section 6 探索了MapReduce在Google内部的使用，包括基于MapRduce重写production（什么？）指标计算系统

### 2. 编程模型
MapReduce以一些键值对作为输入，最后输出一些键值对。用户通过Map和Reduce两个函数来表达计算任务。
- Map：由用户编写，它读入一个键值对，生成一些中间键值对
- MapReduce库根据相同的key把所有的中间value聚集在一起，并将给Reduce函数
- Reduce：由用户编写，接收一个key及其value集合，并合并成一个可能更小的value集合，通常是0或1个value
#### 2.1 例子
考虑计算一个大文档中单词出现的次数，用户可能会写出类似下面的伪代码
```
// 处理文档中的一段内容
map(String key, String value):
    // key: document name
  // value: document contents
    for each word w in value:
        EmitIntermediate(w, "1");
        
// 处理一个key和它的value集合
reduce(String key, Iterator values):
    // key: aword
  // values: a list of counts
  int result = 0;
  for each v in values:
    result += ParseInt(v);
  Emit(AsString(result));                 
```
此外，用户需要向一个mapreduce格式的对象填入input和output file，可能还需要调整参数。用户接着就可以启动MapReduce函数，MapReduce用C++实现。（Appendix A中包含了这个example的完整代码）
#### 2.2 类型
通常，map和reduce的协作关系如下：

【图片】

MapReduce实现只用string作为输入输出，转换交给用户去做。

#### 2.3 更多例子
- 分布式检索
  - map接受一个匹配模式和一段文本，如果该文本与模式匹配，就生成一行（一个value）
  - reduce是一个恒等函数，直接将key的value集合原样输出
  - 该情景下k1和k2相同，list(v2)则没有减小
- URL访问频率
  - map从日志中计算web页面的请求次数，生成(URL，1)键值对
  - reduce生成(URL, total count)对
- 反转web链接图
  - map以(source, target)作为输入，输出(target, source)对
  - reduce生成(target, list(source))

…… （暂时了解即可）

### 3. 实现
MapReduce的实现取决于要运用于什么环境，共享内存机器、NUMA多处理机、基于网络的集群等可以有不同的实现方案。文章的实现基于以下环境：
- x86双处理器，Linux，每台机器2-4GB内存
- 商用网络硬件，传输速度100 MB/s 或者1GB/s，但实际要低许多
- 成百上千台机器构成的集群，因而故障很常见
- 每台机器都配有链家的IDE硬盘，使用公司内部的分布式文件系统管理这些硬盘上的数据
- 用户向调度系统提交job，每一个job都包含一些task，job会被调度器映射到某些机器上去执行

#### 3.1 执行概览
【图片】
（具体的流程叙述见Paper）
- 每个Map task都会在本地磁盘上将中间结果分为R个部分，让所有的Reduce worker都可以读取
- 通常用户不需要将最终的output file文件组合在一起，他们经常会直接被另一个mapreduce调用所需要。
  
#### 3.2 Master的数据结构
- Master保存所有map和reduce task的状态，以及所有worker的身份
- 对于每个完成的map task，master会存储他们在R个中间文件之中的位置和大小，这些信息还会被逐渐推送台正在执行reduce的worker
#### 3.3 容错
1）Worker错误
- master会周期性地ping各个woker节点，如果一定时间内没有响应，master会将它们标记为failed。
- 在failed地worker上未执行完地map任务会被置为idle状态， 从而可以被重新调度到其它worker节点上运行。
- failed的 map worker上已经完成的task也会被重新执行，因为它们的执行结果存储在了本地的磁盘上，而机器坏了没办法访问这些数据。
- 另一方面，failed的reduce worker上已经完成的任务不需要重新执行，因为这些结果存储在全局文件系统上。
- 当出现map任务的转移时，所有正在运行的reduce worker都会收到通知，它们之后就知道去哪里读取map worker的结果了

2）master错误
- master可以定期创建检查点（快照），以便出现故障之后可以通过检查点重新启动一个master
- 但在我们的实现中，并没有这么做，因为master挂掉的可能性很小。但如果真挂了，计算也就挂了……（是这样吗？）

3）出现错误时的语义处理

【暂时没有很理解】
#### 3.4 局部性
为了保留网络带宽资源，GFS尽量将数据保留在本地。

【先过一遍】
