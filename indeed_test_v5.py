import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = 'https://www.indeed.com/q-supply-chain-analyst-l-Jacksonville,-FL-jobs.html'
# conducting a request of the stated URL above:
page = requests.get(URL)
# specifying a desired format of “page” using the html parser -
soup = BeautifulSoup(page.text, 'html.parser')

# Finding locations
def extract_location(soup):
    locations = []
    spans = soup.find_all('span', attrs={'class': 'location'})
    for span in spans:
        locations.append(span.text)
    return locations
extract_location(soup)

# Finding job titles
def extract_job_title(soup):
    jobs = []
    for div in soup.find_all(name='div', attrs={'class':'row'}):
        for a in div.find_all(name='a', attrs={'data-tn-element':'jobTitle'}):
            jobs.append(a['title'])
    return jobs
extract_job_title(soup)

# Finding companies
def extract_company(soup):
    companies = []
    for div in soup.find_all(name='div', attrs={'class':'row'}):
        company = div.find_all(name='span', attrs={'class':'company'})
        if len(company) > 0:
            for b in company:
                companies.append(b.text.strip())
    return companies
extract_company(soup)

#print(extract_location(soup))
#print(extract_job_title(soup))
#print(extract_company(soup))

# Building the dataframe
columns = {'location': locations, 'job_title': jobs, 'company_name': companies}
df = pd.DataFrame.from_dict(columns, orient='index')
df = df.transpose()


print(df)


df.to_csv('indeed_job_postings.csv')
