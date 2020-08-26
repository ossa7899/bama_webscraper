import time as timelib
import mysql.connector
from bs4 import BeautifulSoup as BS
import requests
import re
from sklearn import tree

def guss_price(new_data,help_list):
    clf = help_list[0]
    brand_dict = help_list[1]
    model_dict = help_list[2]
    city_dict = help_list[3]
    color_dict = help_list[4]
    new_data[1]=brand_dict[new_data[1]]
    new_data[2]=model_dict[new_data[2]]
    new_data[3]=city_dict[new_data[3]]
    new_data[5]=color_dict[new_data[5]]
    mylist = [new_data]
    answer = clf.predict(mylist)
    return answer
def do_machin_learning():
    query = 'SELECT * FROM mydata ORDER BY year DESC,month DESC,day DESC,hour DESC,minute DESC,second DESC'
    cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='webScraping')
    cursor = cnx.cursor()
    cursor.execute(query)
    print(cursor)
    l =list()
    x =list()
    y =list()
    brand_dict = dict()
    brand_counter = 0
    model_dict = dict()
    model_counter = 1000
    city_dict = dict()
    city_counter = 1000000
    color_dict = dict()
    color_counter = 100000
    for(year_of_creating,brand,model,city,karkard,price,color,year,month,day,hour,minute,second) in cursor:
        if not (brand in brand_dict.keys()):
            brand_dict[brand] = brand_counter
            brand_counter +=1
        if not (model in model_dict.keys()):
            model_dict[model] = model_counter
            model_counter +=10
        if not (city in city_dict.keys()):
            city_dict[city] = city_counter
            city_counter +=1000
        if not (color in color_dict.keys()):
            color_dict[color] = color_counter
            color_counter +=100
    cnx.close()
    query = 'SELECT * FROM mydata ORDER BY year DESC,month DESC,day DESC,hour DESC,minute DESC,second DESC'
    cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='webScraping')
    cursor = cnx.cursor()
    cursor.execute(query)
    for(year_of_creating,brand,model,city,karkard,price,color,year,month,day,hour,minute,second) in cursor:
        l.append(year_of_creating)
        l.append(brand_dict[brand])
        l.append(model_dict[model])
        l.append(city_dict[city])
        l.append(karkard)
        l.append(color_dict[color])
        l.append(price)
        x.append(l[0:6])
        y.append(l[6])
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(x,y)
    help_list = [clf,brand_dict,model_dict,city_dict,color_dict]
    return help_list

print(guss_price([1390,'پراید','131','تهران',0,'سفید'],do_machin_learning()))





























#port mysql.connector
#ery = 'SELECT * FROM mydata ORDER BY year DESC,month DESC,day DESC,hour DESC,minute DESC,second DESC LIMIT 1'
#x = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='webScraping')
#rsor = cnx.cursor()
#rsor.execute(query)
#int(cursor)
#=list()
#lp = cursor
#
#r(year_of_creating,brand,model,city,karkard,price,color,year,month,day,hour,minute,second) in cursor:
#  l.append(year_of_creating)
#  l.append(brand)
#  l.append(model)
#  l.append(city)
#  l.append(karkard)
#  l.append(price)
#  l.append(color)
#  l.append(year)
#  l.append(month)
#    l.append(day)
#    l.append(hour)
#    l.append(minute)
#    l.append(second)
#    print('%d,%s,%s,%s,%d,%d,%s,%d,%d,%d,%d,%d,%d' % (year_of_creating,brand,model,city,karkard,price,color,year,month,day,hour,minute,second))
#print("after query")
#print(l)
#print(len(l))
#for index in range(0,len(l)):
#    print(index)
#cnx.close()
#query = 'SELECT date FROM data LIMIT 1'
#cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='webScraping')
#cursor = cnx.cursor()
#cursor.execute(query)
#help = list()
#for s in cursor:
#    print(s)
#    print(type(s))
#    print(s[0])
#    print(type(s[0]))
#    for t in s[0].timetuple():
#        help.append(t)
#    print(help)
#cnx.close()
#query = 'SELECT time FROM data LIMIT1'
#cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='webScraping')
#cursor = cnx.cursor()
#cursor.execute(query)
#help = list()
#for s in cursor:
#    print(s)
#    print(type(s))
#    print(s[0])
#    print(type(s[0]))
#    s=s[0]
#    print(s)
#    help.append(s.seconds // 3600)
#    help.append((s.seconds % 3600) // 60)
#    help.append(s.seconds % 60)
#    print(help)