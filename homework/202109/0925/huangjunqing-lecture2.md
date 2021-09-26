# Lecture 2 rpc and threads

[MIT-6.824-Distributed-Systems/l-rpc.txt.md at master · aQuaYi/MIT-6.824-Distributed-Systems (github.com)](https://github.com/aQuaYi/MIT-6.824-Distributed-Systems/blob/master/Lectures/LEC02/l-rpc.txt.md)

[【MIT公开课】6.824 分布式系统 · 2020年春（完结·中英字幕·机翻）_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1qk4y197bB?p=2)

## why Go ?

1、good support for threads and locking、synchronization between threads

2、rpc package

3、type safe and memory safe

4、simple than c++

## threads/go routines?

## concurrency VS parallel 

## thread challenge

sharing data

​	synchronization 

coordination between threads

​	Go channels or WaitGroup

deadLock

## What is a crawler?

## Crawler challenges

I/O concurrency

fetch only once

know when finished

## Solutions

1、Serial 串行化

2、concurrent with mutex

3、concurrent with channel

## RPC

