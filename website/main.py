"""
Test implementation of a Restful API for Uploading Images 
"""
import os
from flask import Flask, render_template, flash, request, redirect
from config import *
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

api.add_resource(HelloWorld,'/')

@app.route('/upload')
def upload_form():
    return render_template('upload.php')


## on a POST request of data 
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        ### Auth
        user_code = str(request.form.get('psw'))
        
        # Open database
        #conn = sqlite3.connect(db_loc)
        #cursor = conn.cursor()
        #cursor.execute("PRAGMA key='%s'"%app_key)
        
        # Run sql query
        #cursor.execute('select * from upload where uploadcode="%s"'%user_code)
        #result = cursor.fetchall() 
        
        # close as we are done with it
        #conn.close()

        #if len(result)==0: 
        #    # If we do not get a match, send a message
        #    flash('Not a valid Code')
        #    return redirect(request.url)
        

        if 'files[]' not in request.files:
            flash('No files found, try again.')
            return redirect(request.url)

        files = request.files.getlist('files[]')
        print(files)
        print(upload_dest)  
        for file in files:
            if file:              
               file.save(os.path.join(upload_dest, file.filename))

        #flash('Files uploaded')
        return redirect('/upload')


if __name__=='__main__':
    cfg_port = os.getenv('PORT', "5000")


    app.run(host="0.0.0.0", port=cfg_port)#, debug=True)
    #Test