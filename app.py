
import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import imghdr

app = Flask(__name__)


app.config['UPLOAD_EXTENSIONS']=['.pdf']
app.config['UPLOAD_PATH'] = 'uploads'

def validate_image(stream):
	header = stream.read(512)
	stream.seek(0)
	format = imghdr.what(None, header)
	if not format:
		return None
	return '.' + (format)


@app.route('/')
def index():
	return render_template('index.html')




@app.route('/upload')
def upload():
	return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
        uploaded_file = request.files['PDF_file']
        filename = secure_filename(uploaded_file.filename)
        if uploaded_file.filename != '':
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in app.config['UPLOAD_EXTENSIONS']: # file_ext != validate_image(uploaded_file.stream):
                       abort(400)
                uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'],filename))
        return redirect(url_for('index'))




if __name__=="__main__":
	app.run(host='0.0.0.0', port=5000)
