## Target
You'll implement a worker process that calls application Map and Reduce functions and handles reading and writing files, 
and a coordinator process that hands out tasks to workers and copes with failed workers.

## Start 
go、git...

## Job
一个coordinator，一个或多个worker，之间通过RPC通信
Coordinator：should notice if a worker hasn't completed its task in a reasonable amount of time (for this lab, use ten seconds), and give the same task to a different worker.
Worker：will ask the coordinator for a task, read the task's input from one or more files, execute the task, and write the task's output to one or more files
