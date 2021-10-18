# worker的任务
从coordinator获取任务，执行，然后给coordinator反馈。
# Worker
Coordinator.GetTask获取任务
# HandleMap
通过哈希散列将map的输出分区。
# HandleReduce
读入中间文件，先排序key然后计算结果并输出