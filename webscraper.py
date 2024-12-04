import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os



load_dotenv()

# MUST login, else it wont work - Modify .env file
linkedin_username = os.getenv('LINKEDIN_USERNAME')
linkedin_password = os.getenv('LINKEDIN_PASSWORD')


driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

driver.get('https://www.linkedin.com/login')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
email_elem = driver.find_element(By.ID, 'username')
password_elem = driver.find_element(By.ID, 'password')


email_elem.send_keys(linkedin_username)
password_elem.send_keys(linkedin_password)
password_elem.send_keys(Keys.RETURN)

try:
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'global-nav__me')))
except Exception as e:
    print("Error: Could not log in successfully.")
    driver.quit()
    exit()

profile_url = 'https://www.linkedin.com/in/alexaislant/'
driver.get(profile_url)
soup = BeautifulSoup(driver.page_source, 'html.parser')
time.sleep(5)


description_element = soup.find('div', {'class': 'text-body-medium break-words'})
description = description_element.text.strip() if description_element else 'Job title not found'
    

summary_divs = soup.find_all('div', class_='LDmeLHPrHxuoxVCdCoUvcPxxJtBGbmbYt')
    

for div in summary_divs:
    span_elem = div.find('span', {'aria-hidden': 'true'})
    if span_elem:
        summary = span_elem.get_text(strip=True).replace('<!---->', '').strip()
        print(f"Summary found: {summary}")
        break


secondary_items = soup.find_all('li', class_='artdeco-list__item')

experiences = []
languages = []
for item in secondary_items:
    title_elem = item.find('div', class_='display-flex align-items-center mr1 t-bold')
    title = title_elem.get_text(strip=True).replace('<!---->','') if title_elem else 'NULL'
    
    company_elem = item.find('span', class_='t-14 t-normal')
    company = company_elem.get_text(strip=True).replace('<!---->','') if company_elem else 'NULL'
    
    # Extracts third info in the card, could be date of experience or level of language
    third_elem = item.find('span', class_='t-14 t-normal t-black--light')
    date_or_level = third_elem.get_text(strip=True).replace('<!---->','') if third_elem else 'NULL'
    
    if (title != "NULL") and (company != "NULL"):
        experiences.append({
            'title': title,
            'company': company,
            'duration': date_or_level
        })
    
    if (title != "NULL") and (date_or_level != "NULL"):
        languages.append({
            'language': title,
            'level': date_or_level
        }
        )



for exp in experiences:
    print(f"Title: {exp['title']}")
    print(f"Company: {exp['company']}")
    print(f"Duration: {exp['duration']}")
    print("---")

for exp in languages:
    print(f"Title: {exp['language']}")
    print(f"level: {exp['level']}")
    print("---")





# Quit the driver
driver.quit()
