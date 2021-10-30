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
* 清空输入重定向 < 文件
* 从标准输入读入,直到分界符 << 分界符

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
| tee    | 保存至文件         |

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

## chapter 4
### shell 脚本
最基本的shell脚本可以视作命令的堆砌  
其改良有如下两个方向:  

1. 耳朵,接收
2. 大脑,判断

其中,1可以通过传递参数实现,如下  

| 变量 | 内容                    |
|------|-------------------------|
| $#   | 参数个数                |
| $0   | 脚本本身的名称          |
| $1   | 传递给脚本的第一个参数  |
| $*   | 全部参数                |
| $@   | 全部参数,不过是分开传递 |

2可以通过条件语句等实现  

#### shell基本运算

1. 算术运算符
2. 关系运算符
3. 布尔运算符
4. 字符串运算符
5. 文件测试运算符

原生bash不支持简单的数学运算,但可以通过其它命令比如expr,awk实现  

关系运算符  
| expr | meaning          |
|------|------------------|
| -eq  | equal            |
| -ne  | not equal        |
| -gt  | greater than     |
| -lt  | less than        |
| -ge  | greater or equal |
| -le  | less or equal    |

布尔运算符  
| expr | meaning |
|------|---------|
| !    | not     |
| -a   | and     |
| -o   | or      |

逻辑运算符  
&&,||  

```
if [ $VALA -eq 10 -a $VALB -eq 20]; then
	# do sth
fi


if [[ $VALA -eq 10 && $VALB -eq 20]]; then
	# do sth
fi
```

shell中使用这两个符号时,注意也可以表示为前一语句执行成功才执行后一语句;前一语句执行失败才执行后一语句  

```
[ ! $USER = root ] && echo "user" || echo root
```

文件测试
| expr | meaning                           |
|------|-----------------------------------|
| -d   | check if is dir                   |
| -e   | check if exists                   |
| -f   | check if is normal file           |
| -r   | check if current user can read    |
| -w   | check if current user can write   |
| -x   | check if current user can execute |

字符串操作  
| expr | meaning                              |
|------|--------------------------------------|
| =    | judge if strings are equal           |
| !=   | judge if strings are not equal       |
| -z   | judge if string's length is zero     |
| -n   | judge if string's length is not zero |
| $    | judge if string is null              |

test,[属于bash内置命令,而[[属于bash关键字,所以[[可以使用通配符,以及数学运算  

#### shell流程控制
```
#!/bin/bash

for I in 1 2 3
do
	echo $I
done

for ((I=1;I<=3;I++))
do 
	echo $I
done

I=1
while [[ $I -le 3 ]]
do
	echo $I
	I=`expr $I + 1`
done

I=1
until [ $I -gt 3 ]; do
	echo $I
	I=`expr $I + 1`
done

echo "I is $I"
if [ $I -eq 1 ]
then
	echo "I is 1"
elif [ $I -eq 2 ]
then
	echo "I is 2"
elif [ $I -eq 3 ]
then
	echo "I is 3"
else
	echo "I is greater than 3"
fi

case $I in
	1)
		echo "I is 1"
		;;
	2)
		echo "I is 2"
		;;
	3)
		echo "I is 3"
		;;
	*)
		echo "I is not 1, 2 or 3"
		;;
esac
```

### 计划任务

* 一次性: at
* 多次性: crond服务


#### at
echo "命令字符串" | at [time]  

```
echo "reboot" | at +2 MINUTE
echo "reboot" | at 19:00
```

删除可用atrm  

#### crond
服务采用crontab进行配置  
```
minute hour date month weekday command
*      *    *    *     *       [command]
*/2    # every two minute
1-5    # at 1,2,3,4 or 5 minute
1,2    # at 1 or 2 minute
```

* 建议不要直接修改配置文件,因为crontab会进行检查  
* 命令使用绝对路径

## chapter 5

### linux中的用户

uid0：root  
uid1-999：系统用户，linux系统服务多半使用独立系统用户运行，以保证控制被害  
uid1000-：普通用户  
  
每个用户都有基本组与扩展组，基本组在创建用户时即创建，只有用户一个组员，往往与用户同名。  
扩展组则是后天指定的。  

#### 用户与组管理指令

| 指令     | 描述             | 常用参数                        |
|----------|------------------|---------------------------------|
| id       | 查看用户和组信息 |                                 |
| useradd  | 添加用户         | -G 指定拓展组，-s 指定默认shell |
| usermod  | 改变用户状态     | -L -U 锁定解锁                  |
| userdel  | 删除用户         |                                 |
| groupadd | 创建新的用户组   |                                 |
| passwd   | 修改用户密码     |                                 |

### 文件权限管理

#### 权限概述
基本的权限有rwx，分别为读，写，执行  
对于dir而言：  

* 读：获取目录里文件列表
* 写：更改目录里文件列表（删除目录内文件需要此权限）
* 执行：进入该目录

具体而言：  

|   | 文件     | 目录  |
|---|----------|-------|
| r | cat      | ls    |
| w | vim      | touch |
| x | ./script | cd    |

#### 权限分类
对于文件，往往有类似如下的文件权限信息：  
```
dwrs-r---T+
```
其中第0位表示文件类型，后9位，3组信息对应所属用户，所属组，其它用户的权限。  
若为x则表示执行权限，s或t表示有执行权限与特殊权限，S或T表示有特殊权限无执行权限。  
+表示文件访问控制列表设定，.表示没有。  
注意：**隐藏权限**不在此处显示。  
上述的字母也可以用三位或四位数字表示，如755  

linux中文件的权限如下：  

1. 基本权限
2. 特殊权限 suid sgid sbit
3. 隐藏权限
4. 文件访问控制表 facl

命令：  

```
chomod：chomod -R 777 文件，chmod o+t 文件
chown：chown [-R] 所有者:所有组 文件
```

#### 特殊权限
suid(set user id)：进程的发起者，同文件的属主，则应用文件属主权限。设置suid即允许用户以该文件的属主的权限执行该文件（此时进程发起者为属主），如系统的passwd，需要更改/etc/passwd，/etc/shadow。只针对二进制文件。  
guid(set group id)：对文件设置时，与suid类似。对目录设置时，目录内新创建文件自动继承该目录原有组的名称。  
sbit(set bit)：保护位/粘滞位。针对目录，设置后目录内文件只有属主才能删除。  

#### 隐藏权限

通过setattr，lsattr设置和显示  
setattr +属性 文件  
setattr -属性 文件  

#### 文件访问控制表

针对单一用户或用户组设置权限。  
setfacl  
getfacl 不能使用绝对路径  

使用getfacl对权限备份和恢复：  
```
getfacl -R [dirname] > backup.acl
setfacl --restore backup.acl
```
