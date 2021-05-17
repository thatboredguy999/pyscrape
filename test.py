from PyPDF2 import PdfFileReader


def text_extractor(path):
	with open(path, 'rb') as f:
		pdf = PdfFileReader(f)
		
		page = pdf.getPage(1)
		print(page)
		text = page.extractText()
		print(text)

if __name__ == '__main__':
	path = 'example.pdf'
	text_extractor(path)
	
