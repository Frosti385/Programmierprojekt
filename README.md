# Programmierprojekt

HS Osnabrück - 5 Semester - Assessment for the module Programming Project

## Project description

The purpose of this project is to classify six caterogies of trash. The categories are cardboard, paper, glass, plastic and trash. 
To classify a picture of trash( only JPGs are allowed) uploaded via the website / API Endpoint a neural network is used. This neural network is based on resnet-152 a free to use pretrained neural network, which is used to preclassify the given image. Afterwards a much smaller network maps the result of the first network of the six trash categories and gives a prediction of the type of trash the picture displays.
Thanks to the pretrained network and tuning of this and the mapping network an accuracy of 95% (95,6%) is reached.

## Project Management

The project is implemented in three sprints. Management is carried out via Jira.
TODO: Put link here

## Access via Frontend

The frontend of this application is available via
TODO

## Deployment

The API is deployed via a CI/CD pipeline using github actions. With the deployment of new changes the main python file is tested and afterwards pushed to the server 

Both the linting and code validity is checked before doing so.

Only after the build step is completed the deploy step begins

The three relevant enpoints are as follows:

TODO implement endpoint descriptions
### This index html file

URL to index

### Upload page

URL to upload


## How to use
(The token is given separately)

1. git clone https://github-token@github.com/Frosti385/Programmierprojekt.git
1. pip install virtualenv
1. python -m venv env
1. .\evn\Scripts\activate
1. pip3 install -r .\requirements.txt

### Run API

1. python .\main.py

When the API starts, the pretrained network(resnet-152) and the trained epoch (model) with the accuracy of 95% are downloaded. The model is downloaded via web request (python package "requests") from the netcase server of the Hochschule Osnabrück because the file is to big for Github.

### Classify a picture
(The passcode is given separately)

1. Call the website (under the given URL on the server or if your are running the script locally under localhost:5000)
1. In the upload mask you need to type in the passcode to be able to upload a file
1. After selecting a JPG file of trash click the "Submit"- Button
1. You will be redirected to a loading page. 
1. After the process of predicting is finished the type of trash shown on the picture you will be redirected to the resultpage and your result is displayed



