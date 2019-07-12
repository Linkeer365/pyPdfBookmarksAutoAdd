import pdf2image #去死吧, 浪费了我整整4个小时的时间没配出来!!
# import pdf2jpg.pdf2jpg as p2j
# fitz也是狗屎!! 根本配置不出来!!
import pytesseract
from PIL import Image as PI
import shutil
import io
import os
import random
from PyPDF2 import PdfFileReader,PdfFileWriter
import re
import ghostscript
from PythonMagick import Image as PMI
# import fitz


cnt=2
title='无书签_逻辑的引擎_{}'.format(cnt)
pdf_path='D:\备份地点\文档资料备份地点\cmBooks\数据库\无书签_逻辑的引擎.pdf'
outputDir='D:/pdfImg_{}'.format(title)

# 确保outputdir是空文件夹
if not os.path.exists(outputDir):
    os.mkdir(outputDir)
# else:
#     if os.listdir(outputDir):
#         shutil.rmtree(outputDir)
#         os.mkdir(outputDir)

# 得到目录起始页和终止页

prompt_start,prompt_end='目录起始页:','目录终止页:'
prelog_startIdx,prelog_endIdx=int(input(prompt_start)),int(input(prompt_end))

# 取出这几页目录, 生成新文件

rd=PdfFileReader(open(pdf_path,'rb')) # pdfilereader -> rd
page_cnt=rd.getNumPages()
wt=PdfFileWriter()
for prelogue_pageIdx in range(prelog_startIdx,prelog_endIdx+1): # prelog_idx 是和pdf上面显示的页码对应的
    page_obj=rd.getPage(prelogue_pageIdx-1) # getpage时候, 从零算起, 故真实页码-1
    wt.addPage(page_obj)
prelog_path=outputDir+'\\'+'目录集合.pdf'
output_fd=open(prelog_path,'wb') # fd 指的是一个句柄, 传给wt去写入
wt.write(output_fd)
output_fd.close() ## 这一行值1亿美元!!

print('生成所有目录!')

print('目录地址:{}; 目标地址:{}'.format(prelog_path,outputDir))

# save pics
print('pdf->image,转换中...')

# for idx in range(page_cnt):
#     os.chdir(outputDir)
#     PMI_rd=PMI()
#     # PMI_obj.density('600')
#     PMI_rd.read(prelog_path)
#     size='{}x{}'.format(PMI_rd.columns(),PMI_rd.rows())
#     PMI_wt=PMI(size)
#     PMI_wt.magick('JPG')
#     PMI_wt.write(prelog_path.replace('.pdf','.jpg'))
# print('canoni1!!')

# cnt=46
# prelog_dir=prelog_path
# 下面这行花了我5个小时!!! 操你妈!!
images=pdf2image.convert_from_path(prelog_path,dpi=800,output_folder=outputDir,fmt='jpg',thread_count=4)
# images=p2j.convert_pdf2jpg(inputpath=prelog_path,outputpath='D:/op',dpi=300)
# images=fitz.utils.
print('pdf->image,转换完成!')
# print('Images:',images)
# for idx,img in enumerate(images):
#     img.save(os.path.join(outputDir,'page_{}.jpg'.format(idx)))

# 生成文本的目录页
prelogue=[]
os.chdir(outputDir)
for each in os.listdir(outputDir):
    if each.endswith('.jpg'):
        pi_obj=PI.open(outputDir+os.sep+each)
        # psm 的参数很重要，表示 tesseract 识别图像的方式，比如说是一行一行识别还是逐字识别。希望逐字识别可以使用 -psm 10, 逐行是6
        ocr_page=pytesseract.image_to_string(pi_obj,lang='eng') # 之所以使用英文OCR, 相当于直接排除了中文的干扰, 这是不得已的办法!
        print('解析一张目录!')
        with open('{}_ocr.txt'.format(each.replace('.jpg','')[-1]),'w',encoding='utf-8') as f:
            f.write(ocr_page)
print('所有目录完成解析!')

# 检查目录页OCR质量, 如果每一行最后几位数中不是isdigit就不行
max_idx_len=len(str(page_cnt))
print('这本书一共有{}页,因此每页idx不超过{}位数!'.format(page_cnt,max_idx_len))
lineCnts_indices=[]

line_cnt=0 # line_cnt 要放在外面, 因为整个文件夹下面不管多少个txt都是一本书, 一本书的line_cnt会一直持续计数!
for each in os.listdir(outputDir):
    if each.endswith('.txt'):
        with open(each,'r') as f:
            for eachline in f.readlines(): # readlines() 返回每一行组成的列表
                if eachline: # 空行直接无视!
                    line_cnt += 1
                    tails=eachline.strip()[-max_idx_len:].strip()
                    if tails.isdigit():
                        lineCnts_indices.append((line_cnt, tails))
                    else:
                        checking_prompt='末尾是{}, 请核实是否是正常现象,键入y或其余任意字符'.format(tails)
                        if input(checking_prompt)=='y':
                            lineCnts_indices.append((line_cnt,''.join(re.findall(r'\d',tails)))) # 注意, /w会匹配到数字!! 这个注意一下不要想当然!!
                        else:
                            lineCnts_indices.append((line_cnt,'Invalid'))
# 看下这个所谓的一览表!
# print('得到目录一览表了! 列表如下!')
# for line,idx in lineCnts_indices:
#     print('{}\t->\t{}'.format(line,idx))
lineCnts_indices=dict(lineCnts_indices) # 这个不用试了, 直接在shell里写一个a=[(1,2),(3,4)] -> dict(a)
# print(lineCnts_indices)

# 注意, 到这之前的idx也全是字符串!


# 一级校验, 测试出Invalid分子

for lineCnt in lineCnts_indices.keys():
    if lineCnts_indices[lineCnt]=='Invalid':
        prompt_writeInCorrIndex='第{}个未能正确OCR, 请手动输入:'.format(lineCnt)
        while True:
            idxInput=input(prompt_writeInCorrIndex)
            if idxInput.isdigit():
                corrIdx=idxInput
                print('第{}个写入目录{}'.format(lineCnt,corrIdx))
                lineCnts_indices[lineCnt]=corrIdx
                break
            else:
                print('输入有误,请重新输入')
                continue

## 测试一级校验是否成功

# for each in lineCnts_indices.values():
#     if not each.isdigit():
#         print('去除Invalid未成功! 余孽是{}'.format(each))


# 二级校验, 测试出哪些错误的数字
## 打印一览表

print('二级校验现在开始, 以下是当前的目录一览图, 请比对书中的具体目录')
for lineCnt,index in lineCnts_indices.items():
    print('{}\t->\t{}'.format(lineCnt,index))

prompt_modifyOrneglect='请输入行号与对应目录, 用问号分隔开:\t没问题请键入ok'

while True:
    choice=input(prompt_modifyOrneglect)
    if choice=='ok':
        print('完整版目录一览表已成功生成')
    else:
        newLineCnt,newIdx=choice.split('?')
        if newLineCnt.isdigit() and newIdx.isdigit():
            print('已检测, 输入全部是数字.')
            if not newLineCnt in lineCnts_indices:
                print('行号过大/过小, 请检查!')
                continue
            elif int(newIdx)>int(page_cnt) or int(newIdx)<0:
                print('别想用边界搞我, 我不帮你们擦屁股!')
                continue
            else:
                lineCnts_indices[newLineCnt]=newIdx
                print('修改产生!第{}行变成{}'.format(newLineCnt,newIdx))
                continue
        else:
            print('输入有误, 请重输!')
            continue

final_prelog_dict=lineCnts_indices

print('Perfect prelog is completed.')

















