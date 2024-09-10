import torch.nn as nn
import configs.model_config as model_config
 
 
conf=model_config.load_config()
conf_set=conf['conf_set']
conf_len=conf['conf_len']
 
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        # 第一層神經網路
        # nn.Sequential: 將裡面的模塊依次加入到神經網絡中
        self.layer1 = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=1), # 3通道變成16通道，圖片：48*140
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2)  # 圖片：22*70 /24*70
        )
        # 第2層神經網絡
        self.layer2 = nn.Sequential(
            nn.Conv2d(16, 64, kernel_size=3), # 16通道變成64通道，圖片：22*68
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2)  # 圖片：10*34 / 11*34
        )
        # 第3層神經網絡
        self.layer3 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3), # 16通道變成128通道，圖片： 9*32
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2)  # 圖片： 4*16
        )
        # 第4層神經網絡
        self.fc1 = nn.Sequential(
            nn.Linear(4*16*128, 1024),
            nn.Dropout(0.2),  # drop 20% of the neuron
            nn.ReLU()
        )
        # 第5層神經網絡
        self.fc2 = nn.Linear(1024, 4*36) # 4:驗證碼的長度， 36: 字母列表的長度
 
    #前向傳播
    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        x = self.fc2(x)
        return x