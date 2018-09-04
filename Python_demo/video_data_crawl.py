


'''
������ʽ�ļ���requests���������stream��ΪTrue�Ϳ�������[�ĵ��ڴ�](http://docs.python-requests.org/en/master/user/advanced/#body-content-workflow)��

����һ����Ƶ��ַ����һ�£�

'''
# -*- coding: utf-8 -*-
import requests
 
def download_file(url, path):
    #stream=True�������Ӳ��ᱻ�ر�,���Ƕ�ȡ�������ݻ��ߵ���Response.close
    with requests.get(url, stream=True) as r:
        chunk_size = 1024
        content_size = int(r.headers['content-length'])
        print '���ؿ�ʼ'
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
 

'''
��������û��ʵ����������Ҫ��__exit__��������Ȼֻ��Ϊ�˱�֤Ҫ��r���close���ͷ����ӳأ��Ǿ�ʹ��contextlib��closing���Ժ��ˣ�
'''

# -*- coding: utf-8 -*-
import requests
from contextlib import closing
 
def download_file(url, path):
    with closing(requests.get(url, stream=True)) as r:
        chunk_size = 1024
        content_size = int(r.headers['content-length'])
        print '���ؿ�ʼ'
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)




'''
�������������ˣ������Ҷ������ļ�����ô��С�����䰡������������˶������أ�����Ҫ���ºõ����ݼ�ʱ���Ӳ�̣�����ʡ���ڴ��ǲ��ǣ�
'''

# -*- coding: utf-8 -*-
import requests
from contextlib import closing
import os
 
def download_file(url, path):
    with closing(requests.get(url, stream=True)) as r:
        chunk_size = 1024
        content_size = int(r.headers['content-length'])
        print '���ؿ�ʼ'
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                f.flush()
                os.fsync(f.fileno())


'''
�ļ������ۿɼ����ٶ��������������ҵ�Ӳ�̣��������һ��д��Ӳ�̰ɣ������мǸ����ͺ���

'''

def download_file(url, path):
    with closing(requests.get(url, stream=True)) as r:
        chunk_size = 1024
        content_size = int(r.headers['content-length'])
        print '���ؿ�ʼ'
        with open(path, "wb") as f:
            n = 1
            for chunk in r.iter_content(chunk_size=chunk_size):
                loaded = n*1024.0/content_size
                f.write(chunk)
                print '������{0:%}'.format(loaded)
                n += 1

'''
����ͺ�ֱ���ˣ�

������2.579129%
������2.581255%
������2.583382%
������2.585508%
'''

'''
�Ļ�Զ�����������ô��ֻ��������һ���أ�д����һ��ʹ�ðɣ�
'''
# -*- coding: utf-8 -*-
import requests
from contextlib import closing
import time
 
def download_file(url, path):
    with closing(requests.get(url, stream=True)) as r:
        chunk_size = 1024*10
        content_size = int(r.headers['content-length'])
        print '���ؿ�ʼ'
        with open(path, "wb") as f:
            p = ProgressData(size = content_size, unit='Kb', block=chunk_size)
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                p.output()
 
 
class ProgressData(object):
 
    def __init__(self, block,size, unit, file_name='', ):
        self.file_name = file_name
        self.block = block/1000.0
        self.size = size/1000.0
        self.unit = unit
        self.count = 0
        self.start = time.time()
    def output(self):
        self.end = time.time()
        self.count += 1
        speed = self.block/(self.end-self.start) if (self.end-self.start)>0 else 0
        self.start = time.time()
        loaded = self.count*self.block
        progress = round(loaded/self.size, 4)
        if loaded >= self.size:
            print u'%s�������\r\n'%self.file_name
        else:
            print u'{0}���ؽ���{1:.2f}{2}/{3:.2f}{4} �����ٶ�{5:.2%} {6:.2f}{7}/s'.\
                  format(self.file_name, loaded, self.unit,\
                  self.size, self.unit, progress, speed, self.unit)
            print '%50s'%('/'*int((1-progress)*50))

