import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest


job_title = []
company_name = []
locations = []
job_sill = []
links = []
responsibilities = []
date = []

result = requests.get("https://wuzzuf.net/search/jobs/?q=web+developer&a=hpb")

src = result.content

soup = BeautifulSoup(src, "lxml")

job_titles = soup.find_all("h2", {"class": "css-m604qf"})
company_names = soup.find_all("a", {"class": "css-17s97q8"})
location = soup.find_all("span", {"class": "css-5wys0k"})
job_sills = soup.find_all("div", {"class": "css-y4udm8"})
posted_new = soup.find_all("div", {"class": "css-4c4ojb"})
posted_old = soup.find_all("div", {"class": "css-do6t5g"})
posted = [*posted_new, *posted_old]


for i in range(len(job_titles)):
    job_title.append(job_titles[i].text)
    company_name.append(company_names[i].text)
    locations.append(location[i].text)
    job_sill.append(job_sills[i].text)
    links.append("https://wuzzuf.net"+job_titles[i].find("a").attrs['href'])
    date.append(posted[i].text)


for link in links:
    result = requests.get(link)
    src = result.content
    soup = BeautifulSoup(src, "lxml")
    
    try:
        job_requirements = soup.find("div", {"class":"css-1t5f0fr"}).ul
        respon_text = ""
        for li in job_requirements.find_all("li"):
            respon_text += li.text+" | "

        respon_text = respon_text[:-2]
        responsibilities.append(respon_text)
    except:
        print("error")



file_list = [job_title, date, company_name, locations, job_sill, links, responsibilities]
exported = zip_longest(*file_list)

with open("C:/Users/ahkor/OneDrive/Desktop/web scraping/results.csv", "w") as myfile:
    wr = csv.writer(myfile)
    wr.writerow(['job title','post date' ,'company name', 'location', 'job skills', 'links', 'responsibilities'])
    wr.writerows(exported)
