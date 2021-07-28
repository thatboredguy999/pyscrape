import psycopg2, tempfile, subprocess, requests
from flask import Flask, json, jsonify, Response
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
        command =('CREATE TABLE {tab} (PhyDate, Code, ProdDate, FSPrice,PrKey)')


        conn = psycopg2.connect(
                host="localhost",
                database="sample",
                user="postgres",
                password="root")
        cur = conn.cursor()
       # cur.execute('''DROP TABLE IF EXISTS "{tab}";'''.format(tab=filename))
       # cur.execute('''CREATE TABLE "{tab}" (PhyDate char(50), Code char(50), ProdDate char(50), FSPrice char(50) NOT NULL, PrKey char(50) PRIMARY KEY);'''.format(tab=filename))
        tablename='FSPrice'
        with open(name , 'r') as f:

                #print('PostgreSQL database version:')
                cur.copy_from(f, tablename, sep=' ')
        conn.commit()
        cur.close()
        if conn is not None:
                conn.close()
                print('Database connection close.')





def query_data(querylist):
	os.remove("hold_query.txt")
	conn = psycopg2.connect(
		host="localhost",
		database="sample",
		user="postgres",
		password="root")
	cur = conn.cursor()
	length1=len(querylist)
	i=0

	f = open("hold_query.txt","a")
	while i < length1:
		cur.execute('''SELECT FSPrice FROM "FSPrice" WHERE PrKey= '{tab}';'''.format(tab=(querylist[i])))
		temp = cur.fetchone()
		temp = str(temp)
		if temp != "None":
			f.write(querylist[i])
			f.write(temp)
			f.write("\n")
		i+=1
		print(temp)
	f1 = open("hold_query.txt","r")
	conn.commit()
	cur.close()
	return


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
                
                filename=filename.strip('.pdf')
                primkey=filename
                primhold=filename
                filename=filename.strip('H_')
                filename=filename.replace('_', '/')
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
                                        destination.write(filename +' '+ word+ ' ')
                                        print(word)
                                elif count==2:
                                        hold=word


                                elif check==True :
                                        check=False
                                        hold="_"
                                        primkey="".join((primkey,hold,word))
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
                                                destination.write(hold + ' '+primkey+'\n')
                                                primkey=primhold
                                                print(hold)
                                                broken=False
                                        else:
                                                print(word)
                                                destination.write(word +' '+primkey+ '\n')
                                                primkey=primhold
                                                counton=False
                                                count=0
                                if counton==True:
                                        count +=1
        conn = psycopg2.connect(
               host='localhost',
               database='sample',
               user='postgres',
               password='root')
        curr = conn.cursor()
        curr.execute('''SELECT FSPrice FROM "FSPrice" WHERE PhyDate = '{tab}';'''.format(tab=(filename)))
        temp1 = curr.fetchone()
        if temp1 != None:
             curr.execute('''DELETE FROM "FSPrice" WHERE PhyDate = '{tab}';'''.format(tab=(filename)))
        conn.commit()
        curr.close()

        insert_data(newfile2)




@app.route('/')
def index():
	return render_template('index.html')




@app.route('/upload')
def upload():
	return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
 #       uploaded_file = flask.request.files.getlist['PDF_file[]']
#        print (uploaded_file)
       for f in request.files.getlist('PDF_file[]'): 
          filename = secure_filename(f.filename)
          if f.filename != '':
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in app.config['UPLOAD_EXTENSIONS']: # file_ext != validate_image(uploaded_file.stream):
                       abort(400)
                f.save(os.path.join(app.config['UPLOAD_PATH'],filename))

          filelayout(filename)
       return redirect(url_for('index'))

@app.route('/queries')
def queries():
	return render_template('queries.html')

