import requests
import jieba
from bs4 import BeautifulSoup

class ptt_requests:
    def __init__(self) -> None:
        self.url = 'https://www.ptt.cc/bbs/Gossiping/index.html'
        self.my_headers = {'cookie' : 'over18=1;'}
        self.all_url = []

    def find_index_url(self) :
        r = requests.get(self.url , headers = self.my_headers)
        soup = BeautifulSoup(r.text , 'html5lib') 
        url = soup.find(class_='btn-group btn-group-paging')
        index_url  = url.find_all('a' , href = True)
        index_url = str(index_url[1]['href'])
        index_url = index_url.replace('/bbs/Gossiping/index' , '').replace('.html' , '')
        index_url = int(index_url) + 1
        self.index_url = index_url

    def get_all_url(self) :
        r = requests.get(self.url , headers = self.my_headers)
        soup = BeautifulSoup(r.text , 'html5lib') 
        url = soup.select('.title')
        for i in url:
            self.all_url.append(i.find('a' , href = True)['href'])

        

    def get_all_context(self) :
        pass

class ptt_nlp:
    def __init__(self) -> None:
        pass
    def ptt_jieba(self):
        pass
def main():
    ptt_requests_q = ptt_requests()
    ptt_requests_q.test()
if __name__ == '__main__':
    main()


'''
my_url = "https://www.ptt.cc/bbs/Gossiping/M.1704110086.A.17B.html"
# 設定Header與Cookie
my_headers = {'cookie': 'over18=1;'}

r = requests.get(my_url , headers = my_headers)
soup = BeautifulSoup(r.text, "html5lib")
reser = soup.select('.push')
shhh = 0
push = 0
shhh_words = []
push_words = []
word_count = {}
for i in reser:

    try:
        if '噓' in str(i.find('span' , class_='f1 hl push-tag').get_text()) :
            shhh += 1
            txt = str(i.find('span' , class_='f3 push-content').get_text().replace(':','').replace(' ',''))
            shhh_words.append(txt)

    except:
        if '推' in str(i.find('span' , class_='hl push-tag').get_text()) :
            push += 1
            txt = str(i.find('span' , class_='f3 push-content').get_text().replace(':','').replace(' ',''))
            push_words.append(txt)

for i in push_words:
    s1_list = jieba.cut(i, cut_all =True)
    for n  in s1_list :
        if n in word_count:
            word_count[n] +=1
        else:
            word_count[n] = 1
print(sorted(word_count.items(), key=lambda x:x[1]))
#print(sorted(word_count.keys()))
#print(word_count)
'''