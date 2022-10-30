
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import os
from joblib import Parallel, delayed

def collect_info_per_page(number_page):
    url=template_url.replace('{replace_me}',str(number_page))
    page = r.get(url)
    soup = BeautifulSoup(page.text,'html.parser')

    main_information=soup.find_all("div", {"class": 'startupimport-teaser-content'})


    for startup in tqdm(main_information, desc='obtaining startups information'):

        title= startup.find("h2").find('span').text
        print('startup',title)
        
        description=startup.find("div", {"class": 'startupimport-teaser-description'}).find('p')
        description= description.text if hasattr(description,'text') else 'unknown'
     

        extra_info=startup.find_all("div", {"class": 'startupimport-teaser-info-row'})
        if len(extra_info)>1:
            sector= extra_info[0].text.replace('\n','')
            foundation_year=extra_info[1].contents[1].text.replace('\n','')
            location=extra_info[1].contents[3].text.replace('\n','')
        else:
            sector= 'unknown'
            foundation_year=extra_info[0].contents[1].text.replace('\n','')
            location=extra_info[0].contents[3].text.replace('\n','')
        url=startup.find("a", {"class": 'startupimport-teaser-website'})
        
        url= url.get('href') if url else 'unknown'

        return            {
                'title':title,
                'description':description,
                'sector':sector,
                'foundation_year':foundation_year,
                'location':location,
                'url':url,
                'page':number_page,
            }
        
n_jobs=10
template_url='https://www.swiss.tech/swiss-startups?page={replace_me}'
output='startups_tech_swiss'
# We need create the session to keep the cookies, if not don't return the page correctly
r=requests.Session() 
# Create object page
# information=[]
# for number_page in range(0,196): #this 196 should be the number of startup/12
#     url=template_url.replace('{replace_me}',str(number_page))
#     page = r.get(url)
#     soup = BeautifulSoup(page.text,'html.parser')

#     main_information=soup.find_all("div", {"class": 'startupimport-teaser-content'})


#     for startup in tqdm(main_information, desc='obtaining startups information'):

#         title= startup.find("h2").find('span').text
#         print('startup',title)
        
#         description=startup.find("div", {"class": 'startupimport-teaser-description'}).find('p')
#         description= description.text if hasattr(description,'text') else 'unknown'
     

#         extra_info=startup.find_all("div", {"class": 'startupimport-teaser-info-row'})
#         if len(extra_info)>1:
#             sector= extra_info[0].text.replace('\n','')
#             foundation_year=extra_info[1].contents[1].text.replace('\n','')
#             location=extra_info[1].contents[3].text.replace('\n','')
#         else:
#             sector= 'unknown'
#             foundation_year=extra_info[0].contents[1].text.replace('\n','')
#             location=extra_info[0].contents[3].text.replace('\n','')
#         url=startup.find("a", {"class": 'startupimport-teaser-website'})
        
#         url= url.get('href') if url else 'unknown'

#         information.append(
#             {
#                 'title':title,
#                 'description':description,
#                 'sector':sector,
#                 'foundation_year':foundation_year,
#                 'location':location,
#                 'url':url,
#                 'page':number_page,
#             }
#         )
#         print('hi')

if n_jobs==1:
        values=[collect_info_per_page(page) for page in tqdm(range(1,196),desc=' doing scrapping per page') ]
else:   
    values=Parallel(n_jobs=n_jobs)(delayed(collect_info_per_page)(
        page) for page in tqdm(range(1,196),desc=' doing scrapping per page')   
    )
        
df=pd.DataFrame(values)
print(df.head())
df.to_csv(output,index=False)