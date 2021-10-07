#### 2.3 检测和响应失败

VMware FT使用UDP心跳的方式来检测是否发生server的崩溃。VMware FT还会监视主备server之间的logging流量和应答。

但这些错误检测方式会对split-brain问题会过于敏感。因此，必须确保同一时刻主备服务器中只有一台是提供服务的。通过对共享虚拟磁盘数据的原子操作来实现。

### 3. 实践中的FT实现

Section 2是设计原理，接下来是实现。

#### 3.1 启动和重启FT虚拟机

VMware VMotion使得可以以最小的干扰从一台服务器切换到另一台服务器。中断时间小于1s。我们使用修改后的VMotion版本，直接clone出一台一样的VM而不是迁移状态。

还有一个问题是为clone出来的VM选择一台集群服务器来运行。VMware vSphere实现了这样的集群服务，在failure发生后的几分钟内就可以重新建立起冗余VM。

#### 3.2 管理Loggin Channel

有很多种方式来实现对loggin channel的流量管理。在我们的实现中，hypervisor为主备VM维护了一个大的buffer。信息从一台VM的buffer经过channel到达另一台VM的buffer。在这个过程有很多的细节问题需要处理。

#### 3.3 FT VM上的操作

很多主备VM之间的操作同步需要通过logging channel来进行。大多数操作只先在主VM上进行初始化，然后传输control entry到备VM上。为要在主备VM上分别执行的操作是VMotion。

#### 3.4 磁盘IO问题

一、需要检测IO竞争，并强制把竞争的磁盘操作化为主备一直的序列化操作。

二、应用/OS和磁盘在读同一块memory的时候也会发生不一致性。可以使用页保护机制。

三、如果主VM在执行磁盘IO操作失败了，这时候备VM接管了怎么办？

#### 3.5 网络IO问题

VMware vSphere提供的异步更新会带来一致性问题。我们禁止了这样的异步更新，这是最大的更改和优化。

第二个优化是减少了传输包的延迟。






