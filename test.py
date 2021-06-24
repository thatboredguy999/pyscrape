from PyPDF2 import PdfFileReader


def text_extractor(path):
	with open(path, 'rb') as f:
		myText = open(r'blank.csv','w')
		pdf = PdfFileReader(f)
		numPage = pdf.getNumPages()
		count = 0
		
		for x in range (count,numPage):
			page = pdf.getPage(count)
			print(page)
			text = page.extractText()
			count +=1
			myText.write(text)
			print(text)
		myText.close()

if __name__ == '__main__':
	path = 'H_2021_06_22.pdf'
	text_extractor(path)
	
