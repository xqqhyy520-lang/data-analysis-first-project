import pandas as pd

# 读取数据
df = pd.read_csv("student_scores.csv")

# 查看数据
print("=== 数据预览 ===")
print(df)

# 计算平均分
print("\n=== 各科平均分 ===")
print(df.mean(numeric_only=True))

# 计算总分
df["total"] = df["math"] + df["english"] + df["physics"]

# 排名
print("\n=== 总分排名 ===")
print(df.sort_values("total", ascending=False))
