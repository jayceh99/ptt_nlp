import requests
import jieba
from bs4 import BeautifulSoup

class c_ptt_requests:
    def __init__(self) -> None:
        self.url = 'https://www.ptt.cc/bbs/Gossiping/index.html'
        self.my_headers = {'cookie' : 'over18=1;'}
        self.all_url = []
        self.index_url = []

    def f_find_index_url(self) :
        r = requests.get(self.url , headers = self.my_headers)
        soup = BeautifulSoup(r.text , 'html5lib') 
        url = soup.find(class_='btn-group btn-group-paging')
        index_url_number  = url.find_all('a' , href = True)
        index_url_number = str(index_url_number[1]['href'])
        index_url_number = index_url_number.replace('/bbs/Gossiping/index' , '').replace('.html' , '')
        index_url_number = int(index_url_number) + 1
        for i in range (0,10):
            url_tmp = index_url_number - i
            self.index_url.append('https://www.ptt.cc/bbs/Gossiping/index'+str(url_tmp)+'.html')


    def f_get_all_url(self) :
        for k in self.index_url :
            try :
                r = requests.get(k , headers = self.my_headers)
                soup = BeautifulSoup(r.text , 'html5lib') 
                url = soup.select('.title')
                for i in url:
                    self.all_url.append('https://www.ptt.cc'+i.find('a' , href = True)['href'])
            except :
                pass
        print(self.all_url)


    def f_get_all_context(self) :
        count = 0
        shhh = 0
        push = 0
        shhh_words = []
        push_words = []
        push_word_count = {}
        shhh_word_count = {}
        for i in self.all_url:
            r = requests.get(i , headers = self.my_headers)
            soup = BeautifulSoup(r.text, "html5lib")
            reser = soup.select('.push')
            
            count += 1
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
                    if n in push_word_count:
                        push_word_count[n] +=1
                    else:
                        push_word_count[n] = 1
            for i in shhh_words:
                s1_list = jieba.cut(i, cut_all =True)
                for n  in s1_list :
                    if n in shhh_word_count:
                        shhh_word_count[n] +=1
                    else:
                        shhh_word_count[n] = 1
        print(sorted(push_word_count.items(), key=lambda x:x[1]))
        print(sorted(shhh_word_count.items(), key=lambda x:x[1]))
        print(count)
#print(sorted(word_count.keys()))
#print(word_count)

class c_ptt_nlp:
    def __init__(self) -> None:
        pass
    def f_ptt_jieba(self):
        pass
def main():
    ptt_requests_q = c_ptt_requests()
    ptt_requests_q.f_find_index_url()
    ptt_requests_q.f_get_all_url()
    ptt_requests_q.f_get_all_context()
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