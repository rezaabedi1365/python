import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime
import random

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
from sklearn.metrics import classification_report, confusion_matrix

# تنظیم seed برای reproducibility
def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

# مدل ترکیبی CNN + LSTM
class CNN_LSTMNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_layers=1):
        super(CNN_LSTMNet, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        self.conv1 = nn.Conv1d(in_channels=input_size, out_channels=64, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool1d(kernel_size=2)

        self.lstm = nn.LSTM(input_size=64, hidden_size=hidden_size, num_layers=num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = x.permute(0, 2, 1)  # [batch, features, seq_len]
        x = self.conv1(x)
        x = self.relu(x)
        x = self.pool(x)  # [batch, 64, seq_len//2]
        x = x.permute(0, 2, 1)  # [batch, seq_len//2, 64]

        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)

        out, _ = self.lstm(x, (h0, c0))
        out = out[:, -1, :]
        return self.fc(out)

# بارگذاری داده‌ها با تبدیل به numpy (حافظه بهینه)
def load_sequence_data(path, seq_len=10):
    df = pd.read_csv(path)
    X_all = df.drop("labels", axis=1).values
    y_all = df["labels"].values

    num_sequences = len(X_all) - seq_len + 1
    X_seq = []
    y_seq = []
    for i in range(num_sequences):
        X_seq.append(X_all[i:i+seq_len])
        y_seq.append(y_all[i+seq_len-1])  # برچسب گام آخر توالی

    X_np = np.array(X_seq)
    y_np = np.array(y_seq)

    X_tensor = torch.tensor(X_np, dtype=torch.float32)
    y_tensor = torch.tensor(y_np, dtype=torch.long)
    return X_tensor, y_tensor

# آموزش مدل
def train(model, dataloader, criterion, optimizer, device):
    model.train()
    total_loss = 0
    for x_batch, y_batch in dataloader:
        x_batch, y_batch = x_batch.to(device), y_batch.to(device)
        optimizer.zero_grad()
        outputs = model(x_batch)
        loss = criterion(outputs, y_batch)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(dataloader)

# اعتبارسنجی مدل
def validate(model, dataloader, criterion, device):
    model.eval()
    total_loss = 0
    all_preds, all_labels = [], []
    with torch.no_grad():
        for x_batch, y_batch in dataloader:
            x_batch, y_batch = x_batch.to(device), y_batch.to(device)
            outputs = model(x_batch)
            loss = criterion(outputs, y_batch)
            total_loss += loss.item()
            preds = torch.argmax(outputs, dim=1).cpu()
            all_preds.extend(preds.numpy())
            all_labels.extend(y_batch.cpu().numpy())
    avg_loss = total_loss / len(dataloader)
    return avg_loss, np.array(all_preds), np.array(all_labels)

if __name__ == "__main__":
    set_seed(42)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Device:", device)

    train_path = "./dataset/sequence_train.data"
    val_path = "./dataset/sequence_val.data"
    test_path = "./dataset/sequence_test.data"

    seq_len = 10
    batch_size = 64

    train_x, train_y = load_sequence_data(train_path, seq_len)
    val_x, val_y = load_sequence_data(val_path, seq_len)
    test_x, test_y = load_sequence_data(test_path, seq_len)

    input_size = train_x.shape[2]
    num_classes = len(np.unique(train_y.numpy()))

    train_loader = DataLoader(TensorDataset(train_x, train_y), batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(TensorDataset(val_x, val_y), batch_size=batch_size)
    test_loader = DataLoader(TensorDataset(test_x, test_y), batch_size=batch_size)

    model = CNN_LSTMNet(input_size, hidden_size=100, output_size=num_classes, num_layers=1).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    run_dir = f"results_cnn_lstm/{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(run_dir, exist_ok=True)

    best_val_loss = float('inf')
    losses = []
    val_losses = []

    epochs = 30
    for epoch in range(epochs):
        train_loss = train(model, train_loader, criterion, optimizer, device)
        val_loss, val_preds, val_trues = validate(model, val_loader, criterion, device)

        print(f"Epoch {epoch+1}/{epochs} - Train Loss: {train_loss:.4f} - Val Loss: {val_loss:.4f}")

        losses.append(train_loss)
        val_losses.append(val_loss)

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), os.path.join(run_dir, "best_model.pth"))
            print("Saved Best Model")

    # ارزیابی نهایی
    model.load_state_dict(torch.load(os.path.join(run_dir, "best_model.pth")))
    test_loss, preds, trues = validate(model, test_loader, criterion, device)

    acc = np.mean(preds == trues)
    print(f"\nTest Accuracy: {acc:.4f}")
    print("Classification Report:")
    print(classification_report(trues, preds))

    cm = confusion_matrix(trues, preds)

    # نمودارها
    plt.plot(losses, label="Train Loss")
    plt.plot(val_losses, label="Validation Loss")
    plt.title("Training and Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.savefig(os.path.join(run_dir, "losses.png"))
    plt.close()

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.title("Confusion Matrix")
    plt.savefig(os.path.join(run_dir, "conf_matrix.png"))
    plt.close()
