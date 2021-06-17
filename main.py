

import os
from summarizer import Summarizer
import email
import pandas as pd

# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import Flask, render_template, request, redirect, url_for, send_from_directory


# from werkzeug import secure_filename

# Initialize the Flask application
app = Flask(__name__)

# This is the path to the upload directory
# app.config['UPLOAD_FOLDER'] = 'uploads/'
# # These are the extension that we are accepting to be uploaded
# app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# # For a given file, return whether it's an allowed type or not
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return render_template('index.html')


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded files
    uploaded_files = request.files.getlist("file[]")
    print('&&&&&&',uploaded_files)
    filenames = []
    def Convert(tup, di):
        di = dict(tup)
        return di


    d={}
    for file in uploaded_files:
        # print('***************',file)
        text=file.read()
        text=text.decode('utf-8')
        email_decoded=email.message_from_string(text)
        e_dict={}
        dict_email=Convert(email_decoded._headers, e_dict)
        orig_text=email_decoded._payload
        orig_text=orig_text.replace('\r','')
        orig_text=orig_text.replace('\n','')
        print(orig_text)
        dict_email['original_text']=orig_text
        
        # d[file]=dict_email
        
        
        
        # print('******',text)
        model = Summarizer()
        result = model(email_decoded._payload,ratio=0.7)
        print("***********",result)# Specified with ratio
        result=result.replace('\r','')
        result=result.replace('\n','')
        dict_email['Summary']=result
        d[file]=dict_email
        
    df_final=pd.DataFrame.from_dict(d,orient='index')
    df_final=df_final.reset_index(drop=True)

    print(df_final)
        
        
        
        # Check if the file is one of the allowed types/extensions
        
            # Make the filename safe, remove unsupported chars
            
            # Move the file form the temporal folder to the upload
            # folder we setup
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Save the filename into a list, we'll use it later
            # filenames.append(filename)
            
            # Redirect the user to the uploaded_file route, which
            # will basicaly show on the browser the uploaded file
    # Load an html page with a link to each uploaded file
    return render_template('upload.html',  tables=[df_final.to_html(classes='data', header="true")])
# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)

if __name__ == '__main__':
    app.run(debug=False)
