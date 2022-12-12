import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pandas.io.clipboard import clipboard_get
import pyautogui as pya
import csv
import copy 

from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())

#helium can potentially click points

# driver = webdriver.Chrome('chromedriver/chromedriver')  # Optional argument, if not specified will search path.

# Logs into the page
def login(username, password):
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(1)
    # usernameBox = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input')
    # passwordBox = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input')
    # logInButton = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button')

    usernameBox = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
    passwordBox = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
    logInButton = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button')


    usernameBox.send_keys(username)
    passwordBox.send_keys(password)
    logInButton.click()

    time.sleep(3)

def toClipboard(index, type):

    ac = ActionChains(driver) # Make a new actionchain instance
    post_obj = posts[index]
    driver.execute_script("arguments[0].scrollIntoView();", post_obj)
    post = ac.move_to_element(post_obj)
    size = post_obj.size
    # time.sleep(1)
    if type == 'stats':
        post.move_by_offset(-25, size['height']*0.03).context_click().perform()
    else:
        post.move_by_offset(0, size['height']*0.1).context_click().perform()
    # time.sleep(0.5)

    pya.hotkey('command','c')
    time.sleep(0.3)
    pya.hotkey('return')
    time.sleep(0.1)

def runScan(username, password, scanName, scanNumber):
    #Gets profile page
    login(username, password)
    driver.get('https://www.instagram.com/{}/'.format(scanName))
    time.sleep(0.5)
    driver.execute_script("window.scrollTo(0, 400)") 

    scanNumber = int(driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span').text)

    global posts
    posts = list(driver.find_elements_by_class_name('KL4Bh')) # List of elements

    rowCount = 1 # row number
    postCount = 1 # post number 1-3 in row of 3 posts
    postIndex = 0

    with open('CSV/' + scanName + '.csv', 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(['link', 'likes/views','comments'])
        for i in range(scanNumber):

            try:
                lastPost = str(posts[postIndex])
            except IndexError as error: 
                posts = list(driver.find_elements_by_class_name('KL4Bh')) # List of elements
                strPosts = [str(pst) for pst in posts]
                postIndex = strPosts.index(lastPost) + 1

            toClipboard(postIndex, 'link')
            time.sleep(0.5)
            link = clipboard_get().strip()
            print('Link: ', link)

            toClipboard(postIndex, 'stats')
            time.sleep(0.5)
            stats = clipboard_get().strip().splitlines()
            print('Stats: ', stats, '\n')

            if len(stats) == 2:
                writer.writerow([link, str(stats[0]), str(stats[1])])
            elif len(stats) == 1:
                writer.writerow([link, str(stats[0])])
            else:
                pass

            # if clipboard_get.startswith('https://www.instagram.com'): possible error checking later


            postIndex += 1
            postCount += 1
            if postCount == 3:
                rowCount+=1
                postCount=1


    driver.quit() # close when done!


# NOTES: Post xpaths
# //*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div/div[{rowNum}]/div[{postNum}]/a/div/div[2]
# //*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div/div[{rowNum}]/div[{postNum}]/a/div[1]/div[2] - if post is video
# 1
# //*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]/a/div/div[2]
# 2
# //*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div/div[1]/div[2]/a/div/div[2]
# 3 vid
# //*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div/div[1]/div[3]/a/div[1]/div[2] -video
# 4
# //*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div/div[2]/div[1]/a/div/div[2]
# 5
# //*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div/div[2]/div[2]/a/div/div[2]
# 6
# //*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div/div[2]/div[3]/a/div/div[2]