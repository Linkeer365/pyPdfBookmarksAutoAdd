import requests
from lxml import etree
from selenium import webdriver,common
import sys
import os
import PyPDF2
import re
ua={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

while True:
    pdfs_tochoose=[]
    for each in os.listdir('.'):
        if each.endswith('.pdf'):
            pdfs_tochoose.append(each)
    for idx,pdf in enumerate(pdfs_tochoose,1):
        print('第{}本书\t->{}'.format(idx,pdf))
    prompt='请输入你想要第几本书:'
    input_pdfChoose=input(prompt)
    if not input_pdfChoose.isdigit():
        continue
    else:
        pdf_title=pdfs_tochoose[int(input_pdfChoose)-1].replace('.pdf','')
    # raw_input='大冰'
    # fake_ip='116.208.52.178'
    # fake_type='http'
    # proxies={fake_type:fake_ip}
    # ISBN=9787563383870
    douban_root_url='https://book.douban.com/subject_search?search_text='
    douban_search_page=douban_root_url+pdf_title
    # ff_path=r'C:\Program Files\Mozilla Firefox\firefox.exe'

    driver=webdriver.Firefox()
    driver.get(douban_search_page)

    print(driver.current_url)


    # 先滑动到最底部, 因为下一页按钮肯定在下面
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.implicitly_wait(4)
    packs=[]
    try:
        if driver.find_element_by_class_name('next'):
            # 最大到多少, 公差是多少
            max_num = int(driver.find_element_by_xpath('//a[@class="next"]/preceding-sibling::*[1]').text)
            # 这里的preceding**[num],num表示的是和该节点的距离
            print(max_num)
            driver.find_element_by_class_name('next').click()
            step=int(driver.current_url.split('=')[-1]) # 因为进去第一页=0, 第二页的start=num, 那么num就是step
            print(step)
            # 构建starts
            starts=[pageNum*step for pageNum in range(0,max_num)]
            pages=[douban_search_page+'&start='+str(start) for start in starts]
            page_need=2
            cnt=0
            for page in pages:
                cnt+=1
                driver.get(page)
                # print('yes!')
                # details_page=driver.page_source
                href_xp='//a[contains(@href,"https://book.douban.com/subject/") and @class="cover-link"]'
                title_xp='//a[contains(@href,"https://book.douban.com/subject/") and @class="title-text"]'
                metaInfos_xp='//div[@class="meta abstract" and not(@style)]'
                # hrefElems=driver.find_elements_by_xpath(href_xp)
                # print(hrefElems)
                hrefs,titles,metaInfos_s=[],[],[]
                hrefElems,titleElems,metaInfoElems_s=list(map(driver.find_elements_by_xpath,[href_xp,title_xp,metaInfos_xp]))
                for hrefE in hrefElems:
                    hrefs.append(hrefE.get_attribute('href'))
                for titleE in titleElems:
                    titles.append(titleE.text)
                for metaE in metaInfoElems_s:
                    metaInfos_s.append(metaE.text)
                # print(hrefs,titles,metaInfos_s,sep='\n')
                packs.extend(list(zip(hrefs,titles,metaInfos_s)))
                if cnt>page_need:
                    break
            break
    except common.exceptions.NoSuchElementException:
        print('返回只有一页!')
        href_xp = '//a[contains(@href,"https://book.douban.com/subject/") and @class="cover-link"]'
        title_xp = '//a[contains(@href,"https://book.douban.com/subject/") and @class="title-text"]'
        metaInfos_xp = '//div[@class="meta abstract" and not(@style)]'
        # hrefElems=driver.find_elements_by_xpath(href_xp)
        # print(hrefElems)
        hrefs, titles, metaInfos_s = [], [], []
        hrefElems, titleElems, metaInfoElems_s = list(map(driver.find_elements_by_xpath, [href_xp, title_xp, metaInfos_xp]))
        if hrefElems:
            for hrefE in hrefElems:
                hrefs.append(hrefE.get_attribute('href'))
            for titleE in titleElems:
                titles.append(titleE.text)
            for metaE in metaInfoElems_s:
                metaInfos_s.append(metaE.text)
            # print(hrefs,titles,metaInfos_s,sep='\n')
            packs.extend(list(zip(hrefs, titles, metaInfos_s)))
            break
        else:
            print('未返回任何信息, 请重新输入!')
            continue
print('返回全部情况如下:')
print('第x本书','链接','书名','元信息',sep='\t')
for idx,(href,title,metaInfo) in enumerate(packs,1):
    print(idx,href,title,metaInfo,sep='\t->')
prompt_bookchoice='请输入你要第几本书:'
while True:
    book_idx=input(prompt_bookchoice)
    if book_idx.isdigit():
        pack_choose=packs[int(book_idx)-1]
        # 注意到没有, 在pycharm下面回车很多时候不好使~
        prompt_agree='再次确认:{};确认后键入y,否则随便输入什么字符'.format(pack_choose)
        if input(prompt_agree)=='y':
            break
        else:
            continue
href=pack_choose[0]
driver.get(href)

page_text=driver.find_element_by_xpath('//a[contains(text(),"更多")]').click()
driver.implicitly_wait(3)
whole_page=driver.page_source
whole_index=driver.find_element_by_xpath('//div[@class="indent" and contains(@id,"full")]').text
book_title=driver.find_element_by_xpath('//span[@property="v:itemreviewed"]').text
# 这个正则比较dirty, 但经过实验是可用的
page_num_str=re.findall('页数(.*?)定价',whole_page,re.S)[0]
page_num=int(''.join([each for each in page_num_str if each.isdigit()]))

print('Page num:',page_num)

whole_index='\n'.join(whole_index.split('\n')[:-1]) # 把最后那行的...去掉
print(whole_index)
whole_index_list=whole_index.split('\n')

# 下面想法有点sb, 有这种情况: 8.7　操作系统的全局中断与进程的局部中断—信号414, 一行3个, 看你咋办?
# digits_found=re.findall('\\d+',whole_index,re.S) # 用一手正则的贪婪模式, 匹配所有给定的目录数字
digits_found=[] # 好好看, 这才叫正则!
for oneline_idx in whole_index_list:
    digit_list=re.findall('.*?(\\d+)$',oneline_idx,re.S) # 少一个问号要人命!! 没有问号会把.*一只匹配过去, 这样最后就只剩一位数了!
    if not digit_list: # "本书导读", "前言" 什么的没有加数字是很自然的
        digits_found.append('n') # no need
    else:
        digits_found.append(digit_list[0])
print('我匹配到了什么:\n',digits_found)
if abs(len(digits_found)-len(whole_index_list))<15:
    # print('真实页码已在网页中给出!')
    indices=[]
    for idx,page_idx in enumerate(digits_found):
        if page_idx=='n':
            print('"{}"没有加页码, 请在下面补充页码![无pdf偏差值请输入-1]'.format(whole_index_list[idx]))
            prompt_askIdx='输入页码:\t'
            prompt_writeAg='确认页码:\t'
            while True:
                input_askIdx=input(prompt_askIdx)
                input_again=input(prompt_writeAg)
                # 靠, '-1' 是不能用isdigit()的!! 因为'-'相当于减号!
                if (input_askIdx==input_again) and (input_askIdx.isdigit() or input_askIdx=='-1'):
                    digits_found[idx]=input_askIdx
                    break
    indices=digits_found
# lines_endwithdigits=[]
# for oneline_idx in whole_index_list:
#     if oneline_idx[-1].isdigit():
#         lines_endwithdigits.append(oneline_idx)
# if abs(len(lines_endwithdigits)-len(whole_index_list))<=2:
#     print('真实目录已在网页中给出!')
#     for oneline_idx in whole_index_

# 这段代码可以去掉了, 因为我融合了一下有页码和无页码两种情况!!

# else:
#     print('\n网页版未给出目录,请依照书上的真实目录, 进行输入!')
#     prompt_oneLineATime = '\n一行一行进行输入目录,输入y,否则输入其他字符:\t'
#     prompt_batch = '\n批量输入,输入y,否则输入其他字符:\t'
#     prompt_enterline='\n请输入该行目录:\t'
#     prompt_enterbatch='\n批量输入, 请用问号?进行分割:\t'
#     indices=[]
#     # titles_indices=[]
#     while True:
#         choice_oneline=input(prompt_oneLineATime)
#         choice_batch=input(prompt_batch)
#         if choice_oneline=='y' and choice_batch!='y':
#             for title in whole_index_list:
#                 while True:
#                     idx=input('{}'.format(title)+prompt_enterline)
#                     if idx.isdigit():
#                         indices.append(idx)
#                         break
#                     else:
#                         print('输入非纯数字, 请重新输入!')
#                         continue
#         elif choice_batch=='y' and choice_oneline!='y':
#             enter_idx_str=input(prompt_enterbatch)
#             if not '?' in enter_idx_str:
#                 print('未检测出问号,请重新输入!')
#                 continue
#             if not enter_idx_str.replace('?','').isdigit():
#                 print('非纯数字, 请重新输入!')
#                 continue
#             enter_idx_list=enter_idx_str.split('?')
#             if len(whole_index_list)!=len(enter_idx_list):
#                 print('输入长度与真实目录不匹配, 请重新输入')
#             indices.extend(enter_idx_list)
#         else:
#             print('请做出明确选择!')
#             continue
#         if len(indices)==len(whole_index_list):
#             break

titles_indices=list(zip(whole_index_list,indices))

# print('T and I:')

cata_path= './{}_目录.txt'.format(book_title)
if os.path.exists(cata_path):
    os.remove(cata_path)
console_file=sys.stdout
for title,idx in titles_indices:
    a_fd=open(cata_path, 'a', encoding='utf-8')
    sys.stdout=a_fd
    print(title,idx,sep='\t\t->')
a_fd.close()

sys.stdout=console_file
print('\n目录文件写入完成')
while True:
    prompt_offset='请输入pdf文件的偏差值:\t->[页码表示为a(b/c)时, offset=b-a]\n'
    input_offset=input(prompt_offset)
    if input_offset.isdigit():
        offset=input_offset
        break
    else:
        continue

for title,idx in titles_indices:
    print('题目:{}\t->页码:{}'.format(title,idx))

# 最开始就直接在文件夹下读取到pdf文件, 保存为pdf_title即可
# pdfs_possible=[]
# for each in os.listdir('.'):
#     if each.endswith('.pdf') and len(each and book_title)>3:
#         pdfs_possible.append(each)
# if len(pdfs_possible)==1:
#     pdf_title=pdfs_possible[0]
# else:
#     prompt_askPdf = '发现多个相似pdf!请选择第几个:'
#     for idx,pdf_possible in enumerate(1,pdfs_possible):
#         print('第{}个'.format(idx),pdfs_possible,sep='\t')
#     while not pdf_possible:
#         askPdf=input(prompt_askPdf)
#         if not askPdf.isdigit() and 1<=int(askPdf)<=len(pdfs_possible):
#             pdf_title=pdfs_possible[int(askPdf)-1]
#         else:
#             print('请重新输入!')


pdf_in_path= './{}.pdf'.format(pdf_title)
pdf_rd=PyPDF2.PdfFileReader(pdf_in_path)
pdf_wt=PyPDF2.PdfFileWriter()
pdf_pagecnt=pdf_rd.getNumPages()

# 查一下有没有pdf页数越界情况, webget叫做page_num, pdf读取的叫pdf_pagecnt

if page_num!=pdf_pagecnt:
    print('警告:页数不符!')

pages=[]

# 再次注意, 此处的addBookMark的idx参数指的是"绝对页数", 具体可见testAdder里面写的

for pageNum in range(0,pdf_pagecnt):
    pages.append(pdf_rd.getPage(pageNum))

# offset=5 # 单独的一个临时变量
for page in pages:
    pdf_wt.addPage(page)
for title,idx in titles_indices:
    if idx!=-1: # 库函数没错, 是这个标题中TM就有什么进程1, 进程2, 那么这个时候加入目录就变成进程187, 那么读到的数字也就变成页码是187的了, 草!
        pdf_wt.addBookmark(title,int(idx)+int(offset)-1) # 注意, 在pdf_wt眼中, pdf是从第0页开始的, 但是我们输入还是照样输入就对了, 这边处理一下就对了!
    # 上面int(idx)可能会调整为int(idx)+offset

pdf_out_path=pdf_in_path.split('.pdf')[0]+'_完成添加.pdf' # [in] a='yhssb.pdf'; a.split('.pdf') [out]:['yhssb', '']
if os.path.exists(pdf_out_path):
    os.remove(pdf_out_path)
pdf_wt.write(open(pdf_out_path,'wb'))

print('大功告成!')


# index_path='D:/{}_目录.txt'.format(book_title)
# with open(index_path,'w',encoding='utf-8') as f:
#     f.write(titles_indices)


# cur_page_marker=driver.find_element_by_class_name('num activate thispage')
# if not cur_page_marker:
#     print('搜索结果只有一页!')
# elif cur_page_marker.text==1:
#     max_num=driver.find_elements_by_xpath('//{}/following-sibling::*')[-1].text
#
# page_text=driver.page_source
# print(driver.page_source)
# text=requests.get(page_text,headers=ua,proxies=proxies).text
# print(text)

# if
#
#
# search_html=etree.HTML(page_text)
# book_pages=search_html.xpath('//a[@class="cover-link"]//@href')
# # print(book_page)
# if len(book_pages)==1:
#     book_page=book_pages[0]
# else:
#     book_page=0
#     print('book_pages多返回了!')
# driver.get(book_page)
# page_text=driver.find_element_by_xpath('//a[contains(text(),"更多")]').click()
# driver.implicitly_wait(3)
# whole_page=driver.page_source
# whole_index=driver.find_element_by_xpath('//div[@class="indent" and contains(@id,"full")]').text
# title=driver.find_element_by_xpath('//span[@property="v:itemreviewed"]').text
# print(whole_index)
#
# index_path='D:/{}_目录.txt'.format(title)
# with open(index_path,'w',encoding='utf-8') as f:
#     f.write(whole_index)










