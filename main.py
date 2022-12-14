import requests
from scrapping import collect_info_per_page
from tqdm import tqdm
from joblib import Parallel, delayed
import pandas as pd


n_jobs=10
template_url='https://www.swiss.tech/swiss-startups?page={replace_me}'
output='startups_tech_swiss.csv'
# We need create the session to keep the cookies, if not don't return the page correctly
r=requests.Session() 

if n_jobs==1:
        values=[collect_info_per_page(page) for page in tqdm(range(0,196),desc=' doing scrapping per page') ]
else:   
    values=Parallel(n_jobs=n_jobs)(delayed(collect_info_per_page)(
        page,template_url,r) for page in tqdm(range(0,200),desc=' doing scrapping per page')   
    )

values = [x for xs in values for x in xs]   
df=pd.DataFrame(values)
# print(df.head())
df_grouped=df.groupby('title').agg({'description':'size', 'foundation_year':'mean'}) \
       .rename(columns={'description':'count','foundation_year':'foundation_year'}).sort_values('count',ascending=False)
print(df_grouped.head(20))
df.to_csv(output,index=False)

print(df.shape)
df.drop_duplicates(subset=df.columns.tolist().remove('page'),inplace=True)
print(df.shape)
df.to_csv('startups_tech_swiss_without_duplicates.csv',index=False)