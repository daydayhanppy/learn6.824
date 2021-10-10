# lecture4 容错

> https://mit-public-courses-cn-translatio.gitbook.io/mit6-824/lecture-04-vmware-ft

## 4.1 复制

fail-stop故障：停止运行

复制不能处理软件中的bug和硬件设计中的缺陷

## 4.2 状态转移和复制状态机

复制状态机：将来自客户端的操作或者其他外部事件，从Primary传输到Backup

## 4.3 VMware FT 工作原理

VMware FT需要两个物理服务器

两个物理服务器上的VM会为每个虚拟机分配一段内存，这两段内存的镜像需要完全一致，或者说我们的目标就是让Primary和Backup的内存镜像完全一致

通过网络连接了这两个物理服务器

## 4.4 非确定性事件

- 客户端输入：随时会到达
- 随机数等
- 多CPU的并发

## 4.5 输出控制

输出：对客户端请求的响应

故障：控制输出（Output Rule）：直到Backup虚机确认收到了相应的Log条目，Primary虚机不允许生成任何输出

## 4.6 重复输出

晕了