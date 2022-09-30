"""
Test implementation of a Restful API for Uploading Images 
"""
import os
from flask import Flask, render_template
from flask_restful import Api, Resource

app = Flask(__name__)

api =   Api(app)

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

api.add_resource(HelloWorld,'/hello')

@app.route('/upload')
def upload_form():
    return render_template('upload.html')

if __name__=='__main__':
    cfg_port = os.getenv('PORT', "5000")


    app.run(host="0.0.0.0", port=cfg_port)#, debug=True)
    #Test