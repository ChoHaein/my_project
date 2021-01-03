import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

def get_detail_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    lists = soup.select('#div_profile > div.s-list.basic-info > ul > li')
    title = soup.select_one('#div_profile > div.s-list.pic-grade > div.tit-point > p')
    # rating = soup.select_one('#div_profile > div.s-list.pic-grad > div.sns-grade > p > span.point > strong')
    rating = soup.select_one('#lbl_star_point > span.point')
    img = soup.select_one('#div_profile > div.s-list.pic-grade > ul > li.bimg.btn-gallery-open > img')['src']
    all_tags = soup.select('#div_profile > div.s-list.appraisal > div.grade-info > ul.app-arti > li > p.icon')
    tags = []
    keywords = soup.select('#div_profile > div.s-list.pic-grade > div.btxt > a')
    # only_keyword = keyword.text.strip()
    # tags.append(only_keyword)
    for kw in keywords :
        keyword = kw.text.strip()
        tags.append(keyword)

    #print(data.text)
    all_hour = soup.select('#div_hour > div.busi-hours > ul > li')
    open_days = []
    for od in all_hour :
        open_days.append(od.text.strip().replace('  ','').replace('\n',': '))

    for tag in all_tags:
        # text_tag = tag.text
        only_tag = tag.text.split('(')[0]
        tags.append(only_tag)

    main_tag1 = lists[2].text.strip()
    main_tag2 = lists[3].text.strip()
    tags.append(main_tag1)
    tags.append(main_tag2)

    if rating is None:
        rating = ''
    else :
        rating = rating.text.strip()

    info = {
            "title" : title.text.strip(),
            "img" : img,
            "addr" : lists[0].text.strip(),
            "tel" : lists[1].text.strip(),
            "main_tag1" : main_tag1,
            "main_tag2" : main_tag2,
            "keyword" : keyword,
            "tag" : tags,
            "rating": rating,
            "open_days" : open_days
            }
    print(info)
    db.pubstreet.insert_one(info)

def get_detail_urls(page=1):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    params = {
                'query' : '서울+도봉+술집',
                'page' : page
            }
    data = requests.get('https://www.diningcode.com/list.php', headers=headers, params=params)
    soup = BeautifulSoup(data.text, 'html.parser')
    lists = soup.select('#div_list > li')
    urls = []

    for list in lists:
        a = list.select_one('a')
        if a is not None:
            base_url = 'https://www.diningcode.com'
            url = base_url + a['href']
            urls.append(url)
    return urls

def insert_all():
    for page in range(1, 10):
        urls = get_detail_urls(page)
        for url in urls:
            get_detail_info(url)
            print('[알림] 데이터 저장이 완료되었습니다!')
### 실행하기
insert_all()