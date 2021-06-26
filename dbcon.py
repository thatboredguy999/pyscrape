import psycopg2
import os

name = 'hold.txt'

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

if __name__ == '__main__':
	insert_data(name)
	
