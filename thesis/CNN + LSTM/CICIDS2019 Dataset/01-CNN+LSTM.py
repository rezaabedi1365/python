import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import torch
import torch.nn as nn
import torch.optim as optim
import os
from datetime import datetime
import gc

# ================= Data Loader =====================
class data_cls:
    def __init__(self, path):
        self.df = pd.read_csv(path, sep=',')
        self.loaded = True
        self.path = path

    def get_data(self):
        if not self.loaded:
            self._load_df()
        shuffled_df = self.df.sample(frac=1).reset_index(drop=True)
        labels = torch.tensor(shuffled_df['labels'].values, dtype=torch.float32)
        features = torch.tensor(shuffled_df.drop('labels', axis=1).values, dtype=torch.float32)
        features = features.unsqueeze(1)  # برای CNN+LSTM
        return features, labels

    def _load_df(self):
        self.df = pd.read_csv(self.path, sep=',')

    def load_test_data(self, test_path):
        test_df = pd.read_csv(test_path, sep=',')
        test_features = torch.tensor(test_df.iloc[:, :-1].values, dtype=torch.float32)
        test_labels = torch.tensor(test_df.iloc[:, -1].values, dtype=torch.float32)
        test_features = test_features.unsqueeze(1)  # برای CNN+LSTM
        return test_features, test_labels

# ================= Environment =====================
class RLenv(data_cls):
    def __init__(self, path):
        super().__init__(path)
        self.state_shape = self.df.shape[1] - 1

    def reset(self):
        states, labels = self.get_data()
        return states, labels

    def step(self, actions, i_iter, states_all, labels_all):
        done = (i_iter + 1 >= len(states_all))
        next_states, labels = states_all[i_iter + 1], labels_all[i_iter + 1]
        rewards = (actions == labels_all[i_iter]).float() * 1.0
        return next_states, rewards, done

# ================= Model: CNN + LSTM =====================
class CNNLSTMNet(nn.Module):
    def __init__(self, input_dim, cnn_out_channels, lstm_hidden_size, num_classes):
        super(CNNLSTMNet, self).__init__()
        self.conv1 = nn.Conv1d(1, cnn_out_channels, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool1d(kernel_size=2)
        self.lstm = nn.LSTM(input_size=cnn_out_channels, hidden_size=lstm_hidden_size, batch_first=True)
        self.fc = nn.Linear(lstm_hidden_size, num_classes)

    def forward(self, x):
        x = self.relu(self.conv1(x))         # (B, C, L)
        x = self.pool(x)                     # (B, C, L/2)
        x = x.permute(0, 2, 1)               # (B, L/2, C)
        lstm_out, _ = self.lstm(x)
        out = self.fc(lstm_out[:, -1, :])    # Last timestep
        return out

# ================= Main =====================
if __name__ == "__main__":
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Config
    kdd_path = "./dataset/formated_train_simple.data"
    valid_actions = [0, 1]
    num_actions = len(valid_actions)
    num_epoch = 4000
    decay_rate = 0.9
    gamma = 0.1
    learning_rate = 0.1

    cnn_channels = 64
    lstm_hidden = 100

    parent_directory = "result_CNNLSTM"
    if not os.path.exists(parent_directory):
        os.makedirs(parent_directory)
    directory_name = datetime.now().strftime('%Y%m%d_%H%M%S')
    run_directory = os.path.join(parent_directory, directory_name)
    os.makedirs(run_directory)

    # Env + Model
    env = RLenv(kdd_path)
    model = CNNLSTMNet(input_dim=env.state_shape, cnn_out_channels=cnn_channels,
                       lstm_hidden_size=lstm_hidden, num_classes=num_actions).to(device)
    optimizer = optim.SGD(model.parameters(), lr=learning_rate)
    criterion = nn.MSELoss()

    reward_chain = []
    loss_chain = []

    for epoch in range(num_epoch):
        states_all, labels_all = env.reset()
        states_all = states_all.to(device)
        labels_all = labels_all.to(device)
        total_rewards = 0

        all_target_q_values = []
        all_current_q_values = []

        for i_iteration in range(len(states_all) // 10):
            states = states_all[i_iteration].unsqueeze(0)  # (1, 1, input_dim)
            q_values = model(states)
            exploration = decay_rate ** (epoch / 5)

            if np.random.rand() < exploration:
                actions = torch.tensor([np.random.choice(valid_actions)], device=device)
            else:
                actions = torch.argmax(q_values, dim=1)

            next_states, rewards, done = env.step(actions, i_iteration, states_all, labels_all)
            next_states = next_states.unsqueeze(0).to(device)  # (1, 1, input_dim)
            rewards = rewards.to(device)

            with torch.no_grad():
                next_q_values = model(next_states)
                max_next_q_values = next_q_values.max(1)[0]
                target_q_values = rewards + (1 - done) * gamma * max_next_q_values

            actions = actions.type(torch.int64)
            current_q_values = q_values.gather(1, actions.view(-1, 1)).squeeze(1)

            all_target_q_values.append(target_q_values)
            all_current_q_values.append(current_q_values)

            total_rewards += rewards.item()

            if done:
                break

        all_target_q_values = torch.stack(all_target_q_values)
        all_current_q_values = torch.stack(all_current_q_values)
        loss = criterion(all_current_q_values, all_target_q_values)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        reward_chain.append(total_rewards / (len(states_all)/10))
        loss_chain.append(loss.item())

        print(f"Epoch {epoch + 1}/{num_epoch} | Loss: {loss:.6f} | Rewards: {reward_chain[-1]:.4f}")

        del all_target_q_values, all_current_q_values
        torch.cuda.empty_cache()
        gc.collect()

    # Save Model
    model_path1 = os.path.join(run_directory, 'model.pth')
    torch.save(model.state_dict(), model_path1)

    # Save Reward & Loss Graphs
    plt.figure(figsize=(10, 5))
    plt.subplot(211)
    plt.plot(np.arange(len(reward_chain)), reward_chain)
    plt.title('Total Reward by Epoch -- CNN-LSTM')
    plt.xlabel('Epoch')
    plt.ylabel('Total Reward')

    plt.subplot(212)
    plt.plot(np.arange(len(loss_chain)), loss_chain)
    plt.title('Loss by Epoch -- CNN-LSTM')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.tight_layout()
    plt.savefig(os.path.join(run_directory, 'reward_loss_by_epoch.png'))
    plt.close()

    # =================== Test Phase ===================
    test_features, test_labels = env.load_test_data("./dataset/formated_test_simple.data")
    test_features = test_features.to(device)
    test_labels = test_labels.to(device)

    model.eval()
    with torch.no_grad():
        test_q_values = model(test_features)
        test_actions = torch.argmax(test_q_values, dim=1).cpu()

    test_labels_np = test_labels.cpu().numpy()
    test_actions_np = test_actions.numpy()
    accuracy = (test_actions_np == test_labels_np).sum() / len(test_labels_np)

    print(f"\nTest Accuracy: {accuracy:.4f}")
    cm = confusion_matrix(test_labels_np, test_actions_np)
    print("Confusion Matrix:")
    print(cm)
    print("Classification Report:")
    print(classification_report(test_labels_np, test_actions_np))

    # Confusion Matrix Plot
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Predicted 0', 'Predicted 1'],
                yticklabels=['Actual 0', 'Actual 1'])
    plt.title('Confusion Matrix -- CNN-LSTM')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.savefig(os.path.join(run_directory, 'confusion_matrix.png'))
    plt.close()
