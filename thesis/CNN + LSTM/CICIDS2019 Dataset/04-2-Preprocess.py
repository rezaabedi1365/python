import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import os

def preprocess_and_save(data_path, output_dir, seq_len=10, test_size=0.2, val_size=0.1):
    # بارگذاری داده‌ی خام
    df = pd.read_csv(data_path)

    # فرض بر این است که آخرین ستون، برچسب است
    features = df.iloc[:, :-1].values
    labels = df.iloc[:, -1].values

    # نرمال‌سازی ویژگی‌ها
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    # ترکیب ویژگی‌ها و برچسب‌ها برای ساخت مجدد DataFrame
    data = np.hstack([features_scaled, labels.reshape(-1, 1)])
    df_scaled = pd.DataFrame(data)
    df_scaled.columns = [f'feature_{i}' for i in range(features.shape[1])] + ['labels']

    # تقسیم داده‌ها
    train_val_data, test_data = train_test_split(df_scaled, test_size=test_size, stratify=df_scaled['labels'], random_state=42)
    train_data, val_data = train_test_split(train_val_data, test_size=val_size, stratify=train_val_data['labels'], random_state=42)

    # ذخیره‌سازی
    os.makedirs(output_dir, exist_ok=True)
    train_data.to_csv(os.path.join(output_dir, 'sequence_train.data'), index=False)
    val_data.to_csv(os.path.join(output_dir, 'sequence_val.data'), index=False)
    test_data.to_csv(os.path.join(output_dir, 'sequence_test.data'), index=False)
    print("Preprocessing done. Files saved in:", output_dir)

# استفاده:
if __name__ == "__main__":
    preprocess_and_save(
        data_path="raw_dataset.csv",   # فایل CSV اولیه با ویژگی‌ها و برچسب‌ها
        output_dir="./dataset",
        seq_len=10,
        test_size=0.2,
        val_size=0.1
    )
