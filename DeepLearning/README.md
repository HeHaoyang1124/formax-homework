# 2026 SCUT Racing招新DeepLearning作业

- 卷积维度变化：3 → 32 → 64 → 128
- 池化维度变化：128 → 64 → 32 → 16
- 全连接层维度变化：128x16x16 → 256 → 3
- 损失函数定义：分类任务使用交叉熵损失
- 优化器： Adam
- 学习率调度器：ReduceLROnPlateau