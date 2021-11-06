import numpy as np
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
        )

        self.action_head = nn.Sequential(
            nn.Conv2d(32, 2, kernel_size=(1, 1)),
            nn.BatchNorm2d(2),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(2 * (width - 4) * (height - 4), outputs),
        )

        # initialization function, first checks the module type,
        # then applies the desired changes to the weights
        def init_normal(m):
            if type(m) == nn.Linear:
                nn.init.uniform_(m.weight)

        # use the modules apply function to recursively apply the initialization
        self.conv_sequential.apply(init_normal)
        self.value_head.apply(init_normal)
        self.action_head.apply(init_normal)

    def forward(self, x):
        #print("Before", x)
        x = self.conv_sequential(x)
        #print("After", x)
        action_prob = F.softmax(self.action_head(x), dim=-1)
        state_value = torch.tanh(self.value_head(x))
        #print(action_prob)
        #print(state_value)
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

