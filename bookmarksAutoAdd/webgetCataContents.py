import requests
from lxml import etree
from selenium import webdriver

ua={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
prompt_ISBN='请输入ISBN:'
ISBN=int(input(prompt_ISBN))
# fake_ip='116.208.52.178'
# fake_type='http'
# proxies={fake_type:fake_ip}
# ISBN=9787563383870
douban_root_url='https://book.douban.com/subject_search?search_text='
douban_search_page=douban_root_url+str(ISBN)
# ff_path=r'C:\Program Files\Mozilla Firefox\firefox.exe'

driver=webdriver.Firefox()
driver.get(douban_search_page)
page_text=driver.page_source
# print(driver.page_source)
# text=requests.get(page_text,headers=ua,proxies=proxies).text
# print(text)
search_html=etree.HTML(page_text)
book_pages=search_html.xpath('//a[@class="cover-link"]//@href')
# print(book_page)
if len(book_pages)==1:
    book_page=book_pages[0]
else:
    book_page=0
    print('book_pages多返回了!')
driver.get(book_page)
page_text=driver.find_element_by_xpath('//a[contains(text(),"更多")]').click()
driver.implicitly_wait(3)
whole_page=driver.page_source
whole_index=driver.find_element_by_xpath('//div[@class="indent" and contains(@id,"full")]').text
title=driver.find_element_by_xpath('//span[@property="v:itemreviewed"]').text
print(whole_index)

index_path='D:/{}_目录.txt'.format(title)
with open(index_path,'w',encoding='utf-8') as f:
    f.write(whole_index)










