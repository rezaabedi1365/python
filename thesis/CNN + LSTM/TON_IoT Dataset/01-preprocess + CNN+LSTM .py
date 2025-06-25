

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

# مرحله 1: بارگذاری داده
df = pd.read_csv("Train_Test_Network_traffic.csv")

# فقط حملات DDoS و Benign
df = df[df['Attack'].isin(['DDoS', 'Benign'])].copy()

# برچسب‌ها و ویژگی‌ها
labels = df['Attack']
df_features = df.drop(columns=['Attack', 'Source IP', 'Destination IP', 'Timestamp'], errors='ignore')
df_features = df_features.select_dtypes(include=[np.number])  # فقط ویژگی‌های عددی

# نرمال‌سازی
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_features)
X = X_scaled.reshape((X_scaled.shape[0], X_scaled.shape[1], 1))

# برچسب‌ها به اعداد و one-hot
le = LabelEncoder()
y_encoded = le.fit_transform(labels)  # Benign=0, DDoS=1
y = to_categorical(y_encoded, num_classes=2)

# تقسیم داده
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# مرحله 2: تعریف مدل
def build_model(input_shape):
    model = Sequential()
    model.add(Conv1D(64, kernel_size=3, activation='relu', input_shape=input_shape))
    model.add(MaxPooling1D(pool_size=2))
    model.add(LSTM(64))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(2, activation='softmax'))  # 2 کلاس
    model.compile(optimizer=Adam(learning_rate=0.001),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model

model = build_model(X_train.shape[1:])

# مرحله 3: آموزش مدل
history = model.fit(X_train, y_train,
                    epochs=10,
                    batch_size=32,
                    validation_split=0.2)

# مرحله 4: ارزیابی مدل
loss, acc = model.evaluate(X_test, y_test)
print(f"\n🎯 دقت نهایی روی داده تست: {acc:.4f}\n")

# مرحله 5: رسم نمودارها
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(acc) + 1)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(epochs, acc, 'b', label='دقت آموزش')
plt.plot(epochs, val_acc, 'g', label='دقت اعتبارسنجی')
plt.title('دقت مدل در طول آموزش')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(epochs, loss, 'b', label='خطای آموزش')
plt.plot(epochs, val_loss, 'g', label='خطای اعتبارسنجی')
plt.title('خطای مدل در طول آموزش')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.show()

# مرحله 6: گزارش دقیق مدل
y_pred_probs = model.predict(X_test)
y_pred = np.argmax(y_pred_probs, axis=1)
y_true = np.argmax(y_test, axis=1)

cm = confusion_matrix(y_true, y_pred)
class_names = ['Benign', 'DDoS']

plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=class_names,
            yticklabels=class_names)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

print("\n📊 گزارش آماری عملکرد مدل:\n")
print(classification_report(y_true, y_pred, target_names=class_names))

# مرحله 7: ذخیره مدل
model.save("ddos_cnn_lstm_model.h5")
print("\n✅ مدل با موفقیت ذخیره شد: ddos_cnn_lstm_model.h5")
