# lab资料参考

这几天断断续续地做lab，发现有两大障碍。一是之前没写分布式的系统，基本没有经验可言，具体实现一头雾水；二是没有Golang经验，当有一个小小的想法时，编码本身也很艰难。于是今天开始试着参考网上别人的博客和代码，受到了很多的启发。回过头来看，如果全靠自己造，估计再给一个礼拜我可能也搞不定。

我主要参考了这篇文章以及作者给出的lab1的代码：https://zhuanlan.zhihu.com/p/372814816。总结一些设计要点如下：
- coordinator和worker都是两个工作循环。
- worker不断地向coordinator申请任务，然后执行任务；worker可能会执行Map或Reduce任务，但从系统的角度来看，要先执行完全部的Map任务，然后再执行Reduce任务。
- Coordinator总体分为MAP和REDUCE两个阶段，前者需要不断地处理Worker的Task申请、Task完成的通知，在Task全部完成之后，转移至REDUCE阶段；在REDUCE阶段，COordinator不断地分配Reduce Task。Coordinator需要周期性地巡检正在运行地Task，发现Task运行时长超过10s后重新分配其到新地Worker上运行。

