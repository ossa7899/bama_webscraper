import time as timelib
import mysql.connector
from bs4 import BeautifulSoup as BS
import requests
import re
from sklearn import tree
def guss_price(new_data,clf):
    answer = clf.predict(new_data)
    return answer
def do_machin_learning():
    query = 'SELECT * FROM mydata'
    cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='webScraping')
    cursor = cnx.cursor()
    cursor.execute(query)
    l =list()
    x =list()
    y =list()
    for(year_of_creating,brand,model,city,karkard,price,color,year,month,day,hour,minute,second) in cursor:
        l.append(year_of_creating)
        l.append(brand)
        l.append(model)
        l.append(city)
        l.append(karkard)
        l.append(price)
        l.append(color)
        l.append(year)
        l.append(month)
        l.append(day)
        l.append(hour)
        l.append(minute)
        l.append(second)
    x.append(l[0:5])
    x.append(l[6])
    y.append(l[5])
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(x,y)
    return clf

def are_same(new,last):
    if(len(last)==0):
        return False
    for index in range(0,len(new)):
        if(not new[index] == last[index]):
            return False
    return True


def add_to_DB(mylist):
    print("inseting")
    query= 'INSERT INTO mydata VALUES (\'%d\',\'%s\',\'%s\',\'%s\',\'%d\',\'%d\',\'%s\',\'%d\',\'%d\',\'%d\',\'%d\',\'%d\',\'%d\')' % (mylist[0],mylist[1],mylist[2],mylist[3],mylist[4],mylist[5],mylist[6],mylist[7],mylist[8],mylist[9],mylist[10],mylist[11],mylist[12])
    cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='webScraping')
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    print('inserted')
    cnx.close()


def last_data_in_DB():
    print('in last data in DB')
    query = 'SELECT * FROM mydata ORDER BY year DESC,month DESC,day DESC,hour DESC,minute DESC,second DESC LIMIT 1'
    cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='webScraping')
    cursor = cnx.cursor()
    cursor.execute(query)
    l =list()
    for(year_of_creating,brand,model,city,karkard,price,color,year,month,day,hour,minute,second) in cursor:
        l.append(year_of_creating)
        l.append(brand)
        l.append(model)
        l.append(city)
        l.append(karkard)
        l.append(price)
        l.append(color)
        l.append(year)
        l.append(month)
        l.append(day)
        l.append(hour)
        l.append(minute)
        l.append(second)
        print('%d,%s,%s,%s,%d,%d,%s,%d,%d,%d,%d,%d,%d' % (year_of_creating,brand,model,city,karkard,price,color,year,month,day,hour,minute,second))
    print(l)
    cnx.close()
    return l  


def data_finder(string):
    strings = timelib.strftime("%Y,%m,%d,%H,%M,%S")
    t = strings.split(',')
    time = [ int(x) for x in t ]
    
    result = list()
    raw_list = list()
    
    if not ('کارکرد' in string):
        print("KARKARD NABBOOD")
        result = [False,raw_list]
        return result
    raw_list.append(int(string[0].split('،')[0]))#سال تولید
    raw_list.append(string[1].split('،')[0])#برند
    raw_list.append(string[2])#مدل ماشین
    if string[1 + string.index('کارکرد')] == 'صفر':
        raw_list.append(string[4+string.index('کارکرد')].split('،')[0])#نام شهر
        raw_list.append(int(0))#مقدار کارکرد
    else:
        price = string[1 + string.index('کارکرد')].split(',')
        raw_list.append(string[4+string.index('کارکرد')].split('،')[0])#نام شهر
        result = ''
        for elem in price:
            result += elem 
        raw_list.append(int(result))#مقدار کارکرد
    if 'تومان' in string:
        price = string[string.index('تومان') - 1].split(',')#قیمت
        result = ''
        for elem in price:
            result += elem 
        raw_list.append(int(result))
    elif 'ماهانه' in string:
        price = string[string.index('ماهانه') - 3].split(',')#قیمت
        result = ''
        for elem in price:
            result += elem
        raw_list.append(int(result))
    if 'رنگ' in string:        
        raw_list.append(string[string.index('رنگ')+1].split('،')[0])#رنگ
    if 'دقیقه' in string:
        minute = int(string[string.index('دقیقه')-1])
        if time[4] - minute >0:
            time[4] = time[4] - minute
        else:
            minute-=time[4]
            time[4]=0
            if(time[3]-1 <= 0 ):
                time[2]-=1
                time[3]+23
            else:
                time[3]-=1
            time[4]+=60-minute
        #زمان
        raw_list.append(int(time[0]))
        raw_list.append(int(time[1]))
        raw_list.append(int(time[2]))
        raw_list.append(int(time[3]))
        raw_list.append(int(time[4]))
        raw_list.append(int(time[5]))
    if 'لحظه' in string:
        #زمان
        raw_list.append(int(time[0]))
        raw_list.append(int(time[1]))
        raw_list.append(int(time[2]))
        raw_list.append(int(time[3]))
        raw_list.append(int(time[4]))
        raw_list.append(int(time[5]))
    
    result = [True,raw_list]
    return result



def web_scraper(url,last_data):
    print(url)
    flag = False
    response = requests.get(url)
    soup = BS(response.text, "html.parser")
    cars = soup.find_all('div', attrs={'class': 'listdata'})
    for car in cars:
        print("in for")
        string = re.sub(r'\s+', ' ', car.text).strip(' ').split(' ')
        result = data_finder(string)
        print('before check')
        if result[0] and len(result[1])==13 and (not are_same(result[1],last_data)):
            print('adding to DB')
            add_to_DB(result[1])
            flag = True
            print('added to DB')
        elif(are_same(result[1],last_data)):
            print('goodbuy')
            flag = False
            break 
    return flag


last_data=last_data_in_DB()
flag = True
i = 1
while flag:
    flag = web_scraper('https://bama.ir/car/?page=' + str(i),last_data)
    i += 1

#print(guss_price([1397,'پژو','206','تهران',0,'سفید'],do_machin_learning()))