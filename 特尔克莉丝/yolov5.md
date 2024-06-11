### 1. 环境配置

```bash
git clone https://github.com/ultralytics/yolov5.git
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```



#### **1.1 YOLOv5目录结构中重要部分**

- `data/`: 存放数据集的配置文件。
- `models/`: 存放预训练模型的配置文件。
- `runs/`: 训练后生成的最佳模型和检测后生成的文件存放于此。

- `train.py/`: 训练模型
- `detect.py/`: 检测图片



#### **1.2 预训练模型下载及预测示例**

1. **下载预训练模型** `yolov5s.pt`:  
   
从YOLOv5的官方GitHub仓库下载预训练模型，或者使用提供的脚本自动下载。
   
2. **使用预训练模型进行预测**:

   ```bash
   # 使用下载的`yolov5s.pt`模型对`data/images/`目录中的图片进行目标检测，检测后的图片会生成在`runs/`目录里面
   python detect.py --source data/images/ --weights ./yolov5s.pt
   ```



### 2. coco128数据集的下载、训练和预测

预训练模型yolov5s.pt可以预测图片，但如果想要检测一些自定义的东西，我们需要自己准备数据集用来训练模型

这里可以先用coco128数据集来体验一下训练流程，里面包含了人类、车、猫等图片以及对应的标签

#### 2.1 训练

下载好coco128数据集后，可以看到里面包含images和labels，接下来开始训练

1. 打开`data/coco128.yaml`，这是数据集的配置文件，在里面设置好刚刚下载的coco数据集的训练集和验证集的路径等信息

2. 需要选择模型进行训练，这里选用上面提到的yolov5s.pt，在./models/可以看到配置文件，不过这个一般不需要修改

3. **运行命令**

   ```shell
   python train.py --img 640 --batch 16 --epochs 5 --data ./data/coco128.yaml --cfg ./models/yolov5s.yaml --weights ./yolov5s.pt
   
   # 这些参数可以直接在train.py里面设置
   ```

4. 在runs文件夹里面可以看到部分检测效果
5. 训练完毕后，整个过程的最好权重`best.pt`和最后权重`last.pt`程序会保存runs下面

#### 2.2 推断

```shell
# 设置需要检测的图片路径、训练好的最佳模型，图片会生成在runs
python .\detect.py --source .\data\images\zidane.jpg --weights .\runs\trai
n\exp7\weights\best.pt
```

