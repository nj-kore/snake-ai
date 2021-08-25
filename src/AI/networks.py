import torch
import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):

    def __init__(self, inputs, outputs):
        super(Net, self).__init__()
        depth = inputs[0]
        width = inputs[1]
        height = inputs[2]

        self.conv_sequential = nn.Sequential(
            nn.Conv2d(depth, 32, kernel_size=(3,3)),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 32, kernel_size=(3,3)),
            nn.BatchNorm2d(32),
            nn.ReLU(),
        )

        self.value_head = nn.Sequential(
            nn.Conv2d(32, 1, kernel_size=(1, 1)),
            nn.BatchNorm2d(1),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear((width - 4) * (height - 4), 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Tanh()
        )

        self.actor_head = nn.Sequential(
            nn.Conv2d(32, 2, kernel_size=(1, 1)),
            nn.BatchNorm2d(2),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(2 * (width - 4) * (height - 4), outputs),
            nn.Softmax(dim=-1)
        )

    def forward(self, x):
        x = self.conv_sequential(x)
        action_prob = self.actor_head(x)
        state_value = self.value_head(x)
        return action_prob, state_value


"""
class ValueNet(Net):
    def __init__(self, width, height, depth):
        super(ValueNet, self).__init__(width, height, depth)

        

    def forward(self, x):
        x = super().forward(x)
        x = self.head_sequential(x)
        return x


class PolicyNet(Net):
    def __init__(self, width, height, depth, outputs):
        super(PolicyNet, self).__init__(width, height, depth)

        

    def forward(self, x):
        x = super().forward(x)
        x = self.head_sequential(x)
        return x

"""

