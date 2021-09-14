# 机器学习 周志华
```
 __  __            _     _            
|  \/  | __ _  ___| |__ (_)_ __   ___ 
| |\/| |/ _` |/ __| '_ \| | '_ \ / _ \
| |  | | (_| | (__| | | | | | | |  __/
|_|  |_|\__,_|\___|_| |_|_|_| |_|\___|
                                      
 _                          _             
| |    ___  __ _ _ __ _ __ (_)_ __   __ _ 
| |   / _ \/ _` | '__| '_ \| | '_ \ / _` |
| |__|  __/ (_| | |  | | | | | | | | (_| |
|_____\___|\__,_|_|  |_| |_|_|_| |_|\__, |
                                    |___/ 
```
[toc]

## 第一章 绪论
<p style="text-align: center;"><img src="./img/ML-1.0.png" width=600/></p>
机器学习是什么:  
利用经验改善系统性能

### 基础概念
| 术语                 |                                                       |
|----------------------|-------------------------------------------------------|
| 监督学习vs无监督学习 | 监督学习:训练数据有标签                               |
| 分类,回归,聚类       | 回归:目标标签是连续值 聚类:将训练集中的样本分为若干簇 |
| 数据,样本,标签       |                                                       |
| 假设空间             | g的候选集合,学习过程就是从假设空间进行搜索的过程      |
| 版本空间             | 与训练集一致的假设的集合                              |


### NFL定理
没有免费的午餐定理:  
一个算法若再某些问题上比另一个算法好,则一定存在另一些问题,使后一算法优于前者  

$$
E_{ote}(\mathfrak L_a | X,f) = \sum_h \sum_{x \in \mathcal X-X} P(x)\mathrm{II}(h(x) \neq f(x))P(h | X, \mathfrak L_a)
$$

### 习题
1.2 穷举法程序见./programs  

## 第二章 模型评估
<p style="text-align: center;"><img src="./img/ML-2.0.png" width=800/></p>

### 基础概念
<p style="text-align: center;"><img src="./img/ML-2.1.png" width=600/></p>
训练数据分层  
1. 训练集:用来训练模型,模型的迭代优化
2. 验证集:调整超参数,优化模型
3. 测试集:不参与训练流程,检测模型效果

经验误差和泛化误差  
1. 经验误差:训练集上的误差
2. 泛化误差:在"未来"样本上的误差,对应测试集数据
3. 验证集:调整超参数

### 混淆矩阵
* 二分类数据集包含正例和负例
* 模型分类后包含预测正例和预测负例
* 由此共四种数据集合

<table>
	<tr>
		<td colspan="2" rowspan="2"></td><td colspan="2">Actual Values</td>
	</tr>
	<tr>
		<td>Positive (1)</td><td>Negative (0)</td>
	</tr>
	<tr>
		<td rowspan="2">Predicted Values</td><td>Positive (1)</td><td>TP</td><td>FP</td>
	</tr>
	<tr>
		<td>Negative (0)</td><td>FN</td><td>TN</td>
	</tr>
</table>

#### 根据混淆矩阵得到的评价指标
召回率,真实数据为正中,预测也为正的比例  
即召回的数据中,对正样本的覆盖率  
$$
Recall = TP/(TP+FN)
$$

精准率,召回的数据中,精准度的衡量  
$$
Precision = TP/(TP+FP)
$$

准确率和F1是对上两者的平衡  
$$
Accuracy = (TP+TN) / Total
$$
$$
F1 = 2*Recall*Precision/(Recall+Precision)
$$

AUC动态混淆矩阵


评估方法
1. 留出法
2. 交叉验证法
3. 自助法

性能度量
1. 均方误差 ROC AUC
2. 错误率vs精度 查准率vs查全率