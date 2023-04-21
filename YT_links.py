# import requests
# from bs4 import BeautifulSoup

# #Create a program that scrapes the links of all yt vids 
# # loaded on yt homepage then puts all of the links in a dictionary 
# # and selects one at random

# url = "https://www.youtube.com/"
# response = requests.get(url)

# soup = BeautifulSoup(response.content, "html.parser")
# divs = soup.find_all("div", {"class": "style-scope ytd-rich-grind-media"})

# for div in divs:
#     p = div.find("a", {"id": "video-title-link"})
#     print(p.text)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import webbrowser, random

#static varaible
global hrefs, vid_ids

#create a method that ensures a random number isnt picked twice
#create a r_links method to refresh the links
#call r_links from r_video
#add an option if user doesnt want to log in

def init_yt():
    global hrefs
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options) 
    options.add_argument("--headless=new")
    driver.get("https://www.youtube.com/")
    hrefs = [video.get_attribute('href') for video in driver.find_elements(By.ID, "thumbnail")]


def links():
    global hrefs, vid_ids
    if len(vid_ids) > 30:
        driver.refresh() #refreshes the links 
    #hrefs = [video.get_attribute('href') for video in driver.find_elements(By.ID, "thumbnail")]
    for i, href in enumerate(hrefs):
        if href is not None:
            if "shorts" in href: 
                hrefs.pop(i)
                print(f'---------removed: {href}---------')
                continue
            print(href)
    print(f'Amount of links: {len(hrefs)}') 
    r_video() #random video
    
def r_video(): 
    global hrefs, vid_ids
    ranVid = random.randint(1, len(hrefs))
    check_vid_id(ranVid)
    url = hrefs[ranVid-1]
    print(f'selected video: {url}')
    webbrowser.open(url, new=0, autoraise=True) 
    vid_ids.append(ranVid)
    
def check_vid_id(ranVid):
    global vid_ids
    if ranVid in vid_ids:
        r_video()
    
def login():
    #initializes the yt page
    init_yt()
    #CLICK THE SIGN IN BUTTON
    signin_button = driver.find_element(By.XPATH, '//button[@aria-label="Sign in"]')
    signin_button.click()
    email_field = driver.find_element(By.XPATH, '//input[@type="email"]')
    email_field.send_keys(email)
    email_field.send_keys(Keys.ENTER)
    password_field = driver.find_element(By.XPATH, '//input[@type="password"]')
    password_field.send_keys(password)
    password_field.send_keys(Keys.ENTER)
    # verify that user is logged in
    profile_button = driver.find_element(By.XPATH, '//button[@aria-label="Profile picture"]')
    print("Logged in as:", profile_button.get_attribute('aria-label'))
    driver.get("https://www.youtube.com/")
    links()
    
def begin():
    starting = str(input('Press v to start!: '))
    if 'v' in starting.lower():
        log = input('Would you like to log in? (Y/N): ')
        if 'y' in log.lower():
            login()
        elif 'n' in log.lower():
            init_yt()
            links()
        else:
            print('---Please respond again---')
            begin()
    else: 
        exit('no.')





vid_ids = [0] #initializing the type
begin()
while True:
    refresh = input('Press r to for a new video! (s to stop): ')
    #driver.refresh() if refresh is 'r' else continue
    if 'r' in refresh.lower():
        r_video()
    if 's' in refresh.lower():
        exit(0)
    continue

