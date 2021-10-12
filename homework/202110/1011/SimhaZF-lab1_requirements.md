# lab1:MapReduce
任务：实现一个简单mapreduce,它由coordinator和worker组成。
- 只有一个coordinator和数个worker。
- 单机运行
- worker使用RPC与coordinator通讯
- 每个Worker进程将向Master进程请求一个任务，从一个或多个文件读取任务的输入，执行任务，并将任务的输出写入一个或多个文件。
- 如果一个Worker没有在合理的时间内完成任务(本实验规定10秒)，Master应该将该任务交给另一个Worker。
- 每次都要确保word-count插件是新构建的
> go build -buildmode=plugin ../mrapps/wc.go 
- 当worker和master都完成，在mr-out-xxx查看输出。输出文件的排序并集应与顺序输出匹配.