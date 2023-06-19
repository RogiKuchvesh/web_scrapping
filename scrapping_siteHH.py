import requests
from fake_headers import Headers
import bs4
import json

headers = Headers(browser="firefox", os="win")
headers_data = headers.generate()

filter_keywords = ["Django", "Flask"]
vacancies = []

response = requests.get("https://spb.hh.ru/search/vacancy?text=python&area=1&area=2", headers=headers_data)
html_data = response.text
soup = bs4.BeautifulSoup(html_data, features='lxml')
vacancy_list_pars = soup.find(id='a11y-main-content')
vacancy_list_pars_all = vacancy_list_pars.find_all(class_="vacancy-serp-item__layout")

for vacancy_about in vacancy_list_pars_all:
    a_tag = vacancy_about.find('a')    
    vacancy_name = a_tag.text
    link = a_tag['href']
    company_tag = vacancy_about.find('div', class_ = 'vacancy-serp-item__meta-info-company')
    company = company_tag.text
    city_tag = vacancy_about.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address', 'class': 'bloko-text'})
    city = city_tag.text
    salary_range_tag = vacancy_about.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation', 'class': 'bloko-header-section-3'})
    if salary_range_tag is None:
        salary_range = ""
    else:
        salary_range = salary_range_tag.text
    
    full_vacancy_html = requests.get(link, headers=headers_data).text
    full_vacancy_soup = bs4.BeautifulSoup(full_vacancy_html, features='lxml')
    full_vacancy_tag = full_vacancy_soup.find('div', class_ = 'vacancy-section')
    full_vacancy_text = full_vacancy_tag.text
     
    if all(keyword in full_vacancy_text for keyword in filter_keywords):        
        vacancy_info = {
            "link": link,
            "salary_range": salary_range,
            "company": company,
            "city": city            
        }
        vacancies.append(vacancy_info)

with open("vacancies.json", "w", encoding="utf-8") as f:
    json.dump(vacancies, f, indent=4, ensure_ascii=False)