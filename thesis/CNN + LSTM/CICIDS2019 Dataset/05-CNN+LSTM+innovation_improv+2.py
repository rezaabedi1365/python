#https://data.mendeley.com/datasets/ssnc74xm6r/1?utm_source=chatgpt.com

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import confusion_matrix, classification_report
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv1D, MaxPooling1D, LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical

# 1️⃣ بارگذاری دیتاست
df = pd.read_csv("cicddos2019_dataset.csv")

# حذف ستون‌های غیر ضروری (FlowID, IPها، پورت‌ها، timestamp)
non_feat = ['Flow ID', 'Source IP', 'Destination IP', 'Source Port', 'Destination Port', 'Timestamp']
df = df.drop(columns=[c for c in non_feat if c in df.columns], errors='ignore')

# فیلتر فقط نمونه‌های DDoS و BENIGN
df = df[df[' Label'].isin(['BENIGN', 'DDOS'])]
df = df.rename(columns={' Label':'Label'})  # ساده‌سازی نام ستون

# استخراج ویژگی‌ها و برچسب‌ها
X = df.drop(columns=['Label'])
y = df['Label']

# تبدیل برچسب‌ها به عدد
le = LabelEncoder()
y_enc = le.fit_transform(y)  # BENIGN->0, DDOS->1
y_cat = to_categorical(y_enc, num_classes=2)

# حذف ستون‌های متن باقی‌مانده (در صورتی وجود)
X = X.select_dtypes(include=[np.number])

# نرمال‌سازی ویژگی‌ها
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_tensor = X_scaled.reshape((X_scaled.shape[0], X_scaled.shape[1], 1))

# تقسیم داده
X_train, X_test, y_train, y_test = train_test_split(
    X_tensor, y_cat, test_size=0.2, random_state=42)

# 2️⃣ تعریف و ساخت مدل
def build_model(input_shape):
    model = Sequential([
        Conv1D(64, 3, activation='relu', input_shape=input_shape),
        MaxPooling1D(2),
        LSTM(64),
        Dense(64, activation='relu'),
        Dropout(0.5),
        Dense(2, activation='softmax')
    ])
    model.compile(optimizer=Adam(0.001), 
                  loss='categorical_crossentropy', 
                  metrics=['accuracy'])
    return model

model = build_model(X_train.shape[1:])

# 3️⃣ آموزش مدل
history = model.fit(
    X_train, y_train,
    epochs=10, batch_size=64,
    validation_split=0.2
)

# 4️⃣ ارزیابی و نمایش نتایج
loss, acc = model.evaluate(X_test, y_test)
print(f"\n🎯 Test Accuracy: {acc:.4f}")

# رسم نمودار دقت و خطا
epochs_range = range(1, len(history.history['accuracy'])+1)
plt.figure(figsize=(12,5))
plt.subplot(1,2,1)
plt.plot(epochs_range, history.history['accuracy'], label='Train')
plt.plot(epochs_range, history.history['val_accuracy'], label='Val')
plt.title('Accuracy')
plt.xlabel('Epoch'); plt.ylabel('Accuracy'); plt.legend()
plt.subplot(1,2,2)
plt.plot(epochs_range, history.history['loss'], label='Train')
plt.plot(epochs_range, history.history['val_loss'], label='Val')
plt.title('Loss')
plt.xlabel('Epoch'); plt.ylabel('Loss'); plt.legend()
plt.tight_layout(); plt.show()

# ماتریس سردرگمی و گزارش آماری
y_pred = np.argmax(model.predict(X_test), axis=1)
y_true = np.argmax(y_test, axis=1)
cm = confusion_matrix(y_true, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=le.classes_, yticklabels=le.classes_)
plt.xlabel('Predicted'); plt.ylabel('Actual')
plt.title('Confusion Matrix'); plt.show()
print("\n📊 Classification Report:")
print(classification_report(y_true, y_pred, target_names=le.classes_))

# 5️⃣ ذخیره مدل
model.save("cicddos2019_cnn_lstm.h5")
print("\n✅ Model saved to cicddos2019_cnn_lstm.h5")
