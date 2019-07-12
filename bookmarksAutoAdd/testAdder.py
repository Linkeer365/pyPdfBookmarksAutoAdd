# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import PyPDF2 # 注意, import是区分大小写的
# import codecs

def testPacksGenerate(max_index):
    names_pool=['晚安','左右田右卫门左卫门'] # 唯一因变量
    indices_pool=random.sample(range(1,max_index),len(names_pool)) # sample can pass on rangeType, index must be integer
    packs=list(zip(names_pool,indices_pool))
    packs_str='\n'.join([name+' '*1+str(index) for name,index in packs])
    with open('D:/testOCR.txt','a',encoding='utf-8') as f:
        f.write(packs_str)
    print('书签测试文件已生成!')
    return packs

out_pdfWriter=PyPDF2.PdfFileWriter()
infile_path='D:/bc.pdf'
infile_fd=open(infile_path,'rb')
in_pdfReader=PyPDF2.PdfFileReader(infile_fd)
# print(in_pdfReader.isEncrypted)
pagecnt=in_pdfReader.numPages
print(pagecnt)
# infile_fd=codecs.open(infile_path,'rb')
# in_pdfReader=PyPDF2.PdfFileReader(infile_fd)
# page_cnt=in_pdfReader.getNumPages()

# out_pdfWriter.cloneDocumentFromReader(in_pdfReader) # 所有的return都是空白页面, 操你妈!

# 这里自己写一个clone的函数
pages=[]
for pageNum in range(0,pagecnt):
    pages.append(in_pdfReader.getPage(pageNum))
print(pages)
testpack=testPacksGenerate(3)
# out_pdfWriter=PyPDF2.PdfFileWriter()
print('testpack is',testpack)

for page in pages:
    out_pdfWriter.addPage(page)
for name,index in testpack:
    print('Name:{};\tInd:{}'.format(name,index))
    out_pdfWriter.addBookmark(name,index)
print('完成writer创建!')
# infile_fd.close()
output=open('D:/bs.pdf','wb')
out_pdfWriter.write(output)
# output.close()
# infile_fd.close()



print('书签添加完成, 现在创建新的pdf文件!')
# outfile_path=infile_path.replace('.pdf','_完成OCR.pdf')
# with open(outfile_path,'wb') as f:
#     f.write(out_pdfWriter)

print('创建完成!')
output.close()
infile_fd.close()


# testTxtGenerate(4)
