
from bs4 import BeautifulSoup


def collect_info_per_page(number_page,template_url,session):
    url=template_url.replace('{replace_me}',str(number_page))
    page = session.get(url)
    soup = BeautifulSoup(page.text,'html.parser')

    main_information=soup.find_all("div", {"class": 'startupimport-teaser-content'})

    information=[]
    for startup in main_information:

        title= startup.find("h2").find('span').text
        
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

        information.append(           {
                'title':title,
                'description':description,
                'sector':sector,
                'foundation_year':foundation_year,
                'location':location,
                'url':url,
                'page':number_page,
            }
        )
    return information
        
