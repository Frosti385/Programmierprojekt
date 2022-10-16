'''
Global arguments
'''
import os

# maximum filesize in megabytes
#file_mb_max = 100
# encryption key
APP_KEY = '148'
# full path destination for our upload files
upload_dest = os.path.join(os.getcwd(), 'uploads') #os.getcwd() #
# list of allowed allowed extensions
extensions = set(['image/jpg', 'image/jpeg'])
