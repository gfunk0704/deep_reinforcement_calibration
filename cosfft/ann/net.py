import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
  def __init__(self):
    super(Net, self).__init__()
    self.func1 = nn.Linear(11, 200)
    self.func2 = nn.Linear(200, 200)
    self.func3 = nn.Linear(200, 200)
    self.func4 = nn.Linear(200, 200)
    self.output = nn.Linear(200, 1)
  
  def forward(self, x):
    x = F.relu(self.func1(x))
    x = F.relu(self.func2(x))
    x = F.relu(self.func3(x))
    x = F.relu(self.func4(x))
    x = self.output(x)
    return x