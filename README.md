# 基于yolov5的跌倒检测
先把VOC格式的数据集放到FallDataset文件夹里<br>
然后在train.py里选择想训练的模型

### 划分训练集和验证集，然后生成txt格式的标签
```python
python my_test.py                                                                                                                          
python my_label.py 
```
### 训练
```python
python train.py 
```
