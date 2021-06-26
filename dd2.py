import os, tempfile, subprocess

def filelayout():
	out, err = subprocess.Popen(["pdftotext", "-layout", 'H_2021_06_22.pdf','H_2021_06_22.txt']).communicate()


with open('data2.txt','r') as file, open('hold.txt','w') as destination:
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
if __name__=='__main__':
	filelayout()
				
