import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
import webbrowser
import getpass


from generateQnA import init

def random_sleep(min_seconds, max_seconds):
    time.sleep(random.uniform(min_seconds, max_seconds))

def create_file(content, filename='output.html'):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def human_like_interaction(driver):
    action = ActionChains(driver)
    for _ in range(random.randint(2, 5)):
        action.move_by_offset(random.randint(0, 200), random.randint(0, 200)).perform()
        random_sleep(1, 3)
        action.send_keys(Keys.PAGE_DOWN).perform()
        random_sleep(1, 3)
        action.move_by_offset(random.randint(0, 200), random.randint(0, 200)).perform()
        random_sleep(1, 3)
        action.send_keys(Keys.PAGE_UP).perform()
        random_sleep(1, 3)

def login_to_google(driver, email, password):
    driver.get("https://accounts.google.com/signin")

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "identifierId"))).send_keys(email)
    driver.find_element(By.ID, "identifierNext").click()

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "Passwd")))

    # Debugging output to check if the password field is located
    print("Password field located. Attempting to enter password.")

    password_input = driver.find_element(By.NAME, "Passwd")
    password_input.send_keys(password)

    # Debugging output to confirm the password is being typed
    print("Password entered. Attempting to submit.")

    driver.find_element(By.ID, "passwordNext").click()

    WebDriverWait(driver, 20).until(EC.url_contains("myaccount.google.com"))
    
def click_button_with_selector(driver, css_selector):
    try:
        # Wait for the button to be clickable
        button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
        )
        print(f"Button with selector '{css_selector}' is clickable. Clicking now.")
        button.click()
    except Exception as e:
        print(f"Failed to click button with selector '{css_selector}': {e}")

def bypass_detection(url, email, password, max_retries=3):
    print(f"Attempting to bypass Cloudflare for {url}")
    
    driver = None  # Initialize driver variable outside the loop
    
    for attempt in range(max_retries):
        try:
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.137 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.77 Safari/537.36 Edg/110.0.1587.49",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15",
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0"
            ]
            
            options = Options()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-infobars')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument(f'user-agent={random.choice(user_agents)}')
            # options.add_argument('--headless')  # Optional, if you don't need a visible browser

            # Additional randomized headers
            options.add_argument('--accept=application/json, text/javascript, */*; q=0.01')
            options.add_argument('--accept-language=en-US,en;q=0.5')
            options.add_argument('--accept-encoding=gzip, deflate, br')

            # Custom navigator properties
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)

            # Initialize the Chrome driver
            driver = webdriver.Chrome(options=options)
            driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                      get: () => undefined
                    });
                    Object.defineProperty(navigator, 'languages', {
                      get: () => ['en-US', 'en']
                    });
                    Object.defineProperty(navigator, 'plugins', {
                      get: () => [1, 2, 3, 4, 5]
                    });
                    window.chrome = {
                      runtime: {}
                    };
                    Object.defineProperty(navigator, 'connection', {
                      get: () => ({
                        downlink: 10,
                        effectiveType: '4g'
                      })
                    });
                '''
            })

            driver.set_page_load_timeout(30)
            
            # Perform Google login
            login_to_google(driver, email, password) # this check has been passed 
            
            parsed_url = urlparse(url)
            # driver.get(f"{parsed_url.scheme}://{parsed_url.netloc}")
            driver.get("https://swayam.gov.in/")
            click_button_with_selector(driver, "#header > div.container.modified-container.notranslate > div > div.col-2.custome-width.header_align.web-display > li > a > button")
            click_button_with_selector(driver, "#GoogleExchange")
      
            driver.get(url.split("/unit")[0] + "/course")
  
            driver.get(url)
            # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "submit")))
            # print("Successfully located the button")
            # driver.find_element(By.NAME, "submit").click()
            # print(f"Attempt {attempt + 1}: Navigating to {url}")
            # driver.get(url)

            # random_sleep(5, 10)

            # Wait for the body to be present
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Perform extensive human-like interactions
            # human_like_interaction(driver)

            # random_sleep(10, 15)

            html_content = driver.page_source
            create_file(html_content)

            # Check if still on the Cloudflare page
            if "Checking your browser" in html_content or "Just a moment" in html_content:
                print("Still on Cloudflare challenge page. Retrying...")
                driver.quit()
                continue

            if "Your browser is out of date!" in html_content:
                print("Browser detected as out of date. Retrying with a different user-agent...")
                driver.quit()
                continue

            print("Successfully bypassed Cloudflare!")
            driver.quit()
            return True

        except Exception as e:
            print(f"An error occurred: {e}")
            if driver:
                driver.quit()

    print("Failed to bypass Cloudflare after multiple attempts.")
    return None

print("Welcome to NPTEL Assignmnet Solver")
print("developed by - Rahul Singh")


def check_file_exists(file_path):
    return os.path.isfile(file_path)

def openBrowser():
    # Define the path to the PDF file
    pdf_file = 'output.pdf'

    # Automatically determine the current working directory
    directory = os.getcwd()
    file_path = os.path.join(directory, pdf_file)

    # Open the PDF file in the default web browser
    webbrowser.open(f'file://{file_path}')

ch = "yes"
while ch[0] == "Y" or ch[0] == "y":
    
    
    
    if(check_file_exists("output.html")):
        # os.remove("output.html")
        print("---------------------------------------------------------------")
        
        print("Choose 1 . for solving the assignment")
        
        ch = int(input("Enter the Choice : "))
        
        if(ch == 1):
            option = input("Is the questions are in Image format yes/no :  ")
            if(option[0] == "y" or option[0]=="Y"):
                init("output.html" , async_mode=False)
                os.remove("output.html")
                openBrowser()
                                
            else:
                init("output.html" , async_mode=True)
                os.remove("output.html")
                openBrowser()
                
    else:
        
        email = str(input("Enter your email college mail : "))
        password = getpass.getpass("Enter your email password: ")
        nptelAssignmentUrl = str(input("Enter your NPTEL Assignment URL : (example : https://onlinecourses.nptel.ac.in/noc24_cs94/unit?unit=18&assessment=187) :: "))
        
        bypass_detection(nptelAssignmentUrl, email, password)
        print("SuccessFully Created the NPTEL Assignment")
        
    
    
    ch = input("Run Again The Code y/n : ")