'''
���У�

���ؿ�ʼ
���ؽ���10.24Kb/120174.05Kb 0.01% �����ٶ�4.75Kb/s
/////////////////////////////////////////////////
���ؽ���20.48Kb/120174.05Kb 0.02% �����ٶ�32.93Kb/s
/////////////////////////////////////////////////
'''

'''
����ȥ������ˡ�

����Ҫ���ľ��Ƕ��߳�ͬʱ�����ˣ����߳�����url������У������̻߳�ȡurl��
'''
# -*- coding: utf-8 -*-
import requests
from contextlib import closing
import time
import Queue
import hashlib
import threading
import os
 
 
def download_file(url, path):
    #һֱ�������� closing   ������with���  ����������ݿ⣬�������������Զ��ر�
    with closing(requests.get(url, stream=True)) as r:
        chunk_size = 1024*10
        #r.headers �����Ӧ�ı�
        content_size = int(r.headers['content-length'])
        if os.path.exists(path) and os.path.getsize(path)>=content_size:
            print '������'
            return
        print '���ؿ�ʼ'
        with open(path, "wb") as f:
            p = ProgressData(size = content_size, unit='Kb', block=chunk_size, file_name=path)
            #�ֿ������д��
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                p.output()
 
 
class ProgressData(object):
 
    def __init__(self, block,size, unit, file_name='', ):
        self.file_name = file_name
        self.block = block/1000.0
        self.size = size/1000.0
        self.unit = unit
        self.count = 0
        self.start = time.time()
    def output(self):
        self.end = time.time()
        self.count += 1
        speed = self.block/(self.end-self.start) if (self.end-self.start)>0 else 0
        self.start = time.time()
        loaded = self.count*self.block
        progress = round(loaded/self.size, 4)
        if loaded >= self.size:
            print u'%s�������\r\n'%self.file_name
        else:
            print u'{0}���ؽ���{1:.2f}{2}/{3:.2f}{4} {5:.2%} �����ٶ�{6:.2f}{7}/s'.\
                  format(self.file_name, loaded, self.unit,\
                  self.size, self.unit, progress, speed, self.unit)
            print '%50s'%('/'*int((1-progress)*50))
 
 
queue = Queue.Queue()
 
 
def run():
    while True:
        #����timeout���յ���Ϊ�˷�ֹurl���ɷ��ʣ�������Ӧ�ٶ�̫����ɵ�ʱ���˷�
        #�㻹����ͨ�����  ��֪�����Ҫ��ÿ�������
        url = queue.get(timeout=100)
        if url is None:
            print u'ȫ������'
            break
        #��ϰ��MD5���ܺ��ֵ��128bit�ģ���4λ��������ϳ�һ��ʮ�����ƣ�������������ʮ�������ַ�����32��������d3379f609e1aa88da2f50018d4fa218f��
        h = hashlib.md5()
        h.update(url)
        name = h.hexdigest()
        path = 'e:/download/' + name + '.mp4'
        download_file(url, path)
 
 
def get_url():
    queue.put(None)
 
 
if __name__ == '__main__':
    get_url()
    for i in xrange(4):
        t = threading.Thread(target=run)
        #�ػ��߳�
        #��thread.start()֮ǰ���ã�������ܳ�һ��IllegalThreadStateException�쳣���㲻�ܰ��������еĳ����߳�����Ϊ�ػ��̡߳� 
        #��Daemon�߳��в��������߳�Ҳ��Daemon�ġ�
        #�ػ��߳�Ӧ����Զ��ȥ���ʹ�����Դ�����ļ������ݿ⣬��Ϊ�������κ�ʱ��������һ���������м䷢���жϡ�
        t.daemon = True
        t.start()


if __name__ == '__main__':
    url = '����ԭ��...'
    path = '����Ķ���'
    download_file(url, path)


