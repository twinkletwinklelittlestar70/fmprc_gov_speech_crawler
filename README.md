# Crawler for fmprc gov website
In order to generate high-quality Chinese-English parallel corpora, this script can crawl the full text of speeches published by the official website of the Chinese Ministry of Foreign Affairs.

## install
```
pip install -r requirements.txt
```

## settings
``` py
# open the crawler.py and change the configure
LIST_PAGE_URL_CN = 'https://www.fmprc.gov.cn/web/ziliao_674904/zyjh_674906/'
LIST_PAGE_URL_EN = 'https://www.fmprc.gov.cn/mfa_eng/wjdt_665385/zyjh_665391/'
SAVE_FILE = 'data.xlsx'    # file to save
```

## run the crawler
```
python crawler.py
```