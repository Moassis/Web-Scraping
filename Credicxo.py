from distutils.log import error
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup

headers={
'accept': 'text/html,*/*',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-US,en;q=0.9',
'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
}
data=[]
list1=[]
with open('amazoncsv.csv','rt')as file:
    for line in file:
        x=x+1
        cols=line.split(',')
        a=cols[3][:-1]
        link1="https://www.amazon."+a+"/dp/"+cols[2]
        
        try:
            r1= requests.get(link1, headers=headers).text
            soup1=BeautifulSoup(r1,'html.parser')
        except requests.exceptions.RequestException as err:
            print("{"+link1+"}"+" "+"URL is not available.")
                    
        try:
            title=soup1.find('span', attrs={'id':'productTitle'}).text.strip()
        except:
            print("{"+link1+"}"+" "+"Requested page could not be found.")
            title="{"+link1+"}"+" "+"Requested page could not be found."
            
        try:
            price=soup1.find('span', attrs={'class':'a-price-whole'}).text+soup1.find('span', attrs={'class':'a-price-fraction'}).text+" "+soup1.find('span', attrs={'class':'a-price-symbol'}).text
        except:
            price="-"
            
        try:
            link2=soup1.find('div', attrs={'id':'main-image-container'}).find('img').get('src')              
        except:
            link2="-"
            
        try:
            detail=soup1.find('div', attrs={'id':'feature-bullets'}).find('span', attrs={'class':'a-list-item'}).text.strip()                
        except:
            detail="-"
                    
                
        b={}
        b['Title']=title
        b['Image_Url']=link2
        b['Price']=price
        b['Details']=detail
        list1.append(b)
        
        data.insert(101,[title, price, link2, detail])

df=pd.DataFrame(data, columns=['Title','Price','Image_Url','Details'])
df.to_excel('credicxo.xlsx')
print("sucess") 
        
s=json.dumps(list1)
print(s)