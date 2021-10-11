[toc]

## 第二章

### system related commands
#### systemctl
* start
* stop
* restart
* enable
* disable

#### reboot
#### poweroff
#### date
#### timedatectl
* set-time
* set-timezone

### process related commands
#### ps
* aux: to see every process on the system using BSD syntax
#### pstree
like ps, but show process in a tree
#### pidof
show pid(s) of a process
#### kill
kill certain process with given pid
#### killall
kill certain service with all its pids
#### top
##### first line
load average: average length of queue for 1, 5, 15 mins
##### cpu line
us: usage, id: idol
#### nice
* n [niceness_value] [command]: launch a program with altered priority

### states of process in Linux
| state | meaning                   | description                                                                                |
|-------|---------------------------|--------------------------------------------------------------------------------------------|
| R     | TASK_RUNNING              | ready or running                                                                           |
| S     | TASK_INTERRUPTIBLE        | waiting, suspended                                                                         |
| D     | TASK_UNINTERRUPTIBLE      | to avoid process being interrupted e.g. in kernal mode, this state is hardly catched by ps |
| Z     | TASK_DEAD - EXIT_ZOMBIE   | all resources being recycled, except task_struct which contains info as exit_code          |
| X     | TASK_DEAD - EXIT_DEAD     | all resources being recycled                                                               |
| T     | TASK_STOPPED, TASK_TRACED |                                                                                            |
