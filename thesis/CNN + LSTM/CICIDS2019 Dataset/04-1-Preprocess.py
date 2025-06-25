#https://www.unb.ca/cic/datasets/ddos-2019.html
#https://www.kaggle.com/datasets/tarundhamor/cicids-2019-dataset

import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

# تنظیمات
input_file = "CICDDoS2019.csv"  # مسیر فایل اصلی
output_dir = "./dataset"
seq_len = 10

os.makedirs(output_dir, exist_ok=True)

# بارگذاری داده
print("Loading data...")
df = pd.read_csv(input_file)

# حذف ستون‌های غیر عددی به جز label
non_numeric_cols = df.select_dtypes(include=['object']).columns.tolist()
non_numeric_cols = [col for col in non_numeric_cols if col != 'Label']
df = df.dropna()
df = df.drop(columns=[col for col in non_numeric_cols if col != 'Label'])

# رمزگذاری برچسب‌ها
print("Encoding labels...")
label_encoder = LabelEncoder()
df['labels'] = label_encoder.fit_transform(df['Label'])
df = df.drop(columns=['Label'])

# جدا کردن ویژگی‌ها و نرمال‌سازی
features = df.drop(columns=['labels']).values
scaler = StandardScaler()
features = scaler.fit_transform(features)
labels = df['labels'].values

# ساخت توالی‌ها
print("Creating sequences...")
X_seq, y_seq = [], []
for i in range(len(features) - seq_len + 1):
    X_seq.append(features[i:i+seq_len])
    y_seq.append(labels[i+seq_len-1])

X_seq = np.array(X_seq, dtype=np.float32)
y_seq = np.array(y_seq, dtype=np.int64)

# تقسیم داده به train/val/test
print("Splitting...")
X_temp, X_test, y_temp, y_test = train_test_split(X_seq, y_seq, test_size=0.2, stratify=y_seq, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.2, stratify=y_temp, random_state=42)

# ذخیره به عنوان فایل CSV
def save_to_csv(X, y, filename):
    N, T, F = X.shape
    X_flat = X.reshape(N, T * F)
    df = pd.DataFrame(X_flat)
    df['labels'] = y
    df.to_csv(os.path.join(output_dir, filename), index=False)

print("Saving...")
save_to_csv(X_train, y_train, "sequence_train.data")
save_to_csv(X_val, y_val, "sequence_val.data")
save_to_csv(X_test, y_test, "sequence_test.data")

print("Done. Files saved to", output_dir)
