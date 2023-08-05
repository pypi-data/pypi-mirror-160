from torch.nn import *
from torch.nn.functional import *


class Net(Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = Conv2d(3, 12, (4, 4))
        self.layers = Sequential(
            Conv2d(3, 12, (4, 4)),
            Conv2d(3, 12, (4, 4)),
            Conv2d(3, 12, (4, 4)),
            Conv2d(3, 12, (4, 4))
        )

    def forward(self, x):
        return softmax(self.layers(x))
