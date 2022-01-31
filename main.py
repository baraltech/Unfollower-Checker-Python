import time # Allowing us to sleep so Instagram doesn't block the bot
from selenium import webdriver as wd
from selenium.webdriver.common.by import By # Allowing us to access specific elements
from selenium.webdriver.support.ui import WebDriverWait # Allowing us to wait until an element is found
from selenium.webdriver.common.action_chains import ActionChains # Allowing us to scroll down
from selenium.webdriver.support import expected_conditions as EC # Allowing us to check if an element is located
from selenium.webdriver.common.keys import Keys # Allowing our bot to type

USERNAME = str(input("Enter Username (For Login): "))
PASSWORD = str(input("Enter Password (For Login): "))

TIMEOUT = 15 # Seconds to wait unless we find the desired elements

user = str(input("Enter the account you want to check for unfollowers: "))

followers_to_scrape = int(input("How many followers do you want to check for? "))

SHOW_CHROME = False

# Setting up the webdriver

options = wd.ChromeOptions()
if not SHOW_CHROME:
    options.add_argument("--headless")
options.add_argument("--log-level=3")
mobile_emulation = {
    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}
options.add_experimental_option("mobileEmulation", mobile_emulation)

driver = wd.Chrome(options=options)
driver.set_window_size(600, 1000)

driver.get('https://www.instagram.com/accounts/login/')

# Wait for 2 seconds
time.sleep(2)

print(f"Logging in to {USERNAME}...")

# Logging in

# Putting in the username
user_element = WebDriverWait(driver, TIMEOUT).until(
    EC.presence_of_element_located((
        By.XPATH, '//*[@id="loginForm"]/div[1]/div[3]/div/label/input')))

user_element.send_keys(USERNAME)

# Putting in the password
pass_element = WebDriverWait(driver, TIMEOUT).until(
    EC.presence_of_element_located((
        By.XPATH, '//*[@id="loginForm"]/div[1]/div[4]/div/label/input')))

pass_element.send_keys(PASSWORD)

# Pressing the login button
login_button = WebDriverWait(driver, TIMEOUT).until(
    EC.presence_of_element_located((
        By.XPATH, '//*[@id="loginForm"]/div[1]/div[6]/button')))

# Waiting for 0.4 seconds and clicking the button
time.sleep(0.4)

login_button.click()

time.sleep(5)

# Getting the Instagram account of the user
driver.get('https://www.instagram.com/{}/'.format(user))

time.sleep(3.5)

# Finding the followers
WebDriverWait(driver, TIMEOUT).until(
    EC.presence_of_element_located((
        By.XPATH, '//*[@id="react-root"]/section/main/div/ul/li[2]/a'))).click()

time.sleep(2)

print(f'Finding who unfollowed {user}...')

followers = set()

# Scrolling down on the page with followers to find all of them
for _ in range(round(followers_to_scrape // 10)):

    ActionChains(driver).send_keys(Keys.END).perform()

    time.sleep(2)

    follower_elements = driver.find_elements_by_xpath(
        '//*[@id="react-root"]/section/main/div/ul/div/li/div/div[1]/div[2]/div[1]/a')

    # Getting url from href attribute
    for i in follower_elements:
        if i.get_attribute('href'):
            followers.add(i.get_attribute('href').split("/")[3])
        else:
            continue

# Opening the old followers and checking who unfollowed
with open('followers.txt', 'r') as followerdata:
    old_followers = []
    unfollowed = 0
    for follower in followerdata:
        old_followers.append(follower.rstrip())
    for old_follower in old_followers:
        if old_followers == []:
            break
        if old_follower not in followers:
            unfollowed += 1
            print(f"{old_follower} unfollowed you!")
    print(f"People that unfollowed: {unfollowed}")

# Writing the current followers to the text file
with open('followers.txt', 'w') as followerdata:
    followerdata.write('\n'.join(followers) + "\n")