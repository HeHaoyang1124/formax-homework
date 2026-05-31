import os
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from tqdm import tqdm

# ----------------------------
# 1. 配置信息
# ----------------------------

# 设备选择
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"使用设备: {device}")

# 超参数设置
BATCH = 64
EPOCHS = 10
IMG_SIZE = 128
LEARNING_RATE = 0.001
NUM_CLASSES = 3  # 红黄蓝三种颜色

# 保存文件名和路径
MODEL_NAME = 'color.pt'
EXPORT_ONNX_NAME = 'color.onnx'
DATASET_ROOT = r'path/to/dataset'

# ----------------------------
# 2. 数据准备
# ----------------------------
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

# 加载自定义数据集
train_dataset = ImageFolder(root=f'{DATASET_ROOT}/train', transform=transform)
valid_dataset = ImageFolder(root=f'{DATASET_ROOT}/test1', transform=transform)
train_loader = DataLoader(train_dataset, batch_size=BATCH, shuffle=True, num_workers=0)
valid_loader = DataLoader(valid_dataset, batch_size=BATCH, shuffle=False, num_workers=0)

print(f"训练集类别: {train_dataset.classes}")
print(f"训练集样本数: {len(train_dataset)}")
print(f"验证集样本数: {len(valid_dataset)}")


# ----------------------------
# 3. 定义模型结构
# ----------------------------
class ColorCNN(nn.Module):
    def __init__(self, num_classes=3):
        super(ColorCNN, self).__init__()
        self.features = nn.Sequential(
            # 维度 3 -> 32
            # 长宽 128 -> 64
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.LeakyReLU(),
            nn.MaxPool2d(2, 2),

            # 维度 32 -> 64
            # 长宽 64 -> 32
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.LeakyReLU(),
            nn.MaxPool2d(2, 2),

            # 维度 64 -> 128
            # 长宽 32 -> 16
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.LeakyReLU(),
            nn.MaxPool2d(2, 2)
        )

        self.classifier = nn.Sequential(
            # 全连接层输入维度：128 * 16 * 16 -> 256 -> 3
            nn.Flatten(),
            nn.Linear(128 * 16 * 16, 256),
            nn.LeakyReLU(),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x


model = ColorCNN(num_classes=NUM_CLASSES).to(device)

# ----------------------------
# 4. 加载预训练模型（如果存在）
# ----------------------------

if os.path.exists(MODEL_NAME):
    print(f"\n检测到预训练模型: {MODEL_NAME}")
    try:
        model.load_state_dict(torch.load(MODEL_NAME, map_location=device))
        print(f"预训练模型加载成功，从已有模型继续训练\n")
    except Exception as e:
        print(f"加载预训练模型失败，从头开始训练: {e}")
else:
    print(f"\n未找到预训练模型，从头开始训练\n")

# ----------------------------
# 5. 开始训练
# ----------------------------

# 损失函数：交叉熵损失
criterion = nn.CrossEntropyLoss()
# 优化器：Adam
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
# 学习率调度器：ReduceLROnPlateau
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=3)

best_acc = 0.0  # 初始化最佳准确率

for epoch in range(0, EPOCHS):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    # 训练过程进度条
    train_iterator = tqdm(train_loader, desc=f"Epoch [{epoch + 1}/{EPOCHS}] 训练中", leave=True)

    for batch_idx, (images, labels) in enumerate(train_iterator):
        # 将数据移动到设备上
        images: torch.Tensor = images.to(device)
        labels: torch.Tensor = labels.to(device)

        # 1. 前向传播
        outputs = model(images)
        # 2. 计算损失
        loss = criterion(outputs, labels)
        # 3. 清空梯度, 反向传播, 计算梯度
        optimizer.zero_grad()
        loss.backward()
        # 4. 更新参数
        optimizer.step()

        # 统计损失和准确率
        running_loss += loss.item()
        # 在维度 1 上寻找最大值的索引（即预测的类别）
        _, predicted = outputs.max(1)
        # 累计样本数和正确预测数
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

        # 更新进度条显示当前损失和准确率
        train_iterator.set_postfix({'loss': f'{loss.item():.4f}',
                                    'acc': f'{100. * correct / total:.2f}%'})

    # 训练阶段结束，计算平均损失和准确率
    train_acc = 100. * correct / total
    avg_loss = running_loss / len(train_loader)

    # 验证阶段
    model.eval()
    val_correct = 0
    val_total = 0
    val_iterator = tqdm(valid_loader, desc=f"Epoch [{epoch + 1}/{EPOCHS}] 验证中", leave=True)
    with torch.no_grad():  # 验证不用梯度计算，加快速度
        for images, labels in val_iterator:
            # 将数据移动到设备(GPU)上
            images, labels = images.to(device), labels.to(device)
            # 前向传播
            outputs = model(images)
            # 在维度 1 上寻找最大值的索引（即预测的类别）
            _, predicted = outputs.max(1)
            # 累计样本数和正确预测数
            val_total += labels.size(0)
            val_correct += predicted.eq(labels).sum().item()
            # 更新进度条显示当前准确率
            val_iterator.set_postfix({'acc': f'{100. * val_correct / val_total:.2f}%'})

    # 获取验证准确度
    val_acc = 100. * val_correct / val_total
    # 根据验证损失调整学习率
    scheduler.step(avg_loss)

    print(f"\n{'=' * 60}")
    print(f"Epoch [{epoch + 1}/{EPOCHS}] 完成")
    print(f"  训练损失: {avg_loss:.4f}")
    print(f"  训练准确率: {train_acc:.2f}%")
    print(f"  验证准确率: {val_acc:.2f}%")
    print(f"  当前学习率: {optimizer.param_groups[0]['lr']:.6f}")

    # 保存最佳模型
    if val_acc > best_acc:
        best_acc = val_acc
        torch.save(model.state_dict(), MODEL_NAME)
        print(f"保存最佳模型")
    else:
        print(f"历史最佳准确率： {best_acc:.2f}%")
    print(f"{'=' * 60}\n")
