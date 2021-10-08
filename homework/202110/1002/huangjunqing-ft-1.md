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
### 检测和响应故障
    
