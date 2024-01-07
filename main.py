import requests
import jieba
from bs4 import BeautifulSoup

class c_ptt_requests:
    def __init__(self) -> None:
        self.url = 'https://www.ptt.cc/bbs/Gossiping/index.html'
        #self.url = 'https://www.ptt.cc/bbs/HatePolitics/index.html'
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
        #index_url_number = index_url_number.replace('/bbs/HatePolitics/index' , '').replace('.html' , '')
        index_url_number = int(index_url_number) + 1
        for i in range (0,20):
            url_tmp = index_url_number - i
            self.index_url.append('https://www.ptt.cc/bbs/Gossiping/index'+str(url_tmp)+'.html')
            #self.index_url.append('https://www.ptt.cc/bbs/HatePolitics/index'+str(url_tmp)+'.html')

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

    def f_get_all_context(self) :
        count = 0
        shhh = 0
        push = 0
        shhh_words = []
        push_words = []
        
        for k in self.all_url:
            r = requests.get(k , headers = self.my_headers)
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
                
        print(count)
        print(shhh)
        print(push)
        return shhh_words , push_words
        
class c_ptt_nlp:
    def __init__(self , push_words , shhh_words) -> None:
        self.push_words = push_words
        self.shhh_words = shhh_words
    def f_ptt_jieba(self):
        push_word_count = {}
        shhh_word_count = {}
        del_push = []
        del_shhh= []
        for i in self.push_words:
            s1_list = jieba.cut(i, cut_all =True)
            for n  in s1_list :
                if len(n) > 0 :
                    if n in push_word_count:
                        push_word_count[n] +=1
                    else:
                        push_word_count[n] = 1
        for i in self.shhh_words:
            s1_list = jieba.cut(i, cut_all =True)
            for n  in s1_list :
                if len(n) > 0 :
                    if n in shhh_word_count:
                        shhh_word_count[n] +=1
                    else:
                        shhh_word_count[n] = 1

        for i in push_word_count :
            if push_word_count[i] < 10 :
                del_push.append(i)
        for i in del_push :
            del push_word_count[i]
            
        for i in shhh_word_count :
            if shhh_word_count[i] < 10 :
                del_shhh.append(i)
        for i in del_shhh :
            del shhh_word_count[i]

        print("push_words:\n")
        print(sorted(push_word_count.items(), key=lambda x:x[1]))
        print("shhh_words:\n")
        print(sorted(shhh_word_count.items(), key=lambda x:x[1]))
        
def main():
    ptt_requests_q = c_ptt_requests()
    ptt_requests_q.f_find_index_url()
    ptt_requests_q.f_get_all_url()
    shhh_words , push_words = ptt_requests_q.f_get_all_context()
    ptt_nlp_q = c_ptt_nlp(shhh_words=shhh_words , push_words=push_words)
    ptt_nlp_q.f_ptt_jieba()

if __name__ == '__main__':
    main()