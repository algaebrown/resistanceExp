import requests
s=requests.Session()
url ="http://hr2sys.tmu.edu.tw/tmu_planhum_full/login_full_duty.aspx"
headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36"}


r=s.get(url)
dct=s.cookies.get_dict()#you will get a ASP.net cookie pass it in header along with other headers


aid = dct['ASP.NET_SessionId']
head = {'ASP.NET_SessionId':aid,'id' : 'form1', 'name' : 'form1'}
login_data = {'UserName' : 'A228645626', 'Password': 'Xca125Xcta'}
r = s.post(url, data=login_data,headers=head)
