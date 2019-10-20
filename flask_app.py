import os
from flask import Flask, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename

# from huffman_coding import *
from huffman_encoding import HuffmanCoding

app = Flask(__name__)

app.config['FILE_UPLOADS'] = 'static/uploads'
# Allowed file extensions
app.config['ALLOWED_FILE_EXTENSIONS'] = ['TXT', 'PNG', 'JPG', 'JPEG', 'PDF']

def allowed_extensions(filename):
    '''
    Function that checks wether the file upload is one of the allowed ones.
    '''
    if not '.' in filename:
        return False
    
    ext = filename.rsplit('.', 1)[1]

    if ext.upper() in app.config['ALLOWED_FILE_EXTENSIONS']:
        return True
    else:
        return False


@app.route("/", methods=['GET', 'POST'])
def home(): 
    '''Returns the home page with the file upload form'''

    if request.method == 'POST':
        if request.files:
            # store file 
            file_upload = request.files['file-upload']

            if file_upload.filename == '':
                print("must have a filename")
                return redirect(request.url)

            if not allowed_extensions(file_upload.filename):
                print("Not supported file extension")  
            
            else:
                filename = secure_filename(file_upload.filename)
        
                file_upload.save(os.path.join(app.config['FILE_UPLOADS'], filename))
            
            print('file saved') 

           # render compress page after successfully uploading a file
            return render_template('compress_file.html', file_upload=file_upload)

    
    return render_template('index.html') 

if __name__ == '__main__': 
    app.run(debug=True)
