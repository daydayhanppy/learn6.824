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
