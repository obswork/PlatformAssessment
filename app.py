import os
from flask import Flask, g, render_template, request
import sqlite3
from werkzeug.utils import secure_filename
import threading
from app_utils import get_engine, create_table, get_uploaded_files, read_upload_file, CWD, UPLOAD_FOLDER, DATABASE
import time


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 3000000

SLEEP_TIME = 5


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/upload')
def render_file_form():
   return render_template('file_submit.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
      return 'file uploaded successfully'


def loader():
    while True:
        try:
            uploaded_files = get_uploaded_files()
            if uploaded_files:
                engine = get_engine()
                with engine.connect() as conn:
                    for file in uploaded_files:
                        read_upload_file(file, conn)
                engine.dispose()
        except:
            pass
        time.sleep(SLEEP_TIME)




if __name__ == '__main__':
    create_table()
    loader_thread = threading.Thread(target=loader, name='file_loader_thread', daemon=True)
    loader_thread.start()
    app.run(debug = True)
