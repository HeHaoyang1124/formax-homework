"""岭回归（L2正则化）"""
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error, r2_score

from linear_regression_manual import LinearRegressionManual, standardize_features, apply_standardization


def evaluate_model(name: str, y_true: np.ndarray, y_pred: np.ndarray) -> None:
    """评估模型性能，计算并打印RMSE和R²指标。
    
    参数:
        name: 模型名称（用于显示）
        y_true: 真实目标值数组
        y_pred: 模型预测值数组
    """
    rmse = root_mean_squared_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    print(f"{name} RMSE: {rmse:.4f}, R²: {r2:.4f}")


def main() -> None:
    """主函数：执行岭回归分析流程（含L2正则化）。"""
    # 1. 加载加州房价数据集
    dataset = fetch_california_housing()
    x, y = dataset.data, dataset.target

    # 2. 划分训练集和测试集（80%训练，20%测试）
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )

    # 3. 特征标准化（Z-score标准化）
    x_train_std, mean, std = standardize_features(x_train)
    x_test_std = apply_standardization(x_test, mean, std)

    # 4. 训练岭回归模型（L2正则化，λ=100）
    l2_lambda = 100.0
    model = LinearRegressionManual(l2_lambda=l2_lambda)
    model.fit(x_train_std, y_train)
    y_pred = model.predict(x_test_std)
    
    # 5. 评估模型
    print(f"正则化参数 λ={l2_lambda}")
    evaluate_model("岭回归(L2正则化)", y_test, y_pred)

    # 6. 展示前5个样本的预测结果
    print("\n前5个样本预测结果:")
    for i, (true_y, pred_y) in enumerate(zip(y_test[:5], y_pred[:5]), 1):
        print(f"  {i}. 真实值={true_y:.3f}, 预测值={pred_y:.3f}, 误差={abs(true_y - pred_y):.3f}")


if __name__ == "__main__":
    main()
