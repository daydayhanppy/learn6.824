# lab2A
完成一个选择leader的功能，同时旧leader宕机后，可以选举新leader接管。
论文中其实已经有详细的数据结构了。raft本身就是一个结构体，分析清楚每一个rpc中需要携带什么信息。
# timer
定时器功能。当一定时间内没收到leader的心跳，自身转换为候选人，发起投票请求。
# heartbeat
心跳。leader向follower发送心跳。