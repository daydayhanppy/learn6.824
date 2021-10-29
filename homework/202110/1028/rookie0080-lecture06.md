# MapReduce Q&A

### lab1 solution walkthroough

1. Implement RPC structs
2. Write coordinator handlers for RPCs
3. Create worker loop to send out GetTask RPCs and handle replies
4. Write worker helper functions to handle temporary/intermediate files
5. Implement worker map
6. Implement worker reduce
7. Create coordinator loop to handle requests and assign tasks

区别:
- 我没有用条件变量，而是用了channel来进行任务同步，原理是一样的，channel更高级
- 未收到有效任务我就把worker退出了，想想不是很合理，coordinator之后可能会重新分配task啊！【后面看看有没有坑】

### some alternative solution designs

没有任务谁来等待？——coordinator或者worker之一负责等待（channel可以起到等待的作用？）

### Design mistakes and bugs

- Pusing too much worker to the coordinator
  - Coordinator sorts results
  - Coordinator reads file contents
- Sending redundants RPCs

#### General tips

#### Q&A