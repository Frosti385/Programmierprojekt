"""
Test implementation of a Restful API for Uploading Images 
"""
import os
from flask import Flask, render_template, flash, request, redirect
from config import *
from flask_restful import Api, Resource
import requests 

import torch
import torchvision
from torch.utils.data import Dataset
import torch.nn as nn
from torchvision import transforms

class TrashDataset(Dataset):

            def __init__(self, images, targets):
                self.targets = targets
                self.images = images

            def __len__(self):
                return len(self.targets)

            transform = transforms.Compose(
                [transforms.ToPILImage(),
                transforms.Resize((224, 224)),
                transforms.ToTensor()])

            def __getitem__(self, index):
                return self.targets[index], self.transform(self.images[index])

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.network = torchvision.models.resnet152(pretrained=True)
        self.fc1 = nn.Linear(1000, 6)
    def forward(self, x):
        x = self.network(x)
        x = self.fc1(x)
        return x

model = Net()

URL = "https://netcase.hs-osnabrueck.de/index.php/s/hhmg0Df8GrrNlLo/download"
response = requests.get(URL)
open('./models/epoch.93_95.max', 'wb').write(response.content)

app = Flask(__name__)

api =   Api(app)

app.secret_key = app_key

@app.route('/')
def index_form():
    return render_template('index.html')

@app.route('/upload')
def upload_form():
    return render_template('upload.html')

## on a POST request of data 
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        ### Auth
        user_code = str(request.form.get('psw'))

        if 'files[]' not in request.files:
            flash('No files found, try again.')
            return redirect(request.url)

        files = request.files.getlist('files[]')
        print('Testprint')

        for file in files:
            if file:   
                if(app.secret_key == user_code):
                    global filename
                    filename = os.path.join(upload_dest, file.filename)
                    file.save(os.path.join(upload_dest, file.filename))
                    return redirect('/calculating')
                else:
                    print('Wrong passcode')
                    return redirect('/upload')
        return "false"

@app.route('/calculating')
def calculating():

    return render_template('calculating.html') #redirect('/upload')

@app.route('/result', methods=['POST'])
def resultfunction():
    if request.method == 'POST':

       
       

       
        classes = ['Glas', 'Papier', 'Pappe', 'Plastik', 'Metall', 'Müll']
        
        
        model = torch.load('./models/epoch.93_95.max', map_location='cpu')
       
        
        transform = transforms.Compose(
            [transforms.ToPILImage(),
            transforms.Resize((224, 224)),
            transforms.ToTensor()])


        try_image = transform(torchvision.io.read_image(filename))

        model.eval()
        with torch.no_grad():
            inputs = try_image
            inputs = inputs.cuda()
            inputs = inputs.unsqueeze(0)
            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            print("Müll auf dem Bild entspricht dem Typ " + classes[predicted])


if __name__=='__main__':
    cfg_port = os.getenv('PORT', "5000")

    app.run(host="0.0.0.0", port=cfg_port)