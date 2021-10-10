# Lecture 4

#### Failures

- 此处只讨论和解决Fail-stop failures（包括地震等原因导致的停机）
- 不关心 logic bugs、配置错误、恶意错误，假设不会发生

#### Challenges

- Has primary failed？Not network (avoid split-brain problem)
- keep the primary and backup in sync(aplly changes in order, non determinism)
- Fail over (means the backup takes over)

#### Two approaches

1. State transfer
2. Replicate state machine: send operations, not state changes or modifications
  
#### level of operations to replicate

- application-level operations (file append)
- machine level / processor level (use virtual machines!)

#### VM FT: exploit virtualization

- transparent replication
- appears to Client that Server is a single machine
- Vmware product

#### Overview

VM FT就是修改之后的hypervisor，每台机器上都安装相同的虚拟机，使状态的保持变得更容易。

VM FT到 VM FT之间在逻辑上有一层logging channel，用来传输operations（instructions）；backup只执行ooperations，不在网络上传输执行结果 

网络上还有storage server，被primary和backup共享。primary和backup在修改数据前会先访问storage上的一个flag，采用test and set的方式，如果发现已经被设置了，自己就不会再执行写操作。这样可以防止出现split-brain问题，即同时出现两个在工作的primary。【问题：flag什么时候被reset？】

> 50min处


  