# lecture3 gfs

**分布式存储系统：** 性能 $\rightarrow$切片 $\rightarrow$容错$\rightarrow$复制$\rightarrow$一致性$\rightarrow$性能

**Master ：** Active-Standby模式，所以只有一个Master节点在工作。 

**一致性 ：** 如果Primary返回写入成功，那么一切都还好，如果Primary返回写入失败，Primary返回写入失败会导致不同的副本有完全不同的数据。GFS弱一致性。

**问题：**

-  Master节点必须为每个文件，每个Chunk维护表单，随着GFS的应用越来越多，这意味着涉及的文件也越来越多，最终Master会耗尽内存来存储文件表单。
- 单个Master节点要承载数千个客户端的请求，而Master节点的CPU每秒只能处理数百个请求，尤其Master还需要将部分数据写入磁盘，很快，客户端数量超过了单个Master的能力。
- Master节点的故障切换不是自动的。GFS需要人工干预来处理已经永久故障的Master节点，并更换新的服务器，这可能需要几十分钟甚至更长的而时间来处理。对于某些应用程序来说，这个时间太长了。
