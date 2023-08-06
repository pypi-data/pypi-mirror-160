import requests
import re, os, datetime, json,time
from requests_toolbelt.multipart.encoder import MultipartEncoder
from lxml import etree
from gne import GeneralNewsExtractor,ListPageExtractor
import pandas as pd
from urllib.parse import urljoin,urlparse,urlunparse
from posixpath import normpath

pic_api = ''
upload_api = ''
rt = ''
TIMEOUT = 10

class Snow:
    """雪花算法生成全局自增唯一id"""

    init_date = time.strptime('2022-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")
    start = int(time.mktime(init_date) * 1000)
    last = int(time.time() * 1000)
    pc_room = 1
    pc = 1
    seq = 0

    @classmethod
    def get_guid(cls):
        """获取雪花算法生成的id"""
        now = int(time.time() * 1000)
        if now != cls.last:
            cls.last = now
            cls.seq = 1
        else:
            while cls.seq >= 4096:
                time.sleep(0.1)
                return cls.get_guid()
            cls.seq += 1

        time_diff = now - cls.start
        pk = (time_diff << 22) ^ (cls.pc_room << 18) ^ (cls.pc << 12) ^ cls.seq

        return pk


class ruinewsV2():
    hd = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Mobile Safari/537.36',
        # 'Content-Type':'Content-Type: application/json;charset=UTF-8',
    }
    post_url = 'http://172.18.155.227:8888'
    add_url = '/doc/overall/addTop'
    file_url = '/doc/overall/uploadFile'
    token=None
    TYPE=['.html','.htm','shtml','.php']
    def __init__(self,domain_url,web_code='utf-8'):
        self.domain_url=domain_url
        self.web_code=web_code

    def element_convert(self,s):
        # xpath取到的element转换为html
        s = etree.tostring(s, pretty_print=True, method='html', encoding='utf-8')
        s = str(s, encoding="utf-8")
        return s
    def have_file(self,src:str):
        # src=src.lower()
        flag=False
        FILE_EXT=['.doc','.docx','.xls','.xlsx','.pdf','.wps','.ppt','.pptx']

        for file in FILE_EXT:
            if file in src:
                flag=True
                break
        if flag:
            ix=src.find('href="')
            jx=src.find('">',ix)

            return src[ix+6:jx]
        else:
            return None
    def get_token(self):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36',
            'Content-Type': 'application/json',

        }
        data = {
            'username': '22070400001',
            'password': 'admin123'
        }
        login_url = self.post_url + '/login'
        r = requests.post(login_url, data=json.dumps(data), headers=headers)
        msg = json.loads(r.content.decode('utf-8'))
        if msg is None:
            print('token 获取失败')
            return None
        self.token = msg['token']
        return self.token
    def post_data(self,data:dict):
        if self.token is None:
            self.token=self.get_token()
        url=self.post_url+self.add_url

        headers = {
            'Content-Type': 'application/json',
            'Authorization':'Bearer '+self.token
        }
        r=requests.post(url,data=json.dumps(data),headers=headers)
        return r.text
    def url_join(self,base, url):
        url1 = urljoin(base, url)
        arr = urlparse(url1)
        path = normpath(arr[2])
        return urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))
    def form_upload_file(self,dn_url,file_path):
        try:
            r = requests.get(dn_url,headers=self.hd)
            if r.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(r.content)
            else:
                return None
            file_name=dn_url.split('/')[-1]
            m = MultipartEncoder(
                fields={'file': (file_name, open(file_path, 'rb'))}
            )
            if self.token is None:
                self.token=self.get_token()
            headers = {'Content-Type': m.content_type,'Authorization': 'Bearer ' + self.token}

            r = requests.post(self.post_url+self.file_url, data=m.read(), headers=headers)

            if r.status_code == 200:
                r = r.text
                new_file_url = json.loads(r)['data'][file_name]

                # os.remove(file_name)
                return new_file_url
            else:
                print('ERR:文件上传接口出错%s' % r.status_code)
                return None
        except:
            print('error:下载文件出错')
            return ''
    def file_process(self,art_url,file_url):
        file_dir = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')[0:6]
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)

        file_name = file_dir + '/' + file_url.split('/')[-1]
        dnurl=file_url
        if not file_url.startswith('http'):
            dnurl = self.url_join(art_url, file_url)

        return self.form_upload_file(dnurl,file_name)
    def pic_process(self,art_content, art_url, domain_url=''):
        pic_path = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')[0:6]
        pic_url = re.findall(' src="(.*?)"', art_content, re.S)
        if domain_url == '':
            domain_url = art_url[0:art_url.find('/', art_url.find('://') + 3)]

        # //data:image
        for url in pic_url:
            pic_name = url.split('/')[-1]
            file = pic_path + '/' + url.split('/')[-1]
            if url.startswith('data:image') and art_content.find('data-src=') > 0:
                art_content = art_content.replace(url, '')
                art_content = art_content.replace('data-src=', '><img src=')
                continue
            if pic_name.find('.') == -1:
                art_content = art_content.replace(url, '')
                continue
            if not os.path.isdir(pic_path):
                os.makedirs(pic_path)
            dnurl = url


            if not str(url).startswith('http'):
                dnurl = self.url_join(art_url,url)

            return self.form_upload_file(dnurl,file)

    def filter_tags_tw(self,htmlstr, tags,arturl):
        if htmlstr is None or len(htmlstr)==0:
            return ''
        htmlstr = ''.join(htmlstr)
        htmlstr = htmlstr.replace('<br>', '<p>')
        htmlstr = htmlstr.replace('<br />', '<p>')
        html = etree.HTML(htmlstr)
        hrefs = html.xpath("//a/@href")
        file_p = ''
        for href in hrefs:
            if self.have_file(href) is not None:
                file_p += '<p href="' + href + '"></p>'

        re_h = re.compile('(?!</?(' + tags + ').*?>)<.*?>')
        s = re_h.sub('', htmlstr)  # 去掉HTML 标签
        s = s.replace(' ' * 3, '')
        # s = s.replace('<img', '<p')
        s = s.replace('<a', '<p')
        s = s.replace('<div>', '<p>')
        s = s.replace('</div>', '</p>')
        s = s.replace('<div ', '<p ')

        s = s.replace('\t', '').replace('\r', '').replace('\n', '')
        s = s.replace(u'\u3000', u'').replace(u'\xa0', u' ').replace('\u2003', '')
        s = s.replace('\r\n', '<br>')
        s += file_p
        if '</table' in htmlstr:
            s+='<p>'+arturl+'</p>'
        return s

    def check_url(self,url:str,num:int):
        '''
        查重url并写入history.csv文件中
        :return:
        '''
        csv = 'history.csv'
        # 文件不存在创建，存在取前条数据查重
        if os.path.exists(csv):
            df_csv = pd.read_csv(csv).tail(num)
        else:
            df_csv = pd.DataFrame(columns=['url'])
        df_csv.set_index('url')
        csv_ls = []
        # 判断csv文件是否存在
        rtn = False
        if df_csv[df_csv['url'].isin([url])].empty:
            if url not in csv_ls:
                csv_ls.append(url)
                rtn = True
        if len(csv_ls) > 0:
            dfb = pd.DataFrame(csv_ls, columns=['url'])
            if df_csv.empty:
                dfb.to_csv(csv)
            else:
                dfb.to_csv(csv, mode='a', header=False)
        return rtn
    def filter_json_url(self,news_ls):
        #查重json返回的url
        if len(news_ls) == 0:
            print('no data')
            return []
        csv = 'history.csv'
        if os.path.exists(csv):
            df_csv = pd.read_csv(csv)
        else:
            df_csv = pd.DataFrame(columns=['url'])
        df_csv.set_index('url')
        csv_ls = []
        for item in news_ls:
            url = item['url']
            if not url.startswith('http'):
                url=self.url_join(self.domain_url,url)

            if df_csv[df_csv['url'].isin([url])].empty:
                if url not in csv_ls:
                    csv_ls.append(url)

        if len(csv_ls) > 0:
            dfb = pd.DataFrame(csv_ls, columns=['url'])
            if df_csv.empty:
                dfb.to_csv(csv)
            else:
                dfb.to_csv(csv, mode='a', header=False)
            return csv_ls
        else:
            return []
    def get_news_list(self,pg_url,links_xpath,is_etree=False):
        #get list方式 返回列表
        r = requests.get(pg_url, headers=self.hd, verify=False)
        html = r.content.decode(self.web_code)
        if is_etree==True:
            html=etree.HTML(html)
            news_ls=html.xpath(links_xpath)
        else:
            ls_ex = ListPageExtractor()
            news_ls = ls_ex.extract(html, feature=links_xpath)

        if len(news_ls) == 0:
            print('no data')
            return []
        csv = 'history.csv'
        if os.path.exists(csv):
            df_csv = pd.read_csv(csv)
        else:
            df_csv = pd.DataFrame(columns=['url'])
        df_csv.set_index('url')
        csv_ls = []
        for item in news_ls:
            if is_etree==True:
                url=item
            else:
                url = item['url']
            for ty in self.TYPE:
                if ty not in url:
                    continue

            if not url.startswith('http'):
                url = self.url_join(pg_url, url)

            if df_csv[df_csv['url'].isin([url])].empty:
                if url not in csv_ls:
                    csv_ls.append(url)

        if len(csv_ls) > 0:
            dfb = pd.DataFrame(csv_ls, columns=['url'])
            if df_csv.empty:
                dfb.to_csv(csv)
            else:
                dfb.to_csv(csv, mode='a', header=False)
            return csv_ls
        else:
            return []
    def get_news_detail(self,url,content_xpath='',is_kwd=False,
                title_xpath='',test_flag=False,proc_art_date='',
                author_xpath='',no_gne_content=True,del_tag='',
                source_xpath='',IS_EN_SITE=False,html_rp='',
                publish_time_xpath='',web_code=''):


        if not url.startswith('http'):
            url=self.url_join(self.domain_url,url)


        art_ex = GeneralNewsExtractor()
        r=requests.get(url, headers=self.hd, verify=False)
        if r.status_code!=200:
            print('request error')
            return
        if web_code:
            art_html = r.content.decode(web_code)
        else:
            art_html = r.content.decode(self.web_code)
        etree_html=etree.HTML(art_html)
        if del_tag != '':
            div = etree_html.xpath(del_tag)

            for d in div:
                d.getparent().remove(d)
        if html_rp!='':
            art_html=eval(html_rp)

        art_html = art_html.replace('\r', '').replace('\n', '')
        #art_html = re.sub(r' style="/' + '(.*?)' + '">', '>', art_html)
        art_html = re.sub(r'<style' + '(.*?)' + '</style>', '', art_html)
        try:
            rst = art_ex.extract(art_html, title_xpath=title_xpath,publish_time_xpath=publish_time_xpath,
                                 body_xpath=content_xpath, with_body_html=True,source_xpath=source_xpath,author_xpath=author_xpath)
        except:
            print('GNE解析出错')
            return


        art_title = rst['title']
        art_date = rst['publish_time'].replace('年','-').replace('月','-').replace('日','')
        if no_gne_content==True:
            etree_html=etree.HTML(art_html)
            if content_xpath!='':
                art_content = self.element_convert(etree_html.xpath(content_xpath)[0])
            else:
                art_content = rst['body_html']
        else:
            art_content = rst['body_html']
        if art_title == '' or art_content == '':
            print('title or content is empty')
            return

        art_author = rst['author']
        art_source = rst['source']

        art_url = url
        art_content = self.filter_tags_tw(art_content,'p|img|div',art_url)



        nitem = {}

        nitem['title'] = art_title
        nitem['html'] = art_content
        nitem['source'] = art_source
        nitem['url'] = art_url
        nitem['author'] = art_author
        nitem['releaseAt'] = art_date

        return nitem