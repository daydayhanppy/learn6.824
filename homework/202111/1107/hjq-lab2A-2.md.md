# lab2

### 链接

[简介 - MIT6.824 (gitbook.io)](https://mit-public-courses-cn-translatio.gitbook.io/mit6-824/)

[raft-zh_cn/raft-zh_cn.md at master · maemual/raft-zh_cn (github.com)](https://github.com/maemual/raft-zh_cn/blob/master/raft-zh_cn.md) 论文中文版

### lab2A

主要参照

![raft-图2.png](lab2%209a92cb6867124abca9f75e0ff21d2f95/raft-%E5%9B%BE2.png)

day1 

按照论文中fig2定义raft结构体和RPC参数（RequestVoteArgs、RequestVoteReply 、AppendEntriesArgs、AppendEntriesReply）

day2 

实现Make()入口方法和GetState()方法，学了GO的defer关键字