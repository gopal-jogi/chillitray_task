from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException 
import json
import time

def scrape_yelu(location_url, category, page):
    try:
        chrome_options = Options()
        driver_path = 'C:\\Users\\admin\\Desktop\\selenium\\chromedriver.exe'  
        service = Service(driver_path)
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        base_url = 'https://www.yelu.in'
        url = f'{base_url}/category/{category}/{page}/city:{location_url}'
        
        driver.get(url)
        
        # Let the page load
        time.sleep(5)
        
        wait = WebDriverWait(driver, 10)
        companies = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'g_0')))
        
        all_companies = []
        for company in companies:
            company_data = {}
            try:
                company_data['Company_name'] = company.find_element(By.TAG_NAME, 'h4').text.strip()
            except NoSuchElementException as e:
                print(f"Error locating company name element: {e}.")
                company_data['Company_name'] = None
            
            try:
                company_data['Company_address'] = company.find_element(By.CLASS_NAME, 'address').text.strip()
            except NoSuchElementException as e:
                print(f"Error locating company address element: {e}.")
                company_data['Company_address'] = None
            
            try:
                company_data['Company_description'] = company.find_element(By.CLASS_NAME, 'details').text.strip()
            except NoSuchElementException as e:
                print(f"Error locating company description element: {e}.")
                company_data['Company_description'] = None
            
            try:
                company_data['Company_rating'] = company.find_element(By.CLASS_NAME, 'rate').text.strip()
            except NoSuchElementException as e:
                print(f"Error locating company rating element: {e}.")
                company_data['Company_rating'] = None
            
            try:
                company_data['Company_verified_tag'] = company.find_element(By.CLASS_NAME, 'v').text.strip()
            except NoSuchElementException as e:
                print(f"Error locating company verified tag element: {e}.")
                company_data['Company_verified_tag'] = None
            
            try:
                company_data['Company_icon'] = company.find_element(By.TAG_NAME, 'img').get_attribute('data-src')
            except NoSuchElementException as e:
                print(f"Error locating company icon element: {e}.")
                company_data['Company_icon'] = None
            
            try:
                company_data['Link_to_individual_company_page'] = base_url + company.find_element(By.TAG_NAME, 'a').get_attribute('href')
            except NoSuchElementException as e:
                print(f"Error locating company link element: {e}.")
                company_data['Link_to_individual_company_page'] = None
                
            all_companies.append(company_data)
        
        driver.quit()
        return all_companies
    except Exception as e:
        print(f"Error occurred: {e}.")
        return []



def save_to_json(data, filename):
    try:
        with open(filename, 'r') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        existing_data = {}

    for category, companies in data.items():
        if category not in existing_data:
            existing_data[category] = []
        existing_data[category].extend(companies)

    with open(filename, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)

def main():
    location_url = 'mumbai'
    categories = ['restaurants','advertising'] 

    all_companies = {}
    for category in categories:
        all_companies[category] = []
        page = 1
        while True:
            companies = scrape_yelu(location_url, category, page)
            if not companies:
                break
            all_companies[category].extend(companies)
            page += 1

    save_to_json(all_companies, 'yelu_data_with_page.json')

if __name__ == "__main__":
    main()