@app.route('/queries', methods=['POST'])
def get_queries():
	
	startrun = request.form.get('InfoType',None)
	StartYear = request.form.get('StartYear',None)
	StartMonth = request.form.get('StartMonth',None)
	StartDay = request.form.get('StartDay',None)
	MonthYear = request.form.get('MonthYear',None)
	EndMonth = request.form.get('EndMonth',None)
	EndDay = request.form.get('EndDay',None)
	EndYear = request.form.get('EndYear',None)
	test1=int(StartDay)
	test2=int(StartMonth)
	
	if test1<= 9:
		StartDay=int(StartDay)
		StartDay=str(StartDay)
		StartDay="".join(("0",StartDay))

	if test2<=9:
		StartMonth=int(StartMonth)
		StartMonth=str(StartMonth)
		StartMonth="".join(("0",StartMonth))

	test12=int(EndDay)
	test22=int(EndMonth)

	if test12<=9:
		EndDay=int(EndDay)
		EndDay=str(EndDay)
		EndDay="".join(("0",EndDay))
	if test22<=9:
		EndMonth=int(EndMonth)
		EndMonth=str(EndMonth)
		EndMonth="".join(("0",EndMonth))


	print(startrun)
	fill = "_"
	startrun="".join((startrun, fill))
	startrun="".join((startrun, StartYear))
	startrun="".join((startrun, fill))
	startrun="".join((startrun, StartMonth))
	startrun="".join((startrun, fill))
	startrun="".join((startrun, StartDay))
	startrun="".join((startrun, fill))
	startrun="".join((startrun, MonthYear))
	querylist=[]
	querylist.append(startrun)

	endrun = request.form.get('InfoType')
	endrun= endrun + fill+ EndYear+ fill+ EndMonth+fill+EndDay+fill+MonthYear
	#	endrun="".join((startrun, fill))
	#	endrun="".join((startrun, EndYear))
	#	endrun="".join((startrun, fill))
	#	endrun="".join((startrun, EndMonth))
	#	endrun="".join((startrun, fill))
	#	endrun="".join((startrun, EndDay))
	#	endrun="".join((startrun, fill))
	#	endrun="".join((startrun, MonthYear))
	
	month=int(StartMonth)
	day=int(StartDay)
	year=int(StartYear)
	stopMonth=int(EndMonth)
	stopDay=int(EndDay)
	stopYear=int(EndYear)

	hold=startrun
	print (startrun)
	print (endrun)
	while hold != endrun:

		if day < 32:
			Pkey = request.form.get('InfoType')
			day +=1
			if day <10:
				hday='0'+str(day)
			else:
				hday=str(day)
			if month <10:
				hmonth='0'+str(month)
			else:
				hmonth=str(month)
			Pkey=Pkey + fill + str(year)+ fill + hmonth + fill + hday + fill + str (MonthYear)
			#print (Pkey)
			#print (startrun)
			querylist.append(Pkey)
			hold=Pkey
		else: 
			day = 1
			month +=1
			if month == 13:
				month = 1
				year +=1

	query_data(querylist)
	f = open("hold_query.txt","r")
	return render_template('content.html',text=f.read()) 
#	return (querylist)


@app.route('/excel_queries', methods=['GET'])
def excel_queries():

        startrun = request.args.get('InfoType')
        StartYear = request.args.get('StartYear')
        StartMonth = request.args.get('StartMonth')
        StartDay = request.args.get('StartDay')
        MonthYear = request.args.get('MonthYear')
        EndMonth = request.args.get('EndMonth')
        EndDay = request.args.get('EndDay')
        EndYear = request.args.get('EndYear')

        print(startrun)
        fill = "_"
        print(startrun)
        startrun="".join((startrun, fill))
        print(StartYear)
        startrun="".join((startrun, StartYear))
        startrun="".join((startrun, fill))
        startrun="".join((startrun, StartMonth))
        startrun="".join((startrun, fill))
        startrun="".join((startrun, StartDay))
        startrun="".join((startrun, fill))
        startrun="".join((startrun, MonthYear))
        querylist=[]
        querylist.append(startrun)

        endrun = InfoType
        endrun= startrun + fill+ EndYear+ fill+ EndMonth+fill+EndDay+fill+MonthYear
        month=int(StartMonth)
        day=int(StartDay)
        year=int(StartYear)
        stopMonth=int(EndMonth)
        stopDay=int(EndDay)
        stopYear=int(EndYear)

        hold=startrun
        print (startrun)
        print (endrun)
        while hold != endrun:

                if day < 32:
                        Pkey = request.form.get('InfoType')
                        day +=1
                        if day <10:
                                hday='0'+str(day)
                        else:
                                hday=str(day)
                        if month <10:
                                hmonth='0'+str(month)
                        else:
                                hmonth=str(month)
                        Pkey=Pkey + fill + str(year)+ fill + hmonth + fill + hday + fill + str (MonthYear)
                        #print (Pkey)
                        #print (startrun)
                        querylist.append(Pkey)
                        hold=Pkey
                else:
                        day = 1
                        month +=1
                        if month == 13:
                                month = 1
                                year +=1

        query_data(querylist)
        f = open("hold_query.txt","r")
        return render_template('content.html',text=f.read())


if __name__=="__main__":
	app.run(host='0.0.0.0', port=5000)
