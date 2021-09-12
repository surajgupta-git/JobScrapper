from PIL import Image
import base64
import matplotlib.pyplot as plt
import json
import time
import streamlit as st
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models import DataTable, TableColumn, HTMLTemplateFormatter
from streamlit_bokeh_events import streamlit_bokeh_events
import requests
import bs4 as bs
import requests
import pandas as pd
import numpy as np



st.set_page_config(layout="wide")
#---------------------------------#
# Title
image = Image.open('link.jpg')

st.image(image, width = 50)

st.title('Latest LinkedIn Job Postings')
st.markdown("""
This app retrieves LinkedIn Jobs!
""")
#---------------------------------#
# About
st.markdown("""
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn, BeautifulSoup, requests, json, time
* **Data source:** [www.linkedin.com]
""")


url_analyst = 'https://www.linkedin.com/jobs/search/?geoId=103644278&keywords=data%20analyst%20summer%202022&location=United%20States&start='
url_sde = 'https://www.linkedin.com/jobs/search/?keywords=sde%20intern%202022&start='

st.sidebar.title("Filter Source")
source = st.sidebar.selectbox("Select type", [url_analyst,url_sde])

def load_data(url_p):
        pages = np.arange(0,100,25)
        job_links = []
        roles = []
        company = []
        time = []
        location = []

        for page in pages:
                urlPath = url_p + str(page)

                html_text = requests.get(urlPath).text
                soup = bs.BeautifulSoup(html_text, 'lxml')
                #print(soup)

                jobs = soup.find('ul', class_="jobs-search__results-list")
                job = jobs.find_all('li')
                #print(job[1])
                for i in job:
                        ref = i.find('a',class_ ='base-card__full-link')['href']
                        job_links.append(ref)
                        r = i.find('h3',class_ = 'base-search-card__title').text.strip()
                        roles.append(r)
                        com = i.find('h4',class_ = 'base-search-card__subtitle').text.strip()
                        company.append(com)
                        # t = i.find('time', class_ = 'job-search-card__listdate').text.strip()
                        # time.append(t)
                        loc = i.find('span',class_ = 'job-search-card__location').text.strip()
                        location.append(loc)

        df = pd.DataFrame({
            'Job Title': roles,
            'Company Name': company,
            'Location' : location,
            # 'Date posted': time,
            'Job link': job_links  })



        Names= df['Job Title'].tolist()
        Company = df['Company Name'].tolist()
        location = df['Location'].tolist()
        # dates = df['Date posted'].tolist()

        Joblinks = df['Job link'].tolist()

        df = pd.DataFrame({'Role' : Names , 'Company':Company, 'location': location,
         # 'Date' : dates,
            'link': Joblinks
        }) 

        def convert(row):
                #print(row)
                return '<a href="{}">{}</a>'.format(row['link'],  'Apply')

        df['link'] = df.apply(convert, axis=1)

        return df

df = load_data(source)



expander_bar1 = st.expander("See Jobs for Data Analyst Summer Intern 2022 Roles")
expander_bar1.write(df.to_html(escape=False), unsafe_allow_html=True)




