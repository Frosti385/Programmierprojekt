import torch
import torchvision
from torchvision import transforms
from PIL import Image
from os import listdir
import random
import torch.optim as optim
from torch.autograd import Variable
import torch.nn.functional as F
import torch.nn as nn

normalize = transforms.Normalize(
    mean = [0.485, 0.456, 0.406],
    std = [0.229, 0.224, 0.225]
)

transforms = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(256),
    transforms.ToTensor(),
    normalize
])

train_data_list = []
target_list = []
train_data = []
files = listdir('C:/Users/moehlenkamj/Documents/Studium/Semester 5/Programmierprojekt/Projekt/Bilder/Garbage classification/Garbage classification/train/')
for i in range(len(listdir('C:/Users/moehlenkamj/Documents/Studium/Semester 5/Programmierprojekt/Projekt/Bilder/Garbage classification/Garbage classification/train/'))):
  f = random.choice(files)
  files.remove(f)
  img = Image.open("C:/Users/moehlenkamj/Documents/Studium/Semester 5/Programmierprojekt/Projekt/Bilder/Garbage classification/Garbage classification/train/" + f)
  img_tensor = transforms(img)
  train_data_list.append(img_tensor)
  isCardboard = 1 if 'cardboard' in f else 0
  isGlass = 1 if 'glass' in f else 0
  isMetal = 1 if 'metal' in f else 0
  isPaper = 1 if 'paper' in f else 0
  isPlastic = 1 if 'plastic' in f else 0
  isTrash = 1 if 'plastic' in f else 0
  target = [isCardboard, isGlass, isMetal, isPaper, isPlastic, isTrash]
  target_list.append(target)
  if len(train_data_list) >= 64:
    train_data.append((torch.stack(train_data_list), target_list))
    train_data_list = []
    print('Loaded batch ', len(train_data), 'of ', int(len(listdir('C:/Users/moehlenkamj/Documents/Studium/Semester 5/Programmierprojekt/Projekt/Bilder/Garbage classification/Garbage classification/train/'))/64))
    print('Percentage Done: ', int(len(train_data)*100/int(len(listdir("C:/Users/moehlenkamj/Documents/Studium/Semester 5/Programmierprojekt/Projekt/Bilder/Garbage classification/Garbage classification/train/"))/64)), '%')
    if len(train_data) > 150:
            break

class Netz(nn.Module):
  def __init__(self):
    print("init")
    super(Netz, self).__init__()
    self.conv1 = nn.Conv2d(3, 6, kernel_size=5)
    self.conv2 = nn.Conv2d(6, 12, kernel_size=5)
    self.conv3 = nn.Conv2d(12,18, kernel_size=5)
    self.conv4 = nn.Conv2d(18,24, kernel_size=5)
    self.fc1 = nn.Linear(3456, 1000)
    self.fc2 = nn.Linear(1000, 6)
    print("init ende")
    
  def forward(self, x):
    x = self.conv1(x)
    x = F.max_pool2d(x,2)
    x = F.relu(x)
    x = self.conv2(x)
    x = F.max_pool2d(x,2)
    x = F.relu(x)
    x = self.conv3(x)
    x = F.max_pool2d(x,2)
    x = F.relu(x)
    x = self.conv4(x)
    x = F.max_pool2d(x,2)
    x = F.relu(x)
    x = x.view(-1, 3456)
    x = F.relu(self.fc1(x))
    x = self.fc2(x)
    return F.sigmoid(x)

print("model=Netz()")
model = Netz()
#model.cuda()

optimizer = optim.Adam(model.parameters(), lr=0.01)
def train(epoch):
  model.train()
  batch_id = 0
  for data, target in train_data:
    data = data#.cuda()
    target = torch.Tensor(target)#.cuda()
    data = Variable(data)
    target = Variable(target)
    optimizer.zero_grad()
    out = model(data)
    criterion = F.binary_cross_entropy
    loss = criterion(out, target)
    loss.backward()
    optimizer.step()
    print('Train Epoch : {} [{}/{} ({..0f}%)]\tLoss: {:.6f}'.format(epoch, batch_id * len(train_data.dataset), 100 * batch_id / len(train_data), loss.data[0]))
    batch_id = batch_id + 1

def test():
  model.eval()
  files = listdir('C:/Users/moehlenkamj/Documents/Studium/Semester 5/Programmierprojekt/Projekt/Bilder/Garbage classification/Garbage classification/train/')
  f = random.choice(files)
  img = Image.open('C:/Users/moehlenkamj/Documents/Studium/Semester 5/Programmierprojekt/Projekt/Bilder/Garbage classification/Garbage classification/train/' + f)
  img_eval_tensor = transforms(img)
  img_eval_tensor.unsqueeze_(0)
  data = Variable(img_eval_tensor)#.cuda())
  out = model(data)
  print(out.data.max(1, keepdim = True) [1])
  img.show()
  x = input('')

for epoch in range(1,30):
  train(epoch)

test()