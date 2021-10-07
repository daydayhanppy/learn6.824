# Falt-Tolerant VM
目的：实现一个自动容错的虚拟机主从备份系统，当虚拟机出问题时，备份虚拟机上线，且外界无法感知异常。

# 架构设计
通过hypervisor监控所有对VM的操作，os和app跑在vm中，主备vm，共享disk存储，主节点提供服务同时把所有的input通过log channel同步到备节点，Backup上的输出会被丢弃掉；方案属于复制状态机方案，主备节点初始状态一致，包括磁盘和内存，将同样的指令，input作为操作同步，最终的状态保持一致。

# 如何检测故障
检测方法：VMware FT 在主机之间发送 UDP 心跳包来检测是否故障，同时监视 Logging channel 是否出现异常。

脑裂问题：因为采用UDP心跳包的方式监测故障，如果断网，Primary 和 Backup 都会认为对方出现了故障。两台主机都想要上线，这时采用 TEST-AND-SET 原子操作，操作共享硬盘上的一个值，谁 SET 了谁就上线。（自旋锁）

故障处理：Primary 故障，Backup 需要执行完所有 Logging Channel 里的操作，然后 Backup 提升为新的 Primary，需要向局域网发送自己的 MAC 地址，这样交换机会将外界的输入发给新的 Primary。Backup 故障，Primary 切换到正常模式，不在发送 log entry。**不管哪种故障，最后，Primary 需要启动新的 Backup。**
# 如何保证一致性
当客户端得到的输出是一致的时候，是不会感知到主备切换的。那么怎么保证向外部的输出一致呢？

这里就确定了一个输出规则：primary遇到输出指令不马上输出，而是存入log，直到backup确认收到这条log时候才真的输出给客户端。

这样或许会发生backup接手后重复输出的情况，但是tcp可以检测重传然后丢弃所以无所谓。
