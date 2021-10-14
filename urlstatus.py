import sys
import requests
from bs4 import BeautifulSoup
import socket
import re
from requests.packages import urllib3
urllib3.disable_warnings()
### 新增网站IP

file = sys.argv[1]
#file = '''E:\\Users\\Desktop\\123.txt'''
a = file.rindex('.')

def getIP(domain):
    if domain[:5] == 'https':
        domain = domain[8:]
    elif domain[:4] == 'http':
        domain = domain[7:]

    if domain.rfind(":") != -1:
        domain_1 = domain[:domain.rfind(":")]
    else:
        domain_1 = domain
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(domain_1):
        return domain_1
    else:
        try:
            myaddr = socket.getaddrinfo(domain_1, 'http')
            return myaddr[0][4][0]
        except:
            return '未建站'




try:
    b = file.rindex('\\')
    csv_file = file[b+1:a] + '.csv'
    file_path = file[:b+1]
    file_path_file = file_path + csv_file
except:
    file_path_file = file[:a] + '.csv'
csv=open(file_path_file,'w')
csv.write('url,IP,状态码,title\n')
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'}

for line in open(file):
    IP = ''
    line = line.replace('\n','').strip()
    if line != '':
        if line[:4] != 'http':
            url = 'http://' + line
        else:
            url = line

        try:
            strhtml = requests.get(url,headers=headers, timeout=10, verify=False)
            

        except:
            IP = getIP(url)
            a = '%s,%s,网址无法访问\n' %(url,IP)
            print(a)
            csv.write(a)
            continue
        try:
            IP = strhtml.raw._connection.sock.getpeername()[0]
        except:
            IP = getIP(url)
        if strhtml.status_code == requests.codes.ok:
            try:
                strhtml.encoding = 'utf-8'
                soup = BeautifulSoup(strhtml.text, 'lxml')
                a = '%s,%s,%s,%s\n' %(url,IP,strhtml.status_code,soup.title.text.replace('\n','').replace("\r", "").strip())
                print(a)
                csv.write(a)
            except:
                a = '%s,%s,%s,无标题\n' %(url,IP,strhtml.status_code)
                print(a)
                csv.write(a)
        else:
            
            a = '%s,%s,%s,\n' %(url,IP,strhtml.status_code)
            print(a)
            csv.write(a)
csv.close()
