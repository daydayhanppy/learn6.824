# Falt-Tolerant VM
目的：实现一个自动容错的虚拟机主从备份系统，当虚拟机出问题时，备份虚拟机上线，且外界无法感知异常。


# 容错
容错是为了提高高可用性。VMware FT应对的方法是复制。

复制**可以解决**：Fail-Stop类型的失效，独立的失效，网络丢包，网络分区

复制**不可以解决**：执行出错但是不崩溃，人为因素，级联失效

# 复制状态机
按照固定的顺序对于机器从同一个初始状态运行一系列op那么就能得到确定的最终状态。

# FT的特点
从底层实现复制。复制寄存器和内存，所以只要在FT管理的机器上运行的软件，把me都可以实现容错

# FT的工作原理
通过hypervisor监控所有对VM的操作，os和app跑在vm中，主备vm，共享disk存储，主节点提供服务同时把所有的input通过log channel同步到备节点，Backup上的输出会被丢弃掉；方案属于复制状态机方案，主备节点初始状态一致，包括磁盘和内存，将同样的指令，input作为操作同步，最终的状态保持一致。
# 术语
log entry是primary在log channel上传送给backup的事件

# 当primary挂掉会发生什么？
Primary 故障，Backup 需要执行完所有 Logging Channel 里的操作，然后 Backup 提升为新的 Primary，需要向局域网发送自己的 MAC 地址，这样交换机会将外界的输入发给新的 Primary。Backup 故障，Primary 切换到正常模式，不在发送 log entry。**不管哪种故障，最后，Primary 需要启动新的 Backup。**