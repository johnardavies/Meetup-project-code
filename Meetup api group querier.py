import json
import ssl
import pprint
import requests
import time
import re
import csv
from meetupauth import *  #Pulls in the authentification details
#The * function unpacks arguments


# This code returns groups from the Meetup API that fall within a given radius of a point specified by a latitude and longitude
# It works through the set of pages returned in response to the call, parses the json that is returned and write it to a csv file

#######Function which parses the json and writes it to a csv file'####################################################
def write(x):
  print 'write function called'
  for elem in x['results']:
    name=elem['name'].replace(",","").encode('utf-8')
    print name #prints name to the screen
    ids=elem['id']
    creat=elem['created']
    country=elem['country']
    city=elem['city'].encode('utf-8')
    mem=elem['members']
    lat=elem['lat']
    lon=elem['lon']
    try:
     cats=elem['category']['name']
    except:
     cats=""
    sa=""
    topics=elem['topics']
    for part in topics:
       thing=part['name'].encode('utf-8')
       sa=sa+" "+thing
       sa=sa.replace("\n","").replace('\r', '')
    try:
     desc=elem['description'].encode('utf-8')
     desc=desc.replace(",","")
     #Removes various different tags
     desc=desc.replace("<p>","")
     desc=desc.replace("</p>","")
     desc=desc.replace("<br>","")
     desc=desc.replace("</br>","")
     desc=desc.replace("<span>","")
     desc=desc.replace("</span>","")
     desc=desc.replace("\n","").replace('\r', '')
    except:
      desc=""
    if country=='GB': #Checks that the country information is right
     with open("output filepath", "a",) as csvFile: #Writes the data to a csv file
      writer=csv.writer(csvFile, lineterminator='\n')
      writer.writerow((str(name),str(city),str(ids),str(creat),str(cats),str(mem),str(country),str(lon),str(lat),str(sa),str(desc),'1'))
     csvFile.close()


#########Function which recursively calls the pages from the Meetup API
def recurs(x):
  try:
   rs=requests.get(x)
   data=rs.json()
   rs.headers
   c=rs.headers['x-ratelimit-remaining']
   if c==2:
    time.sleep(60*5)
   else:
    time.sleep(2) 
   write(data)
   try:
    a=data['meta']['next']
    if a=='':
      print 'no more pages'
    else: 
     print a
     recurs(a)
   except:
    print 'call failed 2'
  except:
    print 'call failed 1'
 
######### Function which calls the Meetup api and which downloads the pages#####################################
def pager(x,y):
     payload = {'key': x, 'format': 'json' ,'country':'GB'}
     print payload
     time.sleep(3)
     rs=requests.get(y, params=payload)
     b=rs.url
     print b
     recurs(b)

#The https request that is used
mu_url2='https://api.meetup.com/2/groups?&sign=true&photo-host=public&lat=54.00366&lon=-2.547855&radius=500&page=100'

#and starting from the shetlands

#sh_url2='https://api.meetup.com/2/groups?&sign=true&photo-host=public&lat=60.397360&lon=-1.354070&radius=300&page=100'

################################################################################################################
##########Calls pager function to start the program #############################################################
pager(KEY, mu_url2)





