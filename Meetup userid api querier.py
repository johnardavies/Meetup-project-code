import json
import ssl
import pprint
import requests
import time
import re
import csv
from collections import defaultdict
from meetupauth import *  #Pulls in the authentification details
#The * function unpacks arguments

##This code extracts members information from the Meetup API for a set of Meetup group ids########
#The http requests that we are making are variants of the below 

mu_url2='https://api.meetup.com/2/members?&sign=true&page=100'


##################################################################################
#This function parses the json, removes comms and line breaks and writes to a csv
 
def write(x,y):        
  for elem in x['results']:
    name=elem['name'].replace(',','') #Removes the commas
    name=name.replace('\n','').replace('\r', '') #Removes new line and carriage returns
    name=name.encode('utf-8') #encodes as utf
    try:
     bio=elem['bio'].replace(",","")
     bio=bio.replace('\n','').replace('\r','')
     bio=bio.encode('utf-8')  
    except:
     bio="none"
    ids=elem['id']
    try:
     gen=elem['gender']
    except:
     gen="unknown"
    try: 
     join=elem['joined']
    except:
     join ="unknown"
    try:
     lat=elem['lat']
     lon=elem['lon']
    except:
     lat='NA'
     lon='NA'
    try:
     dat=elem['city'].encode('utf-8')
    except:
     dat='unknown' 
    groupid=y
    sa='' #initialising the topics list with a blank element
    try:
     for part in elem['topics']: #Loops through the topics that they are interested in.
       thing=part['name']
       sa=sa+" "+thing  #appends the topics to the list while adding a space
     sa=sa.replace(",","")
     sa=sa.encode('utf-8')
     sa=sa.replace('\n','').replace('\r','')
    except:
      sa="unknown"
    with open("filepath of csv file data is written to", "a",) as csvFile:
     writer=csv.writer(csvFile, lineterminator='\n')
     writer.writerow((str(groupid),str(name), str(gen), str(ids), str(dat), str(join), str(lat),str(lon),str(bio),str(sa),'1'))
    csvFile.close()

################################################################################
#This function recursively calls the pages from the Meetup API
def recurs(x,y):
  try:
   rs=requests.get(x)
   data=rs.json()
   rs.headers
   c=rs.headers['x-ratelimit-remaining']  #Sees how many calls can still be made 
   if c==1: #If only one more call can be made adds in a 5 minute delay
    time.sleep(60*5)
   else:
    time.sleep(0.3) 
   write(data, y) #calls the function that writes the data to a csv
   try:
    a=data['meta']['next'] #Checks to see if there is another page still to get
    if a=='':
     print 'no more pages'
    else: 
     print a
     recurs(a,y) #If there is another page calls recurs again
   except:
    print 'call fails for', y  
  except:
    print 'call fails for ', y
  

################################################################################
#This function makes http calls depending on the group id that is fed it 
def pager(x,y, k):
      payload = {'key': x, 'format': 'json', 'group_id':k}
      print payload
      time.sleep(0.5)
      rs=requests.get(y, params=payload)
      b=rs.url
      print b  #This prints the http page call that is being made
      recurs(b,k) #This calls the function that recursively make the http calls
   

##################################################################################
#Reads in the group id information################################################

ifile  = open('filepath of csv file group ids are stored in', "rb")
field_names=['ids']
reader =  csv.DictReader(ifile,fieldnames=field_names) 
#creates a dictionary with the ids as the keys and the names and speaker status as the values
names=defaultdict(list)
for row in reader:
   print row['ids']  
   pager(KEY, mu_url2, row['ids']) 

