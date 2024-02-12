import requests
from bs4 import BeautifulSoup
import json

def scrape_yelu(location_url, category, page, proxies):
    for proxy in proxies:
        try:
            base_url = 'https://www.yelu.in'
            url = f'{base_url}/category/{category}/{page}/city:{location_url}'
            response = requests.get(url, proxies=proxy, timeout=15)  
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            companies = []
            for company in soup.find_all('div', class_='g_0'):
                company_data = {}
                company_data['Company_name'] = company.find('h4').text.strip()
                company_data['Company_address'] = company.find('div', class_='address').text.strip()
                company_data['Company_description'] = company.find('div', class_='details').text.strip()
                company_data['Company_rating'] = company.find('div', class_='rate').text.strip()
                company_data['Company_verified_tag'] = company.find('u', class_='v').text.strip()
                company_data['Company_icon'] = company.find('img')['src']
                company_data['Link_to_individual_company_page'] = base_url + company.find('a')['href']
                companies.append(company_data)
            return companies
        except requests.exceptions.RequestException as e:
            print(f"Error occurred with {proxy}: {e}. Trying next proxy...")
            continue
    print("All proxies failed. Unable to scrape data.")
    return []

def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def main():
    location_url = 'mumbai'
    categories = ['advertising', 'restaurants']  

    
    with open("validProxies.txt", "r") as f:
        proxies = [{"http": line.strip(), "https": line.strip()} for line in f.readlines()]

    all_companies = {}
    for category in categories:
        all_companies[category] = []
        page = 1
        while True:
            companies = scrape_yelu(location_url, category, page, proxies)
            if not companies:
                break
            all_companies[category].extend(companies)
            page += 1

    save_to_json(all_companies, 'yelu_data_with_page.json')

if __name__ == "__main__":
    main()
