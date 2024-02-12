from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import json
import time

def crawl_profiles(links):
    profiles = []
    chrome_options = Options()
    driver_path = 'C:\\Users\\admin\\Desktop\\selenium\\chromedriver.exe'  
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    for link in links:
        driver.get(link)
        time.sleep(3)  
        
        profile = {}
        try:
            profile['Company_name'] = driver.find_element(By.ID, 'company_name').text.strip()
        except NoSuchElementException:
            profile['Company_name'] = None
        
        try:
            profile['Company_address'] = driver.find_element(By.CLASS_NAME, 'location').text.strip()
        except NoSuchElementException:
            profile['Company_address'] = None

        try:
            profile['Phone_number'] = driver.find_element(By.CLASS_NAME, 'phone').text.strip()
        except NoSuchElementException:
            profile['Phone_number'] = None
        
        try:
            profile['Website'] = driver.find_element(By.CSS_SELECTOR, '.weblinks > a').get_attribute('href')
        except NoSuchElementException:
            profile['Website'] = None
        
        try:
            profile['Email'] = driver.find_element(By.CSS_SELECTOR, 'a[itemprop="email"]').text.strip()
        except NoSuchElementException:
            profile['Email'] = None

        try:
            profile['Company_rating'] = driver.find_element(By.CLASS_NAME, 'rate').text.strip()
        except NoSuchElementException as e:
            print(f"Error locating company rating element: {e}.")
            profile['Company_rating'] = None
        
        try:
            profile['Company_verified_tag'] = driver.find_element(By.CLASS_NAME, 'vvv').text.strip()
        except NoSuchElementException as e:
            print(f"Error locating company verified tag element: {e}.")
            profile['Company_verified_tag'] = None

        try:
            profile['About'] = driver.find_element(By.CLASS_NAME, 'desc').text.strip()
        except NoSuchElementException:
            profile['About'] = None
        
        for key, value in profile.items():
            if value is not None and isinstance(value, str):
                profile[key] = value.strip()
        
        profiles.append(profile)
    
    driver.quit()
    return profiles

def main():
    with open('yelu_data_with_page.json', 'r') as json_file:
        data = json.load(json_file)

    links = [company['Link_to_individual_company_page'] for category in data.values() for company in category]

    profiles = crawl_profiles(links[:20]) 
    
    with open('company_profiles.json', 'w') as json_file:
        json.dump(profiles, json_file, indent=4)

if __name__ == "__main__":
    main()
