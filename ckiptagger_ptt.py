import requests
import jieba
from bs4 import BeautifulSoup
from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
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
        for i in range (0,20):
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

    def f_get_all_context(self) :
        count = 0
        shhh = 0
        push = 0
        shhh_words = []
        push_words = []
        
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
        print(count)
        return shhh_words , push_words

class c_ckiptagger_ptt:
    def __init__(self , push_words , shhh_words) -> None:
        self.push_words = push_words
        self.shhh_words = shhh_words

    def f_ckiptagger_ptt(self):
        push_word_count = {}
        shhh_word_count = {}
        del_push = []
        del_shhh= []
        ws = WS("./data")
        '''
        pos = POS("./data")
        ner = NER("./data")
        '''

        word_sentence_list = ws(
            self.push_words,
        )
        '''
        pos_sentence_list = pos(word_sentence_list)
        entity_sentence_list = ner(word_sentence_list, pos_sentence_list)

        print('WS: ', word_sentence_list)
        print('POS: ', pos_sentence_list)
        print('NER: ', entity_sentence_list)
        '''
       
        for i in word_sentence_list :
            for k in i :
                if k in push_word_count:
                    push_word_count[k] +=1
                else:
                    push_word_count[k] = 1

        for i in push_word_count :
            if push_word_count[i] < 50 :
                del_push.append(i)
        for i in del_push :
            del push_word_count[i]
        print("push_words:\n")
        print(sorted(push_word_count.items(), key=lambda x:x[1]))

        word_sentence_list = ws(
            self.shhh_words,
        )
        for i in word_sentence_list :
            for k in i :
                if k in shhh_word_count:
                    shhh_word_count[k] +=1
                else:
                    shhh_word_count[k] = 1

        for i in shhh_word_count :
            if shhh_word_count[i] < 50 :
                del_shhh.append(i)
        for i in del_shhh :
            del shhh_word_count[i]
        print("shhh_words:\n")
        print(sorted(shhh_word_count.items(), key=lambda x:x[1]))

def main():

    ptt_requests_q = c_ptt_requests()
    ptt_requests_q.f_find_index_url()
    ptt_requests_q.f_get_all_url()
    shhh_words , push_words = ptt_requests_q.f_get_all_context()
    ptt_c = c_ckiptagger_ptt(shhh_words=shhh_words , push_words=push_words)
    ptt_c.f_ckiptagger_ptt()


if __name__ == '__main__':
    main()