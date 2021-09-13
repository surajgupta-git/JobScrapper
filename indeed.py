import bs4 as bs
import requests
import pandas as pd
import numpy as np
import time

pages = np.arange(0,100,10)
job_links = []
roles = []
company = []
time = []
location = []

for page in pages:
    urlPath = 'https://www.indeed.com/jobs?q=data%20analyst&l=United%20States&jt=internship&start='+str(page)+'&vjk=c00c9ba9ea849fbf '

    html_text = requests.get(urlPath).text
    soup = bs.BeautifulSoup(html_text, 'lxml')
    jobs_v = soup.find_all('div', class_ = 'mosaic-zone')
    jobs = jobs_v[1].find_all('a')
    for i in jobs:
        try:
            ref = i['href']
            
            r = i.find('h2',class_ = 'jobTitle jobTitle-color-purple').span['title']
            
            com = i.find('span',class_ = 'companyName').text.strip()
            
            t = i.find('span', class_ = 'date').text.strip()
            
            loc = i.find('div',class_ = 'companyLocation').text.strip()
            location.append(loc)
            job_links.append(ref)
            roles.append(r)
            company.append(com)
            time.append(t)
        except:
            pass
df = pd.DataFrame({
            'Job Title': roles,
            'Company Name': company,
            'Location' : location,
            'Date posted': time,
            'Job link': job_links  })
