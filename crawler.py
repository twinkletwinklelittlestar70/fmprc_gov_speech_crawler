import requests, bs4
from bs4 import BeautifulSoup
import xlsxwriter
# xlsxwriter document: https://xlsxwriter.readthedocs.io/

LIST_PAGE_URL_CN = 'https://www.fmprc.gov.cn/web/ziliao_674904/zyjh_674906/'
LIST_PAGE_URL_EN = 'https://www.fmprc.gov.cn/mfa_eng/wjdt_665385/zyjh_665391/'
SAVE_FILE = 'data.xlsx'    #保存的文件

# Crawl the list page and return article url
def get_article_list(url, selector):
    res = requests.get(url,
        headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'})
    # print(r.content)
    soup = BeautifulSoup(res.text, 'html.parser')
    link_eles = soup.select(selector)
    links = [ele.get('href') for ele in link_eles]
    
    print('====> links len=', len(links))
    return links

def get_article_doc(url, lang='en', title_sel='', time_sel='', content_sel=''):
    res = requests.get(url,
        headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'})
    # print('Encoding=====>', res.encoding)
    res.encoding = "gbk2312" # charset 解决中文编码问题
    # print(res.text)

    if title_sel=='' or time_sel=='' or content_sel=='':
        print('[Error]: No selector sepcify!')
        return []

    soup = BeautifulSoup(res.text, 'html.parser')
    title = soup.select(title_sel)[0].get_text()
    time = soup.select(time_sel)[0].get_text()
    full_content = soup.select(content_sel)[0].get_text()

    print('[title]====>', title)

    return [title, time, full_content]

def init_worksheet(workbook, name, style):
    # Add sheet
    worksheet = workbook.add_worksheet(name)
    # Write sheet head
    row0 = ["title", "time", "content"]
    for i in range(0,len(row0)):
      worksheet.write(0,i,row0[i], style)
    
    return worksheet


if __name__ == '__main__':    
    workbook = xlsxwriter.Workbook(SAVE_FILE)
    # Add style
    bold = workbook.add_format({'bold': True})
    regular = workbook.add_format({'bold': False})

    # crawl CN data 
    worksheet_cn = init_worksheet(workbook, 'cn', bold)

    article_links_cn = get_article_list(LIST_PAGE_URL_CN, '.newsBd a')
    # article_links = ['./202112/t20211201_10460659.shtml'] # for test
    
    for index, link in enumerate(article_links_cn):
        full_link = LIST_PAGE_URL_CN + link
        # print('full_link:', full_link)
        title_sel = ".news-title h1"
        time_sel = ".news-title p.time"
        content_sel = ".news-main"
        article_data = get_article_doc(full_link, 'cn', title_sel, time_sel, content_sel)
        for i in range(0,len(article_data)):
            worksheet_cn.write(index+1,i,article_data[i], regular)

    # crawl EN data 
    worksheet_en = init_worksheet(workbook, 'en', bold)
    article_links_en = get_article_list(LIST_PAGE_URL_EN, '.newsLst_mod a')
    # print('======>', len(article_links_en))
    # article_links_en = [article_links_en[0]] # for test
    for index, link in enumerate(article_links_en):
        full_link = LIST_PAGE_URL_EN + link
        title_sel = ".content_mod h2.title"
        time_sel = ".content_mod #News_Body_Time"
        content_sel = ".content_mod .content"
        article_data = get_article_doc(full_link, 'en', title_sel, time_sel, content_sel)
        for i in range(0,len(article_data)):
            worksheet_en.write(index+1,i,article_data[i], regular)
    
    workbook.close()

