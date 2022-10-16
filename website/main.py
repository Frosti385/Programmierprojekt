"""
Test implementation of a Restful API for Uploading Images
"""
import os
import json
from flask import Flask, render_template, flash, request, redirect
from config import *
from flask_restful import Api
import requests
import torch
import torchvision
from torch.utils.data import Dataset
#import torch.nn as nn
from torch import nn
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
with requests.get(URL) as response:
    open('./models/epoch.93_95.max', 'wb').write(response.content)

app = Flask(__name__)

api =   Api(app)

app.secret_key = APP_KEY

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
                if app.secret_key == user_code and file.mimetype in extensions:
                    global FILENAME
                    FILENAME = os.path.join(upload_dest, file.FILENAME)
                    file.save(os.path.join(upload_dest, file.FILENAME))
                    return redirect('/calc')
            else:    
                print('Wrong passcode')
                return redirect('/upload')
        

@app.route('/calc')
def calculating():

    return render_template('calculating.html')

@app.route('/result', methods=['POST'])
def resultfunction():
    if request.method == 'POST':

        out = ["","","","","",""]
        classes = ['Glas', 'Papier', 'Pappe', 'Plastik', 'Metall', 'Muell']

        model = Net()

        model = torch.load('./models/epoch.93_95.max', map_location='cpu')

        transform = transforms.Compose(
            [transforms.ToPILImage(),
            transforms.Resize((224, 224)),
            transforms.ToTensor()])

        try_image = transform(torchvision.io.read_image(FILENAME))

        model.eval()

        with torch.no_grad():
            inputs = try_image
            inputs = inputs.unsqueeze(0)
            outputs = model(inputs)
            probability = torch.softmax(outputs.data, 1).cpu().numpy()[0]
            print(probability)
            maximum = 0
            for j in range(0,6):
                for i in range(0,6):
                    if probability[i] == max(probability):
                        maximum = i
                        break
                out[j] = (f"Muell auf dem Bild entspricht zu " +
                         "{0:.10f}".format(float(probability[maximum]*100)) + "% dem Typ " + classes[maximum])
                probability[maximum] = 0
            js = {
                    "0" : out[0] ,
                    "1" : out[1],
                    "2" : out[2],
                    "3" : out[3],
                    "4" : out[4],
                    "5" : out[5]
                }

            data = json.dumps(js)
            file = open("./Output.json", "w")
            file.write(data)
            file.close()
            jsonfile = 'Output.json'
            with open(jsonfile,'r') as j:
                data = json.loads(j.read())

            return data

if __name__=='__main__':
    cfg_port = os.getenv('PORT', "5000")

    app.run(host="0.0.0.0", port=cfg_port)
