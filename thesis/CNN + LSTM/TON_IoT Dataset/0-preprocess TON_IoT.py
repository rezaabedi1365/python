#https://research.unsw.edu.au/projects/toniot-datasets
# download and change name to TON_IoT_Network.csv and save it to project path

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

# بارگذاری دیتاست
df = pd.read_csv("TON_IoT_Network.csv")

# بررسی ستون‌ها
print("ستون‌های دیتاست:", df.columns)

# اگر ستون Label وجود دارد و برچسب‌ها در آن است:
if 'Label' in df.columns:
    labels = df['Label']
else:
    raise Exception("ستون Label در دیتاست وجود ندارد!")

# حذف ستون‌های غیر عددی (به جز Label که حذف نمی‌کنیم)
non_num_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()
non_num_cols.remove('Label')  # Label رو حذف نکن
df = df.drop(columns=non_num_cols)

# استخراج ویژگی‌ها و برچسب‌ها
X = df.drop(columns=['Label'])
y = labels

# تبدیل برچسب‌ها به اعداد (مثلا 'DDoS' = 1 و 'Benign' = 0)
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# نرمال‌سازی داده‌ها
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# تغییر شکل داده برای مدل (samples, timesteps, features)
# چون داده‌ها سری زمانی نیستند، timesteps=1 و features=تعداد ویژگی‌ها
X_reshaped = X_scaled.reshape((X_scaled.shape[0], X_scaled.shape[1], 1))

# تبدیل برچسب‌ها به one-hot
num_classes = len(np.unique(y_encoded))
y_cat = to_categorical(y_encoded, num_classes=num_classes)

# تقسیم داده به آموزش و تست
X_train, X_test, y_train, y_test = train_test_split(X_reshaped, y_cat, test_size=0.2, random_state=42)

print("ابعاد X_train:", X_train.shape)
print("ابعاد y_train:", y_train.shape)



