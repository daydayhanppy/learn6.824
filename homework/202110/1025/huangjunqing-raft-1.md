6.1 脑裂（Split Brain）
单节点系统和单点故障
当一个客户端可以与其中一个服务器通信，但是不能与另一个通信时，有可能出现脑裂的问题。
6.2 过半票决（Majority Vote）
在任何时候为了完成任何操作，你必须凑够过半的服务器来批准相应的操作.
如果系统有 2 * F + 1 个服务器，那么系统最多可以接受F个服务器出现故障，仍然可以正常工作。
6.3 Raft 初探
代码结构
应用程序在节点上层，raft在下层。应用程序要把自己的状态传递给raft，并接受反馈信息。
应用程序代码接收RPC或者其他客户端请求；不同节点的Raft库之间相互合作，来维护多副本之间的操作同步。
数据流
客户端发送请求给Key-Value数据库，这个请求不会立即被执行，因为这个请求还没有被拷贝。当且仅当这个请求存在于过半的副本节点中时，Raft才会通知Leader节点，只有在这个时候，Leader才会实际的执行这个请求。对于Put请求来说，就是更新Value，对于Get请求来说，就是读取Value。最终，请求返回给客户端，这就是一个普通请求的处理过程。
6.4 Log 同步时序
用时序图来描述 客户段与服务端、服务段内部机器的交互
https://files.gitbook.com/v0/b/gitbook-28427.appspot.com/o/assets%2F-MAkokVMtbC7djI1pgSw%2F-MBGHvLZY-xqxN_-Tncs%2F-MBGLhoKUS1MMjgE38KQ%2Fimage.png?alt=media&token=9235825d-d6ab-4570-b741-3777083086ea
Q：跟随者的log什么时候commit？
A：一旦Leader发现请求被commit之后，它需要将这个消息通知给其他的副本。所以这里有一个额外的消息。
https://files.gitbook.com/v0/b/gitbook-28427.appspot.com/o/assets%2F-MAkokVMtbC7djI1pgSw%2F-MBGHvLZY-xqxN_-Tncs%2F-MBGR2pnDa99hWttXxYr%2Fimage.png?alt=media&token=60d2d4bf-73ce-4c49-8528-d86fd88693bb
Q：也就是说commit信息是随着普通的AppendEntries消息发出的？那其他副本的状态更新就不是很及时了。
A：是的，作为实现者，这取决于你在什么时候将新的commit号发出。如果客户端请求很稀疏，那么Leader或许要发送一个心跳或者发送一条特殊的AppendEntries消息。如果客户端请求很频繁，那就无所谓了。因为如果每秒有1000个请求，那么下一条AppendEntries很快就会发出，你可以在下一条消息中带上新的commit号，而不用生成一条额外的消息。额外的消息代价还是有点高的，反正你要发送别的消息，可以把新的commit号带在别的消息里
6.5 日志（Raft Log）
1、Log是Leader用来对操作排序的一种手段，确定一个顺序，其他跟随者必须遵守。
2、在一个（非Leader，也就是Follower）副本收到了操作，但是还没有执行操作时。该副本需要将这个操作存放在某处，直到收到了Leader发送的新的commit号才执行。
3、记录操作，可以用于保证重启时数据不丢失。
6.6 应用层接口
start(command) 客户端 -> 服务端 我接到了这个请求，请把它存在Log中，并在committed之后告诉我。
replay(command's index, term) 服务端 -> 客户端 你刚刚在Start函数中传给我的请求已经commit了