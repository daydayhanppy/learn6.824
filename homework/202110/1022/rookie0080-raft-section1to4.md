# In Search of an Understandable Consensus Algorithm

### 1. Introduction

一致性算法过去以Paxos为代表，但是Paxos的可理解性比较差，学习和理解很困难。于是，斯坦福大学的老师设计了一种新的一致性算法，号称比包括Paxos在内的其它一致性算法更容易理解，也更容易实现。

### 2. Replicated state machines

一致性算法一般产生于对replicated state machines的的谈论。replicated state machine 可以解决分布式系统中的许多容错相关的问题。

replicated state machines通常基于replicated log来实现。（要保持相同状态的）每台server都有一份log，其中包含了一系列的指令，server上的状态机会依次执行这些指令。由于每一台server上的log是一致的，所以每台server上的状态机会得到同样的结果，因而这些server会拥有相同的状态。一致性算法的职责就是维持这些server上log的一致性。

如paper中图1所示，某一台server上的一致性模块收到来自client的的指令后，将指令加入自己的log中，并联络其它server上的一致性模块，最终所有server上的log都包含了相同的指令顺序。

真实系统中的一致性算法通常具有下面的性质：
- 【……】
- 【……】
- 【……】
- 【……】

### 3. What's wrong with Paxos?

1. 难以理解
2. 难以实现，很多实现方案从Paxos开始，到后面就相差甚远，费时费力且容易引入错误

### 4. Designing for understandability

……

