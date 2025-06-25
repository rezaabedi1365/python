import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import confusion_matrix, classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical

# 1️⃣ بارگذاری دیتاست
df = pd.read_csv(cicddos2019_dataset.csv)

# حذف ستون‌های غیر ضروری (FlowID, IPها، پورت‌ها، timestamp)
non_feat = ['Flow ID', 'Source IP', 'Destination IP', 'Source Port', 'Destination Port', 'Timestamp']
df = df.drop(columns=[c for c in non_feat if c in df.columns], errors='ignore')

# فیلتر فقط نمونه‌های DDoS و BENIGN
df = df[df[' Label'].isin(['BENIGN', 'DDOS'])]
df = df.rename(columns={' Label''Label'})  # ساده‌سازی نام ستون

# انتخاب ویژگی‌های عددی محدود (مثلاً 20 ویژگی اول عددی برای کاهش بار محاسباتی)
X = df.select_dtypes(include=[np.number]).iloc[, 20]  # فقط 20 ویژگی اول عددی
y = df['Label']

# تبدیل برچسب‌ها به عدد
le = LabelEncoder()
y_enc = le.fit_transform(y)  # BENIGN-0, DDOS-1
y_cat = to_categorical(y_enc, num_classes=2)

# نرمال‌سازی ویژگی‌ها
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# reshape برای LSTM و Conv1D [نمونه‌ها, زمان (ویژگی‌ها), کانال=1]
X_tensor = X_scaled.reshape((X_scaled.shape[0], X_scaled.shape[1], 1))

# تقسیم داده به آموزش و تست
X_train, X_test, y_train, y_test = train_test_split(
    X_tensor, y_cat, test_size=0.2, random_state=42)

# 2️⃣ تعریف مدل سبک‌وزن بهینه‌شده
def build_lightweight_model(input_shape)
    model = Sequential([
        Conv1D(32, 3, activation='relu', input_shape=input_shape),  # کاهش فیلترها به 32
        MaxPooling1D(2),
        LSTM(32),  # کاهش واحدهای LSTM به 32
        Dropout(0.3),
        Dense(32, activation='relu'),
        Dropout(0.3),
        Dense(2, activation='softmax')
    ])
    model.compile(optimizer=Adam(0.001), 
                  loss='categorical_crossentropy', 
                  metrics=['accuracy'])
    return model

model = build_lightweight_model(X_train.shape[1])

# 3️⃣ آموزش مدل
history = model.fit(
    X_train, y_train,
    epochs=15, batch_size=64,
    validation_split=0.2,
    verbose=2
)

# 4️⃣ ارزیابی مدل
loss, acc = model.evaluate(X_test, y_test, verbose=0)
print(fn🎯 Test Accuracy {acc.4f})

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

# ماتریس سردرگمی و گزارش طبقه‌بندی
y_pred = np.argmax(model.predict(X_test), axis=1)
y_true = np.argmax(y_test, axis=1)
cm = confusion_matrix(y_true, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=le.classes_, yticklabels=le.classes_)
plt.xlabel('Predicted'); plt.ylabel('Actual')
plt.title('Confusion Matrix'); plt.show()
print(n📊 Classification Report)
print(classification_report(y_true, y_pred, target_names=le.classes_))

# 5️⃣ ذخیره مدل (برای بهینه‌سازی بیشتر می‌توانید از TensorFlow Lite استفاده کنید)
model.save(lightweight_cicddos2019_cnn_lstm.h5)
print(n✅ Model saved to lightweight_cicddos2019_cnn_lstm.h5)

# --- نکته برای کوانتیزاسیون و فشرده‌سازی مدل می‌توانید از TensorFlow Lite استفاده کنید ---
# نمونه کد تبدیل مدل به TFLite با کوانتیزاسیون (پس از آموزش مدل)

import tensorflow as tf

converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

with open('model_quantized.tflite', 'wb') as f
    f.write(tflite_model)
print(✅ Quantized TFLite model saved.)

