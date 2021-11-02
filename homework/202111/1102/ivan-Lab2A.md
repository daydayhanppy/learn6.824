# Lab2A

> https://pdos.csail.mit.edu/6.824/labs/lab-raft.html
>
> https://github.com/maemual/raft-zh_cn/blob/master/raft-zh_cn.md
>
> https://raft.github.io/

Lab2A：实现Raft复制状态机协议

Lab2B：在Raft基础上实现KV服务

## intro

- 实现容错：在多个复制机中存储状态(state)的完整复制
- 挑战：系统的运行错误可能导致不同的复制机有不同的数据拷贝

Raft实例通过RPC通信

目标

- 支持无限的带有编号（index number）的log entries命令
- entries最终会被commit，commit时需要发送给上层

## Fig2 in article

### State



### AppendEntries RPC



### RequestVote RPC



### Rules for Servers



## Student’s Guide

> https://thesquareplanet.com/blog/students-guide-to-raft/

Go的优势：适合并发、分布式（goroutines）

lab2A：构建一致性的日志

lab2B：在2A基础上构建KV数据库

lab2C：在集群上考虑容错













