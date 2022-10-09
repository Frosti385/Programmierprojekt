'''
Global arguments
'''
import os 

# maximum filesize in megabytes
file_mb_max = 100
# encryption key
app_key = '148Programmierprojekt'
# full path destination for our upload files
upload_dest = os.path.join(os.getcwd(), 'uploads') #os.getcwd() #
# list of allowed allowed extensions
extensions = set(['txt', 'pdf', 'png', 'tiff','gtiff'])