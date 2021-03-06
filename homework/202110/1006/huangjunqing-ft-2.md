## Falt-Tolerant VM
### 摘要：基于通过在另一个服务器上的备份虚拟机复制执行主虚拟机的方法，实现了一个支持容错的虚拟机的企业级商用系统
### 引言：
主从备份(Primary/Backup)
    主服务上的执行可以在备份服务上复制运行，如果主服务挂了，备份服务能够接管服务而且没有任何中断或者状态的丢失。
    具体实现：1、把服务看作是状态机，保证初始状态和以相同顺序接受相同请求 2、额外协议保证主服务和备份服务同步
VM为什么相比于物理机更适合做P/B
    “因为虚拟机监视器对于虚拟机执行有完全的控制权，包括输入数据的传递，所以虚拟机监视器能够捕获所有主虚拟机上涉及的非确定性操作的有效信息，然后在备份虚拟机上正确的重放这些操作。”
    “不需要硬件修改来驾驭新的处理器以提升硬件性能”
    “主服务和备份服务的物理分区，比如主服务可以分布在区域内不同的物理机上”
### 架构设计
https://raw.githubusercontent.com/RiverFerry/picBed/master/Snipaste_2021-02-17_23-19-06_water.jpg

```
—— —— ——> Primary VM   —— —— ——>   Backup VM
              \                       /
               \                     /
                \                   /
                 \                 /
                  \               /
                   \             /
                   Virtual Storage 
```
为什么使用共享存储？

### 确定性重放
即保证主机和备机通过日志通道发送信息来保持同步
  "确定性重放允许虚拟的输入和所有与虚拟机执行相关联的可能的不确定性能够通过写到日志文件的日志项的流记录下来。通过读取日志文件的日志项，可以在稍后准确的回访虚拟机的执行"
  "对于不确定性操作，充足的信息必须被日记记录下来，来让重放的时候操作可以按照相同的状态改变和输出被重置。对于不确定性的事件比如时钟中断或者IO完成中断，还必须记录事件发生的确切指令。在重放期间，必须在指令流的同一时间点传递事件"

### 容错协议
为什么需要容错？
    日志不是记录在虚拟磁盘上，而是通过网络发给BackUp VM
为什么需要输出规则？如何规定？
    保证备机在接管时和主机的输出状态保持一致
    主机直到备机接收被确认了和产生输出相关联的日志项的时候，才发送输出给外部世界。
    操作系统以异步IO的方式完成与虚拟磁盘和backup VM的通信
    
https://raw.githubusercontent.com/RiverFerry/picBed/master/Snipaste_2021-02-17_23-19-23_water.jpg
该图展示了主机和备机上事件的时间线。主机线到备机线的箭头表示日志项的传输，备机线到主机线的箭头表示确认。异步事件的信息，输入，和输出操作都必须被发送给备机，以日志项的方式，然后由备机确认。如图中说明的那样，对于外部世界的输出会被延迟到主机已经接收到来自备机的确认信息，在备机收到和输出操作相关联的日志项的时候会进行确认。如果输出规则得以遵守，备机将能够以和主机最后输出一致性的状态进行接管。
### 检测和响应故障
如何检测故障
1、服务器之间的udp心跳包
2、主机发送给备机的日志
3、备机发给主机的确认
一旦以上上述流量暂停时间超过了指定时间，即判定为故障
如何应对
主机故障，备机上线
备机故障，主机不再发送日志
如何解决脑裂问题
共享虚拟存储 + 锁

### go live points
一个被标记为go-live point的日志项可以用来表示对于重放一个指令或者特别的设备操作必要的一系列日志项中的最后一个日志项

## FT 实现
### 启动和重新启动 FT VM
VMware VMotion可以在最小化中断的代价下将运行的虚拟机从一台服务器迁移到另一台服务器-虚拟机的暂停时间通常小于1秒
当故障发生而主机需要一个新的备机重建冗余的时候，主机会通知集聚服务它需要一个新的备机。集聚服务基于资源申请，使用和其他约束来选择运行备机的最佳服务器。然后集聚服务自动调用容错Vmotion来创建新的备机。

### 日志缓存
为什么使用buffer(缓冲)
1、顾名思义，减少冲击。因为不同机器的数据处理速度不匹配。
2、解耦
3、减少数据传输次数。因为可以把缓冲区写满后一次性发送出去。
会带来哪些问题
缓冲区大小有限，带宽有限，不同机器数据处理速度差距
1、日志通道的带宽太小以至于无法承载正在生成的日志项的容量
2、备机执行过慢以至于消费日志项太慢
如何解决
1、处理速度 PV 取决于机器的CPU、内存等，可以通过调整CPU份额来调整处理速度
2、处理速度 PV 可以通过主机和备机之间的日志和确认来传输
3、主备机之间通过 PV 的 日志 + 确认 + feedBack loop 来控制延迟，避免缓冲区满
### 其他操作
一些控制操作通过日志实现
    当主机显式关机的时候，备机也应该关机，而不是尝试上线。
    主机上任何的资源管理改变(比如增加了cpu份额)也应该应用到备机
## 磁盘IO问题


