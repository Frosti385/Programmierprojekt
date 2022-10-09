"""
Test implementation of a Restful API for Uploading Images 
"""
import os
from flask import Flask, render_template, flash, request, redirect
from config import *
from flask_restful import Api, Resource


app = Flask(__name__)

api =   Api(app)

#github = Github('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')
#repository = github.get_user().get_repo('GithubTestProject2')

app.secret_key = app_key

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
    return render_template('upload.html')


class result(Resource):
    """
    Test API Endpoint
    """
    def get(self):
        """
        Getter for hello world
        """

        data= os.path.join(os.getcwd(), '/uploads') 

        return data

api.add_resource(result,'/result')



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
                    file.save(os.path.join(upload_dest, file.filename))
                    return redirect('/calculating')
                else:
                    print('Wrong passcode')
                    return redirect('/upload')
        #flash('Files uploaded')
        

        return "false"
         # hier wird gerendert dann und unten wird dann die Methode zur berechnung aufgerufen   BULLSHIT


@app.route('/calculating')
def calculating():

    return render_template('calculating.html') #redirect('/upload')


@app.route('/result', methods=['POST'])
def resultfunction():
    if request.method == 'POST':
        for i in range(500000):
            print(i)

    return "Test" #redirect('/upload')

if __name__=='__main__':
    cfg_port = os.getenv('PORT', "5000")


    app.run(host="0.0.0.0", port=cfg_port)#, debug=True)
    #Test