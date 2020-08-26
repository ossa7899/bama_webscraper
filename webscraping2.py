import time as timelib
import mysql.connector
from bs4 import BeautifulSoup as BS
import requests
import re

def canUpdate(raw_list):
    query = 'SELECT * FROM data LIMIT 1'
    cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='webScraping')
    cursor = cnx.cursor()
    cursor.execute(query)
    for(year_of_creating,brand,model,city,karkard,price,color,date,time) in cursor:
        if (not raw_list[0] == year_of_creating) or (not raw_list[1] == brand) or (not raw_list[2] == model) or (not raw_list[3] == city) or (not raw_list[4] == karkard) or (not raw_list[5] == price) or (not raw_list[6] == color) :
            cnx.close()
            return True
        else:
            cnx.close()
            return False
        print('%d,%s,%s,%s,%d,%d,%s,%s,%s' % (year_of_creating,brand,model,city,karkard,price,color,date,time))
    print("after query")
    

def date_comparing(past,now):
    if past[0] <= now[0]:
        if past[1] <= now[1]:
            if past[2] <= now[2]:
                return True
    return False

def time_comparing(past,now):
    if past[0] <= now[3]:
        if past[1] <= now[4]:
            if past[2] <= now[5]:
                return True
    return False
    

def web_scraper(url, cursor):
    
    flag = True
    response = requests.get(url)
    soup = BS(response.text, "html.parser")
    cars = soup.find_all('div', attrs={'class': 'listdata'})
    if len(cars) < 12:
        flag = False
    for car in cars:
        print(str(len(database_list)) + '  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        strings = timelib.strftime("%Y,%m,%d,%H,%M,%S")
        t = strings.split(',')
        time = [ int(x) for x in t ]
        lastdate = list()
        lasttime = list()
        if len(database_list) == 100:
            flag = False
            break
        raw_list = list()
        string = re.sub(r'\s+', ' ', car.text).strip(' ').split(' ')
        if not ('کارکرد' in string):
            print("KARKARD NABBOOD")
            continue
        result = 0
        raw_list.append(string[0].split('،')[0])#سال تولید
        raw_list.append(string[1].split('،')[0])#برند
        raw_list.append(string[2])#مدل ماشین
        if string[1 + string.index('کارکرد')] == 'صفر':
            raw_list.append(string[4+string.index('کارکرد')].split('،')[0])
            raw_list.append(int(result))
        else:
            price = string[1 + string.index('کارکرد')].split(',')
            raw_list.append(string[4+string.index('کارکرد')].split('،')[0])
            result = ''
            for elem in price:
                result += elem 
            try:   
                raw_list.append(int(result))
            except ValueError:
                print("KARKARD Moshkel dash ******************************")
                continue

        if 'تومان' in string:
            try:
                price = string[string.index('تومان') - 1].split(',')
                result = ''
                for elem in price:
                    result += elem 
                raw_list.append(int(result))
            except ValueError:
                print("TOMAN Moshkel dash ******************************")
                continue
        elif 'ماهانه' in string:
            try:
                price = string[string.index('ماهانه') - 3].split(',')
                result = ''
                for elem in price:
                    result += elem
                raw_list.append(int(result))
            except ValueError:
                print("MAHANE Moshkel dash ******************************")
                continue
        if 'رنگ' in string:
            try:
                raw_list.append(string[string.index('رنگ')+1].split('،')[0])
            except ValueError:
                print("RANG Moshkel dash ******************************")
                continue
        if 'دقیقه' in string:
            try:
                minute = int(string[string.index('دقیقه')-1])
                if time[4] - minute >0:
                    time[4] = time[4] - minute
                else:
                    minute-=time[4]
                    time[4]=0
                    time[3]-=1
                    time[4]+=60-minute
                raw_list.append(time)
            except ValueError:
                print("ZAMAN Moshkel dash ******************************")
                continue
        if not (len(database_list) == 0):
            print("befor SELECT query")
            query = 'SELECT date FROM data LIMIT 1'
            cursor.execute(query)
            for s in cursor:
                print("##################################")
                print(s)
                print("##################################")
                for t in s[0].timetuple():
                    lastdate.append(t)
            print(lastdate)
            query = 'SELECT time FROM data LIMIT 1'
            cursor.execute(query)
            for s in cursor:
                s=s[0]
                print("##################################")
                print(s)
                print("##################################")
                lasttime.append(s.seconds // 3600)
                lasttime.append((s.seconds % 3600) // 60)
                lasttime.append(s.seconds % 60)
            print(lasttime)
        if(len(raw_list)==8):
            if(len(database_list) == 0):
                print("adding to DB")
                database_list.append(raw_list)
                query = 'INSERT INTO data VALUES (\'%d\',\'%s\',\'%s\',\'%s\',\'%d\',\'%d\',\'%s\',\'%s\',\'%s\')' % (int(raw_list[0]), raw_list[1],raw_list[2],raw_list[3],raw_list[4],raw_list[5],raw_list[6],str(raw_list[7][0])+'-'+str(raw_list[7][1])+'-'+str(raw_list[7][2]),str(raw_list[7][3])+':'+str(raw_list[7][4])+':'+str(raw_list[7][5]))
                cursor.execute(query)
                print("added to DB")
                cnx.commit()
                print(raw_list[7])
            else:
                if((date_comparing(lastdate,raw_list[7]) and time_comparing(lasttime,raw_list[7]))):
                    update = canUpdate(raw_list)
                if(update):
                    print("adding to DB")
                    database_list.append(raw_list)
                    query = 'INSERT INTO data VALUES (\'%d\',\'%s\',\'%s\',\'%s\',\'%d\',\'%d\',\'%s\',\'%s\',\'%s\')' % (int(raw_list[0]), raw_list[1],raw_list[2],raw_list[3],raw_list[4],raw_list[5],raw_list[6],str(raw_list[7][0])+'-'+str(raw_list[7][1])+'-'+str(raw_list[7][2]),str(raw_list[7][3])+':'+str(raw_list[7][4])+':'+str(raw_list[7][5]))
                    cursor.execute(query)
                    print("added to DB")
                    cnx.commit()
                elif update == False:
                    flag=False
                    break
                else:
                    continue
        else:
            continue

    return flag
    

data_base = input('لطفا نام پایگاه داده خود را وارد کنید')
cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database=data_base)
cursor = cnx.cursor()
database_list = list()
flag = True
i = 1
while flag:
    flag = web_scraper('https://bama.ir/car/?page=' + str(i), cursor)
    i += 1
