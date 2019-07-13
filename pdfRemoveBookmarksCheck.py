from PyPDF2 import PdfFileReader as pdrd 
from PyPDF2 import PdfFileWriter as pdwt 

pdf_path='D:/逻辑的引擎.pdf'
rd=pdrd(pdf_path)
page_cnt=rd.getNumPages()

wt=pdwt()

pages=[]
for i in range(0,page_cnt):
    pages.append(rd.getPage(i))
for page in pages:
    wt.addPage(page)

pdf_out_fd=open(pdf_path.split('.pdf')[0]+'_普本.pdf','wb')
wt.write(pdf_out_fd)


