import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical

# --- بارگذاری دیتاست ---
df = pd.read_csv("iot_dh.csv")
print(df.head())
print("ستون‌ها:", df.columns)

# دقت کنید ستون‌ها: dt, dur, dur_nsec, tot_dur, pktrate, protocol, port_no, tx_kbps, rx_kbps, tot_kbps, label :contentReference[oaicite:4]{index=4}

# --- انتخاب ویژگی‌ها و برچسب‌ها ---
X = df[['dt','dur','dur_nsec','tot_dur','pktrate','protocol','port_no','tx_kbps','rx_kbps','tot_kbps']]
y = df['label']  # 0=Normal، 1=Attack :contentReference[oaicite:5]{index=5}

# --- نرمال‌سازی ---
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ---reshape برای مدل---
X_reshaped = X_scaled.reshape((X_scaled.shape[0], X_scaled.shape[1], 1))

# -- تبدیل y به one-hot --
y_cat = to_categorical(y, num_classes=2)

# --- تقسیم داده ---
X_train, X_test, y_train, y_test = train_test_split(X_reshaped, y_cat, test_size=0.2, random_state=42)

# --- ساخت مدل ---
def build_model(input_shape):
    model = Sequential([
        Conv1D(64, 3, activation='relu', input_shape=input_shape),
        MaxPooling1D(2),
        LSTM(64),
        Dense(64, activation='relu'),
        Dropout(0.5),
        Dense(2, activation='softmax')
    ])
    model.compile(Adam(0.001), loss='categorical_crossentropy', metrics=['accuracy'])
    return model

model = build_model(X_train.shape[1:])

# --- آموزش مدل ---
history = model.fit(X_train, y_train,
                    epochs=10,
                    batch_size=32,
                    validation_split=0.2)

# --- ارزیابی ---
loss, acc = model.evaluate(X_test, y_test)
print(f"\n🎯 Accuracy: {acc:.4f}")

# --- نمودارهای Accuracy و Loss ---
acc_hist = history.history['accuracy']
val_acc_hist = history.history['val_accuracy']
loss_hist = history.history['loss']
val_loss_hist = history.history['val_loss']
epochs = range(1, len(acc_hist)+1)

plt.figure(figsize=(12,5))
plt.subplot(1,2,1)
plt.plot(epochs, acc_hist, 'b', label='Train')
plt.plot(epochs, val_acc_hist, 'g', label='Val')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(1,2,2)
plt.plot(epochs, loss_hist, 'b', label='Train')
plt.plot(epochs, val_loss_hist, 'g', label='Val')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.tight_layout()
plt.show()

# --- Confusion Matrix و گزارش طبقه‌بندی ---
y_pred = np.argmax(model.predict(X_test), axis=1)
y_true = np.argmax(y_test, axis=1)
cm = confusion_matrix(y_true, y_pred)
print("\n📊 Classification Report:")
print(classification_report(y_true, y_pred, target_names=['Normal','Attack']))

plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Normal','Attack'],
            yticklabels=['Normal','Attack'])
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

# --- ذخیره مدل ---
model.save("iot_dh_cnn_lstm.h5")
print("\n✅ Model saved as iot_dh_cnn_lstm.h5")
