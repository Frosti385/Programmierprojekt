"""
Test implementation of a Restful API for Uploading Images 
"""
import os
from github import Github
from flask import Flask, render_template, flash, request, redirect
from config import *
from flask_restful import Api, Resource

import torch
import torchvision
from torch.utils.data import Dataset
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import transforms


app = Flask(__name__)

api =   Api(app)

github = Github('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')
repository = github.get_user().get_repo('GithubTestProject2')


class HelloWorld(Resource):
    """
    Test API Endpoint
    """
    def get(self):
        """
        Getter for hello world
        """

        data={"data": "Hi there, Programming Project!"}

        return data

api.add_resource(HelloWorld,'/')

@app.route('/upload')
def upload_form():
    return render_template('upload.php')


class TrashDataset(Dataset):

                    def __init__(self, images):                      
                        self.images = images

                    transform = transforms.Compose(
                        [transforms.ToPILImage(),
                        transforms.Resize((224, 224)),
                        transforms.ToTensor()])

                    def __getitem__(self):
                        return self.transform(self.images)


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
               filename = 'tensor.txt'  
               #data = TrashDataset(images=file)
               #torch.save(data, 'tensor.txt' )
               #data2 = open('tensor.txt', 'r')
               #content = data2.read()
               #torch.save(data, 'tensor.txt')
               file.save(os.path.join(upload_dest, file.filename))
               #content = '{\"name\":\"beppe\",\"city\":\"amsterdam\"}'
               #filename = 'file.json'
               #f = repository.create_file(filename, "Test Commit", data2)

        #flash('Files uploaded')
        return redirect('/upload')


if __name__=='__main__':
    cfg_port = os.getenv('PORT', "5000")


    app.run(host="0.0.0.0", port=cfg_port)#, debug=True)
    #Test