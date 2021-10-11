#### Divergence Sources

non-deterministic
- input：primary和backup接受客户端输入的时机应该是一致的【能不能也让主VM把输入发送给备VM呢？】
- timer interrupt
- multicore (disallow)

#### Interrupts

#### Non-deternministic instructions

非确定性指令的数量是比较少的，比如随机数生成器，获取时间的指令，获取计算机的唯一id等，可以让primary把执行结果发送给backup，而backup不真正执行这些指令。

#### Output Rule

不允许Backup执行指令的时间领先于primary







