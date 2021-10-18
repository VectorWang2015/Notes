[toc]

## chapter 2

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
#### uname
unix name, show kernel info  
* a: all info, time is the time when the kernel is packaged

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

### states of process in Linux
| state | meaning                   | description                                                                                |
|-------|---------------------------|--------------------------------------------------------------------------------------------|
| R     | TASK_RUNNING              | ready or running                                                                           |
| S     | TASK_INTERRUPTIBLE        | waiting, suspended                                                                         |
| D     | TASK_UNINTERRUPTIBLE      | to avoid process being interrupted e.g. in kernal mode, this state is hardly catched by ps |
| Z     | TASK_DEAD - EXIT_ZOMBIE   | all resources being recycled, except task_struct which contains info as exit_code          |
| X     | TASK_DEAD - EXIT_DEAD     | all resources being recycled                                                               |
| T     | TASK_STOPPED, TASK_TRACED |                                                                                            |

### system resources related
#### top
##### first line
load average: average length of queue for 1, 5, 15 mins
##### cpu line
us: usage, id: idol
#### uptime
first line of top, user number in redhat 7 is the num of terminals(bug)
#### free
show memory usage
* h: human readable
#### nice
* n [niceness_value] [command]: launch a program with altered priority

### user/network related
#### who/w
show current users loging in 
#### last
show log-in history  
not safe, command will save result in /var/log/lastlog
#### ifconfig
if for interface  
| important info | meaning                                      |
|----------------|----------------------------------------------|
| first para     | name for network device                      |
| inet/inet6     | ip address                                   |
| ether          | mac address                                  |
| rx/tx          | statistics for data received and transmitted |

#### ping
in linux, ping will work continuously
#### tracepath
trace route in linux
#### netstat
* a: show all, including listening and non-listening
* n: show numeric(ip address), instead of symbolic host, port or user names

### console/file related
#### pwd
Print current Working Directory
#### cd
* -: change to the last used directory
#### ls
* a: all, including hidden(start with .)
* l: long, detailed info
#### tree
show hierachy tree for directory
#### file
show file type  
in linux, file is not distinguished through appendix
#### finders
everything inside linux is a file
| command name | detail                      |
|--------------|-----------------------------|
| find         | real time search            |
| locate       | search in database          |
| whereis      | binary, source, manual page |
| which        | only find shell commands    |

##### find
real time search  
* -name: name for file name
* -user: files that belong to the given user
* -exec: execute the command after each search, {} for searched results
e.g. `find -user linuxprobe -exec cp -a {} /root/findresults/ \;`  
##### locate
will update database then search in database  
can use **updatedb** to manualy update
1. cannot find all files
2. faster than find
#### file content
| command | name                                               |
|---------|----------------------------------------------------|
| cat     | contatenate content of file to terminal            |
| more    | cat in page mode, suitable for large files         |
| head    | -n [num]: to show head num lines for file          |
| tail    | similar to head, but tail lines, -f: to auto flush |

to fetch middle lines of a file: use pipe  
e.g. head -n 15 file | tail -n 5  
to show line 10-15
#### tr
translate  
e.g. tr [a-z] [A-z]  
find a-z and change them to capital alphabets
#### wc
words count  
* l: lines
* w: words
#### stat
show detailed file info
| name  | description                                                       |
|-------|-------------------------------------------------------------------|
| ATime | Access time, last time file accessed                              |
| CTime | Change time, last time file attributes changed e.g. location,mode |
| MTime | Modified time                                                     |

#### grep
* n: show nu
* v: inverted
print lines matching pattern
#### cut
divide text in columns and print
#### diff
show difference between files  
* brief: dont show details of difference
#### uniq
report or omit repeated lines  
**file is not changed, only shown in terminal in default**
#### sort
* n: sort in numeric form
#### touch
change file timestamps  
usually used to create text file
#### mkdir
* p: make parents if dont exist
#### cp
* r: recursive
#### dd
convert and copy file  
or copy with some conditions  
this command can be used to copy blocks  
for instance, copy from /dev/zero to create files of random size  
copy from cdrom to create iso file  
#### mv
#### rm
#### history
show history of commands  
1. will not clear when poweroff
2. will not update real-time
3. will show commands with num, commands can be called ![num]
* c: clear history
#### sosreport
collect and pack system info
#### tar
* czvf: pack, c for create, z for gzip, v for visualize, f for file
* xzvf: unpack, x for extract
z is not necessary now, tar can automatically distinguish file type

## chapter 3

### 输入重定向
* 清空输入重定向 <
* 追加输入重定向 <<

### 输出重定向

* 清空 >
* 追加 >>

1. 标准 1>
2. 错误 2>
3. 不加以区分 &>

### shell变量操作
| sign   | description        |
|--------|--------------------|
| =      | 赋值               |
| $      | 取变量值           |
| $$     | 取pid              |
| \|     | 管道符             |
| *      | 全通配             |
| ?      | 匹配任意一位       |
| ^      | 开头               |
| $      | 结尾               |
| []     | 里面的任一字符     |
| {}     | 序列,显示报错      |
| ""     | str                |
| ''     | 全局转义字符串     |
| ``     | 执行命令并返回结果 |
| alias  | 设置别名           |
| type   | 查看命令类型       |
| unset  | 取消变量           |
| export | 导出为全局变量     |

**通配符由shell先解释再执行**  
e.g.  
```
echo 123456 | passwd --stdin linuxprobe
# 更改linuxprobe用户的密码为123456
# history可以看到明文
```

### shell优先级
从高到低  
1. 绝对路径的执行命令
2. 别名命令
3. 内部命令
4. 外部命令

### 常用shell变量
* HOME
* SHELL
* HISTSIZE
* LANG
* RANDOM 生成随机uint
* PSI 提示符
