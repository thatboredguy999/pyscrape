import psycopg2, tempfile, subprocess
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


def insert_data(name):

        sql = """INSERT INTO new(PhyDate, Code, ProdDate, FSPrice)
                VALUES(%s);"""
        filename, file_extension = os.path.splitext(name)
        command =('CREATE TABLE {tab} (PhyDate, Code, ProdDate, FSPrice)')


        conn = psycopg2.connect(
                host="localhost",
                database="sample",
                user="postgres",
                password="root")
        cur = conn.cursor()
        cur.execute('''DROP TABLE IF EXISTS "{tab}";'''.format(tab=filename))
        cur.execute('''CREATE TABLE "{tab}" (PhyDate char(50) PRIMARY KEY, Code char(50) SECONDARY KEY, ProdDate char(50) SECONDARY KEY, FSPrice char(50) NOT NULL);'''.format(tab=filename))
        with open(name , 'r') as f:

                #print('PostgreSQL database version:')
                cur.copy_from(f, filename, sep=' ')
        conn.commit()
        cur.close()
        if conn is not None:
                conn.close()
                print('Database connection close.')


def filelayout(filename):
        newfile=filename.strip('.pdf')
        newfile2=newfile
        add_string='.txt'
        newfile = "".join((newfile, add_string))
        filepath='uploads/{}'.format(filename)
#        subprocess.call(["pdftotext", "-layout", filename, 'data.txt'])
        out, err = subprocess.Popen(["pdftotext", "-layout", filepath, 'data.txt']).communicate()
        addstring='_.txt'
        newfile2="".join((newfile2, addstring))

        with open('data.txt','r') as file, open(newfile2,'w') as destination:
                check=False
                count=0
                counton=False
                hold= ' '
                test=True
                broken=False
                for line in file:
                        for word in line.split():
                                if word == 'H':
                                        check=True
                                        counton=True
                                        destination.write('6/25/2021 '+ word+ ' ')
                                        print(word)
                                elif count==2:
                                        hold=word


                                elif check==True :
                                        check=False
                                        destination.write(word + ' ')
                                        print(word)
                                elif count==5 :
                                        if ',' in word:
                                                broken=True

                                elif count==6 :
                                        if '0' in word:
                                                broken=True

                                        if broken==True:
                                                counton=False
                                                count=0
                                                destination.write(hold + '\n')
                                                print(hold)
                                                broken=False
                                        else:
                                                print(word)
                                                destination.write(word + '\n')
                                                counton=False
                                                count=0
                                if counton==True:
                                        count +=1






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

        filelayout(filename)
        return redirect(url_for('index'))




if __name__=="__main__":
	app.run(host='0.0.0.0', port=5000)
