## 注意事项
### hows

如何看示例：
```
dnf search *[keyword]*
ansible-doc -l
ansible-doc [module name]
```

### Q1

inventory中变量添加ansible_user和ansible_password  
注意cfg文件中设置remote_user，关闭验证  

### Q2

注意给ansible -m使用模块功能时，使用-a和字符串添加参数  

### Q3

注意yum的剧本中，软件组（group）的字符串以@开头，全部软件使用"*"  

### Q4

软件包rhel-system-roles  
参考（example）yaml文件在/usr/share/doc内  
cfg文件中记得添加roles文件夹  

### Q5

```
---
- src: [tar file src]
  name: [role name]
```
```
ansible-galaxy install -r [yaml_name]
```
r的意思是从文件安装roles  

### Q6

```
ansible_galaxy init [role_name]
```
role的task在tasks文件夹中main.yml  
注意role的task不需要写hosts，因为role本身就是“模版”  
```
---
- name:
  [module]:
```

1. 服务：service
2. 防火墙：firewalld
3. 模版：template，模版文件放角色template文件夹

**j2文件的jinja字段{{后和}}前有空格！！！**
```
{{ ansible_fqdn }}
{{ ansible_default_ipv4.address }}
```

### Q7 使用角色

```
---
- name: [name]
  hosts: [hosts]
  roles:
    - [role name]
		...
```
