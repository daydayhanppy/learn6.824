package mr

//
// RPC definitions.
//
// remember to capitalize all names.
//

import (
	"os"
	"strconv"
)

//
// example to show how to declare the arguments
// and reply for an RPC.
//

//worker request
type GetTaskRequest struct {
	X int
}
type GetTaskResponse struct {
	TaskState    int //0:map,1:reduce,2:sleep
	TaskName     string
	RFileName    []string
	MFileName    string
	ReduceNumber int //nReduce
}

//worker reply
type ReplyStatusRequest struct {
	FilesName []string //中间文件的信息
	TaskName  string   //output file name

}
type ReplyStatusResponse struct {
	X int
}
type ExampleArgs struct {
	X int
}

type ExampleReply struct {
	Y int
}

// Add your RPC definitions here.

// Cook up a unique-ish UNIX-domain socket name
// in /var/tmp, for the coordinator.
// Can't use the current directory since
// Athena AFS doesn't support UNIX-domain sockets.
func coordinatorSock() string {
	s := "/var/tmp/824-mr-"
	s += strconv.Itoa(os.Getuid())
	return s
}
